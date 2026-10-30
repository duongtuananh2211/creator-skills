---
name: long-video-to-shorts
description: Cắt một video YouTube dài đã xuất (file MP4 16:9) thành nhiều clip dọc 9:16 cho YouTube Shorts, TikTok, Instagram/Facebook Reels. Skill lấy transcript có thời gian (whisper.cpp chạy trên máy, hoặc file phụ đề .srt có sẵn), chọn các khoảnh khắc đứng một mình được và chấm điểm, sửa đầu đuôi clip (vào muộn hơn, kéo câu mạnh lên đầu, chữ trên màn hình) mà không thêm nội dung không có trong video, rồi dùng ffmpeg cắt ra MP4 1080×1920 (nền mờ hoặc cắt khung, chuẩn hoá âm lượng) kèm file phụ đề .srt riêng từng clip, cùng tiêu đề, chú thích, hashtag và cách gắn về video dài cho từng nền tảng. Dùng khi người dùng nói "cắt video này thành shorts", "chia video dài thành TikTok", "làm reels từ video YouTube", "tìm đoạn hay để làm short", "repurpose video dài", "clip video thành nhiều video ngắn", "turn this video into shorts". Không dùng để viết kịch bản video ngắn mới từ ý tưởng (dùng `story-content-writer`), chỉ nghĩ hook hay tiêu đề (dùng `story-hook-writer`), cắt video của người khác, hay dựng hiệu ứng phức tạp thay CapCut.
---

# Long video to shorts

Skill này nhận một video dài người dùng đã làm xong và trả về một bộ clip dọc đăng được, kèm chữ để đăng. Người dùng làm kênh ảnh minh hoạ hoặc nhân vật đại diện với giọng đọc AI, dựng trong CapCut. Việc của skill là phần tốn thời gian nhất khi tái sử dụng: nghe lại cả video, tìm đoạn đứng một mình được, cắt đúng chỗ ngắt câu, chuyển sang khung dọc. Phần trau chuốt cuối (kiểu phụ đề, chữ móc, nhạc) vẫn để người dùng làm trong CapCut.

Hai nguyên tắc chạy xuyên suốt:

- **Clip chỉ chứa thứ video dài đã nói.** Được: chọn đoạn, bỏ câu dẫn, đổi thứ tự hai đoạn trong cùng một ý, thêm chữ trên màn hình tóm đúng điều clip trả. Không được: chữ móc hay tiêu đề hứa điều clip không có, ghép hai câu ở hai chỗ khác nhau thành một ý video gốc không nói, thu thêm câu dẫn có thông tin mới. Clip cắt khỏi ngữ cảnh mà đổi nghĩa thì vừa mất lòng tin vừa có thể sai sự thật.
- **Ít clip tốt hơn nhiều clip nhạt.** Một video dài thường chỉ có 3–8 khoảnh khắc đứng một mình được. Một kênh Shorts toàn những clip na ná nhau dễ bị YouTube xếp vào nội dung lặp lại.

## Script hỗ trợ

`scripts/clipper.py` (thư viện chuẩn Python, gọi `ffmpeg`/`ffprobe`, và `whisper-cli` của whisper.cpp khi cần chép lời). `HELPER` là đường dẫn tuyệt đối tới script, nằm trong thư mục chứa file SKILL.md này. Chạy từ thư mục gốc dự án người dùng; mọi đường dẫn tương đối, kể cả trong `plan.json`, tính từ đó:

```bash
HELPER="<thư-mục-skill>/scripts/clipper.py"
python3 "$HELPER" probe video.mp4                            # thời lượng, khung hình, công cụ có sẵn
python3 "$HELPER" transcribe video.mp4 --prompt "Xa, cờ bạc, dopamine"   # whisper.cpp, tiếng Việt
python3 "$HELPER" transcribe video.mp4 --srt video.srt       # dùng phụ đề có sẵn, không cần whisper
python3 "$HELPER" cutpoints video.mp4                        # khoảng lặng + lần đổi cảnh
python3 "$HELPER" render shorts/video/plan.json              # cắt mọi clip
python3 "$HELPER" render shorts/video/plan.json --only 03    # cắt lại một clip
```

Kết quả ghi vào `shorts/<tên video>/`: `transcript.json`, `transcript.txt` (mỗi dòng `#số [mm:ss.s–mm:ss.s] câu`), `cutpoints.json`, rồi các clip `01-<slug>.mp4` + `01-<slug>.srt`. Lỗi in ra JSON có `error` và `hint`. Chép lời một video 20 phút mất vài phút; cắt mỗi clip 60 giây mất khoảng 5–15 giây.

