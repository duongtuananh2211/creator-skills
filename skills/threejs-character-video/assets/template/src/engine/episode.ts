import * as THREE from 'three';
import type { EpisodeContext, EpisodeSpec, Format, Vec3, Ease } from './types';
import { parseSubtitles, parseTime, type Cue } from './time';
import { Character, type CharacterInfo } from './character';
import { createStage } from './stage';
import { fetchArrayBuffer, fetchText, loadModel } from './assets';
import { computeEnvelope, type Envelope } from './lipsync';
import { lerp, span } from './keys';

const SIZES: Record<Format, [number, number]> = {
  '9:16': [1080, 1920],
  '16:9': [1920, 1080],
  '1:1': [1080, 1080],
  '4:5': [1080, 1350],
};

interface CamTrack {
  t: number;
  pos: Vec3;
  target: Vec3;
  fov: number;
  ease?: Ease;
  dur?: number;
}

export interface Runtime {
  spec: EpisodeSpec;
  fps: number;
  width: number;
  height: number;
  duration: number;
  frames: number;
  cues: Cue[];
  /** Audio path under public/ that loaded, or null. */
  audio: string | null;
  canvas: HTMLCanvasElement;
  camera: THREE.PerspectiveCamera;
  scene: THREE.Scene;
  renderer: THREE.WebGLRenderer;
  characters: Record<string, Character>;
  /** Where the timeline camera is looking at the last rendered time. */
  cameraTarget: THREE.Vector3;
  /** When true, renderAt leaves the camera alone (free camera in preview). */
  freeCamera: boolean;
  warnings: string[];
  gpu: string;
  renderAt(t: number): void;
  info(): { characters: CharacterInfo[]; warnings: string[] };
}

