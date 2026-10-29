# Tám giọng điệu và cách làm cho từng công cụ

File này dùng ở bước 3 và 5. Chỉ đọc phần chung và phần của giọng điệu đã chọn.

Mức bằng chứng: tag ghi *(chính thức)* có trong danh sách tag v4 hoặc trang Best practices của ElevenLabs; *(tự viết)* là tag tự mô tả, ElevenLabs cho phép nhưng chưa ai kiểm chứng. **Mọi gợi ý về giọng nào hợp giọng điệu nào, mức tốc độ, mức nhấn, độ dài khoảng nghỉ đều là kinh nghiệm chưa kiểm chứng**: điểm bắt đầu để nghe thử rồi chỉnh, không phải thông số chuẩn. Ví dụ dưới đây dùng nhân vật giả định.

## Phần chung

**Viết lại là đổi hình thức.** Được tách câu, đổi dấu câu, đổi từ viết sang từ nói, đảo trật tự trong một câu. Không được thêm sự kiện, con số, cảm xúc, câu cảm thán hay câu mới. Mọi ví dụ "sau" bên dưới chỉ chứa thông tin đã có trong bản "trước".

**Mật độ tag ElevenLabs.** Một tag ở đầu mỗi chỗ cảm xúc đổi, không gắn vào từng câu. Một video 60 giây thường chỉ cần 3–6 tag. Tag phản ứng (`[laughs]`, `[sighs]`, `[crying]`, `[gasps]`) tạo ra âm thanh thật nên chỉ dùng khi kịch bản đã nói rõ cảm xúc đó ở đúng chỗ đó.

**Stability ElevenLabs.** v4: thấp hơn cho biểu cảm, cao hơn cho đều. v3: Creative hoặc Natural khi cần tag ăn rõ, Natural hoặc Robust khi cần ổn định (mô tả chế độ v3 lấy từ trang cũ, có thể đã đổi). Không đưa số cụ thể vì chưa có nguồn.

**Vbee.** Không có tag. Giọng điệu đến từ chữ và dấu câu, giọng, tốc độ, `emphasisIntensity` (0–100, chỉ giọng nhấn nhá) và khoảng nghỉ. Khoảng nghỉ thủ công ghi `[nghỉ Xs]` chỉ trong bản duyệt.

**Nhiều giọng điệu trong một bài.**
- ElevenLabs: đặt tag mới ở câu đầu đoạn đổi giọng điệu. Giữa hai giọng điệu khác xa nhau (hồi hộp sang vui vẻ), thêm `[pause]` hoặc xuống dòng để chuyển không bị gắt.
- Vbee: không đổi được cảm xúc giữa chừng bằng tag. Cách làm: đổi nhịp câu và dấu câu theo từng đoạn; đặt mỗi giọng điệu thành một khối riêng để chỉnh khoảng nghỉ theo khối (Vbee có cấu hình ngắt nghỉ theo khối); nếu cần tốc độ hoặc giọng khác hẳn thì tạo từng đoạn riêng rồi ghép trong trình chỉnh âm thanh. Chưa rõ studio có cho đặt tốc độ riêng từng khối không.

**Bảng tóm tắt** (kinh nghiệm chưa kiểm chứng):

| Giọng điệu | Câu | Tag ElevenLabs chính | Vbee tốc độ | Vbee emphasisIntensity |
| --- | --- | --- | --- | --- |
| Vui vẻ | Vừa, nhịp nhanh nhẹ | optimistic, playful | 1.0–1.1 | 50–70 |
| Hào hứng / năng lượng | Ngắn, dồn | excited, amazed, snappy | 1.05–1.15 | 60–80 |
| Thủ thỉ / tâm sự | Ngắn, nhiều chỗ ngừng | softly, quietly, trusting | 0.85–0.95 | 30–50 |
| Trầm lắng / xúc động | Ngắn, chậm, nghỉ dài | thoughtful, softly, slowly | 0.85–0.9 | 30–50 |
| Kể chuyện (người dẫn) | Vừa, đều, có điểm dừng | thoughtful, curious | 0.95–1.0 | 40–60 |
| Hồi hộp / bí ẩn | Rất ngắn, ngắt cụt | hushed, anxious, slowly | 0.9–0.95 | 40–60 |
| Nghiêm túc / chuyên gia | Vừa, rõ ràng, ít cảm thán | gần như không tag | 0.95–1.0 | 20–40 |
| Hài hước | Ngắn, có quãng ngừng trước câu chốt | playful, mischievously | 1.0–1.1 | 60–80 |

