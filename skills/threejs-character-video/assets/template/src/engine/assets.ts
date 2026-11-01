import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { FBXLoader } from 'three/addons/loaders/FBXLoader.js';
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';
import * as SkeletonUtils from 'three/addons/utils/SkeletonUtils.js';

/** Paths in episodes are relative to public/. */
export function assetUrl(path: string): string {
  if (/^(https?:|data:|blob:|\/)/.test(path)) return path;
  return import.meta.env.BASE_URL + path.replace(/^\.?\//, '');
}

export const baseName = (path: string) =>
  path.split(/[\\/]/).pop()!.replace(/\.[^.]+$/, '');

interface Loaded {
  scene: THREE.Object3D;
  animations: THREE.AnimationClip[];
}

let gltfLoader: GLTFLoader | null = null;
function gltf(): GLTFLoader {
  if (!gltfLoader) {
    const draco = new DRACOLoader().setDecoderPath('/draco/');
    gltfLoader = new GLTFLoader().setDRACOLoader(draco).setMeshoptDecoder(MeshoptDecoder);
  }
  return gltfLoader;
}

const cache = new Map<string, Promise<Loaded>>();

function loadRaw(path: string): Promise<Loaded> {
  let p = cache.get(path);
  if (!p) {
    const url = assetUrl(path);
    const ext = path.toLowerCase().split('?')[0].split('.').pop();
    if (ext === 'fbx') {
      p = new FBXLoader().loadAsync(url).then((g) => ({ scene: g, animations: g.animations }));
    } else if (ext === 'glb' || ext === 'gltf') {
      p = gltf().loadAsync(url).then((g) => ({ scene: g.scene, animations: g.animations }));
    } else {
      p = Promise.reject(new Error(`Chưa hỗ trợ định dạng .${ext} (${path}). Dùng .glb, .gltf hoặc .fbx`));
    }
    p = p.catch((e) => {
      cache.delete(path);
      throw new Error(`Không tải được ${path} (${url}): ${e?.message ?? e}`);
    });
    cache.set(path, p);
  }
  return p;
}

/** A fresh copy of the model (skeletons cloned properly) plus its embedded clips. */
export async function loadModel(path: string): Promise<{ root: THREE.Object3D; clips: THREE.AnimationClip[] }> {
  const src = await loadRaw(path);
  const root = SkeletonUtils.clone(src.scene);
  const clips = src.animations.map((c) => {
    const clip = c.clone();
    // Mixamo FBX clips are all called "mixamo.com"; name them after the file instead.
    if (!clip.name || clip.name === 'mixamo.com') clip.name = baseName(path);
    return clip;
  });
  return { root, clips };
}

/** First clip of an animation file, or `file.fbx#ClipName`. */
export async function loadAnimation(path: string): Promise<THREE.AnimationClip> {
  const [file, wanted] = path.split('#');
  const src = await loadRaw(file);
  const clip = wanted ? src.animations.find((c) => c.name === wanted) : src.animations[0];
  if (!clip) {
    const names = src.animations.map((c) => c.name).join(', ') || 'không có';
    throw new Error(`File ${file} không có clip ${wanted ? `"${wanted}"` : 'nào'} (có: ${names})`);
  }
  return clip.clone();
}

export async function loadTexture(path: string): Promise<THREE.Texture> {
  try {
    const tex = await new THREE.TextureLoader().loadAsync(assetUrl(path));
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
  } catch (e) {
    throw new Error(`Không tải được ảnh ${path}`);
  }
}

export async function fetchArrayBuffer(path: string): Promise<ArrayBuffer | null> {
  const res = await fetch(assetUrl(path));
  if (!res.ok) return null;
  const type = res.headers.get('content-type') ?? '';
  // Vite answers unknown paths with index.html; treat that as missing.
  if (type.includes('text/html')) return null;
  return res.arrayBuffer();
}

export async function fetchText(path: string): Promise<string | null> {
  const buf = await fetchArrayBuffer(path);
  return buf ? new TextDecoder().decode(buf) : null;
}
