import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import type { Runtime } from '../engine/episode';
import { assetUrl } from '../engine/assets';
import { formatClock } from '../engine/time';

/** Preview page: play/scrub against the voice track, free camera to find shots. */
export function mountPreview(rt: Runtime, app: HTMLElement, name: string) {
  app.innerHTML = `
    <div class="stage"><div class="frame"></div></div>
    <div class="cue" hidden></div>
    <div class="toast" hidden></div>
    <aside class="panel" hidden><pre></pre></aside>
    <div class="bar">
      <button class="play" title="Space">▶</button>
      <span class="tc"></span>
      <input class="scrub" type="range" min="0" step="0.001" />
      <span class="fr"></span>
      <button class="free" title="F">Camera tự do</button>
      <button class="copy" title="K">Copy camera</button>
      <button class="inf" title="I">Thông tin</button>
    </div>
    <div class="help">${name} · ${rt.width}×${rt.height} · ${rt.fps} fps · Space phát/dừng · ←/→ một khung · Shift+←/→ một giây · F camera tự do · K copy camera · I clip/morph</div>`;
  const $ = <T extends HTMLElement>(s: string) => app.querySelector(s) as T;
  const frameEl = $('.frame');
  const scrub = $<HTMLInputElement>('.scrub');
  const playBtn = $<HTMLButtonElement>('.play');
  const tc = $('.tc');
  const fr = $('.fr');
  const cueEl = $('.cue');
  const toast = $('.toast');
  const panel = $('.panel');
  frameEl.appendChild(rt.canvas);
  scrub.max = String(rt.duration);

  const fit = () => {
    const bar = 96;
    const s = Math.min((innerWidth - 32) / rt.width, (innerHeight - bar - 24) / rt.height, 1);
    rt.canvas.style.width = `${Math.floor(rt.width * s)}px`;
    rt.canvas.style.height = `${Math.floor(rt.height * s)}px`;
  };
  addEventListener('resize', fit);
  fit();

  const audio = rt.audio ? new Audio(assetUrl(rt.audio)) : null;
  let t = Math.min(Number(new URLSearchParams(location.hash.slice(1)).get('t') ?? 0) || 0, rt.duration);
  let playing = false;
  let wallStart = 0;

  const say = (msg: string) => {
    toast.textContent = msg;
    toast.hidden = false;
    clearTimeout((say as any).timer);
    (say as any).timer = setTimeout(() => (toast.hidden = true), 2200);
  };
  if (rt.warnings.length) {
    rt.warnings.forEach((w) => console.warn(w));
    say(rt.warnings[0]);
  }

  const seek = (to: number) => {
    t = Math.max(0, Math.min(rt.duration, to));
    if (playing) {
      wallStart = performance.now() - t * 1000;
      if (audio) audio.currentTime = t;
    }
  };
  const setPlaying = (on: boolean) => {
    if (on && t >= rt.duration - 1 / rt.fps) t = 0;
    playing = on;
    playBtn.textContent = on ? '❚❚' : '▶';
    if (on) {
      wallStart = performance.now() - t * 1000;
      if (audio) {
        audio.currentTime = t;
        audio.play().catch(() => say('Trình duyệt chặn tự phát âm thanh; bấm ▶ lần nữa.'));
      }
    } else audio?.pause();
  };

  const controls = new OrbitControls(rt.camera, rt.canvas);
  controls.enabled = false;
  const toggleFree = () => {
    rt.freeCamera = !rt.freeCamera;
    controls.enabled = rt.freeCamera;
    if (rt.freeCamera) {
      controls.target.copy(rt.cameraTarget);
      controls.update();
    }
    $('.free').classList.toggle('on', rt.freeCamera);
    say(rt.freeCamera ? 'Camera tự do: kéo để xoay, cuộn để zoom, chuột phải để dời. K để copy.' : 'Về camera theo timeline');
  };
  const r2 = (x: number) => Math.round(x * 100) / 100;
  const copyCam = () => {
    const c = rt.camera;
    const tg = rt.freeCamera ? controls.target : rt.cameraTarget;
    const key = `{ at: ${r2(t)}, pos: [${c.position.toArray().map(r2).join(', ')}], target: [${tg.toArray().map(r2).join(', ')}], fov: ${r2(c.fov)} },`;
    navigator.clipboard?.writeText(key).catch(() => {});
    console.log(key);
    say(`Đã copy: ${key}`);
  };
  const toggleInfo = () => {
    panel.hidden = !panel.hidden;
    panel.querySelector('pre')!.textContent = JSON.stringify(rt.info(), null, 2);
  };

  playBtn.onclick = () => setPlaying(!playing);
  $('.free').onclick = toggleFree;
  $('.copy').onclick = copyCam;
  $('.inf').onclick = toggleInfo;
  scrub.oninput = () => seek(Number(scrub.value));

  addEventListener('keydown', (e) => {
    if ((e.target as HTMLElement).tagName === 'INPUT' && e.key !== ' ') return;
    const step = e.shiftKey ? 1 : 1 / rt.fps;
    if (e.key === ' ') setPlaying(!playing);
    else if (e.key === 'ArrowRight') seek(t + step);
    else if (e.key === 'ArrowLeft') seek(t - step);
    else if (e.key === 'Home') seek(0);
    else if (e.key === 'f' || e.key === 'F') toggleFree();
    else if (e.key === 'k' || e.key === 'K') copyCam();
    else if (e.key === 'i' || e.key === 'I') toggleInfo();
    else return;
    e.preventDefault();
  });

  let lastHash = 0;
  const tick = (now: number) => {
    if (playing) {
      t = (now - wallStart) / 1000;
      if (t >= rt.duration) {
        t = rt.duration;
        setPlaying(false);
      }
    }
    if (rt.freeCamera) controls.update();
    rt.renderAt(t);
    scrub.value = String(t);
    tc.textContent = `${formatClock(t)} / ${formatClock(rt.duration)}`;
    fr.textContent = `khung ${Math.round(t * rt.fps)}`;
    const cue = rt.cues.find((c) => t >= c.start && t < c.end);
    cueEl.hidden = !cue;
    if (cue) cueEl.textContent = `#${cue.index}  ${cue.text}`;
    // Keep the position in the URL so a reload after editing the episode lands on the same frame.
    if (!playing && now - lastHash > 300) {
      lastHash = now;
      history.replaceState(null, '', `${location.search}#t=${t.toFixed(2)}`);
    }
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}