## Đọc reference nào, khi nào

- `references/selection.md`: luôn đọc trước bước 4. Loại khoảnh khắc nên chọn và nên bỏ, thang chấm, cách sửa đầu và đuôi clip, cách đặt điểm cắt.
- `references/platforms.md`: đọc ở bước 5 (chọn chế độ khung dọc) và bước 7 (chữ đăng bài, gắn về video dài), và khi người dùng hỏi thông số, độ dài, phụ đề, lịch đăng.
- Nếu đã cài `story-content-writer`, phần hook và nhịp video ngắn trong `story-content-writer/references/short-video.md` dùng được cho chữ móc và tiêu đề.

## Hồ sơ kênh (nếu có)

Trước bước 1, kiểm tra file `channel-profile.md` ở thư mục gốc dự án (thư mục mở Claude Code). File này do skill `channel-profile` tạo và là nguồn đúng nhất về kênh. Nếu có, đọc nó và dùng như sau:

- **Khán giả** (mục 3) và **trụ cột nội dung** (mục 5): ưu tiên khoảnh khắc chạm đúng câu hỏi của khán giả; ghi trụ cột cho từng clip.
- **Người dẫn / nhân vật đại diện** (mục 4): tên nhân vật và thuật ngữ riêng đưa vào `--prompt` khi chép lời để whisper viết đúng chính tả. Chữ móc và tiêu đề giữ đúng tính cách nhân vật.
- **Định dạng và nhịp đăng** (mục 6): kênh có làm Shorts không, độ dài, series, tần suất, để đề xuất số clip và lịch đăng.
- **Giọng văn** (mục 7): xưng hô, từ hay dùng, từ cấm trong tiêu đề và chú thích.
- **Quy tắc nội dung** (mục 8): chủ đề nhạy cảm và cách kênh xử lý; áp cho cả việc chọn đoạn (một câu nhạy cảm tách khỏi ngữ cảnh có thể nghe khác hẳn).

Những gì hồ sơ đã trả lời thì đừng hỏi lại. Nếu không có file, làm như bình thường; có thể nhắc một lần rằng `channel-profile` (nếu đã cài) giúp các lần sau không phải khai lại.

## Quy trình

### 1. Gom đầu vào

Cần:

1. **File video dài** (MP4 hoặc MOV đã xuất). Người dùng chưa nói đường dẫn thì tìm file video trong dự án và hỏi xác nhận.
2. **Kịch bản gốc** của video, nếu có trong dự án (file `.md` từ `story-content-writer` hoặc `story-voice-script`). Không bắt buộc, nhưng dùng để sửa chính tả transcript và hiểu ý của từng chương.
3. **Số clip và độ dài**: mặc định chọn 3–8 clip tuỳ độ dài video, mỗi clip 30–60 giây.
4. **Nền tảng**: mặc định cả YouTube Shorts, TikTok, Reels, vì cùng một file đăng được cả ba.
5. **Khung dọc**: mặc định `blur` (giữ cả khung ngang trên nền mờ). Xem `references/platforms.md` mục 2.

Tự suy ra những gì đã rõ rồi nêu giả định trong một dòng ("Mình chọn 4–6 clip 30–60 giây cho cả ba nền tảng, khung nền mờ"). Chỉ hỏi khi không tìm thấy video.

### 2. Kiểm tra công cụ

Chạy `probe`. Cần `ffmpeg`. Để chép lời cần `whisper_bin` và `whisper_model` khác `null`. Nếu thiếu, hỏi người dùng một lần bằng AskUserQuestion, đừng tự cài:

- **Cài whisper.cpp** (chạy trên máy, không gửi video đi đâu): `brew install whisper-cpp`, rồi tải model vào `~/.cache/whisper.cpp/`. Khuyên `ggml-large-v3-turbo.bin` (~1,6 GB, chép tiếng Việt tốt) hoặc `ggml-large-v3-turbo-q5_0.bin` (~550 MB, nhẹ hơn, kém hơn chút):
  ```bash
  mkdir -p ~/.cache/whisper.cpp && curl -L -o ~/.cache/whisper.cpp/ggml-large-v3-turbo.bin \
    https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
  ```
- **Dùng phụ đề có sẵn**: file `.srt` xuất từ CapCut, từ công cụ giọng AI, hoặc phụ đề tự động tải về từ YouTube Studio sau khi video đã lên YouTube. Nhập bằng `transcribe --srt`.

`can_burn_subs: false` là bình thường với ffmpeg của Homebrew: clip vẫn có file `.srt` để nhập vào CapCut.