---

## 1. Vui vẻ

**Khi nào dùng:** chuyện có kết quả tốt, chia sẻ niềm vui nhỏ, CTA thân thiện ở cuối video.

**Viết lại:** câu độ dài vừa, nhịp nhanh nhẹ. Dấu chấm than ở câu đã sẵn tin vui, không rải khắp bài. Tiểu từ "nha", "luôn", "nè" được, tối đa một hai chỗ, và chỉ khi người dùng tự nói kiểu đó.

**ElevenLabs:** `[optimistic]`, `[playful]`, `[content]` *(chính thức)*; `[cheerful]`, `[warm]` *(tự viết)*. `[laughs]` chỉ khi kịch bản có chuyện buồn cười thật. Stability thấp đến trung bình.

**Vbee:** thử giọng nhấn nhá trước; tốc độ 1.0–1.1; emphasisIntensity 50–70; giữ nghỉ dấu câu mặc định.

**Ví dụ**
- Trước: "Tháng này mình trả hết khoản nợ 120 triệu. Mất đúng hai năm."
- ElevenLabs v4: `[optimistic] Tháng này, mình trả hết khoản nợ một trăm hai mươi triệu! Mất đúng hai năm luôn.`
- Vbee: `Tháng này, mình trả hết khoản nợ một trăm hai mươi triệu! Mất đúng hai năm luôn.`

## 2. Hào hứng / năng lượng

**Khi nào dùng:** hook mở đầu, khoảnh khắc đạt mốc, mẹo muốn người xem làm ngay.

**Viết lại:** câu ngắn, dồn dập, động từ đứng sớm trong câu. Con số lớn tách thành câu riêng hoặc đặt cuối câu. VIẾT HOA một từ chốt là đủ (chỉ ElevenLabs).

**ElevenLabs:** `[excited]`, `[amazed]`, `[proud]`, `[snappy]`, `[speedy]` *(chính thức)*. Đừng giữ `[excited]` cả bài; xen một câu bình thường để phần cao trào còn nổi. Stability thấp.

**Vbee:** giọng nhấn nhá; tốc độ 1.05–1.15; emphasisIntensity 60–80; nghỉ dấu câu ngắn hơn mặc định một chút nếu dùng API (ví dụ `sentenceBreak` 0.35).

**Ví dụ**
- Trước: "Sau ba tháng, kênh của mình chạm mốc 10.000 người theo dõi, nhiều hơn cả hai năm trước cộng lại."
- ElevenLabs v4: `[excited] Ba tháng sau... kênh của mình chạm mốc MƯỜI NGHÌN người theo dõi! [amazed] Nhiều hơn cả hai năm trước cộng lại.`
- Vbee: `Ba tháng sau, kênh của mình chạm mốc mười nghìn người theo dõi! Nhiều hơn cả hai năm trước cộng lại.`

## 3. Thủ thỉ / tâm sự

**Khi nào dùng:** lời thú nhận, chuyện riêng, đoạn giữa video khi người kể "hạ giọng" nói thật.

**Viết lại:** câu ngắn, nhiều dấu phẩy và chỗ ngừng như đang nghĩ. Dùng từ đời thường. Câu hỏi tu từ nhẹ nếu kịch bản đã có. Tránh dấu chấm than.

**ElevenLabs:** `[softly]`, `[quietly]`, `[trusting]`, `[thoughtful]` *(chính thức)*; `[whispers]` *(chính thức)* chỉ cho một câu, vì thì thầm cả đoạn khó nghe trên loa điện thoại. Stability trung bình.

**Vbee:** tốc độ 0.85–0.95; emphasisIntensity 30–50; nghỉ dài hơn mặc định (API: `sentenceBreak` khoảng 0.6–0.7).

**Ví dụ**
- Trước: "Có một chuyện mình chưa kể với ai: năm đó mình nói dối cả nhà là công ty vẫn ổn."
- ElevenLabs v4: `[softly] Có một chuyện, mình chưa kể với ai. [pause] Năm đó, mình nói dối cả nhà... là công ty vẫn ổn.`
- Vbee (bản dán): `Có một chuyện, mình chưa kể với ai.` (xuống dòng) `Năm đó, mình nói dối cả nhà, là công ty vẫn ổn.`
- Vbee (bản duyệt): thêm `[nghỉ 1s]` sau câu đầu.

