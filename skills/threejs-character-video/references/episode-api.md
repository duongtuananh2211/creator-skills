# Viết một tập

Mỗi tập là `src/episodes/<slug>.ts`, export mặc định `defineEpisode({...})`. Tên file là tên tập trong mọi lệnh (`npm run render -- <slug>`) và trong URL preview (`?ep=<slug>`). Kiểu đầy đủ có chú thích nằm trong `src/engine/types.ts` của dự án; file này giải thích cách dùng.

Quy ước không gian: đơn vị mét, mặt đất `y = 0`, trục `+Z` hướng về phía camera mặc định. `rotY: 0` = nhân vật nhìn về `+Z`; `rotY: 90` = nhìn sang `+X` (bên phải màn hình khi camera ở `z` dương); góc tính bằng độ.

## 1. Khung một tập

| Trường | Ý nghĩa | Mặc định |
|---|---|---|
| `format` | `'9:16'` 1080×1920 · `'16:9'` 1920×1080 · `'1:1'` 1080×1080 · `'4:5'` 1080×1350 | bắt buộc |
| `size` | Ghi đè kích thước pixel `[w, h]` | theo `format` |
| `fps` | Khung/giây | 30 |
| `audio` | Đường dẫn dưới `public/`; được ghép vào video khi render | không |
| `subtitles` | `.srt`/`.vtt` của audio; bật mốc `"cue:N"`, hiện câu đang nói trong preview | không |
| `duration` | `'audio'` hoặc một mốc thời gian | độ dài audio, không có audio thì 10 s kèm cảnh báo |
| `background` | `'#1d2433'` · `{ gradient: ['#trên', '#dưới'] }` · ảnh `'images/nen.png'` (phủ kín, cắt bớt chứ không kéo méo) · `'transparent'` | gradient xanh xám |
| `ground` | `false` (không có sàn) · `{ shadowOpacity: 0.3 }` sàn vô hình chỉ nhận bóng · `{ color: '#2a2a2a' }` sàn đặc | sàn vô hình nhận bóng |
| `lights` | `{ key, keyPos, rim, env, shadows, exposure }` | key 2,2 ở `[2.5, 5, 4]`, rim 1,2, env 0,6 |
| `cameraSway` | Camera rung nhẹ như cầm tay, mét (0,005–0,02) | 0 |
| `characters` | `{ tên: CharacterSpec }` | bắt buộc |
| `props` | `[{ model, position, rotY, height, scale }]` đạo cụ tĩnh | không |
| `camera` | Danh sách keyframe camera | một khung trung cảnh |
| `setup(ctx)` | Chạy một lần sau khi tải; thêm vật thể tuỳ ý | không |
| `update(ctx, t)` | Chạy mỗi khung trước khi vẽ | không |

Ảnh nền từ `google-flow-image-generation` dùng thẳng được: chép vào `public/images/`, đặt `background: 'images/<file>.png'`, giữ sàn vô hình để nhân vật có bóng đổ lên ảnh. Tạo ảnh nền đúng tỉ lệ khung (9:16 hoặc 16:9) và để trống chỗ nhân vật đứng. Ảnh nền là ảnh phẳng: camera di chuyển thì nền không có thị sai, nên với nền ảnh hãy giữ camera gần như đứng yên (chỉ zoom nhẹ bằng `fov` hoặc đẩy vào chút ít).

## 2. Mốc thời gian

Mọi trường `at` (và `ranges`, `duration`) nhận:

- `3.5` (giây), `"1:02.5"` (phút:giây), `"0:01:02.5"`.
- `"cue:4"`: lúc câu 4 trong file phụ đề bắt đầu; `"cue:4:end"`: lúc câu 4 kết thúc.
- Dịch thêm: `"cue:4+0.3"`, `"cue:4:end-0.2"`, `"12+0.5"`.

Số câu là số thứ tự ghi trong file `.srt` (thường 1, 2, 3…). Engine báo lỗi kèm khoảng cue hợp lệ nếu gọi cue không có.

Ưu tiên `cue` hơn số giây: khi thu lại giọng hoặc đổi tốc độ đọc, chỉ cần thay audio và `.srt`. Dùng số giây cho đoạn không có lời (mở đầu, kết).

**Lấy file .srt khớp với audio:**

