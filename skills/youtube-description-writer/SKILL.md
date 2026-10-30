---
name: youtube-description-writer
description: Viết và kiểm tra mô tả video YouTube theo hướng dẫn SEO chính thức của YouTube, cho creator thương hiệu cá nhân và kênh nhân vật đại diện. Chọn 1–2 từ khoá chính từ gợi ý tìm kiếm YouTube (script) và số liệu kênh, viết câu mở trọn ý trong phần hiện trước "Hiện thêm", tóm tắt, chương (mốc lấy từ kịch bản hoặc phụ đề bản dựng cuối, kiểm đúng luật 00:00, ≥ 3 mốc, ≥ 10 giây), link, công bố tài trợ theo Luật Quảng cáo 2025, ghi công, khối kênh, 3–5 hashtag và gợi ý thẻ, rồi chạy script kiểm tra (5.000 ký tự, danh sách từ khoá, câu lặp, ký tự < >, hashtag, chương). Cũng góp ý mô tả có sẵn hoặc video đã đăng. Dùng khi người dùng nói "viết mô tả video", "mô tả YouTube chuẩn SEO", "description cho video này", "làm chương / timestamp cho video", "hashtag và tags cho video", "mô tả này ổn chưa", "tối ưu SEO video đã đăng", "write a YouTube description", "video chapters". Không dùng để đặt tiêu đề hay chữ thumbnail (dùng `story-hook-writer`), thiết kế thumbnail (dùng `thumbnail-designer`), viết kịch bản (dùng `story-content-writer`), hay chú thích TikTok, Reels, Facebook.
---

# YouTube description writer

Skill này viết phần chữ đi kèm video YouTube: mô tả, chương, hashtag và gợi ý thẻ, ở dạng dán thẳng vào YouTube Studio, kèm bản kiểm tra theo quy định chính thức.

Ba nguyên tắc chạy xuyên suốt:

- **Mô tả giúp hiểu và giúp chọn, không phải đòn bẩy chính.** YouTube xếp hạng tìm kiếm theo mức liên quan (tiêu đề, thẻ, mô tả, nội dung video khớp truy vấn), tương tác và chất lượng. Mô tả tốt giúp YouTube và Google hiểu video, và giúp người xem đang lướt tìm kiếm quyết định bấm. Nó không cứu được tiêu đề, thumbnail hay 30 giây đầu yếu. Đừng hứa với người dùng là mô tả sẽ tăng lượt xem bao nhiêu.
- **Viết cho người đọc trước, máy đọc sau.** Từ khoá đặt đúng chỗ (tiêu đề, câu mở, tên chương) và đọc tự nhiên. Danh sách từ khoá, thẻ dán vào mô tả, câu lặp lại là vi phạm chính sách spam của YouTube, không phải mẹo SEO.
- **Không hứa điều video không có.** Mô tả là siêu dữ liệu; chính sách lừa đảo của YouTube áp cho mô tả như cho tiêu đề và thumbnail. Mọi con số, tên, kết quả phải lấy từ video hoặc người dùng xác nhận. Thiếu thì để `[cần bổ sung: …]`.

## Script hỗ trợ

`scripts/desc_tools.py` (thư viện chuẩn Python; lệnh `fetch` cần `yt-dlp`, nếu máy không có thì chạy qua `uvx yt-dlp`, không có cả hai thì hỏi người dùng trước khi cài). `HELPER` là đường dẫn tuyệt đối tới script, nằm trong thư mục chứa file SKILL.md này. Chạy từ thư mục gốc dự án người dùng:

```bash
HELPER="<thư-mục-skill>/scripts/desc_tools.py"
python3 "$HELPER" suggest --q "làm freelancer" --no-accent        # gợi ý tìm kiếm YouTube (VN)
python3 "$HELPER" suggest --q "làm freelancer" --alphabet         # mở rộng ~30 lượt gọi, chỉ cho 1–2 từ
python3 "$HELPER" transcript video-final.srt --every 30           # phụ đề rút gọn theo khối 30 giây để làm chương
python3 "$HELPER" fetch "<link video>" --subs descriptions/subs   # mô tả, chương, thẻ của video đã đăng (+ phụ đề .vtt)
python3 "$HELPER" check descriptions/<slug>.md --title "<tiêu đề>" --keyword "<từ chính>" --duration 12:30
```

