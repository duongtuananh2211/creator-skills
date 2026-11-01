import { defineEpisode } from '../engine/types';

// Tập mẫu: robot CC0 của three.js (Tomás Laulhé, chỉnh sửa bởi Don McCurdy), giọng đọc tạo khi scaffold.
// Mỗi mốc "cue:N" là đầu câu thứ N trong public/audio/demo.srt, nên đổi giọng đọc thì cảnh tự khớp lại.
export default defineEpisode({
  title: 'Demo',
  format: '__FORMAT__',
  fps: __FPS__,
  audio: 'audio/demo.wav',
  subtitles: 'audio/demo.srt',
  background: { gradient: ['#3a4a6b', '#141821'] },
  cameraSway: 0.01,

  characters: {
    robot: {
      model: 'models/RobotExpressive.glb',
      height: 1.6,
      position: [0, 0, 0],
      actions: [
        { at: 0, clip: 'Idle' },
        { at: 'cue:1', clip: 'Wave', loop: false, fade: 0.25 },
        { at: 'cue:1+2.2', clip: 'Idle', fade: 0.4 },
        { at: 'cue:2+0.3', clip: 'Yes', loop: false },
        { at: 'cue:2+2', clip: 'Idle', fade: 0.4 },
        { at: 'cue:3+0.2', clip: 'ThumbsUp', loop: false },
        { at: 'cue:3:end', clip: 'Idle', fade: 0.5 },
      ],
      face: [
        { at: 'cue:2', morph: 'Surprised', value: 0.8 },
        { at: 'cue:2:end', morph: 'Surprised', value: 0 },
      ],
      // Robot không có miệng: gật đầu theo âm lượng giọng đọc.
      lipsync: { bone: 'Head', axis: 'x', amount: 0.12 },
    },
  },

  camera: [
    { at: 0, pos: [0, 1.2, 5.2], target: [0, 0.95, 0], fov: 35 },
    { at: 'cue:2', pos: [0.6, 1.25, 3.2], target: [0, 1.05, 0], dur: 1.2 },
    { at: 'cue:3', pos: [-1.8, 1.0, 2.8], target: [0, 1.0, 0], ease: 'cut' },
    { at: 'cue:3:end', pos: [-0.8, 1.4, 5.5], target: [0, 0.9, 0], dur: 1.5 },
  ],
});
