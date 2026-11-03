# Lọc, gom cụm và chấm từ khoá

Đọc trước bước 3. Các ngưỡng số trong file này là **kinh nghiệm của người viết skill** [suy luận], không phải quy định của nền tảng. Dùng chúng để xếp các từ với nhau, không để kết luận tuyệt đối.

---

## 1. Loại bỏ trước khi chấm

Bỏ ngay, không cần chấm:

- **Lệch niche**: gợi ý trùng chữ nhưng khác nghĩa ("nghiện cờ bạc tái sinh", "nghiện cờ bạc xuyên không" là tên truyện, không phải người đang tìm cách cai).
- **Lệch ý định**: người gõ muốn thứ kênh không làm được ("tiết kiệm tiền bằng giấy" là đồ thủ công cho trẻ em, không phải tài chính cá nhân).
- **Truy vấn hằng ngày**: có ngày, giá, tỉ số hôm nay. Lượng lớn nhưng hết hạn trong vài giờ, báo thắng.
- **Tên người, thương hiệu** mà video sẽ không thật sự nói tới, hoặc nói tới thì vướng rủi ro (người thường trong vụ việc, thương hiệu đối thủ để kéo lượt tìm).
- **Từ khoá mà video phải hứa điều không trả được** ("chữa khỏi", "kiếm 100 triệu/tháng"): vừa giật tít vừa có thể vi phạm chính sách quảng cáo y tế, tài chính.

## 2. Gom cụm theo ý định

Một video trả lời một **cụm**, không phải một từ. Gom các biến thể cùng ý định: "cách tiết kiệm tiền", "cách tiết kiệm tiền hiệu quả", "tiết kiệm tiền như thế nào" là một cụm. Đặt tên cụm bằng biến thể rõ nghĩa nhất và có nhiều tín hiệu nhất.

Nhãn ý định và định dạng hợp:

| Ý định | Dấu hiệu trong cụm từ | Định dạng hợp |
|---|---|---|
| Cách làm | cách, làm sao, hướng dẫn, cho người mới, tại nhà | Video dài có chương; Shorts/TikTok cho một bước |
| Giải thích | vì sao, tại sao, là gì, do đâu, cơ chế | Video dài kể chuyện giải thích; Shorts một ý |
| Cân nhắc, so sánh | có nên, nên chọn, A hay B, nào tốt, review | Video dài so sánh; TikTok kết luận nhanh |
| Tình huống, cứu nguy | phải làm sao, bị … thì làm gì, cách thoát | Video dài đồng cảm + lối ra; cần cẩn trọng giọng |
| Cảm hứng, giải trí | thử thách, một ngày, vlog, câu chuyện | Shorts/TikTok, series |
| Thời sự | sự kiện, tên riêng đang nóng | Chuyển sang `trending-topic-finder` |

## 3. Bốn tín hiệu

Chấm mỗi tín hiệu 1–3. **Hợp kênh là cửa**: đạt 1 thì bỏ, không chấm tiếp.

### Hợp kênh (cửa)

- 3: nằm gọn trong một trụ cột, đúng cách khán giả (mục 3 hồ sơ) gọi vấn đề, kênh trả lời được tốt hơn người khác (góc nhìn mục 2, kinh nghiệm thật của người dẫn).
- 2: thuộc niche nhưng kênh chỉ trả lời ở mức bình thường, hoặc khán giả rộng hơn khán giả chính.
- 1: lạc trụ cột, hoặc kênh không có gì riêng để nói.

### Nhu cầu (từ gợi ý tìm kiếm và dữ liệu người dùng dán)

- 3: có trên ≥2 nền tảng **và** hiện lại ở nhiều truy vấn (`hits` ≥3), hoặc Trends/Studio/vidIQ người dùng dán cho thấy đang lên hay ổn định ở mức cao so với từ khác của kênh.
- 2: có trên 1 nền tảng ở thứ hạng gợi ý đầu (`best_rank` ≤3), hoặc ≥2 nền tảng nhưng ít `hits`.
- 1: chỉ hiện lẻ tẻ ở vị trí cuối, hoặc chỉ hiện khi chạy `--alphabet`.

Đừng viết "nhiều người tìm" khi chỉ có điểm 2–3 từ gợi ý; viết "có trong gợi ý YouTube và TikTok".

### Cạnh tranh (từ `serp`, càng thấp càng dễ, nên điểm ngược)

- 3 (dễ): `title_exact` ≤3 **hoặc** phần lớn kết quả chỉ khớp một phần (`title_most_words` ≤6), tức YouTube đang phải trả video "gần đúng".
- 2: 4–9 tiêu đề khớp đúng cụm, nhiều kênh khác nhau.
- 1 (khó): ≥10 tiêu đề khớp đúng, lượt xem trung vị rất cao so với cỡ kênh người dùng, hoặc trang đầu toàn kênh lớn, báo đài.

Một kênh chiếm nhiều chỗ (`top_channel_share` ≥5/20) là có một "chủ" của cụm này; muốn vào phải có góc khác hẳn.

### Khoảng trống (cơ hội cho video mới)

