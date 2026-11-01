import type { Ease } from './types';

export const clamp01 = (x: number) => (x < 0 ? 0 : x > 1 ? 1 : x);
export const lerp = (a: number, b: number, p: number) => a + (b - a) * p;
export const smoothstep = (x: number) => {
  const c = clamp01(x);
  return c * c * (3 - 2 * c);
};

const EASES: Record<Ease, (x: number) => number> = {
  linear: (x) => x,
  in: (x) => x * x * x,
  out: (x) => 1 - (1 - x) ** 3,
  inOut: (x) => (x < 0.5 ? 4 * x * x * x : 1 - (-2 * x + 2) ** 3 / 2),
  cut: () => 0,
};

export interface TimedKey {
  t: number;
  ease?: Ease;
  dur?: number;
}

/**
 * Find the pair of keys around `t` and the eased progress between them.
 * Keys must be sorted by `t`. The ease and duration of the *later* key describe the move into it.
 */
export function span<K extends TimedKey>(keys: K[], t: number): [K, K, number] {
  const first = keys[0];
  if (t <= first.t) return [first, first, 0];
  let i = 0;
  while (i + 1 < keys.length && keys[i + 1].t <= t) i++;
  const a = keys[i];
  const b = keys[i + 1];
  if (!b) return [a, a, 0];
  const start = b.dur !== undefined ? Math.max(a.t, b.t - b.dur) : a.t;
  const len = b.t - start;
  const raw = len > 0 ? clamp01((t - start) / len) : 1;
  return [a, b, EASES[b.ease ?? 'inOut'](raw)];
}

/** Deterministic pseudo-random in [0, 1) for an integer seed. */
export function hash01(n: number): number {
  const x = Math.sin(n * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
}
