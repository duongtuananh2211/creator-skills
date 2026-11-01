import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import type { EpisodeSpec } from './types';
import { loadTexture } from './assets';

export interface Stage {
  renderer: THREE.WebGLRenderer;
  scene: THREE.Scene;
  camera: THREE.PerspectiveCamera;
  canvas: HTMLCanvasElement;
  transparent: boolean;
}

const IMAGE_RE = /\.(png|jpe?g|webp|avif)$/i;

export async function createStage(spec: EpisodeSpec, width: number, height: number, render: boolean): Promise<Stage> {
  const transparent = spec.background === 'transparent';
  const renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: transparent,
    // Keep the frame readable by toDataURL between render and capture.
    preserveDrawingBuffer: render,
  });
  renderer.setPixelRatio(1);
  renderer.setSize(width, height, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = spec.lights?.exposure ?? 1;
  renderer.shadowMap.enabled = spec.lights?.shadows ?? true;
  renderer.shadowMap.type = THREE.PCFShadowMap;
  if (transparent) renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(35, width / height, 0.05, 500);

  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = spec.lights?.env ?? 0.6;
  pmrem.dispose();

  const L = spec.lights ?? {};
  const key = new THREE.DirectionalLight(0xffffff, L.key ?? 2.2);
  key.position.set(...(L.keyPos ?? [2.5, 5, 4]));
  key.castShadow = L.shadows ?? true;
  key.shadow.mapSize.set(2048, 2048);
  const sc = key.shadow.camera;
  sc.left = sc.bottom = -6;
  sc.right = sc.top = 6;
  sc.near = 0.5;
  sc.far = 30;
  key.shadow.bias = -0.0004;
  key.shadow.normalBias = 0.02;
  scene.add(key, key.target);

  const rim = new THREE.DirectionalLight(0xbcd4ff, L.rim ?? 1.2);
  rim.position.set(-3, 3.5, -4);
  scene.add(rim);

  if (spec.ground !== false) {
    const g = spec.ground ?? {};
    const size = g.size ?? 40;
    const mat = g.color
      ? new THREE.MeshStandardMaterial({ color: g.color, roughness: 0.9 })
      : new THREE.ShadowMaterial({ opacity: g.shadowOpacity ?? 0.3 });
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(size, size), mat);
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    ground.name = 'ground';
    scene.add(ground);
  }

  await setBackground(scene, spec.background, width / height);
  return { renderer, scene, camera, canvas: renderer.domElement, transparent };
}

async function setBackground(scene: THREE.Scene, bg: EpisodeSpec['background'], aspect: number) {
  if (bg === 'transparent') return;
  if (bg === undefined) {
    scene.background = gradient('#2b3245', '#12151d');
  } else if (typeof bg === 'object') {
    scene.background = gradient(bg.gradient[0], bg.gradient[1]);
  } else if (IMAGE_RE.test(bg)) {
    const tex = await loadTexture(bg);
    const img = tex.image as { width: number; height: number };
    const imgAspect = img.width / img.height;
    // Cover-fit: crop the image, never stretch it.
    if (imgAspect > aspect) {
      tex.repeat.set(aspect / imgAspect, 1);
      tex.offset.set((1 - tex.repeat.x) / 2, 0);
    } else {
      tex.repeat.set(1, imgAspect / aspect);
      tex.offset.set(0, (1 - tex.repeat.y) / 2);
    }
    scene.background = tex;
  } else {
    scene.background = new THREE.Color(bg);
  }
}

function gradient(top: string, bottom: string): THREE.Texture {
  const c = document.createElement('canvas');
  c.width = 4;
  c.height = 512;
  const ctx = c.getContext('2d')!;
  const g = ctx.createLinearGradient(0, 0, 0, c.height);
  g.addColorStop(0, top);
  g.addColorStop(1, bottom);
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, c.width, c.height);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}