- 3: kết quả đầu **cũ** (`median_age_days` > 3 năm) hoặc ít video dưới 1 năm (`under_1y` ≤4), mà nhu cầu vẫn còn; hoặc người dùng có nhãn content gap từ Studio/TikTok.
- 2: có video mới nhưng ít video mới có lượt xem tốt (`median_views_under_1y` thấp so với `median_views`): cụm cũ được xem nhiều, video mới chưa ai làm hay.
- 1: nhiều video mới, xem tốt, đúng cụm: thị trường đang đông.

## 4. Xếp hạng

| Hạng | Điều kiện | Làm gì |
|---|---|---|
| **Ưu tiên** | Hợp kênh 3, tổng ba tín hiệu còn lại ≥7 | Làm sớm; dùng làm từ khoá chính |
| **Thử** | Hợp kênh ≥2, tổng 5–6 | Làm khi có góc tốt, hoặc gộp làm từ phụ cho video Ưu tiên |
| **Kho** | Hợp kênh ≥2, tổng ≤4 | Lưu lại; xem lại khi kênh lớn hơn hoặc trend đổi |
| **Bỏ** | Hợp kênh 1, hoặc vướng mục 1 | Không ghi vào kho |

Kênh mới (dưới vài nghìn người đăng ký) nên ưu tiên Cạnh tranh và Khoảng trống hơn Nhu cầu: một cụm hẹp mà trang đầu toàn video cũ, khớp một phần, có cơ hội hơn một cụm lớn đã có chủ [suy luận, khớp với lời khuyên chung "cụ thể hơn thì dễ hơn" của người làm nghề].

## 5. Ví dụ đã chấm (dữ liệu thật, 03/11/2026)

**"cách tiết kiệm tiền"** (kênh tài chính cá nhân cho sinh viên)
- Gợi ý: có trên YouTube và TikTok, cụm "cách tiết kiệm tiền hiệu quả" có `hits` 4. Nhu cầu 3.
- `serp`: 7/20 tiêu đề khớp đúng, 14/20 dưới 1 năm, trung vị 89 nghìn lượt xem, 15 kênh khác nhau. Cạnh tranh 2, Khoảng trống 1.
- Hợp kênh 2 (rộng, không riêng sinh viên). Tổng 6 → **Thử**. Biến thể hẹp hơn "tiết kiệm tiền cho sinh viên" (có trên YouTube, TikTok) đáng chạy `serp` riêng: nhiều khả năng ít đối thủ hơn và hợp kênh 3.

**"nghiện cờ bạc phải làm sao"** (kênh giải thích tâm lý nghiện)
- Gợi ý: YouTube và Google có, **TikTok trả rỗng cho cả "nghiện cờ bạc"** (chủ đề bị chặn gợi ý). Nhu cầu 2.
- `serp`: 0 tiêu đề khớp đúng, 1/20 khớp phần lớn, chỉ 4/20 dưới 1 năm; trang đầu là kênh tâm lý, VTV24, podcast. YouTube đang trả video "gần đúng". Cạnh tranh 3, Khoảng trống 3.
- Hợp kênh 3. Tổng 8 → **Ưu tiên** trên YouTube. Trên TikTok, tránh cụm và hashtag chứa "cờ bạc"; nói qua cơ chế ("vì sao thua rồi vẫn muốn chơi tiếp") và kiểm tra quy tắc nội dung ở mục 8 hồ sơ.

**"cách nấu phở bò"** (kênh nấu ăn mới)
- `serp`: 12/20 tiêu đề khớp đúng, tuổi trung vị khoảng 4 năm, lượt xem cao nhất 3,2 triệu, chỉ 2/20 dưới 1 năm.
- Cạnh tranh 1 (rất đông), nhưng Khoảng trống 3 (kết quả cũ). Cụm lớn đã có chủ cũ; kênh mới vào được bằng biến thể hẹp ("phở bò cho 2 người", "phở bò nồi áp suất") hơn là đánh thẳng cụm gốc.

## 6. Biến thể tiếng Việt cần thử

Khi lập hạt giống và khi gom cụm, kiểm tra:

- **Vùng miền**: lợn/heo, ngô/bắp, dứa/thơm, bát/chén, ốm (gầy/bệnh), "trông"/"giữ". Chạy cả hai nếu khán giả trải nhiều miền; chọn cách gọi của khán giả chính làm từ khoá chính.
- **Không dấu, gõ tắt**: `--no-accent` với từ chính. Không dấu thường trả cùng gợi ý có dấu; nếu khác hẳn, đó là một nhóm người gõ riêng (thường trẻ hơn hoặc gõ trên điện thoại) [suy luận].
- **Từ mượn**: freelance/freelancer/làm tự do, skincare/chăm sóc da, content/nội dung. Chọn dạng hiện nhiều hơn trong gợi ý làm chính.
- **Cách gọi của người trong cuộc và người ngoài**: "cai nghiện cờ bạc" (người thân tìm) và "bỏ cờ bạc" (người chơi tìm) là hai khán giả khác nhau.
- **Câu hỏi đầy đủ**: người Việt hay gõ cả câu ("có nên mua nhà khi chưa có vợ không"). Những câu dài này ít cạnh tranh và rất hợp làm tiêu đề hoặc tên chương.