- Công cụ giọng đọc xuất được phụ đề thì dùng luôn bản đó.
- whisper.cpp chạy trên máy (cùng công cụ skill `long-video-to-shorts` dùng): `ffmpeg -i voice.mp3 -ar 16000 -ac 1 /tmp/voice16.wav && whisper-cli -m ~/.cache/whisper.cpp/ggml-large-v3-turbo.bin -l vi -osrt -of public/audio/voice -f /tmp/voice16.wav`. Whisper chia câu theo nhịp nghỉ, không theo dòng kịch bản, nên mở `.srt` ra đọc trước khi gán `cue:N`; sửa chính tả trong file nếu muốn preview hiện đúng chữ (không sửa mốc thời gian).
- CapCut: tạo phụ đề tự động trên đúng file audio rồi xuất ra `.srt`, nếu bản CapCut đang dùng có mục xuất phụ đề.
- Kịch bản ngắn mà không có công cụ nào: nghe preview, dùng mốc giây. Chạy `npm run dev`, tua tới đầu câu, đọc số giây ở thanh điều khiển.

Audio và `.srt` phải cùng một bản: nếu cắt bớt khoảng lặng đầu audio sau khi tạo phụ đề, mọi cue lệch theo.

## 3. Nhân vật

```ts
characters: {
  xa: {
    model: 'models/xa.glb',            // .glb / .gltf / .fbx dưới public/
    animations: { wave: 'anims/Waving.fbx', walk: 'anims/Walking.fbx#mixamo.com' },
    height: 1.6,                       // thu phóng để cao đúng 1,6 m (model FBX cm tự thu về 1,7 m nếu không đặt)
    scale: 1,                          // nhân thêm sau height
    position: [0, 0, 0],
    rotY: 0,
    inPlace: false,                    // true: bỏ dịch chuyển ngang của hông trong clip (đi tại chỗ)
    actions: [...],
    moves: [...],
    face: [...],
    lipsync: {...},
    blink: {...},
  },
}
```

`animations`: khoá là tên dùng trong `actions`, giá trị là file (lấy clip đầu tiên) hoặc `file#TênClip`. Lấy được clip từ một file GLB khác: `'models/khac.glb#Walk'`. Tên xương kiểu Mixamo (`mixamorig:Hips`, `mixamorigHips`, `mixamorig1:Hips`) tự khớp với nhau; tỉ lệ dịch chuyển của hông tự quy đổi khi model và animation khác đơn vị.

### actions: animation theo thời gian

```ts
actions: [
  { at: 0, clip: 'Idle' },                                 // action đầu tiên giữ từ t = 0
  { at: 'cue:2', clip: 'Wave', loop: false, fade: 0.25 },  // vẫy một lần
  { at: 'cue:2+1.8', clip: 'Idle', fade: 0.4 },            // về idle sau ~độ dài clip Wave
  { at: 'cue:5', clip: 'Talking', speed: 0.9, offset: 1.2 },
]
```

- Mỗi action hoà dần vào action trước trong `fade` giây (mặc định 0,3). Action sau luôn đè action trước; không cần "tắt" action cũ.
- `loop` mặc định `true`. Cử chỉ một lần đặt `loop: false` và **luôn** có action tiếp theo sau khoảng bằng độ dài clip (xem `duration` trong `inspect`), nếu không nhân vật đứng hình ở khung cuối.
- `speed` đổi tốc độ, `offset` bắt đầu giữa clip (hai nhân vật cùng idle thì đặt `offset` khác nhau cho khỏi giống hệt nhau).
- Không khai `actions` mà model có clip tên chứa "idle" thì tự lặp clip đó.
- Cùng một clip dùng lại bao nhiêu lần cũng được, mỗi lần có thời gian riêng.

### moves: đi lại, xoay người

```ts
moves: [
  { at: 4, rotY: 90, dur: 0.5 },                                  // quay sang phải trong 0,5 s trước giây 4
  { at: 8, pos: [2.5, 0, 0], dur: 4, ease: 'linear' },            // đi tới x = 2,5 trong 4 s, tốc độ đều
]
```

Vị trí xuất phát là `position`/`rotY` ở thời điểm 0. **Không có `dur` thì chuyển động kéo dài từ key trước** (ở đây key đầu sẽ xoay từ giây 0 tới giây 4), nên gần như luôn đặt `dur`. Key chỉ có `pos` hoặc chỉ có `rotY` thì giữ nguyên giá trị kia.

Đi bộ: dùng clip đi tại chỗ (Mixamo có ô "In Place"; hoặc đặt `inPlace: true`), chạy action `walk` cùng lúc với một `moves` có `ease: 'linear'`, rồi về `idle` khi tới nơi. Tốc độ bước khoảng 1,2–1,4 m/s cho clip đi thường; chân trượt thì chỉnh `speed` của clip hoặc `dur`.

