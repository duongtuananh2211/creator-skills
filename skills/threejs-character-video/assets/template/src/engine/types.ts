import type * as THREE from 'three';
import type { Character } from './character';

/**
 * A point in time. Seconds (`3.5`), a clock string (`"1:02.5"`), or a subtitle cue
 * (`"cue:4"` = start of cue 4, `"cue:4:end"` = its end), optionally shifted (`"cue:4+0.3"`).
 */
export type Time = number | string;
export type Vec3 = [number, number, number];
/** How a key is reached from the previous one. `cut` = hold the previous value, then jump. */
export type Ease = 'linear' | 'in' | 'out' | 'inOut' | 'cut';
export type Format = '9:16' | '16:9' | '1:1' | '4:5';

export interface CameraKey {
  at: Time;
  pos: Vec3;
  target: Vec3;
  /** Vertical field of view in degrees. Defaults to the previous key's, or 35. */
  fov?: number;
  ease?: Ease;
  /** Seconds the move into this key takes, ending at `at`. Omitted = starts at the previous key. */
  dur?: number;
}

export interface ActionKey {
  at: Time;
  /** Clip name, as listed by `npm run inspect`. */
  clip: string;
  /** Default true. Set false for one-off gestures (wave, nod) and follow with another action. */
  loop?: boolean;
  speed?: number;
  /** Crossfade from the previous action, seconds. Default 0.3. */
  fade?: number;
  /** Start this many seconds into the clip. */
  offset?: number;
}

export interface MoveKey {
  at: Time;
  /** World position of the character's feet. Omitted = keep the previous key's. */
  pos?: Vec3;
  /** Facing, degrees around Y. 0 = facing +Z (towards a default camera). */
  rotY?: number;
  ease?: Ease;
  dur?: number;
}

export interface FaceKey {
  at: Time;
  /** Morph target (blendshape) name, as listed by `npm run inspect`. */
  morph: string;
  value: number;
  /** Seconds to reach `value`. Default 0.25. */
  fade?: number;
}

export interface LipSyncSpec {
  /** Audio to follow. Defaults to the episode audio. */
  audio?: string;
  /** Only move the mouth inside these ranges (when several characters share one voice track). */
  ranges?: [Time, Time][];
  /** Mouth morph(s): `"jawOpen"` or weights like `{ jawOpen: 0.8, mouthFunnel: 0.2 }`. */
  morph?: string | Record<string, number>;
  /** Or rotate a bone (a jaw, or the head as a talking nod when there is no mouth). */
  bone?: string;
  axis?: 'x' | 'y' | 'z';
  /** Bone rotation at full loudness, radians. Default 0.25. */
  amount?: number;
  /** Multiplies loudness before clamping to 1. Default 1. */
  gain?: number;
}

export interface BlinkSpec {
  morph: string | string[];
  /** Average seconds between blinks. Default 3.6. */
  every?: number;
}

export interface CharacterSpec {
  /** Path under public/, e.g. `models/xa.glb`. GLB, glTF or FBX. */
  model: string;
  /** Extra animation files, `{ wave: 'anims/Waving.fbx' }`. Mixamo FBX bone names are matched automatically. */
  animations?: Record<string, string>;
  position?: Vec3;
  rotY?: number;
  /** Scale the model so it is this tall (scene units are metres). */
  height?: number;
  /** Extra multiplier on top of `height`. */
  scale?: number;
  /** Strip horizontal root motion from clips (walk in place, move with `moves`). */
  inPlace?: boolean;
  actions?: ActionKey[];
  moves?: MoveKey[];
  face?: FaceKey[];
  lipsync?: LipSyncSpec;
  blink?: BlinkSpec;
}

export interface PropSpec {
  model: string;
  position?: Vec3;
  rotY?: number;
  height?: number;
  scale?: number;
}

export interface LightSpec {
  /** Key light intensity. Default 2.2. */
  key?: number;
  keyPos?: Vec3;
  /** Back/rim light intensity. Default 1.2. */
  rim?: number;
  /** Image-based ambient light. Default 0.6. */
  env?: number;
  shadows?: boolean;
  exposure?: number;
}

export interface EpisodeContext {
  THREE: typeof THREE;
  scene: THREE.Scene;
  camera: THREE.PerspectiveCamera;
  renderer: THREE.WebGLRenderer;
  characters: Record<string, Character>;
  props: THREE.Object3D[];
  fps: number;
  duration: number;
}

export interface EpisodeSpec {
  title?: string;
  format: Format;
  /** Override the pixel size, `[width, height]`. */
  size?: [number, number];
  fps?: number;
  /** `'audio'` (default when there is audio) or a Time. */
  duration?: Time | 'audio';
  /** Voice/music track under public/, muxed into the render. */
  audio?: string;
  /** .srt or .vtt for the audio; enables `"cue:N"` times and shows lines in the preview. */
  subtitles?: string;
  /**
   * `'#1d2433'`, `{ gradient: ['#top', '#bottom'] }`, an image under public/ (cover-fit),
   * or `'transparent'` (render with `--alpha` for a ProRes 4444 .mov).
   */
  background?: string | { gradient: [string, string] };
  /** Ground plane. Default: invisible plane that only receives shadows. */
  ground?: false | { color?: string; shadowOpacity?: number; size?: number };
  lights?: LightSpec;
  /** Small handheld drift added to the camera, metres. Default 0. */
  cameraSway?: number;
  characters: Record<string, CharacterSpec>;
  props?: PropSpec[];
  camera: CameraKey[];
  /** Runs once after loading. Add custom objects here. */
  setup?: (ctx: EpisodeContext) => void | Promise<void>;
  /** Runs every frame before rendering. Must depend only on `t` so renders are repeatable. */
  update?: (ctx: EpisodeContext, t: number) => void;
}

export function defineEpisode(spec: EpisodeSpec): EpisodeSpec {
  return spec;
}
