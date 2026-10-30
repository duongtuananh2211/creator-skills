# Chọn từ khoá cho mô tả

Mục tiêu: tìm **1–2 từ khoá chính** (đúng lời khuyên chính thức của YouTube) và **3–6 từ liên quan** mà video thật sự trả lời. Không phải tìm càng nhiều từ càng tốt.

## 1. Nguồn, theo thứ tự đáng tin

1. **Số liệu của chính kênh** [chính thức, cần người dùng mở Studio]:
   - Analytics → Reach → "Traffic source: YouTube search": những từ người xem đã gõ để tới video của kênh. Tốt nhất để chọn từ cho video cùng chủ đề.
   - Analytics → tab **Research** (Nghiên cứu): người xem của kênh và người xem trên YouTube đang tìm gì, kèm "content gap" (tìm nhiều mà ít video đáp ứng). Tên và vị trí tab có thể đổi; nếu người dùng không thấy, nhờ họ chụp màn hình phần Analytics họ có.
   Skill không đọc được Studio. Hỏi người dùng có muốn dán vào không; không có cũng làm tiếp được.
2. **Gợi ý tìm kiếm YouTube** [không chính thức nhưng phản ánh cách người ta gõ]: `desc_tools.py suggest --q "<từ>" [--alphabet] [--no-accent]`. Endpoint này không công bố, có thể đổi hoặc chặn; thứ tự gợi ý không phải số lượt tìm.
3. **Google Ads Keyword Planner** [chính thức YouTube có nhắc]: có số lượt tìm ước lượng nhưng là của Google Search, cần tài khoản Ads. Chỉ dùng nếu người dùng đã có.
4. **Tiêu đề và mô tả của video cùng chủ đề đang lên top**: `desc_tools.py fetch <link>` để xem người khác gọi tên chủ đề thế nào. Chỉ để biết cách gọi tên, không chép câu.

## 2. Cách chọn

1. Viết lời hứa của video trong một câu. Từ khoá phải nằm trong lời hứa đó; từ nào video không trả lời thì loại, dù nó được tìm nhiều.
2. Lập 3–5 hạt giống từ tiêu đề, lời hứa, và cách khán giả trong `channel-profile.md` (mục 3) gọi vấn đề. Chạy `suggest` cho 1–2 hạt giống quan trọng nhất (`--alphabet` khoảng 30 lượt gọi mỗi từ, đừng chạy cho mọi từ).
3. Chọn **từ khoá chính**: cụm người ta gõ thật (có trong gợi ý hoặc số liệu kênh), khớp lời hứa, càng cụ thể càng tốt với kênh nhỏ ("làm freelancer thiết kế" thay vì "freelance").
4. Chọn **từ liên quan**: cách gọi khác (freelance/freelancer/làm tự do), câu hỏi người xem hay gõ ("làm freelancer ở đâu"), tên riêng, công cụ, địa danh có trong video.
5. Ghi bảng ngắn cho người dùng:

| Từ | Vai trò | Nguồn | Đặt ở đâu |
|---|---|---|---|
| làm freelancer thiết kế | chính | gợi ý YT | tiêu đề, câu 1 |
| làm freelancer ở đâu | câu hỏi | gợi ý YT | đoạn tóm tắt, tên chương |
| upwork | liên quan | có trong video phút 4 | chương 3 |

## 3. Tiếng Việt: dấu, cách viết, từ mượn

- **Viết đúng dấu trong tiêu đề và mô tả.** Người đọc là người thật; mô tả không dấu trông như spam. Gợi ý tìm kiếm YouTube thường trả cả dạng có dấu cho truy vấn không dấu, cho thấy tìm kiếm có xử lý dấu, nhưng YouTube không công bố cách làm [suy luận]. Muốn chắc thì tìm thử dạng không dấu và xem video cùng chủ đề có hiện không.
- Không thêm bản không dấu của câu vào mô tả. Nếu cần, để dạng không dấu và cách viết sai hay gặp vào **ô Tags** (đúng chỗ YouTube nói thẻ có ích).
- **Từ mượn và tên riêng:** kiểm tra cả hai cách viết ("freelance" và "freelancer", "content creator" và "sáng tạo nội dung"); chọn cách xuất hiện nhiều trong gợi ý làm chính, cách kia dùng một lần ở phần sau.
- **Chủ đề có khán giả quốc tế:** giữ mô tả tiếng Việt, rồi thêm bản dịch tiêu đề và mô tả trong Studio → Languages (Ngôn ngữ) thay vì viết hai thứ tiếng chung một mô tả. Người xem chọn ngôn ngữ khác sẽ thấy bản dịch.

## 4. Những chỗ dễ sai

- **Chọn từ vì nhiều người tìm, không vì video trả lời được.** Người tới từ từ khoá lệch sẽ bỏ đi sớm, kéo tương tác xuống.
- **Từ khoá quá rộng** ("kiếm tiền", "cuộc sống") với kênh nhỏ: cạnh tranh với hàng nghìn video, không giúp gì.
- **Nhồi mọi từ liên quan vào một đoạn.** Mỗi từ liên quan nên xuất hiện ở chỗ nó tự nhiên: một câu tóm tắt, một tên chương.
- **Coi số lượng gợi ý là lượt tìm.** Gợi ý chỉ cho biết người ta có gõ cụm đó, không cho biết bao nhiêu người.