### 3. Chép lời và tìm điểm cắt

Chạy `transcribe` (thêm `--prompt` với tên nhân vật, thuật ngữ của kênh) rồi `cutpoints`. Có kịch bản gốc thì đối chiếu: sửa chữ sai trong trường `text` của `transcript.json` theo kịch bản (tên riêng, thuật ngữ, dấu), **không sửa `start`/`end`**, rồi viết lại `transcript.txt` cho khớp. Phụ đề của clip lấy từ file này, nên sửa ở đây là sửa cho mọi clip.

### 4. Chọn khoảnh khắc

Đọc `references/selection.md`, rồi đọc toàn bộ `transcript.txt`. Video dài quá 40 phút thì đọc theo từng phần, ghi ứng viên sau mỗi phần.

1. Đánh dấu chương và ý chính của video, để biết mỗi đoạn thuộc mạch nào.
2. Gom 8–15 ứng viên theo các loại khoảnh khắc trong reference. Mỗi ứng viên ghi số câu đầu và cuối (`#12–#19`).
3. Soát tham chiếu ngược và sửa đầu, đuôi theo thứ tự trong reference (vào muộn hơn → kéo câu lên đầu → chữ trên màn hình → câu dẫn thu thêm). Sửa không được thì bỏ.
4. Chấm 4 tiêu chí, giữ các ứng viên đạt, trải đều trên các chương và các loại khoảnh khắc.
5. Đặt điểm vào và ra theo `cutpoints.json` (reference mục 5).

### 5. Trình bày kế hoạch và hỏi trước khi cắt

Trình bày trong chat, xếp theo điểm từ cao xuống:

```
**Video:** <tên file> · <thời lượng> · transcript từ <whisper / file srt>
**Giả định:** <số clip, độ dài, nền tảng, khung dọc>

| # | Đoạn gốc | Dài | Loại | Điểm | Câu mở (lời) | Chữ móc trên màn hình | Khung |
|---|---|---|---|---|---|---|---|
| 01 | 03:12–04:05 | 53s | Câu hỏi + lời giải | 11/12 | "Vì sao thua rồi vẫn muốn chơi?" | Thua mà vẫn muốn chơi tiếp? | blur |
| 02 | 11:40–11:58 + 09:02–09:31 | 47s | Sự thật bất ngờ · mở bằng câu kéo lên | 10/12 | … | … | crop x=0.4 |

Đã bỏ: <ứng viên bị loại và lý do một dòng, ví dụ "07:30 — mở bằng 'như đã nói', vào muộn hơn thì mất bối cảnh">
```

Sau bảng, hỏi người dùng muốn cắt những clip nào (mặc định tất cả), có muốn đổi khung, độ dài hay điểm vào của clip nào không. Cắt tốn thời gian và đĩa, nên đợi họ chốt.

### 6. Cắt

Ghi `shorts/<tên video>/plan.json` rồi chạy `render`:

```json
{
  "source": "exports/vi-sao-nghien-co-bac.mp4",
  "transcript": "shorts/vi-sao-nghien-co-bac/transcript.json",
  "out_dir": "shorts/vi-sao-nghien-co-bac",
  "defaults": {"reframe": {"mode": "blur", "x": 0.5, "zoom": 1.0}, "burn_subs": false},
  "clips": [
    {"id": "01", "slug": "thua-van-muon-choi",
     "segments": [{"start": 192.4, "end": 245.1}]},
    {"id": "02", "slug": "may-chinh-suyt-thang",
     "segments": [{"start": "11:40.2", "end": "11:58.0"}, {"start": "09:02.5", "end": "09:31.0"}],
     "reframe": {"mode": "crop", "x": 0.4}}
  ]
}
```

- `segments` phát theo thứ tự ghi; nhiều đoạn là để kéo câu mạnh lên đầu. Thời gian ghi bằng giây hoặc `mm:ss.s`. Script tự đệm 0,05 giây trước và 0,25 giây sau mỗi đoạn (`pad_in`, `pad_out` để đổi).
- `reframe`, `burn_subs`, `loudnorm` đặt ở `defaults` hoặc ghi đè trong từng clip.
- `burn_subs: true` chỉ có tác dụng khi `probe` báo `can_burn_subs: true`.

Clip nào lỗi thì kết quả có `error` và lệnh thoát mã 1; sửa plan rồi chạy lại `--only <id>`.

### 7. Kiểm tra và giao

Kiểm tra từng clip trước khi báo xong:

