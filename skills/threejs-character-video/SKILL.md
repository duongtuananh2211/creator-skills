---
name: threejs-character-video
description: Khởi tạo (scaffold) một dự án Three.js + Vite + TypeScript để dựng video từ nhân vật 3D, rồi giúp dựng tập đầu tiên. Dự án sinh ra có sẵn engine dựng cảnh theo timeline (nhân vật GLB/FBX, ghép animation Mixamo tự khớp xương, chuyển động, biểu cảm bằng blendshape, nhép miệng theo âm lượng giọng đọc, chớp mắt, camera theo keyframe, mốc thời gian bám theo từng câu trong file .srt), trang xem trước có tua, camera tự do và copy vị trí camera, và lệnh render từng khung hình bằng Chrome chạy ngầm ghép ffmpeg ra MP4 1080×1920 hoặc 1920×1080 kèm giọng đọc (hoặc .mov nền trong suốt). Dùng khi người dùng nói "init dự án threejs làm video", "scaffold project 3D để dựng video nhân vật", "dựng video từ nhân vật 3D", "làm video hoạt hình 3D bằng code", "render nhân vật 3D ra mp4", "cho nhân vật 3D nói theo giọng đọc", "threejs video từ model glb/mixamo", hoặc muốn thêm tập, cảnh, nhân vật vào một dự án đã scaffold bằng skill này. Không dùng để làm game hay web 3D tương tác, dựng model 3D từ đầu, chỉnh sửa video đã quay (dùng CapCut, hoặc `long-video-to-shorts` để cắt clip), hay tạo ảnh tĩnh (dùng `google-flow-image-generation`).
---

# Three.js character video

Skill này dựng sẵn một dự án để biến nhân vật 3D thành video: người dùng có model nhân vật và file giọng đọc, viết mỗi tập thành một file TypeScript ngắn (nhân vật làm gì, mặt thế nào, camera ở đâu, tại câu thoại nào), xem trước trên trình duyệt, rồi render ra MP4 để đưa vào CapCut. Dựng bằng code thay vì phần mềm dựng phim vì một khi đã có nhân vật, mỗi tập mới chỉ là một file vài chục dòng, đổi giọng đọc thì cảnh tự khớp lại, và render lúc nào cũng ra đúng một kết quả.

Hai nguyên tắc chạy xuyên suốt:

- **Render phải lặp lại được.** Mọi thứ trong khung hình là hàm của thời gian `t`: animation đặt thời gian trực tiếp, nhép miệng tính trước từ file audio, chớp mắt dùng số giả ngẫu nhiên cố định. Code thêm vào `update(ctx, t)` cũng phải vậy (không `Math.random()`, `Date.now()`, biến cộng dồn qua các khung). Nhờ đó khung chụp kiểm tra giống hệt khung trong video, và render lại một đoạn không lệch.
- **Không dùng model hay animation không rõ quyền.** Model mẫu là robot CC0 của three.js. Model của người dùng thì hỏi nguồn khi chưa rõ, và ghi nguồn vào `public/models/CREDITS.md`. Xem `references/characters.md` mục 5.

## Script hỗ trợ

`scripts/scaffold.py` (thư viện chuẩn Python). `HELPER` là đường dẫn tuyệt đối tới script, nằm trong thư mục chứa file SKILL.md này:

```bash
HELPER="<thư-mục-skill>/scripts/scaffold.py"
python3 "$HELPER" check                                     # node, npm, ffmpeg, Chrome, giọng tiếng Việt của macOS
python3 "$HELPER" init video-3d --format 9:16 --fps 30      # chép template + tải robot mẫu + tạo giọng đọc demo
python3 "$HELPER" init video-3d --no-demo                   # không tải model mẫu, không tạo tập demo
python3 "$HELPER" init . --into-existing                    # thêm vào thư mục đã có file, không ghi đè file nào
python3 "$HELPER" demo-voice video-3d --lines "Câu một.|Câu hai."   # tạo lại giọng demo + .srt
```