export async function loadEpisode(spec: EpisodeSpec, opts: { scale?: number; render?: boolean } = {}): Promise<Runtime> {
  const scale = opts.scale ?? 1;
  const fps = spec.fps ?? 30;
  const [baseW, baseH] = spec.size ?? SIZES[spec.format] ?? SIZES['9:16'];
  const even = (x: number) => Math.max(2, Math.round((x * scale) / 2) * 2);
  const width = even(baseW);
  const height = even(baseH);
  const warnings: string[] = [];

  let cues: Cue[] = [];
  if (spec.subtitles) {
    const text = await fetchText(spec.subtitles);
    if (text === null) warnings.push(`Không tìm thấy phụ đề public/${spec.subtitles}; các mốc "cue:N" sẽ báo lỗi.`);
    else cues = parseSubtitles(text);
  }

  // Decoding is deterministic, so the lip-sync curve is identical in preview and render.
  const decoded = new Map<string, Promise<AudioBuffer | null>>();
  const decode = (path: string) => {
    if (!decoded.has(path)) {
      decoded.set(
        path,
        fetchArrayBuffer(path).then(async (buf) => {
          if (!buf) return null;
          const ctx = new OfflineAudioContext(1, 2, 48000);
          return ctx.decodeAudioData(buf);
        }),
      );
    }
    return decoded.get(path)!;
  };
  const envelopes = new Map<string, Promise<Envelope | null>>();
  const envelope = (path?: string) => {
    const p = path ?? spec.audio;
    if (!p) return Promise.resolve(null);
    if (!envelopes.has(p)) envelopes.set(p, decode(p).then((b) => (b ? computeEnvelope(b) : null)));
    return envelopes.get(p)!;
  };

  let audio: string | null = null;
  let audioDuration: number | null = null;
  if (spec.audio) {
    const buf = await decode(spec.audio).catch((e) => {
      warnings.push(`Không giải mã được ${spec.audio}: ${e?.message ?? e}`);
      return null;
    });
    if (buf) {
      audio = spec.audio;
      audioDuration = buf.duration;
    } else warnings.push(`Không tìm thấy audio public/${spec.audio}; video sẽ không có tiếng.`);
  }

  let duration: number;
  if (spec.duration === undefined || spec.duration === 'audio') {
    if (audioDuration !== null) duration = audioDuration;
    else {
      duration = 10;
      warnings.push('Không có audio và chưa đặt "duration"; dùng tạm 10 giây.');
    }
  } else duration = parseTime(spec.duration, cues);

  const stage = await createStage(spec, width, height, !!opts.render);
  const { scene, camera, renderer } = stage;

  const characters: Record<string, Character> = {};
  for (const [name, cs] of Object.entries(spec.characters)) {
    const c = await Character.create(name, cs, { cues, envelope });
    characters[name] = c;
    scene.add(c.holder);
    warnings.push(...c.info.warnings.map((w) => `${name}: ${w}`));
  }

  const props: THREE.Object3D[] = [];
  for (const p of spec.props ?? []) {
    const { root } = await loadModel(p.model);
    root.updateMatrixWorld(true);
    const box = new THREE.Box3().setFromObject(root);
    const h = Math.max(box.max.y - box.min.y, 1e-6);
    root.scale.multiplyScalar((p.height ? p.height / h : 1) * (p.scale ?? 1));
    root.position.set(...(p.position ?? [0, 0, 0]));
    root.rotation.y = ((p.rotY ?? 0) * Math.PI) / 180;
    root.traverse((o) => {
      const m = o as THREE.Mesh;
      if (m.isMesh) m.castShadow = m.receiveShadow = true;
    });
    scene.add(root);
    props.push(root);
  }

  let fov = 35;
  const cams: CamTrack[] = (spec.camera.length ? spec.camera : [{ at: 0, pos: [0, 1.4, 4.5] as Vec3, target: [0, 1, 0] as Vec3 }])
    .map((k) => ({ ...k, t: parseTime(k.at, cues) }))
    .sort((a, b) => a.t - b.t)
    .map((k) => {
      fov = k.fov ?? fov;
      return { t: k.t, pos: k.pos, target: k.target, fov, ease: k.ease, dur: k.dur };
    });

  const ctx: EpisodeContext = { THREE, scene, camera, renderer, characters, props, fps, duration };
  await spec.setup?.(ctx);

  const cameraTarget = new THREE.Vector3();
  const sway = spec.cameraSway ?? 0;
  const v3 = (a: Vec3, b: Vec3, p: number, out: THREE.Vector3) =>
    out.set(lerp(a[0], b[0], p), lerp(a[1], b[1], p), lerp(a[2], b[2], p));

  const gl = renderer.getContext();
  const dbg = gl.getExtension('WEBGL_debug_renderer_info');
  const gpu = String(dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER));

  const rt: Runtime = {
    spec,
    fps,
    width,
    height,
    duration,
    frames: Math.max(1, Math.round(duration * fps)),
    cues,
    audio,
    canvas: stage.canvas,
    camera,
    scene,
    renderer,
    characters,
    cameraTarget,
    freeCamera: false,
    warnings,
    gpu,
    renderAt(t: number) {
      for (const c of Object.values(characters)) c.apply(t);
      if (!rt.freeCamera) {
        const [a, b, p] = span(cams, t);
        v3(a.pos, b.pos, p, camera.position);
        v3(a.target, b.target, p, cameraTarget);
        if (sway) {
          camera.position.x += (Math.sin(t * 0.9) * 0.6 + Math.sin(t * 2.3 + 1) * 0.4) * sway;
          camera.position.y += (Math.sin(t * 1.3 + 2) * 0.5 + Math.sin(t * 3.1) * 0.25) * sway;
        }
        camera.lookAt(cameraTarget);
        const f = lerp(a.fov, b.fov, p);
        if (camera.fov !== f) {
          camera.fov = f;
          camera.updateProjectionMatrix();
        }
      }
      spec.update?.(ctx, t);
      renderer.render(scene, camera);
    },
    info() {
      return { characters: Object.values(characters).map((c) => c.info), warnings };
    },
  };
  rt.renderAt(0);
  return rt;
}
