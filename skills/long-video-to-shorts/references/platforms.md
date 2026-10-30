# Nền tảng, khung hình, phụ đề và đăng bài

Thông tin nghiên cứu ngày 30/10/2026. **[chính thức]** là điều nền tảng công bố (kể cả khi được trích lại qua báo), **[kinh nghiệm]** là kinh nghiệm người làm nghề. Nền tảng đổi thường xuyên; khi người dùng thấy giao diện khác, tin vào thứ họ đang thấy.

## 1. Thông số chung

Script xuất mọi clip theo một chuẩn đăng được cả ba nơi: 1080×1920 (9:16), H.264, 30 khung/giây, AAC 48 kHz, âm lượng chuẩn hoá về khoảng −14 LUFS. File sạch, không watermark, nên đăng thẳng lên từng nền tảng thay vì tải video TikTok về đăng lại.

| Nền tảng | Độ dài tối đa | Ghi chú |
| --- | --- | --- |
| YouTube Shorts | 3 phút, video dọc hoặc vuông [chính thức, từ 15/10/2024, qua [Social Media Today](https://www.socialmediatoday.com/news/youtube-expands-3-minute-shorts-to-all-users/736967/)] | Video ngang dưới 3 phút vẫn là video thường, không phải Short. Short dài hơn 1 phút có nhạc bản quyền có thể bị chặn theo Content ID. |
| Instagram Reels | 3 phút [chính thức, Mosseri, 1/2025, qua [Buffer](https://buffer.com/resources/instagram-reels-length)] | Reels dài tới 3 phút vẫn được đề xuất. Mosseri nói không có độ dài "hoàn hảo". |
| TikTok | Dài hơn nhiều, không phải giới hạn thực tế | Kiểm tra giới hạn tải lên trong app khi đăng. |
| Facebook Reels | Thay đổi theo đợt | Kiểm tra khi đăng; video dài hơn giới hạn có thể bị đăng thành video thường. |

## 2. Chuyển 16:9 sang 9:16 cho video ảnh minh hoạ

Kênh dùng ảnh minh hoạ hoặc nhân vật đại diện, không quay người, nên không cần bám mặt. Ba cách, khai trong `reframe` của từng clip:

| Chế độ | Trông như thế nào | Khi nào dùng |
| --- | --- | --- |
| `blur` (mặc định) | Cả khung ngang nằm giữa, trên nền là chính hình đó phóng to, làm mờ và tối đi | Ảnh có chữ, biểu đồ, hoặc nhiều chi tiết hai bên. An toàn nhất vì không mất gì. |
| `blur` + `zoom` 1,2–1,4 | Như trên nhưng hình giữa to hơn, xén bớt hai mép | Nhân vật nhỏ trong khung rộng, muốn chiếm nhiều màn hình hơn mà vẫn giữ phần lớn ảnh |
| `crop` + `x` | Cắt một cửa sổ dọc từ khung ngang, phủ kín màn hình | Chủ thể nằm gọn trong 1/3 khung. `x` = 0 lấy mép trái, 0,5 giữa, 1 mép phải. Mất khoảng 68% bề ngang của khung, nên kiểm tra ảnh xem có chữ hay chi tiết quan trọng ở hai bên không. |

Một clip đi qua nhiều ảnh có bố cục khác nhau thì `crop` một vị trí `x` có thể hợp ảnh này nhưng cắt mất chủ thể ảnh khác. Khi đó dùng `blur`. Tách thành nhiều `segments` không giúp được, vì `reframe` áp cho cả clip. Kiểm tra bằng ảnh xem trước (bước kiểm tra trong SKILL.md).

Nâng cấp tuỳ chọn cho clip đáng đầu tư nhất: tạo lại các ảnh của clip ở tỉ lệ 9:16 bằng `google-flow-image-generation` (nếu đã cài) rồi dựng lại trong CapCut với audio của clip. Tốn công hơn nhưng không có viền mờ.

## 3. Vùng an toàn và chữ trên màn hình

[kinh nghiệm] Giao diện TikTok, Reels, Shorts che khoảng 15–20% phía dưới (tên kênh, chú thích, nhạc) và một cột bên phải (nút thích, bình luận, chia sẻ), khoảng 10% phía trên (thanh tìm kiếm, tab). Đặt phụ đề và chữ móc trong khoảng giữa, phần dưới của nửa trên hoặc ngay trên 1/4 dưới cùng; tránh sát mép phải. TikTok khuyên giữ chữ trong vùng an toàn và không quá 5–10 từ mỗi giây [chính thức, [TikTok Ads Help](https://ads.tiktok.com/help/article/creative-best-practices?lang=en)].

Ở chế độ `blur`, khung ảnh gốc nằm giữa màn hình, nên phần nền mờ phía trên là chỗ tốt cho chữ móc và phần nền mờ phía dưới (trên vùng bị che) là chỗ tốt cho phụ đề.

## 4. Phụ đề

Nhiều người xem không bật tiếng, nên clip nào cũng nên có phụ đề [kinh nghiệm, dựa trên lời Mosseri được trích lại]. Script ghi một file `.srt` cạnh mỗi clip: câu đã được chia thành dòng ngắn ≤ 7 từ, thời gian tính lại theo clip (kể cả clip ghép nhiều đoạn).

- **ffmpeg có filter `subtitles`** (`probe` trả `can_burn_subs: true`): đặt `"burn_subs": true` để in phụ đề thẳng vào video (chữ trắng viền đen, phía dưới).
- **Không có filter** (bản ffmpeg của Homebrew hiện không kèm libass): nhập file `.srt` vào CapCut ở phần phụ đề (Captions), chỉnh kiểu chữ một lần rồi lưu thành mẫu cho các clip sau. Tên mục có thể khác theo phiên bản CapCut. Cách khác là dùng tính năng tạo phụ đề tự động của CapCut rồi soát lại chính tả.
- Thời gian chia dòng là ước lượng theo độ dài chữ trong từng câu, không phải theo từng từ, nên có thể lệch nửa giây trong câu dài. Đủ dùng cho phụ đề đọc; muốn kiểu chữ nhảy theo từng từ thì làm trong CapCut.

## 5. Đưa người xem về video dài

- **YouTube Shorts → "Video liên quan"** [chính thức, từ 2023, qua [Search Engine Land](https://searchengineland.com/youtube-enables-linking-shorts-long-form-videos-430655) và [Tubefilter](https://tubefilter.com/2023/09/01/youtube-related-links-multi-format-creators-shorts-live-long-form/)]: khi tải lên hoặc sau đó trong YouTube Studio, chọn một video của chính kênh để gắn vào Short; người xem thấy một nút bấm sang video đó. Mỗi Short gắn được một video. Công cụ đăng tự động qua API thường không đặt được trường này, nên phải đặt tay trong Studio [nguồn thứ cấp].
- [kinh nghiệm] Tỉ lệ bấm thường thấp, nên clip hiệu quả nhất là clip trả trọn một ý rồi để lại một câu hỏi lớn hơn mà video dài trả lời. Thêm bình luận ghim có link video dài.
- **TikTok, Reels**: chú thích không có link bấm được. Ghi "Bản đầy đủ trên YouTube: <tên kênh>" trong chú thích hoặc dùng link ở trang cá nhân.

## 6. Nội dung lặp lại và nội dung tái sử dụng

- **YouTube** [chính thức]: ngày 15/7/2025 YouTube đổi tên chính sách "nội dung lặp lại" (repetitious content) thành "nội dung không chân thực" (inauthentic content), áp cho cả kênh, nhắm vào nội dung sản xuất hàng loạt hoặc lặp đi lặp lại. Chính sách "nội dung tái sử dụng" (reused content) không đổi ([YouTube Help](https://support.google.com/youtube/answer/1311392); diễn giải qua [Search Engine Journal](https://www.searchenginejournal.com/youtube-clarifies-monetization-update-targeting-spam-not-reaction-channels/550123/)). Cắt clip từ video của chính mình không phải là dùng lại nội dung của người khác. Rủi ro thật với kênh ảnh + giọng AI là kênh Shorts toàn những clip na ná nhau, cùng khuôn, cùng câu mở. Mỗi clip nên có câu móc, ý và chữ trên màn hình riêng.
- **Instagram** [chính thức]: Reels mờ, có watermark, có viền, chủ yếu là chữ, hoặc đã đăng trên Instagram trước đó bị giảm hiển thị ([Instagram Ranking Explained](https://about.instagram.com/blog/announcements/instagram-ranking-explained)). Chế độ `blur` có nền mờ quanh khung: chưa có nguồn nói Instagram coi nền mờ là "viền", nhưng clip nào chủ thể đủ rõ để `crop` thì `crop` an toàn hơn cho Reels.

## 7. Lịch đăng

[kinh nghiệm] Không đăng tất cả clip cùng ngày. Một cách phổ biến: clip mạnh nhất đăng cùng ngày hoặc ngay sau ngày đăng video dài, các clip còn lại cách nhau 1–2 ngày. Clip phần 1 / phần 2 đăng liền nhau. Dùng số liệu của chính kênh (tỉ lệ "Đã xem / Đã lướt qua" của Shorts) để biết loại khoảnh khắc nào giữ người xem tốt, rồi chọn clip lần sau theo đó.