Script không bao giờ ghi đè file đã có; thư mục đích có file mà không có `--into-existing` thì dừng và báo lỗi. Lỗi in ra JSON có `error` và `hint`.

Trong dự án đã scaffold, các lệnh chạy bằng npm từ thư mục dự án (chi tiết trong `README.md` của dự án):

```bash
npm run dev                                       # xem trước: http://localhost:5173/?ep=<tập>
npm run still -- <tập> --at 1,4,8 --scale 0.5     # chụp khung → renders/<tập>-<t>s.png + renders/<tập>-sheet.png
npm run render -- <tập> [--from 5 --to 9] [--scale 0.5] [--alpha] [--jpeg] [--crf 18]
npm run inspect -- <tập>                          # thông tin mọi nhân vật trong tập
npm run inspect -- models/x.glb [--anims wave=anims/Waving.fbx]   # clip, morph, xương của một model
npm run typecheck
```

`still`, `render` và `inspect` tự bật Vite và Chrome chạy ngầm, in JSON kết quả ra stdout và tiến độ, cảnh báo, lỗi console của trang ra stderr.

## Đọc reference nào, khi nào

- `references/episode-api.md`: luôn đọc trước khi viết hoặc sửa một tập. Mọi tuỳ chọn của tập, mốc thời gian, cách viết camera cho khung dọc và ngang, các mẫu hay dùng (cử chỉ một lần rồi về idle, hai nhân vật dùng chung một giọng, nhân vật đi lại).
- `references/characters.md`: khi người dùng chưa có nhân vật, có model chưa chạy được, có file Mixamo, VRoid, model tạo bằng AI, hay nhân vật không phải người (ví dụ con rắn); và khi làm nhép miệng, biểu cảm.
- `references/rendering.md`: khi render chậm, lỗi, ra khung đen, thiếu tiếng, và khi bàn giao sang CapCut (phụ đề, nền trong suốt, nhạc).

## Hồ sơ kênh (nếu có)

Trước bước 1, kiểm tra file `channel-profile.md` ở thư mục gốc dự án (do skill `channel-profile` tạo). Nếu có, lấy từ đó: **định dạng** (mục 6: video ngắn dọc hay YouTube ngang → `--format`), **nhân vật đại diện** (mục 4: tên, ngoại hình, tính cách → đặt tên nhân vật trong tập, chọn cử chỉ, gợi ý nguồn model), **giọng đọc AI** (mục 7 hoặc 4: công cụ nào, để biết file audio sẽ đến từ đâu). Những gì hồ sơ đã trả lời thì đừng hỏi lại.

## Quy trình

### 1. Gom đầu vào

Cần biết:

1. **Thư mục dự án.** Mặc định `video-3d/` trong thư mục đang mở. Nếu thư mục đang mở trống và người dùng muốn dựng ngay tại đó thì dùng `.`.
2. **Định dạng**: `9:16` (Shorts, TikTok, Reels; mặc định) hoặc `16:9` (YouTube dài); `1:1`, `4:5` cũng có. **FPS**: mặc định 30.
3. **Nhân vật**: đã có file model chưa (`.glb`, `.gltf`, `.fbx`), có animation chưa, model có blendshape miệng không. Chưa có thì vẫn scaffold với robot mẫu, rồi xem `references/characters.md` mục 1 để chọn hướng.
4. **Giọng đọc** (không bắt buộc ở bước này): file audio và phụ đề `.srt` của tập đầu. Nếu đã cài `story-voice-script`, lời đọc từ đó đưa vào ElevenLabs hoặc Vbee để có file audio.

Tự suy ra những gì đã rõ rồi nêu giả định trong một dòng ("Mình scaffold vào `video-3d/`, khung dọc 9:16, 30 fps, kèm robot mẫu"). Chỉ hỏi khi thật sự không đoán được, ví dụ thư mục đang mở là một dự án code khác.

