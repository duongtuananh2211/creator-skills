# Cấu trúc mô tả và mẫu theo loại video

Cấu trúc dưới đây là tổng hợp từ hướng dẫn chính thức (mấy dòng đầu mô tả video, chương, link playlist, ghi công) và kinh nghiệm người làm nghề (thứ tự các khối, độ dài). Không có cấu trúc "chuẩn" nào được YouTube công bố; bỏ khối nào video không cần.

## 1. Các khối, theo thứ tự

| # | Khối | Nội dung | Độ dài gợi ý [kinh nghiệm] |
|---|---|---|---|
| 1 | **Câu mở** (phần hiện trước "Hiện thêm") | Video cho người xem điều gì, có từ khoá chính. Bổ sung cho tiêu đề, không chép lại. Nếu có tài trợ, câu công bố nằm ngay đây. | 1–2 câu, ý chính trọn trong ~100 ký tự |
| 2 | **Tóm tắt** | Video nói gì, cho ai, có gì cụ thể (con số, nơi chốn, công cụ). Từ liên quan xuất hiện tự nhiên. | 2–4 đoạn ngắn, 50–200 từ; video hướng dẫn có thể dài hơn |
| 3 | **Chương** | Mốc thời gian + tên chương. | Video từ ~5 phút có ≥ 3 ý rõ rệt |
| 4 | **Tài nguyên nhắc trong video** | Link, sách, công cụ, video được nhắc, kèm một dòng mỗi thứ là gì. | Chỉ những gì video thật sự nhắc |
| 5 | **Xem tiếp** | Playlist hoặc 1–2 video liên quan trên kênh. | 1–3 link |
| 6 | **Công bố, ghi công** | Tài trợ, link tiếp thị liên kết (nếu chưa nói ở khối 1), nhạc, tư liệu, người cộng tác. | Đủ để người xem và bên cấp phép thấy |
| 7 | **Khối kênh** | Kênh nói về gì (1 câu), lịch đăng nếu có, link mạng xã hội, liên hệ hợp tác. Giống nhau giữa các video, lưu sẵn trong `descriptions/channel-block.md`. | 3–6 dòng |
| 8 | **Hashtag** | 3–5 cái, cụ thể, liên quan. 3 cái đầu là ứng viên hiện trên tiêu đề. | 1 dòng |

Khối kênh là phần duy nhất được phép giống nhau giữa các video. Có thể đặt vào ô mô tả mặc định (Settings → Upload defaults) để khỏi dán lại, nhưng khi đó nó nằm ở đầu ô mô tả của video mới; nhớ kéo xuống cuối.

## 2. Viết câu mở

Câu mở làm hai việc cùng lúc: cho người đang lướt kết quả tìm kiếm lý do bấm vào, và cho YouTube biết video về gì. Công thức thường dùng [kinh nghiệm]:

- **Lời hứa + bằng chứng:** "Năm đầu làm freelancer thiết kế, mình lỗ 3 tháng liền trước khi có khách quen. Video này mở bảng thu chi thật của 12 tháng."
- **Câu hỏi người xem + câu trả lời có trong video:** "Làm freelancer thiết kế nên nhận khách ở đâu khi chưa có portfolio? Mình kể ba chỗ đã thử và chỗ duy nhất ra tiền."
- **Kênh kể chuyện / nhân vật:** giữ giọng nhân vật nhưng vẫn nói rõ chủ đề. "Xa là con rắn từng nghĩ mình thắng được nhà cái. Tập này Xa giải thích vì sao 'gỡ lại' là cái bẫy của người nghiện cờ bạc."

Tránh: "Xin chào các bạn, chào mừng đến với kênh…", "Trong video hôm nay…" (tốn phần hiện trước "Hiện thêm"), link hay hashtag ở dòng đầu, câu chép nguyên tiêu đề.

**Giữ tò mò mà không giấu chủ đề.** Video kể chuyện không cần tiết lộ kết thúc trong mô tả. Nói rõ chủ đề và cái được mất; giấu kết quả. Mô tả mơ hồ ("Một câu chuyện thay đổi cuộc đời mình") không giúp tìm kiếm và không giúp người xem quyết định.

## 3. Viết tên chương

- Lấy từ kịch bản (mốc "MỐC CHƯƠNG CHO PHẦN MÔ TẢ" nếu kịch bản do `story-content-writer` viết) hoặc phụ đề của bản dựng cuối (`desc_tools.py transcript`). Mốc trong kịch bản chỉ là dự kiến; **mốc phải lấy từ video đã dựng xong**.
- Tên chương nói nội dung và đủ hấp dẫn để bấm: "Khách quen đầu tiên đến từ đâu" thay vì "Phần 3".
- Chương đầu (00:00) là phần mở đầu; đặt tên theo nội dung ("Vì sao mình nghỉ việc"), không cần "Intro".
- Video kể chuyện có thể đặt tên chương gợi tò mò nhưng không lộ kết; video hướng dẫn đặt tên theo bước.
- 4–10 chương cho video 8–30 phút là phổ biến [kinh nghiệm]. Chương quá vụn (dưới 30 giây) làm thanh tiến trình rối.

