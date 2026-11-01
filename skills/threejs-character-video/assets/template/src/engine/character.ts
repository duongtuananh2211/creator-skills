import * as THREE from 'three';
import type { CharacterSpec, Ease, Time, Vec3 } from './types';
import { parseTime, type Cue } from './time';
import { loadAnimation, loadModel } from './assets';
import { findNode, prepareClip } from './retarget';
import { clamp01, hash01, lerp, smoothstep, span } from './keys';
import { sampleEnvelope, type Envelope } from './lipsync';

const DEG = Math.PI / 180;

interface ActionTrack {
  t: number;
  fade: number;
  speed: number;
  offset: number;
  loop: boolean;
  duration: number;
  action: THREE.AnimationAction;
}

interface MoveTrack {
  t: number;
  pos: Vec3;
  rotY: number;
  ease?: Ease;
  dur?: number;
}

interface FaceTrack {
  t: number;
  value: number;
  fade: number;
}

type MorphRef = { mesh: THREE.Mesh; index: number };

export interface ClipInfo {
  name: string;
  duration: number;
  source: string;
  /** For clips from another file: tracks that found a bone in this model. */
  matched?: string;
}

export interface CharacterInfo {
  name: string;
  model: string;
  height: number;
  scale: number;
  clips: ClipInfo[];
  morphs: string[];
  bones: string[];
  warnings: string[];
}

export interface CharacterEnv {
  cues: Cue[];
  /** Envelope for an audio path (or the episode audio when undefined). */
  envelope: (audio?: string) => Promise<Envelope | null>;
}

export class Character {
  /** Move/rotate this; the loaded model sits inside it, already scaled. */
  readonly holder = new THREE.Group();
  readonly root: THREE.Object3D;
  readonly info: CharacterInfo;
  private mixer: THREE.AnimationMixer;
  private tracks: ActionTrack[] = [];
  private moves: MoveTrack[] = [];
  private face = new Map<string, FaceTrack[]>();
  private morphs = new Map<string, MorphRef[]>();
  private controlled = new Set<string>();
  private lip: null | {
    env: Envelope;
    ranges: [number, number][];
    morphs: [string, number][];
    bone: THREE.Object3D | null;
    rest: THREE.Quaternion;
    axis: THREE.Vector3;
    amount: number;
    gain: number;
  } = null;
  private blink: null | { morphs: string[]; every: number } = null;

  private constructor(root: THREE.Object3D, info: CharacterInfo) {
    this.root = root;
    this.info = info;
    this.holder.name = info.name;
    this.holder.add(root);
    this.mixer = new THREE.AnimationMixer(root);
  }