### 2. Kiểm tra công cụ

Chạy `check`. Cần Node.js 20.19+ hoặc 22.12+, ffmpeg, và Chrome/Chromium/Edge. Thiếu thứ gì thì báo lệnh cài trong `hints` và hỏi người dùng trước khi cài (đừng tự `brew install`). Không có giọng tiếng Việt của macOS (`say_vietnamese_voice: false`, hoặc không phải macOS) thì demo vẫn chạy, chỉ là audio im lặng.

### 3. Scaffold và cài đặt

```bash
python3 "$HELPER" init video-3d --format 9:16 --fps 30
cd video-3d && npm install
```

`init` tải robot mẫu (~460 KB, CC0) từ kho three.js trên GitHub và tạo `public/audio/demo.wav` + `demo.srt` bằng `say -v Linh`. Mạng lỗi thì JSON có `warnings`; tập demo sẽ báo thiếu model cho tới khi tải lại.

### 4. Kiểm tra bản chạy được

```bash
npm run typecheck
npm run still -- demo --at 1,7.5,13 --scale 0.5
```

Xem `renders/demo-sheet.png` bằng Read. Phải thấy robot đứng trên nền gradient có bóng, khung thứ hai cận hơn và robot hơi ngạc nhiên (lông mày nhướng), khung thứ ba góc nghiêng. Trường `gpu` trong JSON có `SwiftShader` nghĩa là đang render bằng CPU: vẫn đúng nhưng chậm, xem `references/rendering.md` mục 2. Sau đó `npm run render -- demo` (18 giây video mất khoảng 10 giây trên Mac M2 Pro; máy yếu hơn hoặc render bằng CPU sẽ lâu hơn nhiều) và báo đường dẫn MP4.

Nếu người dùng chỉ cần khung dự án thì dừng ở đây: báo thư mục, các lệnh chính, cách mở preview (`npm run dev`, mở `http://localhost:5173/?ep=demo`; chạy bằng Bash với `run_in_background: true` nếu người dùng muốn agent mở giúp), và bước tiếp theo là đưa nhân vật của họ vào.

### 5. Đưa nhân vật của người dùng vào

1. Chép model vào `public/models/`, animation rời vào `public/anims/`. Ghi nguồn và giấy phép vào `public/models/CREDITS.md`.
2. `npm run inspect -- models/<file> --anims <tên>=anims/<file>,...`. Đọc `clips`, `morphs`, `bones`, `height`, `warnings`:
   - `matched` thấp hoặc cảnh báo "không khớp xương": rig khác nhau, xem `references/characters.md` mục 3.
   - Chiều cao lạ (0,02 hay 180): đặt `height` trong tập.
   - Tìm morph miệng (`jawOpen`, `mouthOpen`, `viseme_aa`, `Fcl_MTH_A`…) và morph chớp mắt; không có thì nhép miệng bằng xương (`bone: 'Jaw'` hoặc gật đầu nhẹ bằng `'Head'`).
3. Có model mới thì tạo tập thử `src/episodes/<tên>-test.ts` chỉ có nhân vật đứng idle, một camera, rồi `still` để kiểm tra kích thước, hướng mặt, vật liệu trước khi dựng cả tập.

### 6. Dựng một tập từ kịch bản và giọng đọc

Đọc `references/episode-api.md`. Đầu vào tốt nhất là file audio + `.srt` khớp nhau (cùng bản xuất, không cắt ghép sau đó), cộng kịch bản nếu có (bảng kịch bản của `story-content-writer` có cột hình ảnh, dùng làm gợi ý hành động và góc máy).