## 4. Trầm lắng / xúc động

**Khi nào dùng:** mất mát, thất bại, khoảnh khắc thay đổi khi kể chậm lại.

**Viết lại:** câu ngắn, chậm, một ý mỗi câu. Hình ảnh cụ thể đứng riêng thành câu. Đừng thêm từ cảm xúc ("đau lắm", "nghẹn ngào") nếu kịch bản không có; để chỗ nghỉ làm việc đó.

**ElevenLabs:** `[thoughtful]`, `[softly]`, `[slowly]`, `[vulnerable]`, `[let down]`, `[long pause]` *(chính thức)*. `[sighs]` chỉ khi kịch bản tả đúng lúc thở dài hoặc mệt mỏi; `[crying]` gần như không bao giờ, trừ khi người dùng kể mình đã khóc ở đúng câu đó. Stability trung bình đến cao để giọng không bị kịch.

**Vbee:** tốc độ 0.85–0.9; emphasisIntensity 30–50; nghỉ dài (API: `sentenceBreak` 0.7, `paragraphBreak` 1.2). Nghỉ thủ công 1–2 giây trước câu nặng nhất.

**Ví dụ**
- Trước: "Ngày đóng cửa quán, mình ngồi lại một mình đến 2h sáng, nhìn mấy cái ghế trống."
- ElevenLabs v4: `[thoughtful] Ngày đóng cửa quán... mình ngồi lại một mình, đến hai giờ sáng. [slowly] Nhìn mấy cái ghế trống.`
- Vbee (bản dán): `Ngày đóng cửa quán, mình ngồi lại một mình, đến hai giờ sáng.` (xuống dòng) `Nhìn mấy cái ghế trống.`
- Vbee (bản duyệt): `[nghỉ 1,5s]` trước câu cuối.

## 5. Kể chuyện (người dẫn)

**Khi nào dùng:** YouTube dài, phần bối cảnh, video kể hành trình theo mốc thời gian. Là lựa chọn an toàn khi người dùng không chắc.

**Viết lại:** câu vừa, nhịp đều. Mốc thời gian đứng đầu câu. Dừng ngắn trước chi tiết quan trọng (con số, câu nói). Giữ từ nối "nhưng", "vì vậy" của kịch bản vì chúng giữ mạch.

**ElevenLabs:** `[thoughtful]`, `[curious]`, `[pause]`, `[slowly]` *(chính thức)*; `[warm storyteller]` *(tự viết)*. Ít tag; chỉ thêm ở bước ngoặt. Stability trung bình đến cao cho bài dài để giọng đều giữa các khối.

**Vbee:** tốc độ 0.95–1.0; emphasisIntensity 40–60; nghỉ đoạn dài hơn mặc định một chút (API: `paragraphBreak` khoảng 0.8–1.0) để tách chương.

**Ví dụ**
- Trước: "Năm 2019, mình nhận công việc đầu tiên ở TP.HCM, lương 7 triệu một tháng."
- ElevenLabs v4: `[thoughtful] Năm hai nghìn không trăm mười chín, mình nhận công việc đầu tiên, ở Thành phố Hồ Chí Minh. [pause] Lương bảy triệu một tháng.`
- Vbee: `Năm hai nghìn không trăm mười chín, mình nhận công việc đầu tiên, ở Thành phố Hồ Chí Minh. Lương bảy triệu một tháng.`

## 6. Hồi hộp / bí ẩn

**Khi nào dùng:** hook vào thẳng cảnh, đoạn trước bước ngoặt, câu "nhưng đó chưa phải phần tệ nhất".

**Viết lại:** câu rất ngắn, có khi chỉ là một cụm danh từ ("Ba giờ sáng."). Giữ lại thông tin quan trọng tới cuối câu. Không giải thích sớm.

**ElevenLabs:** `[hushed]`, `[anxious]`, `[slowly]`, `[long pause]`, `[curious]` *(chính thức)*. `[low threatening]` *(chính thức)* dễ nghe như phim kinh dị, hợp nội dung giải trí hơn chuyện cá nhân. Stability thấp đến trung bình.

