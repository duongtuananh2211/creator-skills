import * as THREE from 'three';

/**
 * Compare bone names across exporters: "mixamorig:LeftArm", "mixamorigLeftArm",
 * "mixamorig1:LeftArm" and "LeftArm" all become "leftarm".
 */
export function normName(name: string): string {
  return name.toLowerCase().replace(/^.*?mixamorig\d*/, '').replace(/[^a-z0-9]/g, '');
}

export function findNode(root: THREE.Object3D, name: string): THREE.Object3D | null {
  const exact = root.getObjectByName(name);
  if (exact) return exact;
  const key = normName(name);
  let found: THREE.Object3D | null = null;
  root.traverse((o) => {
    if (!found && o.name && normName(o.name) === key) found = o;
  });
  return found;
}

export function findHips(root: THREE.Object3D): THREE.Object3D | null {
  const named = findNode(root, 'Hips');
  if (named) return named;
  let rootBone: THREE.Object3D | null = null;
  root.traverse((o) => {
    if (!rootBone && (o as THREE.Bone).isBone && !(o.parent as THREE.Bone | null)?.isBone) rootBone = o;
  });
  return rootBone;
}

export interface PreparedClip {
  clip: THREE.AnimationClip;
  matched: number;
  total: number;
}

/**
 * Make a clip play on `root`: rename tracks to the model's bone names, and for clips from
 * another file keep only rotations plus the hips position (rescaled to the model's units),
 * since per-bone offsets from a different export would distort the mesh.
 */
export function prepareClip(
  clip: THREE.AnimationClip,
  root: THREE.Object3D,
  opts: { external: boolean; inPlace: boolean; name?: string },
): PreparedClip {
  const exact = new Set<string>();
  const byNorm = new Map<string, string>();
  root.traverse((o) => {
    if (!o.name) return;
    exact.add(o.name);
    const k = normName(o.name);
    if (!byNorm.has(k)) byNorm.set(k, o.name);
  });
  const hips = findHips(root);
  const tracks: THREE.KeyframeTrack[] = [];
  let matched = 0;

  for (const track of clip.tracks) {
    let parsed: { nodeName?: string; propertyName: string };
    try {
      parsed = THREE.PropertyBinding.parseTrackName(track.name);
    } catch {
      continue;
    }
    const node = parsed.nodeName ?? '';
    const target = exact.has(node) ? node : byNorm.get(normName(node));
    if (!target) continue;
    matched++;
    const prop = parsed.propertyName;
    const isHips = hips !== null && target === hips.name;
    if (opts.external && (prop === 'scale' || (prop === 'position' && !isHips))) continue;

    const t = track.clone();
    if (track.name.startsWith(node)) t.name = target + track.name.slice(node.length);

    if (prop === 'position' && isHips) {
      const v = t.values;
      if (opts.external && hips && v.length >= 3) {
        const ratio = Math.abs(v[1]) > 1e-6 && Math.abs(hips.position.y) > 1e-6 ? hips.position.y / v[1] : 1;
        if (Number.isFinite(ratio) && ratio > 0) for (let i = 0; i < v.length; i++) v[i] *= ratio;
      }
      if (opts.inPlace) {
        for (let i = 0; i + 2 < v.length; i += 3) {
          v[i] = v[0];
          v[i + 2] = v[2];
        }
      }
    }
    tracks.push(t);
  }
  return {
    clip: new THREE.AnimationClip(opts.name ?? clip.name, clip.duration, tracks),
    matched,
    total: clip.tracks.length,
  };
}
