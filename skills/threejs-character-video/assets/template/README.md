# __PROJECT_NAME__

Dựng video từ nhân vật 3D bằng Three.js. Mỗi tập là một file TypeScript trong `src/episodes/`, mô tả nhân vật, hành động, biểu cảm và camera theo từng câu thoại. Xem trước trên trình duyệt, rồi render từng khung hình bằng Chrome chạy ngầm và ghép thành MP4 kèm giọng đọc bằng ffmpeg.

## Lệnh

```bash
npm install
npm run dev                                   # mở http://localhost:5173/?ep=demo
npm run still -- demo --at 1,4,8 --scale 0.5  # chụp vài khung để kiểm tra nhanh → renders/
npm run render -- demo                        # render cả tập → renders/demo.mp4
npm run render -- demo --from 5 --to 9 --scale 0.5   # nháp một đoạn, nửa độ phân giải
npm run render -- demo --alpha                # nền trong suốt (đặt background: 'transparent') → .mov ProRes 4444
npm run inspect -- models/nhan-vat.glb        # liệt kê clip, morph (blendshape), xương của model
npm run inspect -- models/nv.glb --anims wave=anims/Waving.fbx   # thử ghép animation Mixamo
npm run typecheck
```

Cần Node.js 20.19+ hoặc 22.12+, ffmpeg, và Chrome (hoặc Chromium/Edge; đặt `CHROME_PATH` nếu cài ở chỗ khác).

## Phím tắt trong trang xem trước

Space phát/dừng · ←/→ lùi/tiến một khung · Shift+←/→ một giây · **F** camera tự do (kéo xoay, cuộn zoom, chuột phải dời) · **K** copy vị trí camera hiện tại thành một dòng `{ at, pos, target, fov }` để dán vào tập · **I** xem clip và morph của nhân vật.

Sửa file tập, trang tự tải lại và đứng đúng thời điểm đang xem.

## Thư mục

```
public/models/    model nhân vật, đạo cụ (.glb, .gltf, .fbx)
public/anims/     animation rời (ví dụ tải từ Mixamo)
public/audio/     giọng đọc + phụ đề .srt
public/images/    ảnh nền
src/episodes/     mỗi file một tập
src/engine/       phần lõi (thường không cần sửa)
renders/          kết quả render (không đưa lên git)
```

## Viết một tập

```ts
import { defineEpisode } from '../engine/types';

export default defineEpisode({
  format: '9:16',              // '16:9' | '1:1' | '4:5'
  fps: 30,
  audio: 'audio/tap-01.mp3',   // độ dài video = độ dài audio
  subtitles: 'audio/tap-01.srt', // để dùng mốc "cue:N"
  background: 'images/nen.png',  // hoặc '#1d2433', { gradient: [...] }, 'transparent'

  characters: {
    xa: {
      model: 'models/xa.glb',
      height: 1.6,
      animations: { wave: 'anims/Waving.fbx' },
      actions: [
        { at: 0, clip: 'idle' },
        { at: 'cue:2', clip: 'wave', loop: false },
        { at: 'cue:2+1.8', clip: 'idle' },
      ],
      face: [{ at: 'cue:3', morph: 'mouthSmile', value: 1 }],
      lipsync: { morph: 'jawOpen' },
      blink: { morph: ['eyeBlinkLeft', 'eyeBlinkRight'] },
    },
  },

  camera: [
    { at: 0, pos: [0, 1.4, 4], target: [0, 1.2, 0], fov: 35 },
    { at: 'cue:2', pos: [0.5, 1.5, 2.2], target: [0, 1.4, 0], dur: 1 },  // đẩy vào trong 1 giây
    { at: 'cue:4', pos: [-2, 1.2, 2.5], target: [0, 1.2, 0], ease: 'cut' }, // cắt cảnh
  ],
});
```

Mốc thời gian: số giây (`3.5`), `"1:02.5"`, `"cue:4"` (đầu câu 4 trong file .srt), `"cue:4:end"` (cuối câu 4), cộng trừ thêm: `"cue:4+0.3"`. Đổi giọng đọc thì chỉ cần thay audio và .srt, các cảnh tự khớp lại.

Đơn vị là mét, mặt đất ở `y = 0`, nhân vật mặc định nhìn về `+Z` (về phía camera đặt ở `z` dương). Toàn bộ tuỳ chọn có chú thích trong `src/engine/types.ts`.

`update(ctx, t)` cho phép thêm hiệu ứng riêng bằng code Three.js. Hàm này chỉ được phụ thuộc vào `t` (không dùng `Date.now()`, `Math.random()` hay biến cộng dồn), để render và xem trước ra cùng một khung hình.
