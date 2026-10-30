# Prompt ảnh, chữ đè và xuất file

File này dùng ở bước 5 (viết prompt cho từng concept) và bước 7 (tạo ảnh, đè chữ, xuất file). Các khuyến nghị về prompt là kinh nghiệm dùng công cụ tạo ảnh, không phải tài liệu chính thức của Google Flow; giao diện và model của Flow thay đổi thường xuyên.

---

## 1. Cấu trúc prompt

Viết prompt bằng tiếng Anh (các model tạo ảnh thường bám prompt tiếng Anh sát hơn [kinh nghiệm]), kèm một dòng tóm tắt tiếng Việt để người dùng đọc. Mỗi prompt đi theo thứ tự:

1. **Nhân vật chính và hành động / biểu cảm**: một thứ duy nhất, mô tả cụ thể.
2. **Bố cục**: "16:9 YouTube thumbnail composition", nhân vật chính nằm ở nửa trên hoặc chính giữa phía trên, khoảng trống cho chữ ở 1/3 trên (hoặc bên trái/phải, tuỳ concept), góc dưới bên phải để trống.
3. **Nền**: đơn giản, ít chi tiết, màu tương phản với nhân vật chính ("plain dark teal background", "soft gray studio backdrop").
4. **Ánh sáng và phong cách**: đúng phong cách của kênh (ảnh chụp, 3D, minh hoạ phẳng...), ánh sáng làm nổi nhân vật chính ("rim light", "spotlight on the subject").
5. **Màu**: màu của nhân vật chính và của nền, nêu rõ để tạo tương phản.
6. **Ràng buộc**: "no text, no letters, no logos, no watermark, no extra characters, uncluttered".

Một concept nên có 1 prompt chính và 1–2 biến thể (đổi góc máy, đổi màu nền) để Flow sinh 2–4 ảnh mỗi lần.

## 2. Mặc định không có chữ trong ảnh

Model tạo ảnh hay viết sai hoặc mất dấu tiếng Việt, và chữ nằm trong ảnh thì không sửa hay A/B test được. Vì vậy mặc định: tạo ảnh không chữ, chừa chỗ, rồi đè chữ trong Canva, CapCut hay Photoshop. Nếu người dùng muốn thử để model tự viết chữ, đặt chữ trong ngoặc kép trong prompt và kiểm tra từng dấu trên ảnh kết quả trước khi dùng.

## 3. Giữ nhân vật nhất quán

- **Kênh nhân vật**: lấy mô tả nhân vật từ mục 4 của `channel-profile.md` (bảng màu, dáng, đặc điểm nhận diện) và viết thành **một câu mô tả cố định**, dùng nguyên văn trong mọi prompt của kênh. Ví dụ: "Xa, a small cartoon green snake with large round amber eyes, a tiny red scarf, flat 2D illustration style with thick outlines". Ghi câu này vào `brief.md` để lần sau dùng lại.
- Nếu Flow cho đính kèm ảnh tham chiếu (reference sheet của nhân vật), nhờ người dùng tự tải ảnh đó lên trong Flow; `google-flow-image-generation` hiện không tự động hoá bước tải ảnh lên.
- Biểu cảm nên chọn trong bộ 3–5 biểu cảm cố định của character bible, để nhân vật không "lệch vai".

## 4. Kênh có người dẫn thật