`check` đọc khối mã đầu tiên trong file `.md` (hoặc cả file nếu là `.txt`) và in JSON gồm số ký tự, phần hiện trước "Hiện thêm" (~100 và ~157 ký tự), từ khoá ở đâu, chương, hashtag, link, và danh sách `issues` mức `error` / `warn` / `info`. Đặt URL trong ngoặc kép khi chạy trên zsh. `suggest` dùng endpoint gợi ý không công bố của Google, có thể đổi hoặc bị chặn; thứ tự gợi ý không phải số lượt tìm.

## Đọc reference nào, khi nào

- `references/principles.md`: luôn đọc trước bước 3. Mô tả nặng tới đâu trong SEO, hướng dẫn chính thức (mô tả, chương, hashtag, thẻ, link), ranh giới trung thực, các lời khuyên phổ biến nhưng không có cơ sở, và checklist dùng ở bước 5.
- `references/keywords.md`: đọc ở bước 2. Nguồn từ khoá, cách chọn 1–2 từ chính, chuyện dấu tiếng Việt và từ mượn.
- `references/structure.md`: đọc ở bước 3. Tám khối theo thứ tự, cách viết câu mở và tên chương, mẫu theo loại video (kể chuyện, hướng dẫn, review, kênh nhân vật, Shorts), ví dụ hoàn chỉnh.
- `references/disclosure.md`: đọc khi video có tài trợ, quà tặng, link tiếp thị liên kết, hoặc dùng nhạc, tư liệu của người khác.

## Hồ sơ kênh (nếu có)

Trước bước 1, kiểm tra file `channel-profile.md` ở thư mục gốc dự án. File này do skill `channel-profile` tạo. Nếu có, đọc và dùng:

- **Định vị** (mục 1) và **niche** (mục 2): câu giới thiệu kênh trong khối kênh.
- **Khán giả** (mục 3): họ gọi vấn đề bằng từ gì, để chọn từ khoá.
- **Người dẫn / nhân vật** (mục 4) và **giọng văn** (mục 7): câu mở và tóm tắt phải đúng xưng hô, đúng giọng; kênh nhân vật thì nói bằng giọng nhân vật nhưng vẫn nêu chủ đề bằng từ người ta gõ.
- **Định dạng, nhịp đăng** (mục 6): lịch đăng cho khối kênh.
- **Quy tắc nội dung** (mục 8): điều không được hứa, nguồn hỗ trợ phải kèm với chủ đề nhạy cảm.

Nếu có `descriptions/channel-block.md` (khối kênh dùng chung đã lưu từ lần trước), dùng lại, đừng hỏi lại link. Những gì hồ sơ đã trả lời thì đừng hỏi lại. Không có file thì làm như bình thường.

## Quy trình

### 1. Nắm video

Cần biết:

- **Tiêu đề** đã chốt (hoặc tạm). Chưa có thì gợi ý `story-hook-writer`, vì từ khoá chính phải nằm ở cả tiêu đề và mô tả.
- **Nội dung thật**: kịch bản, phụ đề `.srt`/`.vtt` của bản dựng cuối, hoặc người dùng tóm tắt. Có phụ đề thì chạy `transcript` để đọc nhanh.
- **Độ dài** video và **loại**: dài hay Shorts; kể chuyện, hướng dẫn, review, kênh nhân vật.
- **Link** muốn đặt (tài nguyên nhắc trong video, playlist, video liên quan) và **tài trợ / tiếp thị liên kết / nhạc, tư liệu cần ghi công**.

