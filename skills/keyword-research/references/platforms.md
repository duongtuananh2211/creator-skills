# Đặt từ khoá ở đâu, theo từng nền tảng

Đọc ở bước 6 chế độ B, và khi người dùng hỏi "từ khoá này để ở đâu". Mức bằng chứng như trong `sources.md`.

Quy tắc chung cho mọi nền tảng: từ khoá phải mô tả đúng thứ video có, và xuất hiện ở chỗ nó tự nhiên. Danh sách từ khoá trần, lặp từ để lấy lượt tìm đều bị coi là spam (YouTube nói rõ trong chính sách spam, lừa đảo [chính thức]; TikTok được người làm nghề cảnh báo tương tự [người làm nghề]).

---

## YouTube (video dài)

YouTube nói tìm kiếm xếp hạng theo ba nhóm: **mức liên quan**, **tương tác**, **chất lượng**; mức liên quan xét tiêu đề, thẻ, mô tả và nội dung video khớp với truy vấn tới đâu [chính thức, "How YouTube search works" https://support.google.com/youtube/answer/16090438]. Từ khoá chỉ lo được phần liên quan; video không giữ được người xem thì không lên.

| Chỗ | Đặt gì | Ghi chú |
|---|---|---|
| Tiêu đề | Từ khoá chính, viết đúng như người ta gõ, gần đầu | Ý chính trong khoảng 50–60 ký tự đầu [người làm nghề]. Tiêu đề vẫn phải hấp dẫn người đọc; làm kỹ với `story-hook-writer`. |
| Câu mở mô tả | Từ khoá chính, một lần, trong câu tự nhiên | Phần hiện trước "Hiện thêm" khoảng 100–157 ký tự [người làm nghề]. Viết kỹ với `youtube-description-writer`. |
| Tên chương | Từ dạng câu hỏi, từ phụ | Mỗi chương một ý; tên chương là chỗ hợp nhất cho câu hỏi dài. |
| Lời nói trong video | Nói từ khoá chính trong 30 giây đầu | YouTube xét cả nội dung video [chính thức]; phụ đề đúng giúp việc này. Cách đọc nội dung cụ thể không được công bố [suy luận]. |
| Thẻ (Tags) | Cách viết sai hay gặp, dạng không dấu | Thẻ "đóng vai trò rất nhỏ", chủ yếu có ích khi chủ đề hay bị viết sai [chính thức, https://support.google.com/youtube/answer/146402]. Thẻ nằm trong ô Tags, không dán vào mô tả. |
| Hashtag | 3–5 hashtag cụ thể [người làm nghề] | YouTube chọn tối đa 3 để hiện trên tiêu đề; hơn 60 hashtag thì tất cả bị bỏ qua [chính thức]. |

## YouTube Shorts

- Tiêu đề Shorts ngắn, chứa từ khoá chính; người xem Shorts phần lớn tới từ feed, không phải tìm kiếm, nên từ khoá ít quan trọng hơn câu móc ở giây đầu [suy luận].
- Chữ trên màn hình và lời nói nên có từ khoá: người tìm trong tab Shorts thấy video khớp ý ngay.
- Gắn "Video liên quan" về video dài cùng cụm để người tìm đi tiếp.

## TikTok

TikTok không công bố cách xếp hạng tìm kiếm chi tiết. Những gì dưới đây phần lớn là [người làm nghề], các nguồn không thống nhất về mức quan trọng của từng chỗ.

| Chỗ | Đặt gì | Ghi chú |
|---|---|---|
| Chữ trên màn hình (giây 0–3) | Từ khoá chính dạng câu người ta gõ | Nhiều nguồn cho rằng TikTok đọc chữ trên video bằng nhận dạng ký tự [người làm nghề]. Chữ này cũng là câu móc, nên phải vừa đúng từ vừa gợi tò mò. |
| Lời nói | Nói từ khoá trong câu đầu | Nhiều nguồn cho rằng TikTok chép lời nói để lập chỉ mục [người làm nghề]. Phụ đề tự động bật lên giúp cả người xem tắt tiếng. |
| Chú thích (caption) | Một câu tự nhiên có từ khoá chính + 1 từ phụ | Không nhồi; chú thích ngắn, đọc như người thật viết. |
| Hashtag | 3–5: 1–2 hashtag chủ đề rộng, 2–3 hashtag cụ thể của cụm | Chọn hashtag hot từ Creative Center chỉ khi đúng chủ đề video. |
| Tên âm thanh, tiêu đề ảnh bìa | Có thể chứa từ khoá | Chưa có nguồn đáng tin về tác dụng [suy luận]. |

Lưu ý riêng TikTok:

- **Chủ đề bị chặn gợi ý** (script ghi ở `empty_seed`, ví dụ cờ bạc): đừng dùng cụm đó trong hashtag, chữ trên màn hình. Nói qua cơ chế, cảm xúc, hậu quả bằng từ không bị chặn, và đối chiếu quy tắc ở mục 8 hồ sơ kênh.
- Creator Search Insights có nhãn **content gap** [chính thức]: cụm có nhãn này và hợp kênh nên được ưu tiên trên TikTok kể cả khi YouTube đông.

## Facebook Reels, Instagram Reels

- Không có công cụ từ khoá công khai đáng kể; tìm kiếm trên hai nền tảng này đóng vai trò nhỏ so với feed [suy luận].
- Dùng lại chú thích và chữ trên màn hình của bản TikTok; Instagram có tìm kiếm theo từ khoá trong chú thích, nên giữ từ khoá chính trong câu đầu chú thích [người làm nghề].

## Mẫu "đặt ở đâu" cho một nội dung

```
Từ khoá chính: <cụm>  (gợi ý YT #2, TikTok #1 · serp: 0/20 khớp đúng)
Từ phụ: <cụm 2>, <cụm 3>, <câu hỏi>

YouTube
- Tiêu đề: <phương án có từ khoá chính gần đầu>
- Câu mở mô tả: có "<cụm>" → chuyển cho youtube-description-writer
- Chương: "<câu hỏi>" ở chương 2
- Nói "<cụm>" trong 30 giây đầu
- Thẻ: <không dấu>, <cách viết sai>
TikTok / Shorts
- Chữ màn hình giây 0–3: "<câu người ta gõ>"
- Câu nói đầu: "<…>"
- Chú thích: <một câu>
- Hashtag: #<rộng> #<cụ thể> #<cụ thể>
```
