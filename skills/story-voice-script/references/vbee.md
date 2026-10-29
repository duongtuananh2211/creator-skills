# Vbee AIVoice cho lời đọc tiếng Việt

Nghiên cứu ngày 29/10/2026. Ba mức bằng chứng: **[chính thức]** là trang trợ giúp, changelog hoặc tài liệu API của Vbee; **[kinh nghiệm]** là nguồn bên thứ ba hoặc suy luận từ cách sản phẩm hoạt động; **[chưa kiểm chứng]** là điều chưa tìm được nguồn. Vbee cập nhật giao diện và giọng khá thường xuyên, nên tên nút hay danh sách giọng có thể đã khác.

Nguồn chính: [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt), [Vbee API docs](https://api-docs.vbee.vn/llms-full.txt).

## 1. Điều quan trọng nhất: Vbee không có tag cảm xúc

[chính thức] Không có tài liệu nào về tag cảm xúc, biến thể cảm xúc ("vui", "buồn") hay cú pháp nhấn trong văn bản. Marketing của Vbee nói giọng mô phỏng "ngữ điệu, cảm xúc và cách nhấn nhá", nhưng không có danh sách cảm xúc nào được công bố.

Vì vậy với Vbee, giọng điệu được tạo bằng năm thứ:

1. **Chữ và nhịp câu** trong bản dán (câu ngắn hay dài, dấu chấm hay dấu phẩy, câu hỏi, câu cảm).
2. **Chọn giọng** phù hợp (vùng miền, giới tính, giọng có nhấn nhá).
3. **Tốc độ.**
4. **Mức nhấn** `emphasisIntensity`, chỉ với giọng có hỗ trợ.
5. **Khoảng nghỉ**: tự động theo dấu câu, và chèn thủ công ở chỗ cần.

Bất kỳ thứ gì trong ngoặc (`[nghỉ 1s]`, `(cười)`) mà lọt vào bản dán đều có nguy cơ bị đọc thành tiếng. Bản dán vào Vbee chỉ có chữ và dấu câu thường.

## 2. Giọng đọc và vùng miền

- [chính thức] Vbee AIVoice có khoảng 20 giọng tiếng Việt (một trang FAQ khác đưa con số tổng khác, nên số lượng có thể đã đổi). Bộ lọc giọng gồm tên, giới tính, loại giọng, ngôn ngữ, **vùng miền**, lĩnh vực; mỗi giọng có bản nghe mẫu. Giọng mặc định là HN-Ngọc Huyền.
- [chính thức] Mã giọng có tiền tố vùng: `hn_` là giọng Bắc, `hue_` là giọng Huế (Trung), `sg_` là giọng Nam. Ví dụ: `hn_female_ngochuyen_full_48k-fhg`, `hn_female_maiphuong_vdts_48k-fhg`, `sg_female_lantrinh_vdts_48k-fhg`, `hue_female_huonggiang_full_48k-fhg`, `sg_male_trungkien_vdts_48k-fhg`, `hn_male_thanhlong_talk_48k-fhg`.
- [chính thức] Tên giọng xuất hiện trong changelog: Ngọc Huyền, Lan Trinh, Tường Vy, Thảo Trinh, Mạnh Dũng, Phú Thăng, Anh Khôi, Ngọc Lan, Hà Chi, Việt Bách (giọng trẻ em), Mai Phương.
- [chính thức] Giọng có **nhấn nhá**: Ngọc Huyền 2.0 (v3.85.0, 12/11/2025), Mạnh Dũng 2.0 (v3.132.0, 27/03/2026), Thảo Trinh nhấn nhá, Mạnh Dũng nhấn nhá (Beta).
- [chính thức] Clone giọng: bản nhanh cần 10–30 giây ghi âm, bản chuyên nghiệp cần từ 5 phút; chỉ tiếng Việt. Bản clone nhanh có "tỷ lệ lỗi đọc cao hơn".
- Vbee **không công bố** giọng nào hợp với tâm trạng nào, và không công bố số giọng theo từng vùng.

Cách gợi ý giọng [kinh nghiệm]:
- Chọn vùng theo khán giả và theo giọng thật của creator, nếu họ hay nói giọng Nam thì giọng `sg_` nghe liền mạch hơn với các video họ tự nói.
- Giọng điệu cần biểu cảm (hào hứng, hài hước, hồi hộp, xúc động) thì thử giọng nhấn nhá trước.
- Nghe bản mẫu của 2–3 giọng với chính đoạn mở đầu của kịch bản rồi mới chọn. Skill không khẳng định giọng nào "vui" hay "buồn".

## 3. Tốc độ

- [chính thức] API: `speed` từ 0.25 đến 1.9, mặc định 1.0 (bản cũ là `speed_rate` 0.1–1.9, một chữ số thập phân). Changelog v1.2.0: "Giới hạn tốc độ của tất cả các giọng từ 0.25-1.9". Một trang FAQ ghi "0.25x - 0.9x", nhiều khả năng là lỗi đánh máy.
- [chính thức] Giao diện có 7 mức từ "rất chậm" đến "rất nhanh" và cho nhập giá trị tuỳ chỉnh.
- Mức gợi ý theo giọng điệu nằm trong `voicings.md`. Tất cả là điểm bắt đầu [kinh nghiệm], chỉnh theo tai nghe. Đổi tốc độ thì nhân lại ước tính thời lượng: ở tốc độ 0.9, khoảng 4,5–5,5 âm tiết/giây còn khoảng 4,0–5,0.

## 4. Mức nhấn (emphasisIntensity)

- [chính thức] Tham số API `emphasisIntensity` (bản cũ `emphasis_intensity`): số nguyên 0–100, bước 10, "chỉ hoạt động với giọng hỗ trợ nhấn nhá" (`has_emphasis`).
- [chưa kiểm chứng] Tài liệu không mô tả tên và vị trí thanh chỉnh này trong studio web. Nếu người dùng không thấy, bỏ qua và dựa vào chọn giọng cùng dấu câu.
- Không có cú pháp nào để nhấn một từ cụ thể trong câu. Muốn từ nào nặng hơn thì đặt nó ở cuối câu ngắn, hoặc tách thành câu riêng.

## 5. Khoảng nghỉ

### Trong studio

- [chính thức] **Nghỉ theo dấu câu, tự động**: sau `.` `,` `;` và xuống dòng. Độ dài mặc định chỉnh được trong "Thiết lập ngắt nghỉ dấu câu", có nút "Đặt mặc định". Từ v3.68.0 (26/09/2025) có thể cấu hình ngắt nghỉ theo từng khối văn bản.
- [chính thức] **Nghỉ thủ công**: chọn "Thêm khoảng nghỉ", đặt vào vị trí trong câu, chọn ngắn/vừa/dài hoặc gõ số giây từ 0 đến 60 rồi Enter. Trên điện thoại có sẵn 0,5 / 1 / 2 / 3 giây hoặc nhập số với dấu chấm thập phân (0.3).
- [chính thức] Trong trình chỉnh âm thanh có thể chèn khoảng lặng ở đầu hoặc tại con trỏ.

Cách skill xử lý: bản dán chỉ dùng dấu câu và xuống dòng để tạo nhịp. Chỗ nào cần nghỉ dài hơn dấu câu cho được, bản duyệt ghi `[nghỉ 1s]` (hoặc số giây khác), và người dùng chèn bằng "Thêm khoảng nghỉ" đúng vị trí đó trong studio. Nên dặn họ: số chỗ nghỉ thủ công ít thôi, thường 2–5 chỗ cho video ngắn, đặt ở trước khoảnh khắc thay đổi và trước câu chốt.

### Trong API

- [chính thức] Không có cú pháp SSML hay `<break>` nào trong tài liệu API. Nghỉ được chỉnh bằng object `clientPause`:

| Trường | Mặc định | Khoảng |
| --- | --- | --- |
| `sentenceBreak` | 0.45 s | 0.1–10 |
| `majorBreak` | 0.3 s | 0.1–10 |
| `mediumBreak` | 0.25 s | 0.1–10 |
| `paragraphBreak` | 0.6 s | 0–10 |

- [chưa kiểm chứng] Tài liệu không nói rõ `majorBreak` và `mediumBreak` ứng với dấu nào; đoán là `;` hoặc `:` cho major và `,` cho medium.
- Chưa có thông tin `<break>` viết thẳng trong văn bản gửi API có chạy không. Đừng dùng.

## 6. Cách đọc (từ điển phát âm)

- [chính thức] Tính năng "Tùy chỉnh cách đọc" (đổi tên từ "Từ điển" thành "Cách đọc" ở v2.28.0): nhập từ viết tắt hoặc từ nước ngoài, nhập cách đọc, nghe thử, rồi "Thêm từ". Sửa và xoá được.
- [chính thức] Hướng dẫn viết cách đọc chia hai loại:
  - Từ viết tắt: "QL4H" → "Quốc lộ 4-hát"; "VHVN" sẽ bị đọc "vê hát vê nờ" nếu không thêm "văn hóa Việt Nam".
  - Từ nước ngoài, phiên âm kiểu Việt: "bad" → "bát-đ", "resort" → "ri-xót", "brain" → "b-rên", "six" → "xích-x".
  - Quy tắc phiên âm: s/x → "x"; sh và -tion → "s"; d/z → "d"; gi/j → "gi"; cụm phụ âm giữ phụ âm đầu ("brain" → "b-rên").
  - Lời khuyên chính thức: đọc theo ngữ cảnh, tra khi không chắc, tham khảo cách báo chí chính thống viết.
- [chính thức] **Từ viết tắt không có trong từ điển sẽ bị đánh vần từng chữ cái.**
- [chính thức] "Kiểm tra cách đọc" (AI Biên tập) quét văn bản, gợi ý cách đọc kèm bảng phiên âm; "Áp dụng tất cả" đổi mọi chỗ xuất hiện, "Thêm vào từ điển" lưu lại. "Tìm kiếm và Thay thế" đổi một từ trong cả bài.

Cách skill xử lý: bản dán viết thẳng cách đọc (đã phiên âm, đã chuẩn hoá) để chạy đúng ngay lần đầu mà không cần cài gì. Bảng cách đọc liệt kê các từ đó; từ nào sẽ lặp lại ở video sau thì gợi ý thêm vào "Cách đọc", lúc đó có thể giữ chữ gốc trong văn bản. Nhắc người dùng chạy "Kiểm tra cách đọc" một lượt sau khi dán, vì nó có thể bắt được từ skill bỏ sót.

## 7. Số, ngày giờ và các lỗi đã biết

- [chính thức] Vbee có chuẩn hoá số và ngày giờ tự động nhưng từng có lỗi: đọc sai "năm 10.000 tỷ đồng" và "0 giờ 0 phút 0 giây" (sửa ở v2.33.0), không đọc được "°C" (sửa ở v2.8.1). Tài liệu API không mô tả bước chuẩn hoá nào, chỉ có cắt khoảng trắng.
- [chưa kiểm chứng] Vbee hiện có đọc đúng "1,8 triệu", "23h47", "KPI" hay không thì chưa có tài liệu. Skill chuẩn hoá hết trước (xem `vietnamese-normalization.md`).

## 8. Giới hạn

| Giới hạn | Con số | Ghi chú |
| --- | --- | --- |
| Mỗi khối văn bản trong studio | Khoảng 1.000 ký tự | [chính thức, gián tiếp] Suy ra từ một bản sửa lỗi nhắc "> 1000 ký tự trong mỗi block" |
| Nghe thử mỗi lần | 1.500 ký tự | [chính thức] Một ghi chú cũ hơn nói 1.000, hai nguồn mâu thuẫn |
| Mỗi lần chuyển đổi | 100.000 điểm (gói trả phí), 3.000 điểm (miễn phí) | [chính thức] |
| Quy đổi điểm | 1 ký tự = 1 điểm với giọng cơ bản; ×2 giọng nâng cao và clone nhanh; ×3 giọng premium; giọng nước ngoài ×2 | [chính thức] Nghĩa là gói miễn phí với giọng nâng cao chỉ được khoảng 1.500 ký tự mỗi lần |
| API batch | 100.000 ký tự | [chính thức] |
| API realtime | 300 ký tự; chỉ một số giọng (HN-Ngọc Huyền, SG-Tường Vy, HN-Mai Phương, SG-Lan Trinh, SG-Thảo Trinh) | [chính thức] |

Skill giữ mỗi khối dưới khoảng 1.000 ký tự, cắt ở cuối đoạn, và nhắc người dùng kiểm tra số điểm còn lại trước khi tạo kịch bản YouTube dài.

## 9. Mẹo chính thức khi nhập văn bản

- Văn bản nhập từ file hoặc link có thể lỗi chính tả, lỗi ngắt câu; kiểm tra trước khi chuyển đổi.
- Bôi đen một đoạn rồi "Nghe thử" để kiểm phát âm trước khi tạo cả bài.
- Từ ngữ xúc phạm hoặc bị cấm sẽ làm hiện "Văn bản không hợp lệ".