## 4. Mẫu theo loại video

Mẫu chỉ minh hoạ thứ tự và độ dài. Mọi chi tiết khi làm thật phải lấy từ video của người dùng.

### Video kể chuyện cá nhân (8–30 phút)

```
<Câu mở: chuyện gì + cái được/mất, có từ khoá chính>

<Đoạn 1: bối cảnh, vì sao chính mình kể chuyện này>
<Đoạn 2: video có gì cụ thể: con số, nơi chốn, người (đã được đồng ý)>

00:00 <tên chương>
MM:SS <tên chương>
MM:SS <tên chương>

📌 Nhắc trong video:
- <tài nguyên>: <link>

▶ Xem tiếp: <playlist hoặc video liên quan>

<Khối kênh>

#<từ khoá chính> #<chủ đề> #<series hoặc kênh>
```

### Video hướng dẫn / giải thích

Câu mở trả lời thẳng "video giúp bạn làm được gì". Tóm tắt có thể là danh sách bước (gạch đầu dòng `-`). Chương theo bước. Khối tài nguyên quan trọng hơn: công cụ, phiên bản, file mẫu. Nếu nội dung có thể lỗi thời (giá, phiên bản phần mềm, luật), ghi tháng/năm quay.

### Review sản phẩm / có tài trợ

Câu công bố tài trợ nằm trong câu mở hoặc ngay dòng 2, trước "Hiện thêm". Xem `disclosure.md`. Ghi rõ điều kiện review (mua bằng tiền mình / được tặng / được trả tiền, dùng bao lâu).

### Kênh nhân vật đại diện

Câu mở giữ giọng nhân vật (mục 4 và 7 của hồ sơ kênh) nhưng vẫn nêu chủ đề thật bằng từ người ta gõ. Khối kênh nói một câu nhân vật là ai. Với chủ đề nhạy cảm (cờ bạc, sức khoẻ tâm thần, nợ), thêm dòng nguồn hỗ trợ nếu hồ sơ kênh mục 8 yêu cầu.

### Shorts

- [chính thức] Link trong mô tả Shorts không bấm được. Muốn dẫn về video dài, dùng tính năng "Video liên quan" (Related video) khi đăng Shorts.
- Mô tả Shorts nằm trong bảng phụ, ít người mở; tiêu đề quan trọng hơn [kinh nghiệm].
- Mẫu: 1–2 câu nói Short về gì (có từ khoá) + 2–3 hashtag. Không cần chương, không cần khối kênh dài.

## 5. Ví dụ hoàn chỉnh (minh hoạ)

Video giả định: "Năm đầu freelance: mình kiếm được bao nhiêu thật sự", 12:30, kênh kể chuyện nghề thiết kế.

```
Năm đầu làm freelancer thiết kế, mình lỗ 3 tháng liền trước khi có khách quen. Video này mở bảng thu chi thật của cả 12 tháng.

Mình nghỉ công việc lương 18 triệu ở một agency quảng cáo để nhận việc tự do. Trong video: tiền tiết kiệm mình chuẩn bị trước khi nghỉ, ba tháng đầu tiêu vào đâu, khách quen đầu tiên đến từ đâu, và con số cuối năm so với lương cũ.

Nếu bạn đang tính làm freelancer thiết kế, video này không phải để khuyên nghỉ hay ở lại, chỉ là số liệu của một người đã thử.

00:00 Vì sao mình nghỉ việc
01:20 Ba tháng đầu: lỗ bao nhiêu
04:05 Khách quen đầu tiên đến từ đâu
08:40 Con số sau 12 tháng
11:10 Nếu làm lại, mình sẽ đổi gì

📌 Nhắc trong video:
- Mẫu bảng thu chi mình dùng: https://example.com/bang-thu-chi

▶ Cả series làm freelance: https://www.youtube.com/playlist?list=...

Kênh kể chuyện thật về nghề thiết kế và làm việc tự do, video mới mỗi thứ Năm.
Hợp tác: email@example.com

#lamfreelancer #thietke #freelancer
```

Kiểm tra nhanh: câu đầu 78 ký tự (cả dòng 126), có "làm freelancer thiết kế", nên ý chính hiện đủ cả trên điện thoại; không chép tiêu đề; con số đều là số người dùng đưa; 5 chương, tên nói nội dung; 3 hashtag; 943 ký tự. `check` báo từ khoá chính không có trong tiêu đề: đây là lúc gợi ý bản tiêu đề như "Năm đầu làm freelancer thiết kế: mình kiếm được bao nhiêu thật sự" để người dùng chọn.