- Ưu tiên **ảnh thật** của người dẫn: chụp riêng cho thumbnail, hoặc trích một khung hình rõ nét từ video. Dùng AI cho nền, đạo cụ, hiệu ứng, rồi ghép trong Canva/Photoshop.
- Không dùng AI tạo khuôn mặt của người thật (kể cả người dẫn) làm điều họ không làm, trông như ảnh chụp. Theo YouTube, hình như thật khiến người thật làm điều họ không làm có thể cần nhãn nội dung tổng hợp (https://support.google.com/youtube/answer/14328491), và với thương hiệu cá nhân nó đi ngược lại chính lý do người xem tin creator.
- Biểu cảm trong ảnh chụp phải là biểu cảm hợp với câu chuyện, không diễn quá.

## 5. Ví dụ

Ví dụ minh hoạ định dạng, không phải chuyện thật.

**Kênh nhân vật, cơ chế "ngay trước hậu quả":**

```
Tóm tắt: Xa đẩy cả tổ trứng lên bàn cược, nửa trên là mặt Xa và tổ trứng phát sáng.
Prompt: Xa, a small cartoon green snake with large round amber eyes, a tiny red scarf,
flat 2D illustration style with thick outlines, nervously pushing a glowing golden nest
of eggs onto a dark green casino table with its tail. 16:9 YouTube thumbnail composition:
Xa's face and the glowing nest in the upper half, slightly left of center; empty dark space
in the top-right third for text; bottom-right corner empty. Plain dark background, single
warm spotlight on the nest, strong contrast between the gold nest and the dark table.
No text, no letters, no logos, no watermark, no extra characters, uncluttered.
```

**Kênh người thật, cơ chế "một vật thể, nền trống" (phần nền và vật tạo bằng AI, ghép ảnh thật của người dẫn sau):**

```
Tóm tắt: một tờ hoá đơn dài cuộn xuống từ trên cao, nền đen, chừa chỗ bên trái để ghép ảnh người dẫn.
Prompt: A single very long paper receipt hanging down from the top of the frame and curling
on the floor, photographed on a plain matte black background, one soft spotlight from above,
crisp paper texture, cinematic product photography. 16:9 YouTube thumbnail composition: the
receipt in the right half, the top of the receipt clearly visible in the upper third; empty
black space on the left half for a person to be composited later; bottom-right corner empty.
No text on the receipt, no letters, no logos, no watermark, no people.
```

## 6. Chữ đè

[kinh nghiệm người làm nghề]

- **Font** có hỗ trợ tiếng Việt (trên Google Fonts lọc ngôn ngữ Vietnamese), ví dụ Be Vietnam Pro, Montserrat, Inter, ở độ đậm Bold đến Black. Kênh nên chọn một hai font cố định.
- **Kích thước**: chữ cao khoảng 1/6 đến 1/5 chiều cao ảnh trở lên, tối đa 2 dòng, để còn đọc được ở cỡ 168×94 px.
- **Tương phản**: chữ sáng trên nền tối hoặc ngược lại; thêm viền (stroke) hoặc đổ bóng khi nền phức tạp. Kiểm tra bằng ảnh xám.
- **Vị trí**: 1/3 trên của ảnh nếu concept cho phép (phép thử 50% cho TV), không đè lên mặt nhân vật chính, tránh góc dưới phải.
- **Dấu tiếng Việt**: chữ in hoa có dấu chồng (Ấ, Ẫ, Ộ) cần khoảng cách dòng rộng hơn để dấu không chạm dòng trên. Soát lại từng chữ sau khi xuất.
- **Một từ nhấn**: nếu cần nhấn, đổi màu một từ, đừng đổi màu cả câu.

## 7. Xuất file

- Tỉ lệ 16:9. YouTube khuyến nghị 3840×2160 (tối thiểu rộng 640 px); 1920×1080 là mức an toàn cho phần lớn công cụ. Test & Compare cần từ 1280×720 trở lên.
- JPG hoặc PNG. Tải lên từ điện thoại giới hạn 2 MB, từ máy tính 50 MB: nếu người dùng tải bằng điện thoại, xuất JPG chất lượng khoảng 85–90% để dưới 2 MB.
- Đặt tên theo concept (`a-truoc-hau-qua.jpg`, `b-lac-loai.jpg`) và lưu vào `thumbnails/<slug>/candidates/`, rồi chạy `check` trên bản đã đè chữ, không chỉ bản ảnh nền.