  static async create(name: string, spec: CharacterSpec, env: CharacterEnv): Promise<Character> {
    const { root, clips: embedded } = await loadModel(spec.model);
    const warnings: string[] = [];

    // Size: fit to `height` if given; FBX from Mixamo arrives in centimetres.
    root.updateMatrixWorld(true);
    const box = new THREE.Box3().setFromObject(root);
    const rawHeight = Math.max(box.max.y - box.min.y, 1e-6);
    let fit = 1;
    if (spec.height) fit = spec.height / rawHeight;
    else if (rawHeight > 20) {
      fit = 1.7 / rawHeight;
      warnings.push(`Model cao ${rawHeight.toFixed(0)} đơn vị (có thể là cm), đã thu về 1,7 m. Đặt "height" để chỉnh.`);
    }
    root.scale.multiplyScalar(fit * (spec.scale ?? 1));

    root.traverse((o) => {
      const mesh = o as THREE.Mesh;
      if (!mesh.isMesh) return;
      mesh.castShadow = true;
      mesh.receiveShadow = false;
      // Skinned meshes keep their bind-pose bounds; culling them makes limbs vanish mid-move.
      if ((mesh as THREE.SkinnedMesh).isSkinnedMesh) mesh.frustumCulled = false;
    });

    const info: CharacterInfo = {
      name,
      model: spec.model,
      height: Number((rawHeight * fit * (spec.scale ?? 1)).toFixed(3)),
      scale: Number((fit * (spec.scale ?? 1)).toPrecision(4)),
      clips: [],
      morphs: [],
      bones: [],
      warnings,
    };
    const c = new Character(root, info);

    // Clips: embedded ones keep their names; extra files are named by their key.
    const clips = new Map<string, THREE.AnimationClip>();
    for (const clip of embedded) {
      if (clip.duration <= 0 || !clip.tracks.length) continue; // e.g. empty "Take 001" in FBX
      const p = prepareClip(clip, root, { external: false, inPlace: !!spec.inPlace });
      clips.set(clip.name, p.clip);
      info.clips.push({ name: clip.name, duration: round(clip.duration), source: spec.model });
    }
    for (const [key, path] of Object.entries(spec.animations ?? {})) {
      const raw = await loadAnimation(path);
      const p = prepareClip(raw, root, { external: true, inPlace: !!spec.inPlace, name: key });
      clips.set(key, p.clip);
      info.clips.push({ name: key, duration: round(raw.duration), source: path, matched: `${p.matched}/${p.total}` });
      if (p.matched === 0) warnings.push(`Clip "${key}" (${path}) không khớp xương nào của model; rig khác nhau.`);
      else if (p.matched < p.total * 0.6) warnings.push(`Clip "${key}" chỉ khớp ${p.matched}/${p.total} track; kiểm tra tên xương.`);
    }

    root.traverse((o) => {
      const mesh = o as THREE.Mesh;
      if ((o as THREE.Bone).isBone && !info.bones.includes(o.name)) info.bones.push(o.name);
      if (mesh.isMesh && mesh.morphTargetDictionary) {
        for (const [m, index] of Object.entries(mesh.morphTargetDictionary)) {
          if (!c.morphs.has(m)) c.morphs.set(m, []);
          c.morphs.get(m)!.push({ mesh, index });
        }
      }
    });
    info.morphs = [...c.morphs.keys()];

    const cues = env.cues;
    const at = (v: Time) => parseTime(v, cues);

    // Actions. With none given, loop a clip called *idle* if there is one.
    let actions = spec.actions ?? [];
    if (!actions.length) {
      const idle = [...clips.keys()].find((n) => /idle/i.test(n));
      if (idle) actions = [{ at: 0, clip: idle }];
    }
    for (const k of actions) {
      const clip = clips.get(k.clip);
      if (!clip) throw new Error(`${name}: không có clip "${k.clip}". Có: ${[...clips.keys()].join(', ') || 'không có'}`);
      // Each key gets its own action so the same clip can appear twice with its own timing.
      const action = c.mixer.clipAction(clip.clone());
      action.play();
      action.setEffectiveWeight(0);
      c.tracks.push({
        t: at(k.at),
        fade: k.fade ?? 0.3,
        speed: k.speed ?? 1,
        offset: k.offset ?? 0,
        loop: k.loop ?? true,
        duration: clip.duration,
        action,
      });
    }
    c.tracks.sort((a, b) => a.t - b.t);

    // Moves, filled forward so a key may set only pos or only rotY.
    let pos: Vec3 = spec.position ?? [0, 0, 0];
    let rotY = spec.rotY ?? 0;
    c.moves.push({ t: 0, pos, rotY }); // start pose; the first key moves from here (use `dur` to delay)
    for (const k of [...(spec.moves ?? [])].map((k) => ({ ...k, t: at(k.at) })).sort((a, b) => a.t - b.t)) {
      pos = k.pos ?? pos;
      rotY = k.rotY ?? rotY;
      c.moves.push({ t: k.t, pos, rotY, ease: k.ease, dur: k.dur });
    }
    c.applyMove(0);

    for (const k of spec.face ?? []) {
      c.requireMorph(k.morph, 'face');
      if (!c.face.has(k.morph)) c.face.set(k.morph, []);
      c.face.get(k.morph)!.push({ t: at(k.at), value: k.value, fade: k.fade ?? 0.25 });
      c.controlled.add(k.morph);
    }
    for (const list of c.face.values()) list.sort((a, b) => a.t - b.t);

    if (spec.lipsync) {
      const ls = spec.lipsync;
      const envelope = await env.envelope(ls.audio);
      if (!envelope) warnings.push('lipsync: không có audio để bám theo, miệng sẽ đứng yên.');
      else {
        const morphs: [string, number][] =
          typeof ls.morph === 'string' ? [[ls.morph, 1]] : Object.entries(ls.morph ?? {});
        morphs.forEach(([m]) => {
          c.requireMorph(m, 'lipsync');
          c.controlled.add(m);
        });
        const bone = ls.bone ? findNode(root, ls.bone) : null;
        if (ls.bone && !bone) throw new Error(`${name}: lipsync không tìm thấy xương "${ls.bone}". Xem danh sách bằng npm run inspect.`);
        if (!morphs.length && !bone) throw new Error(`${name}: lipsync cần "morph" hoặc "bone".`);
        const axis = new THREE.Vector3(...({ x: [1, 0, 0], y: [0, 1, 0], z: [0, 0, 1] } as const)[ls.axis ?? 'x']);
        c.lip = {
          env: envelope,
          ranges: (ls.ranges ?? []).map(([a, b]) => [at(a), at(b)]),
          morphs,
          bone,
          rest: bone ? bone.quaternion.clone() : new THREE.Quaternion(),
          axis,
          amount: ls.amount ?? 0.25,
          gain: ls.gain ?? 1,
        };
      }
    }

    if (spec.blink) {
      const morphs = Array.isArray(spec.blink.morph) ? spec.blink.morph : [spec.blink.morph];
      morphs.forEach((m) => {
        c.requireMorph(m, 'blink');
        c.controlled.add(m);
      });
      c.blink = { morphs, every: spec.blink.every ?? 3.6 };
    }

    c.apply(0);
    return c;
  }

