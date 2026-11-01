import type { Time } from './types';

export interface Cue {
  index: number;
  start: number;
  end: number;
  text: string;
}

const TIME_RE = /^(cue:(\d+)(:end)?|\d+(?::\d+){0,2}(?:\.\d+)?)\s*(?:([+-])\s*(\d+(?:\.\d+)?))?$/;

/** Resolve a Time to seconds. Throws with a readable message on a bad value. */
export function parseTime(value: Time, cues: Cue[] = []): number {
  if (typeof value === 'number') return value;
  const m = value.trim().match(TIME_RE);
  if (!m) throw new Error(`Thời điểm không hợp lệ: "${value}" (dùng 3.5, "1:02.5", "cue:4", "cue:4:end+0.2")`);
  let base: number;
  if (m[2]) {
    const n = Number(m[2]);
    const cue = cues.find((c) => c.index === n);
    if (!cue) {
      const hint = cues.length ? `có cue 1–${cues[cues.length - 1].index}` : 'chưa khai báo subtitles';
      throw new Error(`Không có "cue:${n}" (${hint})`);
    }
    base = m[3] ? cue.end : cue.start;
  } else {
    base = m[1].split(':').reduce((acc, part) => acc * 60 + Number(part), 0);
  }
  if (m[4]) base += (m[4] === '-' ? -1 : 1) * Number(m[5]);
  return base;
}

/** Parse .srt or .vtt text. Cue index = the number in the file, or its position (1-based). */
export function parseSubtitles(text: string): Cue[] {
  const cues: Cue[] = [];
  const blocks = text.replace(/\r/g, '').replace(/^﻿/, '').split(/\n{2,}/);
  const stamp = (s: string) => {
    const p = s.trim().replace(',', '.').split(':').map(Number);
    return p.length === 3 ? p[0] * 3600 + p[1] * 60 + p[2] : p[0] * 60 + p[1];
  };
  for (const block of blocks) {
    const lines = block.split('\n').filter((l) => l.trim() !== '');
    const ti = lines.findIndex((l) => l.includes('-->'));
    if (ti < 0) continue;
    const [a, b] = lines[ti].split('-->');
    const num = ti > 0 ? Number(lines[ti - 1].trim()) : NaN;
    cues.push({
      index: Number.isInteger(num) && num > 0 ? num : cues.length + 1,
      start: stamp(a),
      end: stamp(b.trim().split(/\s+/)[0]),
      text: lines.slice(ti + 1).join(' ').replace(/<[^>]+>/g, ''),
    });
  }
  return cues;
}

export function formatClock(t: number): string {
  const m = Math.floor(t / 60);
  const s = t - m * 60;
  return `${String(m).padStart(2, '0')}:${s.toFixed(2).padStart(5, '0')}`;
}