Nếu người dùng đưa link video đã đăng, chạy `fetch` (kèm `--subs` để lấy phụ đề tự động làm chương), rồi coi mô tả hiện có là bản nháp cần góp ý: nhảy tới bước 5, sau đó viết lại nếu họ muốn.

Tự rút những gì suy ra được từ kịch bản hay phụ đề, tóm 2–3 dòng để người dùng kiểm tra. Thiếu gì thì hỏi gộp một lần. Không hỏi những thứ không đổi kết quả; ghi giả định một dòng rồi làm tiếp.

### 2. Chọn từ khoá

Theo `references/keywords.md`:

1. Viết lời hứa của video trong một câu.
2. Lập 3–5 hạt giống, chạy `suggest` cho 1–2 cái quan trọng nhất. Hỏi người dùng có muốn dán số liệu từ Analytics (từ khoá tìm kiếm dẫn tới video, tab Research) không; không có cũng làm tiếp.
3. Chọn **1–2 từ khoá chính** (người ta gõ thật, video trả lời được, đủ cụ thể với cỡ kênh) và **3–6 từ liên quan**. Đưa bảng ngắn: từ, vai trò, nguồn, đặt ở đâu.
4. Nếu từ khoá chính không có trong tiêu đề, nói ra và gợi ý một bản tiêu đề có từ đó (giữ ý của tiêu đề cũ), để người dùng tự quyết.

### 3. Viết

Theo `references/structure.md`, chọn khối nào video cần trong 8 khối: câu mở, tóm tắt, chương, tài nguyên, xem tiếp, công bố và ghi công, khối kênh, hashtag.

- **Câu mở**: nói video cho người xem điều gì, có từ khoá chính, ý chính trọn trong ~100 ký tự, không chép tiêu đề, không chào hỏi, không link hay hashtag ở dòng đầu. Có tài trợ thì câu công bố nằm ở dòng 1 hoặc 2.
- **Tóm tắt**: cụ thể (con số, nơi chốn, công cụ có trong video), từ liên quan xuất hiện ở chỗ tự nhiên. Video kể chuyện giữ kết, nhưng không giấu chủ đề.
- **Chương**: mốc lấy từ bản dựng cuối (phụ đề hoặc người dùng xác nhận), không lấy mốc dự kiến trong kịch bản. Nếu chỉ có kịch bản, ghi mốc dạng `[cần bổ sung: MM:SS]` và nhắc người dùng điền sau khi dựng. Tên chương nói nội dung.
- **Khối kênh**: lần đầu thì viết rồi đề nghị lưu `descriptions/channel-block.md`; các lần sau dùng lại.
- **Hashtag**: 3–5 cái, cụ thể; xếp 3 cái muốn hiện trên tiêu đề lên đầu.
- **Thẻ** (cho ô Tags, không dán vào mô tả): 5–10 cái gồm từ khoá chính, dạng không dấu, cách viết sai hay gặp, tên series hoặc nhân vật.

Shorts: 1–2 câu có từ khoá + 2–3 hashtag; link trong mô tả Shorts không bấm được, nên gợi ý dùng "Video liên quan" để dẫn về video dài.

### 4. Ghi file và chạy kiểm tra

Ghi `descriptions/<slug-video>.md` (mẫu ở mục "Lưu kết quả"), rồi chạy `check` với `--title`, `--keyword` cho từng từ chính, `--duration`, và `--shorts` nếu là Shorts. Sửa hết mục `error`; mục `warn` thì sửa hoặc giải thích vì sao giữ. Chạy lại tới khi sạch.

### 5. Soát theo checklist

Chạy checklist trong `references/principles.md`, phần script không bắt được: câu mở có thật sự bổ sung tiêu đề không, có hứa thêm điều video không làm không, con số nào chưa được xác nhận, tên chương có đáng bấm không, công bố tài trợ có đúng quan hệ thật không. Góp ý mô tả có sẵn thì dùng cùng checklist, mỗi mục ✅ hoặc ⚠️ kèm câu sửa cụ thể.