### face: biểu cảm bằng blendshape

```ts
face: [
  { at: 'cue:3', morph: 'Surprised', value: 0.8 },        // lên 0,8 trong 0,25 s
  { at: 'cue:3:end', morph: 'Surprised', value: 0, fade: 0.5 },
]
```

Mỗi key đưa morph từ giá trị hiện tại tới `value` trong `fade` giây (mặc định 0,25). Nhớ có key trả về 0. Tên morph lấy từ `inspect`; sai tên thì engine báo kèm danh sách đúng.

### lipsync: nhép miệng theo giọng

```ts
lipsync: { morph: 'jawOpen' }                                   // một morph
lipsync: { morph: { jawOpen: 0.7, mouthFunnel: 0.25 }, gain: 1.5 }
lipsync: { bone: 'Jaw', axis: 'x', amount: 0.3 }               // xoay xương hàm (radian)
lipsync: { bone: 'Head', axis: 'x', amount: 0.1 }              // không có miệng: gật nhẹ theo giọng
lipsync: { morph: 'jawOpen', audio: 'audio/nv2.wav' }          // bám theo file audio khác
lipsync: { morph: 'jawOpen', ranges: [['cue:1', 'cue:1:end'], ['cue:4', 'cue:5:end']] }
```

Miệng mở theo độ to của giọng (tính trước từ file audio), không theo từng âm vị. Với nhân vật hoạt hình, cách này đủ thuyết phục; cận mặt nhân vật giống người thật thì sẽ lộ. `gain` cho giọng nhỏ (1,5–2), `amount` cho xương. Trục và dấu của xương hàm tuỳ rig: thử `amount: -0.3` hoặc trục khác nếu miệng mở ngược.

### blink: chớp mắt

```ts
blink: { morph: ['eyeBlinkLeft', 'eyeBlinkRight'], every: 3.6 }
```

Chớp ngẫu nhiên quanh mỗi `every` giây, cố định giữa các lần render.

## 4. Camera

```ts
camera: [
  { at: 0, pos: [0, 1.2, 5.2], target: [0, 0.95, 0], fov: 35 },        // toàn cảnh
  { at: 'cue:2', pos: [0.6, 1.25, 3.2], target: [0, 1.05, 0], dur: 1.2 }, // đẩy vào trong 1,2 s, kết thúc đúng cue 2
  { at: 'cue:3', pos: [-1.8, 1.0, 2.8], target: [0, 1.0, 0], ease: 'cut' }, // cắt cảnh đúng cue 3
  { at: 'cue:3:end', pos: [-0.8, 1.4, 5.5], target: [0, 0.9, 0], dur: 1.5 },
]
```

- Mỗi key là camera ở đâu (`pos`), nhìn vào đâu (`target`), góc nhìn dọc (`fov`, độ; bỏ trống thì giữ như key trước).
- Chuyển từ key trước sang key này: `ease` (`'inOut'` mặc định, `'linear'`, `'in'`, `'out'`, `'cut'` = giữ nguyên rồi nhảy đúng lúc `at`). `dur` = chuyển động kéo dài bao lâu, **kết thúc** ở `at`; không có `dur` thì kéo dài suốt từ key trước (camera trôi liên tục).
- Muốn đứng yên rồi mới di chuyển: dùng `dur`, hoặc lặp lại key cũ ở thời điểm bắt đầu di chuyển.
- Tìm góc máy: `npm run dev`, tua tới chỗ cần, bấm **F** để kéo camera tự do, **K** để copy dòng key, dán vào tập rồi sửa `at`.

**Cỡ cảnh cho nhân vật cao ~1,6 m, `fov` 35** (đã chụp thử; là điểm xuất phát, chỉnh bằng mắt). Muốn cận hơn nữa thì giảm `z` của `pos` (khoảng 1,0 cho cận mặt) hoặc giảm `fov`:

| Cỡ cảnh | Khung dọc 9:16: `pos` / `target` | Khung ngang 16:9: `pos` / `target` |
|---|---|---|
| Toàn thân | `[0, 1.2, 5.2]` / `[0, 0.95, 0]` | `[0, 1.1, 4.2]` / `[0, 0.85, 0]` |
| Trung cảnh rộng (từ gối) | `[0, 1.3, 3.0]` / `[0, 1.1, 0]` | `[0, 1.3, 2.6]` / `[0, 1.1, 0]` |
| Cận trung (từ ngực) | `[0, 1.45, 1.6]` / `[0, 1.4, 0]` | `[0, 1.45, 1.5]` / `[0, 1.4, 0]` |