1. Chép audio và `.srt` vào `public/audio/`. Không có `.srt`: xem `references/episode-api.md` mục 2 về cách lấy, hoặc dùng mốc giây.
2. Đọc `.srt`, lập bảng nháp trong chat: mỗi câu (`cue:N`) → hành động, biểu cảm, camera. Giữ nhịp: một cử chỉ lớn mỗi 2–4 câu, đổi góc máy khi đổi ý, không cử động liên tục mỗi câu.
3. Viết `src/episodes/<slug>.ts` theo bảng. Chỉ dùng tên clip, morph, xương có trong kết quả `inspect`; engine báo lỗi kèm danh sách tên đúng nếu sai.
4. `npm run typecheck`, rồi `still` ở 4–6 thời điểm quan trọng (đầu mỗi cảnh, giữa cử chỉ lớn). Xem ảnh: nhân vật trong khung, không bị cắt đầu ở khung dọc, chỗ trống cho phụ đề (khung dọc: khoảng 1/4 dưới; xem `references/rendering.md` mục 4), bóng đổ hợp lý.
5. Mời người dùng mở preview để xem với tiếng (agent không nghe được nhép miệng có khớp không). Họ chỉnh góc máy bằng F rồi K, dán dòng camera vào chat hoặc vào file.
6. Render nháp `--scale 0.5` nếu tập dài, chốt xong thì render bản cuối.

### 7. Giao

Báo trong chat: đường dẫn MP4 (hoặc `.mov`), độ dài, độ phân giải, những gì còn làm trong CapCut (phụ đề từ chính file `.srt`, chữ móc, nhạc nền, logo). Cảnh báo nào trong JSON render (thiếu audio, render bằng CPU, morph thiếu) thì nêu lại.

## Khi người dùng sửa hoặc phản hồi

- **"Nhân vật làm cử chỉ trễ / sớm"**: dịch mốc bằng `"cue:N+0.3"` / `"cue:N-0.2"` thay vì đổi sang số giây, để còn khớp khi đổi giọng.
- **"Chuyển động giật"**: tăng `fade` của action (0,4–0,6), thêm `dur` cho camera, đổi `ease` sang `'inOut'`.
- **"Miệng nhép quá ít / quá nhiều"**: chỉnh `gain` (1,5–2 cho giọng nhỏ) hoặc `amount` của xương; trọng số trong `morph: { jawOpen: 0.7 }`.
- **"Đổi giọng đọc"**: thay audio + `.srt`, chạy lại `still` ở vài mốc để chắc các câu vẫn đúng số thứ tự.
- **"Thêm nhân vật thứ hai"**: thêm vào `characters`, mỗi người có `lipsync.ranges` theo các câu của mình (xem `references/episode-api.md` mục 6).
- **"Làm khung ngang từ tập dọc"**: chép tập thành file mới, đổi `format`, nới camera ra xa và rộng hơn; đừng chỉ đổi `format` rồi render.

## Những chỗ dễ sai

- **Đoán tên clip hay morph.** Mỗi model đặt tên một kiểu (`Idle`, `idle`, `mixamo.com`, `Armature|Idle`). Luôn chạy `inspect` trước.
- **Gộp `loop: false` mà không có action sau.** Cử chỉ một lần sẽ đứng hình ở khung cuối; luôn có action tiếp theo (thường là idle) sau khoảng bằng độ dài clip.
- **Animation từ rig khác.** Mixamo khớp với Mixamo; rig VRoid, rig tự làm, model AI tự rig thường có tên xương khác. Engine chỉ đổi tên và tỉ lệ, không retarget giữa các bộ xương khác tư thế gốc.
- **Code không thuần trong `update`.** Một `Math.random()` làm khung `still` khác khung trong video và làm render lại một đoạn bị nhảy.
- **Render cả tập để kiểm tra một chi tiết.** Dùng `still` hoặc `--from/--to --scale 0.5`.
- **Ghi đè file của người dùng.** `init` không ghi đè; khi sửa tập đã có, sửa đúng chỗ, đừng viết lại cả file nếu người dùng đã chỉnh tay.