1. **Khung hình**: `render` ghi `01-<slug>.preview.png` (khung đầu, giữa, cuối đặt cạnh nhau). Xem từng ảnh bằng Read. Tìm chủ thể bị cắt mất ở chế độ `crop`, chữ của ảnh gốc bị xén, khung đầu còn sót ảnh trước. Ảnh xem trước chỉ để kiểm tra; nói người dùng có thể xoá trước khi đăng.
2. **Đầu và cuối**: đọc 2 dòng đầu và 2 dòng cuối của `.srt`; câu đầu phải là câu móc đã chốt, câu cuối không bị cụt.
3. **Độ dài** trong kết quả `render` khớp kế hoạch.

Sửa và cắt lại những gì sai, rồi ghi `shorts/<tên video>/plan.md` cho người dùng mở khi đăng. Mỗi clip một mục:

```markdown
## 01 · thua-van-muon-choi.mp4 (53s)
Đoạn gốc: 03:12–04:05 · Loại: câu hỏi + lời giải · Trụ cột: <trụ cột>
Chữ móc (0–3s, thêm trong CapCut): Thua mà vẫn muốn chơi tiếp?
Phụ đề: 01-thua-van-muon-choi.srt (nhập vào CapCut) | đã in vào video

YouTube Shorts
- Tiêu đề: <≤ 100 ký tự, ý chính trong ~50 ký tự đầu>
- Video liên quan: <tên video dài> (đặt trong YouTube Studio)
TikTok
- Chú thích: <1–2 câu không chép lại lời> · Bản đầy đủ trên YouTube: <tên kênh>
- Hashtag: <3–5 cái, sát chủ đề>
Reels
- Chú thích: <như TikTok, chỉnh theo giọng Instagram nếu cần> · Hashtag: <3–5>

Ghi chú dựng: <ví dụ "ảnh ở 0:21 có chữ sát mép phải, đã dùng blur">
```

Tiêu đề, chữ móc và chú thích qua 4 câu hỏi: **đúng sự thật**, **clip trả được lời hứa**, **không xin tương tác** ("comment 'có' để nhận…", "tag bạn bè"), **cảm xúc tương xứng với nội dung**. Không qua thì viết lại. Nếu đã cài `story-hook-writer`, gợi ý dùng nó khi người dùng muốn nhiều phương án tiêu đề hơn cho clip mạnh nhất.

Cuối cùng báo trong chat: thư mục kết quả, danh sách clip kèm độ dài, những gì còn phải làm trong CapCut (phụ đề, chữ móc), và gợi ý lịch đăng (`references/platforms.md` mục 7).

## Khi người dùng sửa hoặc phản hồi

- **"Clip 3 vào chậm / bị cụt chữ đầu / kết lửng"**: chỉnh `start`/`end` theo `transcript.json` và `cutpoints.json`, chạy lại `--only 03`. Cụt chữ đầu thì lùi `start` khoảng 0,3 giây.
- **"Nhân vật bị cắt mất"**: đổi `x` của `crop`, hoặc chuyển sang `blur` với `zoom` 1,2–1,4.
- **"Tìm thêm clip"**: quay lại danh sách ứng viên đã bỏ hoặc các chương chưa có clip, đừng hạ chuẩn chấm.
- **"Dài quá"**: bỏ câu ví dụ thứ hai, câu nhắc lại, câu chuyển; giữ câu móc và câu trả thưởng. Không cắt giữa câu.
- **"Thêm câu mở mới cho cuốn hơn"**: chỉ làm theo cách 4 trong `references/selection.md` mục 3, và nói rõ câu mới phải thu bằng giọng AI rồi ghép trong CapCut.

## Những chỗ dễ sai

- **Chọn đoạn hay với người đã xem cả video.** Đọc câu đầu như một người lạ vừa lướt tới: họ có hiểu đang nói gì không?
- **Chữ móc hứa hơn clip.** Clip giải thích một cơ chế thì chữ móc nói về cơ chế đó, không phải "điều không ai nói cho bạn".
- **Ghép câu làm đổi nghĩa.** Kéo câu lên đầu chỉ dùng trong cùng một ý; không ghép câu hỏi ở chương này với câu trả lời ở chương khác.
- **Tin transcript tuyệt đối.** Whisper sai tên riêng, số và từ tiếng Anh; timestamp lệch vài trăm mili giây. Đối chiếu kịch bản và xem ảnh kiểm tra.
- **Xoá hay ghi đè file của người dùng.** Script chỉ ghi vào `shorts/<tên video>/`; clip trùng tên bị ghi đè khi cắt lại, đó là chủ đích. Không động vào video gốc.