Đánh dấu toàn bản: 🟢 dán được · 🟡 còn ô `[cần bổ sung]` hoặc điều cần người dùng xác nhận · 🔴 hứa điều video không có, nhồi từ khoá, thiếu công bố tài trợ. Không bàn giao bản 🔴.

### 6. Bàn giao

- Bản mô tả trong một khối mã để dán thẳng (giữ xuống dòng), thẻ cho ô Tags trên một dòng cách nhau bằng dấu phẩy.
- Việc cần làm trong Studio, chỉ những gì liên quan: tick Paid promotion nếu có tài trợ; không cần tắt chương tự động vì chương trong mô tả đã ghi đè; thêm "Video liên quan" cho Shorts; thêm bản dịch tiêu đề và mô tả ở mục Languages nếu kênh có khán giả nước ngoài.
- Gợi ý một dòng nếu có ích: sau 1–2 tuần, xem Analytics → Traffic source: YouTube search để biết người ta thật sự tìm thấy video bằng từ gì, rồi chỉnh mô tả và tiêu đề cho video sau.

## Lưu kết quả

Hỏi trước khi ghi file lần đầu trong dự án. Mặc định ghi `descriptions/<slug-video>.md`:

````
# <tiêu đề video>

Từ khoá chính: … · Từ liên quan: … · Độ dài: MM:SS · Mức: 🟢/🟡

## Mô tả (dán vào YouTube Studio)

```text
<mô tả hoàn chỉnh>
```

## Thẻ

<thẻ 1>, <thẻ 2>, …

## Ghi chú

<ô cần bổ sung, việc cần làm trong Studio, kết quả check>
````

Khối kênh dùng chung lưu ở `descriptions/channel-block.md`. Phụ đề tải về bằng `fetch --subs` để ở `descriptions/subs/`.

## Định dạng trả lời

Mở đầu 2–3 dòng: video, lời hứa, từ khoá chính, giả định. Tiếp theo là bảng từ khoá (bước 2), rồi bản mô tả trong khối mã, dòng thẻ, kết quả kiểm tra (số ký tự, phần hiện trước "Hiện thêm", các mục đã sửa), và cuối cùng là các ô `[cần bổ sung]` cùng việc cần làm trong Studio. Góp ý mô tả có sẵn thì thay bản mô tả bằng checklist ✅/⚠️ và bản viết lại nếu được yêu cầu.

## Những chỗ dễ sai

- **Dòng đầu phí phạm.** "Xin chào các bạn, hôm nay…", link, hashtag hay chép nguyên tiêu đề ở dòng đầu làm mất phần duy nhất người xem đọc trong kết quả tìm kiếm.
- **Nhồi từ khoá.** Lặp từ chính trong mọi câu, dán danh sách từ khoá hay thẻ cuối mô tả. Vi phạm chính sách, và người đọc thấy ngay.
- **Mốc chương lấy từ kịch bản.** Bản dựng gần như luôn lệch kịch bản; chương sai mốc tệ hơn không có chương.
- **Mô tả hứa nhiều hơn video.** "Hướng dẫn chi tiết từ A tới Z" cho một video kể chuyện. Mô tả hứa ít hơn tiêu đề thì được, nhiều hơn thì không.
- **Bịa chi tiết cho đầy.** Con số, tên công cụ, link mà người dùng chưa đưa. Để `[cần bổ sung: …]`.
- **Chép một mô tả cho mọi video.** Chỉ khối kênh được giống nhau; phần còn lại mỗi video một bản riêng.
- **Quên công bố tài trợ hoặc chôn nó dưới "Hiện thêm".** Theo Luật Quảng cáo sửa đổi 2025 (hiệu lực 01/01/2026), quảng cáo trên mạng xã hội phải nhận diện được rõ ràng.
- **Hứa kết quả SEO.** "Mô tả này sẽ đưa video lên top" là không có cơ sở. Nói những gì mô tả làm được: giúp YouTube hiểu chủ đề và giúp người tìm kiếm quyết định bấm.