Khung dọc hẹp: nhân vật nên ở giữa, để trống khoảng 1/4 dưới cho phụ đề và 1/8 trên cho giao diện nền tảng. Khung ngang rộng: đặt nhân vật lệch 1/3 (`target` lệch ngược phía) để chừa chỗ cho chữ hoặc hình minh hoạ ghép trong CapCut.

Nhịp: đổi góc khi đổi ý hoặc sang câu quan trọng, mỗi góc giữ ít nhất 2–3 giây; đẩy vào chậm (`dur` 1–3 s) cho câu cảm xúc; cắt (`'cut'`) cho câu bất ngờ. Video ngắn: nên có thay đổi hình (cắt, đẩy, cử chỉ) trong 2 giây đầu.

## 5. Mẫu hay dùng

**Cử chỉ theo câu rồi về nghỉ**

```ts
actions: [
  { at: 0, clip: 'idle' },
  { at: 'cue:3+0.2', clip: 'shrug', loop: false },
  { at: 'cue:3+1.9', clip: 'idle', fade: 0.4 },
],
```

**Đứng nói chuyện lâu**: dùng clip "talking" lặp (Mixamo có nhiều), xen một cử chỉ mỗi vài câu; đừng để idle đứng im quá 6–8 giây khi đang nói.

**Nhân vật bước vào khung**

```ts
position: [-3, 0, 0], rotY: 90,
actions: [{ at: 0, clip: 'walk' }, { at: 2.6, clip: 'idle', fade: 0.4 }],
moves: [{ at: 2.6, pos: [0, 0, 0], dur: 2.6, ease: 'linear' }, { at: 3.2, rotY: 0, dur: 0.5 }],
inPlace: true,
```

**Đạo cụ, nền**

```ts
props: [{ model: 'models/ban.glb', position: [0.8, 0, -0.3], height: 0.75 }],
background: 'images/phong-khach.png',
```

## 6. Hai nhân vật dùng chung một file giọng

Mỗi nhân vật nhép miệng trong các câu của mình bằng `ranges`, và quay mặt về người đang nói nếu cần:

```ts
characters: {
  a: { model: 'models/a.glb', position: [-0.7, 0, 0], rotY: 20,
       lipsync: { morph: 'jawOpen', ranges: [['cue:1', 'cue:1:end'], ['cue:3', 'cue:3:end']] } },
  b: { model: 'models/b.glb', position: [0.7, 0, 0], rotY: -20,
       lipsync: { morph: 'jawOpen', ranges: [['cue:2', 'cue:2:end'], ['cue:4', 'cue:4:end']] } },
},
```

Nếu có file giọng riêng từng người, dùng `lipsync.audio` cho từng người và trộn các file thành một `audio` chung bằng ffmpeg (`amix`) để ghép vào video. Camera kiểu hội thoại: góc qua vai, cắt (`'cut'`) sang người đang nói ở đầu câu của họ.

## 7. Code tuỳ chỉnh: `setup` và `update`

```ts
setup({ THREE, scene }) {
  const sign = new THREE.Mesh(new THREE.BoxGeometry(1, 0.6, 0.05), new THREE.MeshStandardMaterial({ color: '#e94f37' }));
  sign.name = 'sign';
  sign.position.set(1.2, 1.5, -0.5);
  scene.add(sign);
},
update({ scene }, t) {
  const sign = scene.getObjectByName('sign')!;
  sign.rotation.y = Math.sin(t * 1.5) * 0.3;                       // hàm của t: được
  sign.visible = t > 4;                                            // được
  // sign.rotation.y += 0.01;   // KHÔNG: cộng dồn theo số lần gọi
  // Math.random(), Date.now(), performance.now()   // KHÔNG
},
```

`ctx` gồm `THREE`, `scene`, `camera`, `renderer`, `characters` (mỗi nhân vật có `.holder`, `.root`, `.bone(tên)`), `props`, `fps`, `duration`. `update` chạy sau khi nhân vật đã được tạo dáng và camera đã đặt, nên chỉnh xương ở đây là đè lên animation (ví dụ cho đầu nhìn theo một điểm). Xương mà animation không điều khiển sẽ giữ giá trị lần trước: đặt giá trị tuyệt đối (`bone.rotation.x = ...`), đừng cộng dồn.
