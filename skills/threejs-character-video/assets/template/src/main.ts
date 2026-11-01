import type { EpisodeSpec } from './engine/types';
import { loadEpisode, type Runtime } from './engine/episode';
import { Character } from './engine/character';
import { mountPreview } from './ui/preview';

/**
 * Pages:
 *   /                         list of episodes
 *   /?ep=demo                 preview with transport controls
 *   /?ep=demo&render=1        headless render target used by scripts/video.mjs
 *   /?inspect=models/x.glb    clip, morph and bone names of one model (&anims=wave=anims/Wave.fbx,...)
 */
const episodes = import.meta.glob<{ default: EpisodeSpec }>('./episodes/*.ts');
const byName: Record<string, () => Promise<{ default: EpisodeSpec }>> = {};
for (const [path, load] of Object.entries(episodes)) byName[path.split('/').pop()!.replace(/\.ts$/, '')] = load;

interface VideoApi {
  ready: boolean;
  error: string | null;
  info?: unknown;
  frame?: (i: number, mime?: string, quality?: number) => string;
  still?: (t: number) => string;
}
declare global {
  interface Window {
    __video: VideoApi;
  }
}
window.__video = { ready: false, error: null };

const params = new URLSearchParams(location.search);
const app = document.getElementById('app')!;

async function main() {
  const inspect = params.get('inspect');
  if (inspect) return inspectModel(inspect, params.get('anims'));

  const ep = params.get('ep');
  if (!ep || !byName[ep]) return showIndex(ep);

  const spec = (await byName[ep]()).default;
  const render = params.has('render');
  const rt = await loadEpisode(spec, { scale: Number(params.get('scale') ?? 1), render });
  if (render) exposeRender(rt);
  else mountPreview(rt, app, ep);
}

function exposeRender(rt: Runtime) {
  document.body.className = 'render';
  app.appendChild(rt.canvas);
  const grab = (mime: string, q?: number) => rt.canvas.toDataURL(mime, q).split(',')[1];
  window.__video = {
    ready: true,
    error: null,
    info: {
      fps: rt.fps,
      frames: rt.frames,
      duration: rt.duration,
      width: rt.width,
      height: rt.height,
      audio: rt.audio,
      transparent: rt.spec.background === 'transparent',
      gpu: rt.gpu,
      ...rt.info(),
    },
    frame(i: number, mime = 'image/png', quality = 0.92) {
      rt.renderAt(i / rt.fps);
      return grab(mime, quality);
    },
    still(t: number) {
      rt.renderAt(t);
      return grab('image/png');
    },
  };
}

async function inspectModel(model: string, anims: string | null) {
  const animations: Record<string, string> = {};
  for (const pair of (anims ?? '').split(',').filter(Boolean)) {
    const [k, v] = pair.includes('=') ? pair.split('=') : [pair.split('/').pop()!.replace(/\.[^.]+$/, ''), pair];
    animations[k] = v;
  }
  const c = await Character.create('model', { model, animations }, { cues: [], envelope: async () => null });
  window.__video = { ready: true, error: null, info: c.info };
  app.innerHTML = `<pre class="inspect">${escapeHtml(JSON.stringify(c.info, null, 2))}</pre>`;
}

function showIndex(missing: string | null) {
  const names = Object.keys(byName).sort();
  app.innerHTML = `
    <main class="index">
      <h1>Các tập</h1>
      ${missing ? `<p class="err">Không có tập "${escapeHtml(missing)}" trong src/episodes/.</p>` : ''}
      <ul>${names.map((n) => `<li><a href="?ep=${encodeURIComponent(n)}">${escapeHtml(n)}</a></li>`).join('')}</ul>
      <p>Thêm tập mới: tạo file <code>src/episodes/&lt;tên&gt;.ts</code>.</p>
    </main>`;
  window.__video = { ready: true, error: null, info: { episodes: names } };
}

function escapeHtml(s: string) {
  return s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]!);
}

main().catch((e) => {
  const msg = e instanceof Error ? e.message : String(e);
  console.error(e);
  window.__video = { ready: false, error: msg };
  app.innerHTML = `<pre class="fatal">${escapeHtml(msg)}</pre>`;
});
