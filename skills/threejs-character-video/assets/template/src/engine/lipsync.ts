import { clamp01 } from './keys';

/** Mouth-openness curve sampled at a fixed rate, values 0–1. */
export interface Envelope {
  rate: number;
  data: Float32Array;
}

/**
 * Loudness envelope of a voice track. Syllables show up as peaks, which is enough to move a
 * jaw or a mouth-open blendshape convincingly for a stylised character. Pure function of the
 * decoded audio, so preview and render match.
 */
export function computeEnvelope(buf: AudioBuffer, rate = 60): Envelope {
  const sr = buf.sampleRate;
  const len = buf.length;
  const mono = new Float32Array(len);
  for (let c = 0; c < buf.numberOfChannels; c++) {
    const ch = buf.getChannelData(c);
    for (let i = 0; i < len; i++) mono[i] += ch[i] / buf.numberOfChannels;
  }
  // Prefix sums of squares → RMS of any window in O(1).
  const sq = new Float64Array(len + 1);
  for (let i = 0; i < len; i++) sq[i + 1] = sq[i] + mono[i] * mono[i];

  const n = Math.ceil(buf.duration * rate) + 1;
  const half = Math.max(1, Math.round(sr / rate));
  const rms = new Float32Array(n);
  for (let i = 0; i < n; i++) {
    const c = Math.round((i / rate) * sr);
    const a = Math.max(0, c - half);
    const b = Math.min(len, c + half);
    rms[i] = b > a ? Math.sqrt((sq[b] - sq[a]) / (b - a)) : 0;
  }

  const voiced = Array.from(rms).filter((v) => v > 1e-4).sort((x, y) => x - y);
  const hi = voiced.length ? voiced[Math.floor(voiced.length * 0.95)] : 1;
  const lo = hi * 0.12;
  const out = new Float32Array(n);
  let y = 0;
  for (let i = 0; i < n; i++) {
    const x = clamp01((rms[i] - lo) / (hi - lo || 1));
    y += (x - y) * (x > y ? 0.7 : 0.3); // fast open, slower close
    out[i] = y;
  }
  return { rate, data: out };
}

export function sampleEnvelope(env: Envelope, t: number): number {
  const f = t * env.rate;
  const i = Math.floor(f);
  const d = env.data;
  if (i < 0 || d.length === 0) return 0;
  if (i >= d.length - 1) return 0;
  return d[i] + (d[i + 1] - d[i]) * (f - i);
}
