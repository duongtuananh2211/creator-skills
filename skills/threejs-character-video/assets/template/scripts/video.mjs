#!/usr/bin/env node
/**
 * Render episodes to video by stepping the page frame by frame in headless Chrome.
 *
 *   node scripts/video.mjs render <episode> [--out renders/x.mp4] [--from 0] [--to 12.5]
 *                                           [--scale 0.5] [--crf 18] [--jpeg] [--alpha] [--headful]
 *   node scripts/video.mjs still  <episode> --at 1.5[,4,8] [--out renders/x.png] [--scale 0.5]
 *   node scripts/video.mjs inspect <episode | models/x.glb> [--anims wave=anims/Wave.fbx,...]
 *
 * Times accept seconds or mm:ss.s. Progress goes to stderr; a JSON summary goes to stdout.
 * Needs ffmpeg on PATH and a Chrome/Chromium/Edge install (or CHROME_PATH).
 */
import { spawn, spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { once } from 'node:events';
import { dirname, join, resolve } from 'node:path';
import { platform } from 'node:os';

const ROOT = resolve(dirname(new URL(import.meta.url).pathname), '..');
process.chdir(ROOT);

const [cmd, target, ...rest] = process.argv.slice(2);
const flags = {};
for (let i = 0; i < rest.length; i++) {
  const a = rest[i];
  if (!a.startsWith('--')) continue;
  const key = a.slice(2);
  const next = rest[i + 1];
  if (next === undefined || next.startsWith('--')) flags[key] = true;
  else {
    flags[key] = next;
    i++;
  }
}

const log = (msg) => process.stderr.write(msg + '\n');
const emit = (obj) => process.stdout.write(JSON.stringify(obj, null, 1) + '\n');
function fail(error, hint) {
  emit({ error, ...(hint ? { hint } : {}) });
  process.exit(1);
}

if (!['render', 'still', 'inspect'].includes(cmd) || !target) {
  fail('Cách dùng: render|still|inspect <tập hoặc model> [tuỳ chọn]', 'Ví dụ: npm run render -- demo --to 5 --scale 0.5');
}

const seconds = (v) => {
  if (v === undefined || v === true) return undefined;
  const s = String(v);
  const n = s.includes(':') ? s.split(':').reduce((a, p) => a * 60 + Number(p), 0) : Number(s);
  if (!Number.isFinite(n)) fail(`Thời điểm không hợp lệ: ${s}`);
  return n;
};

function findChrome() {
  if (process.env.CHROME_PATH) return process.env.CHROME_PATH;
  const candidates = {
    darwin: [
      '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      '/Applications/Chromium.app/Contents/MacOS/Chromium',
      '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
      '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
      '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary',
    ],
    linux: ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/microsoft-edge'],
    win32: [
      `${process.env['PROGRAMFILES']}\\Google\\Chrome\\Application\\chrome.exe`,
      `${process.env['PROGRAMFILES(X86)']}\\Google\\Chrome\\Application\\chrome.exe`,
      `${process.env['PROGRAMFILES(X86)']}\\Microsoft\\Edge\\Application\\msedge.exe`,
    ],
  }[platform()] ?? [];
  return candidates.find((p) => p && existsSync(p));
}

async function open(query) {
  const chrome = findChrome();
  if (!chrome) {
    fail('Không tìm thấy Chrome/Chromium/Edge', 'Cài Chrome, hoặc đặt CHROME_PATH=/đường/dẫn/chrome, hoặc chạy: npx @puppeteer/browsers install chrome-headless-shell@stable');
  }
  const { createServer } = await import('vite');
  const puppeteer = (await import('puppeteer-core')).default;

  const server = await createServer({
    configFile: join(ROOT, 'vite.config.ts'),
    logLevel: 'error',
    server: { port: 5199, strictPort: false, host: '127.0.0.1', open: false, hmr: false },
  });
  await server.listen();
  const base = server.resolvedUrls.local[0];

  const args = ['--ignore-gpu-blocklist', '--enable-gpu-rasterization', '--autoplay-policy=no-user-gesture-required', '--mute-audio'];
  if (platform() === 'darwin') args.push('--use-angle=metal');
  if (process.env.RENDER_SWIFTSHADER) args.push('--use-angle=swiftshader', '--enable-unsafe-swiftshader');
  const browser = await puppeteer.launch({
    executablePath: chrome,
    headless: flags.headful ? false : true,
    args,
    defaultViewport: { width: 1280, height: 800 },
    protocolTimeout: 600_000,
  });
  const page = await browser.newPage();
  page.on('console', (m) => {
    if (m.type() === 'error' || m.type() === 'warn' || m.type() === 'warning') log(`[trang] ${m.text()}`);
  });
  page.on('pageerror', (e) => log(`[trang] ${e.message}`));

  const close = async () => {
    await browser.close().catch(() => {});
    await server.close().catch(() => {});
  };
  const url = `${base}?${query}`;
  // Vite may reload once while it pre-bundles dependencies on first run; retry through that.
  for (let attempt = 0; ; attempt++) {
    try {
      await page.goto(url, { waitUntil: 'load', timeout: 120_000 });
      await page.waitForFunction(() => window.__video && (window.__video.ready || window.__video.error), { timeout: 180_000, polling: 200 });
      const err = await page.evaluate(() => window.__video.error);
      if (err) {
        await close();
        fail(err);
      }
      break;
    } catch (e) {
      if (attempt < 2 && /context was destroyed|navigation|detached/i.test(String(e))) continue;
      await close();
      fail(`Trang không sẵn sàng: ${e.message}`, 'Chạy npm run dev rồi mở trang để xem lỗi trong console.');
    }
  }
  const info = await page.evaluate(() => window.__video.info);
  return { page, info, close };
}

function warnGpu(info) {
  if (/swiftshader|llvmpipe|software/i.test(info.gpu ?? '')) {
    log(`Cảnh báo: đang render bằng CPU (${info.gpu}). Sẽ chậm; thử --headful để dùng GPU.`);
  }
}

function requireFfmpeg() {
  const r = spawnSync('ffmpeg', ['-version'], { stdio: 'ignore' });
  if (r.error || r.status !== 0) fail('Không tìm thấy ffmpeg', 'macOS: brew install ffmpeg');
}

const isModel = /\.(glb|gltf|fbx)$/i.test(target);

if (cmd === 'inspect') {
  const q = isModel
    ? `inspect=${encodeURIComponent(target)}${flags.anims ? `&anims=${encodeURIComponent(flags.anims)}` : ''}`
    : `ep=${encodeURIComponent(target)}&render=1&scale=0.25`;
  const { info, close } = await open(q);
  await close();
  emit(info);
  process.exit(0);
}

const scale = Number(flags.scale ?? 1);
const { page, info, close } = await open(`ep=${encodeURIComponent(target)}&render=1&scale=${scale}`);
warnGpu(info);
for (const w of info.warnings ?? []) log(`Cảnh báo: ${w}`);

if (cmd === 'still') {
  const times = String(flags.at ?? '0').split(',').map(seconds);
  const outs = [];
  for (const t of times) {
    const out = flags.out && times.length === 1 ? String(flags.out) : `renders/${target}-${t.toFixed(2)}s.png`;
    mkdirSync(dirname(out), { recursive: true });
    const b64 = await page.evaluate((x) => window.__video.still(x), t);
    writeFileSync(out, Buffer.from(b64, 'base64'));
    outs.push(out);
  }
  let sheet = null;
  if (outs.length > 1 && spawnSync('ffmpeg', ['-version'], { stdio: 'ignore' }).status === 0) {
    sheet = `renders/${target}-sheet.png`;
    const inputs = outs.flatMap((o) => ['-i', o]);
    const scaled = outs.map((_, i) => `[${i}:v]scale=-2:640[v${i}]`).join(';');
    const stack = outs.map((_, i) => `[v${i}]`).join('') + `hstack=inputs=${outs.length}`;
    const r = spawnSync('ffmpeg', ['-y', '-loglevel', 'error', ...inputs, '-filter_complex', `${scaled};${stack}`, sheet]);
    if (r.status !== 0) sheet = null;
  }
  await close();
  emit({ stills: outs, sheet, width: info.width, height: info.height, gpu: info.gpu });
  process.exit(0);
}

// render
requireFfmpeg();
const fps = info.fps;
const from = seconds(flags.from) ?? 0;
const to = Math.min(seconds(flags.to) ?? info.duration, info.duration);
const first = Math.round(from * fps);
const last = Math.max(first + 1, Math.round(to * fps));
const total = last - first;
const alpha = !!flags.alpha;
if (alpha && !info.transparent) log('Cảnh báo: --alpha nhưng tập không đặt background: "transparent"; nền vẫn đặc.');
const mime = alpha || !flags.jpeg ? 'image/png' : 'image/jpeg';
const suffix = flags.from || flags.to ? `-${from.toFixed(1)}-${to.toFixed(1)}` : '';
const out = String(flags.out ?? `renders/${target}${suffix}${alpha ? '.mov' : '.mp4'}`);
mkdirSync(dirname(out), { recursive: true });

const audioFile = info.audio && !/^https?:/.test(info.audio) ? join('public', info.audio) : null;
const ff = [
  '-y', '-hide_banner', '-loglevel', 'error',
  '-f', 'image2pipe', '-framerate', String(fps), '-c:v', mime === 'image/png' ? 'png' : 'mjpeg', '-i', '-',
];
if (audioFile && !flags['no-audio']) ff.push('-ss', String(first / fps), '-t', String(total / fps), '-i', audioFile);
if (alpha) ff.push('-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le');
else ff.push('-c:v', 'libx264', '-preset', 'medium', '-crf', String(flags.crf ?? 18), '-pix_fmt', 'yuv420p', '-movflags', '+faststart');
if (audioFile && !flags['no-audio']) ff.push('-c:a', alpha ? 'pcm_s16le' : 'aac', ...(alpha ? [] : ['-b:a', '192k']));
ff.push('-r', String(fps), out);

const enc = spawn('ffmpeg', ff, { stdio: ['pipe', 'inherit', 'inherit'] });
let encError = null;
enc.on('error', (e) => (encError = e));
const done = once(enc, 'close');

log(`Render ${target}: ${info.width}×${info.height} @ ${fps} fps, khung ${first}–${last - 1} (${total} khung) → ${out}`);
log(`GPU: ${info.gpu}`);
const started = Date.now();
for (let i = first; i < last; i++) {
  const b64 = await page.evaluate((n, m) => window.__video.frame(n, m, 0.95), i, mime);
  if (encError || enc.exitCode !== null) break;
  if (!enc.stdin.write(Buffer.from(b64, 'base64'))) await once(enc.stdin, 'drain');
  const n = i - first + 1;
  if (n % 30 === 0 || n === total) {
    const el = (Date.now() - started) / 1000;
    const rate = n / el;
    log(`  ${n}/${total} khung · ${rate.toFixed(1)} khung/giây · còn ~${Math.ceil((total - n) / rate)} giây`);
  }
}
enc.stdin.end();
const [code] = await done;
await close();
if (encError || code !== 0) fail(`ffmpeg lỗi (mã ${code ?? encError?.message})`, 'Xem dòng lỗi ffmpeg ở trên.');
emit({
  out,
  frames: total,
  seconds: Number((total / fps).toFixed(3)),
  size: `${info.width}x${info.height}`,
  fps,
  audio: audioFile && !flags['no-audio'] ? audioFile : null,
  elapsed: Number(((Date.now() - started) / 1000).toFixed(1)),
  gpu: info.gpu,
});