**Vbee:** tốc độ 0.9–0.95; emphasisIntensity 40–60; nghỉ thủ công 1 giây sau câu mở và trước tiết lộ.

**Ví dụ**
- Trước: "3 giờ sáng, đồng sáng lập nhắn: 'Mai mình nói chuyện nhé.'"
- ElevenLabs v4: `[hushed] Ba giờ sáng. [pause] Đồng sáng lập nhắn: [slowly] Mai mình nói chuyện nhé.`
- Vbee (bản dán): `Ba giờ sáng.` (xuống dòng) `Đồng sáng lập nhắn: Mai mình nói chuyện nhé.`
- Vbee (bản duyệt): `[nghỉ 1s]` sau "Ba giờ sáng." và `[nghỉ 0,5s]` sau dấu hai chấm.

## 7. Nghiêm túc / chuyên gia

**Khi nào dùng:** bài học rút ra, mẹo chuyên môn, phần phân tích sai lầm.

**Viết lại:** câu vừa, chủ ngữ rõ, một ý mỗi câu. Bỏ tiểu từ. Không dấu chấm than. Ý chính đặt cuối câu hoặc tách thành câu riêng sau một chỗ nghỉ.

**ElevenLabs:** gần như không cần tag; dấu câu làm phần lớn việc. Nếu cần: `[thoughtful]`, `[slowly]` *(chính thức)*; `[serious]`, `[calm, confident]` *(tự viết)*. `[powerful]` *(chính thức)* chỉ cho một câu chốt. Stability cao để giọng đều.

**Vbee:** chọn giọng có cảm giác đọc rõ, ổn định khi nghe mẫu; tốc độ 0.95–1.0; emphasisIntensity 20–40; nghỉ dấu câu mặc định.

**Ví dụ**
- Trước: "Sai lầm lớn nhất của mình là không tách tài khoản cá nhân và tài khoản kinh doanh trong 2 năm đầu."
- ElevenLabs v4: `Sai lầm lớn nhất của mình là không tách tài khoản cá nhân và tài khoản kinh doanh. [pause] Trong hai năm đầu.`
- Vbee: `Sai lầm lớn nhất của mình, là không tách tài khoản cá nhân và tài khoản kinh doanh. Trong hai năm đầu.`

## 8. Hài hước

**Khi nào dùng:** chuyện tự giễu, khoảng cách giữa kỳ vọng và thực tế, câu chốt bất ngờ.

**Viết lại:** dựng kỳ vọng bằng một câu bình thường, nghỉ, rồi câu chốt ngắn và phẳng. Câu chốt đứng cuối, không giải thích thêm. Cái buồn cười phải nằm sẵn trong kịch bản; skill chỉ canh nhịp, không thêm câu đùa.

**ElevenLabs:** `[playful]`, `[mischievously]`, `[sarcastic]`, `[disbelief]` *(chính thức)*; `[deadpan]` *(tự viết)* cho câu chốt. `[laughs]`, `[snorts]` chỉ khi người dùng muốn có tiếng cười trong lời đọc. Stability thấp.

**Vbee:** giọng nhấn nhá; tốc độ 1.0–1.1; emphasisIntensity 60–80; nghỉ thủ công khoảng 1 giây ngay trước câu chốt, vì quãng ngừng là nơi tạo ra cái buồn cười.

**Ví dụ**
- Trước: "Mình đặt mục tiêu dậy lúc 5h sáng. Ngày đầu tiên mình dậy lúc 9h."
- ElevenLabs v4: `[playful] Mình đặt mục tiêu dậy lúc năm giờ sáng. [pause] [deadpan] Ngày đầu tiên, mình dậy lúc chín giờ.`
- Vbee (bản dán): `Mình đặt mục tiêu dậy lúc năm giờ sáng.` (xuống dòng) `Ngày đầu tiên, mình dậy lúc chín giờ.`
- Vbee (bản duyệt): `[nghỉ 1s]` trước câu chốt.

---

## Flash v2.5 và công cụ khác

Flash v2.5 không có audio tag. Dùng bản Vbee của từng ví dụ làm gốc, thêm `<break time="0.8s" />` (tối đa 3 giây, thưa) ở chỗ bản duyệt ghi `[nghỉ Xs]`. Với công cụ TTS khác, dùng nguyên bản Vbee: chỉ chữ, dấu câu và xuống dòng.