  private requireMorph(m: string, where: string) {
    if (!this.morphs.has(m)) {
      const have = [...this.morphs.keys()];
      throw new Error(`${this.info.name}: ${where} dùng morph "${m}" nhưng model không có. Có: ${have.join(', ') || 'không có morph nào'}`);
    }
  }

  private applyMove(t: number) {
    const [a, b, p] = span(this.moves, t);
    this.holder.position.set(lerp(a.pos[0], b.pos[0], p), lerp(a.pos[1], b.pos[1], p), lerp(a.pos[2], b.pos[2], p));
    this.holder.rotation.y = lerp(a.rotY, b.rotY, p) * DEG;
  }

  /** Pose the character for time `t`. Stateless: any order of calls gives the same frame. */
  apply(t: number) {
    if (this.moves.length > 1) this.applyMove(t);

    if (this.lip?.bone) this.lip.bone.quaternion.copy(this.lip.rest);

    // Each action fades in over the ones before it: w_i = a_i · Π_{j>i}(1 − a_j).
    const n = this.tracks.length;
    if (n) {
      let remaining = 1;
      for (let i = n - 1; i >= 0; i--) {
        const k = this.tracks[i];
        const a = i === 0 ? 1 : t < k.t ? 0 : k.fade > 0 ? smoothstep((t - k.t) / k.fade) : 1;
        const w = a * remaining;
        remaining *= 1 - a;
        let local = Math.max(0, t - k.t) * k.speed + k.offset;
        if (k.duration <= 0) local = 0;
        else local = k.loop ? ((local % k.duration) + k.duration) % k.duration : Math.min(local, k.duration - 1e-4);
        k.action.time = local;
        k.action.setEffectiveWeight(w);
      }
      this.mixer.update(0);
    }

    if (!this.controlled.size && !this.lip?.bone) return;
    const values = new Map<string, number>();
    for (const m of this.controlled) values.set(m, 0);

    for (const [m, keys] of this.face) {
      let v = 0;
      for (let i = 0; i < keys.length; i++) {
        const k = keys[i];
        if (t < k.t) break;
        const until = Math.min(t, keys[i + 1]?.t ?? Infinity);
        v += (k.value - v) * smoothstep(k.fade > 0 ? (until - k.t) / k.fade : 1);
      }
      values.set(m, v);
    }

    if (this.lip) {
      const L = this.lip;
      let gate = L.ranges.length ? 0 : 1;
      for (const [s, e] of L.ranges) gate = Math.max(gate, clamp01((t - s) / 0.06) * clamp01((e - t) / 0.06));
      const open = clamp01(sampleEnvelope(L.env, t) * L.gain) ** 0.8 * gate;
      for (const [m, w] of L.morphs) values.set(m, (values.get(m) ?? 0) + open * w);
      if (L.bone) L.bone.quaternion.multiply(new THREE.Quaternion().setFromAxisAngle(L.axis, open * L.amount));
    }

    if (this.blink) {
      const B = this.blink;
      const k0 = Math.floor(t / B.every);
      let v = 0;
      for (let k = k0 - 1; k <= k0 + 1; k++) {
        const start = (k + 0.2 + hash01(k) * 0.6) * B.every;
        const x = (t - start) / 0.16;
        if (x > 0 && x < 1) v = Math.max(v, 1 - Math.abs(x * 2 - 1));
      }
      for (const m of B.morphs) values.set(m, Math.max(values.get(m) ?? 0, v));
    }

    for (const [m, v] of values) {
      for (const ref of this.morphs.get(m) ?? []) {
        if (ref.mesh.morphTargetInfluences) ref.mesh.morphTargetInfluences[ref.index] = clamp01(v);
      }
    }
  }

  bone(name: string): THREE.Object3D | null {
    return findNode(this.root, name);
  }
}

const round = (x: number) => Math.round(x * 1000) / 1000;
