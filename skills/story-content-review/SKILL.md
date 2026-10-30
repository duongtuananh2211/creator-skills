---
name: story-content-review
description: Chấm và góp ý bản nháp kể chuyện của creator thương hiệu cá nhân (kịch bản video ngắn TikTok/Reels/Shorts, kịch bản hoặc dàn ý YouTube dài, bài viết Facebook/Threads/LinkedIn/X, carousel) theo 10 tiêu chí storytelling và các kiểm tra riêng từng định dạng, gắn cờ lằn ranh đỏ (bịa/phóng đại, mồi tương tác, tiêu đề hứa mà không trả, lộ chuyện riêng người khác), rồi trả về các sửa đổi xếp theo mức độ, có trích nguyên văn và câu viết lại. Dùng khi người dùng đưa bản nháp và nói "review giúp bài này", "chấm kịch bản này", "bài này đăng được chưa", "góp ý content", "đọc thử xem có cuốn không", "review my script", "feedback my draft". Chỉ viết lại toàn bài khi được yêu cầu. Không dùng để viết nội dung mới từ ý tưởng (dùng `story-content-writer`), nghĩ phương án hook/tiêu đề/thumbnail (dùng `story-hook-writer`), soát chính tả đơn thuần, hay duyệt quảng cáo doanh nghiệp.
---

# Story content review

Skill này đọc bản nháp của một creator đang kể chuyện của chính họ (trải nghiệm, bài học, hành trình, hậu trường), chấm theo bộ tiêu chí rồi chỉ ra nên sửa gì trước và sửa thế nào. Thứ creator cần mang về là ba việc cụ thể để làm ngay, chứ không phải một bảng điểm.

## Đọc file tham khảo khi nào

- `references/rubric.md`: đọc trước khi chấm ở bước 3. File mô tả mức 1/3/5 của từng tiêu chí, câu hỏi kiểm tra và cách sửa hay dùng.
- `references/format-checks.md`: ở bước 4, chỉ đọc phần của định dạng đang review (video ngắn, YouTube dài, bài viết chữ hoặc carousel).
- `references/red-flags.md`: đọc khi bản nháp có dấu hiệu ở bước 5 (số liệu khó tin, thoại dài như ghi âm, chuyện riêng của người khác, câu xin tương tác, tiêu đề hứa nhiều) hoặc khi cần viết một góp ý nhạy cảm.
- `references/feedback-style.md`: đọc trước lần trả kết quả đầu tiên trong cuộc trò chuyện. File nói cách viết góp ý cho đúng giọng, ít mà trúng và giữ được giọng của creator.

## Nguyên tắc nền

- **Câu chuyện là của người dùng.** Đừng bịa sự kiện, lời thoại, con số hay cảm xúc, kể cả trong câu viết lại mẫu. Thương hiệu cá nhân sống nhờ niềm tin, và một chi tiết bịa bị phát hiện sẽ làm hỏng cả những gì có thật. Khi câu sửa cần một chi tiết thật mà bản nháp chưa có, để chỗ trống dễ thấy `[cần bổ sung: …]` hoặc hỏi người dùng.
- **Giữ giọng của creator.** Sửa để câu chuyện rõ và mạnh hơn, đừng sửa để nó nghe giống mình. Cách xưng hô, từ địa phương, nhịp câu quen thuộc của họ là một phần thương hiệu.
- **Mỗi nhận xét phải trỏ vào chữ trong bản nháp.** Trích nguyên văn rồi mới góp ý. Nhận xét chung chung kiểu "cần cuốn hơn" không giúp ai sửa được gì.
- **Ít mà trúng.** Một bản nháp có hai mươi lỗi nhỏ thường chỉ có hai, ba lỗi thật sự quyết định. Nêu những lỗi đó trước, phần còn lại gom gọn hoặc bỏ.

## Hồ sơ kênh (nếu có)

Trước bước 1, kiểm tra file `channel-profile.md` ở thư mục gốc dự án (thư mục mở Claude Code). File này do skill `channel-profile` tạo và là nguồn đúng nhất về kênh của người dùng. Nếu có, đọc nó trước và dùng như sau:

- **Khán giả** (mục 3): tiêu chí "liên quan đến người xem" chấm theo khán giả trong hồ sơ.
- **Người dẫn / nhân vật đại diện** (mục 4) và **giọng văn** (mục 7): thêm một kiểm tra "đúng giọng kênh"; chỗ lệch xưng hô hoặc tính cách được ghi ở mức 🟡 Câu chữ, lệch nặng thì 🟠.
- **Định dạng** (mục 6): độ dài và khung cố định của kênh là chuẩn để chấm nhịp và độ dài.
- **Quy tắc nội dung** (mục 8): vi phạm quy tắc kênh (thiếu nguồn, chủ đề nhạy cảm xử lý sai) được gắn cờ như lằn ranh đỏ nếu hồ sơ ghi là bắt buộc.

Những gì hồ sơ đã trả lời thì đừng hỏi lại. Nếu yêu cầu của người dùng trong lượt này khác hồ sơ (ví dụ đổi xưng hô cho một video), làm theo yêu cầu hiện tại và nhắc một dòng rằng nó khác hồ sơ. Nếu không có file, làm như bình thường; có thể nhắc một lần rằng `channel-profile` (nếu đã cài) giúp các lần sau không phải khai lại.

## Quy trình

### 1. Nắm bối cảnh

Xác định bốn điều: **định dạng và nền tảng**, **mục tiêu của bài** (truyền cảm hứng, chia sẻ bài học, dạy một mẹo, dẫn về sản phẩm hay dịch vụ), **người xem** là ai, và với video thì **thời lượng dự kiến**.

Phần lớn có thể suy ra từ bản nháp: kịch bản hai cột hay có ghi chú `[B-roll]` là video; "Slide 1/Slide 2" là carousel; đoạn văn dài có hashtag là bài viết. Chỉ hỏi khi câu trả lời làm đổi kết luận, ví dụ không rõ video 30 giây hay 90 giây (đổi hẳn nhận định về độ dài), hoặc không rõ đăng LinkedIn hay Facebook (đổi giọng và kiểu CTA). Nếu phải hỏi thì gộp vào một lần (AskUserQuestion). Còn lại, ghi giả định trong một dòng ở đầu câu trả lời rồi làm tiếp.

Với video YouTube, tiêu đề và chữ trên thumbnail là một phần của lời hứa. Nếu người dùng chưa đưa, nhờ họ dán vào. Nếu họ không có, ghi rõ là đã bỏ qua phần kiểm tra khớp gói nội dung (packaging).

Cũng xác định đây là **câu chuyện** hay **bài chia sẻ mẹo/kiến thức** có khung chuyện. Bộ tiêu chí vẫn dùng chung, nhưng vài tiêu chí được hiểu khác (xem bước 3).

### 2. Đọc hai lượt: cấu trúc trước, câu chữ sau

Thứ tự này quan trọng vì gọt câu trong một đoạn sắp bị cắt là phí công của cả hai bên, và người dùng sẽ nhầm rằng bài chỉ cần sửa vặt.

**Lượt cấu trúc.** Đọc một mạch như người xem lần đầu, rồi trả lời:
- Thông điệp của bài tóm được trong một câu không? Viết câu đó ra.
- Khoảnh khắc thay đổi nằm ở đâu? Nó được kể thành cảnh hay chỉ được nhắc qua?
- Tóm bài thành 4–7 nhịp (beat). Giữa các nhịp là "nhưng/vì vậy" hay "và rồi"?
- Đọc đến đâu thì bắt đầu chán hoặc rối? Đoạn nào bỏ đi mà câu chuyện không mất gì?

Nếu cấu trúc hỏng (không có thông điệp rõ, không có thay đổi, hoặc câu chuyện thật nằm chôn ở giữa bài), đừng sửa từng câu. Đưa ra dàn ý sắp xếp lại (giữ đoạn nào, cắt đoạn nào, đưa câu nào lên đầu) và chỉ sửa câu chữ cho câu mở đầu và câu chốt.

**Lượt câu chữ.** Chỉ làm với những phần sẽ được giữ lại: chỗ nói chung chung cần chi tiết, câu rườm, nhịp đều đều, câu nghe như AI viết, lời kể thay vì cảnh.

### 3. Chấm 10 tiêu chí

Chấm mỗi tiêu chí từ 1 đến 5, kèm một dòng bằng chứng trích từ bản nháp. Mức 1/3/5 và câu hỏi kiểm tra chi tiết nằm trong `references/rubric.md`.

| # | Tiêu chí | Câu hỏi cốt lõi |
|---|---|---|
| 1 | Câu móc (hook) và lời hứa | 1–3 giây hoặc dòng đầu có mở ra một khoảng trống cụ thể mà người xem quan tâm, và bài có trả lời nó không? |
| 2 | Rủi ro (stakes) | Người kể có thể mất gì hoặc được gì? Người xem biết điều đó sớm không? |
| 3 | Sự thay đổi và khoảnh khắc chuyển hóa | Trước và sau khác nhau thế nào? Khoảnh khắc đó có được kể thành cảnh không? |
| 4 | Nhân quả "nhưng/vì vậy" | Các nhịp nối với nhau bằng nguyên nhân và trở ngại, hay chỉ "và rồi… và rồi…"? |
| 5 | Chi tiết cụ thể và cảnh (show, don't tell) | Có tên, số, nơi chốn, lời thoại, chi tiết giác quan, hay toàn tính từ và khái niệm? |
| 6 | Một thông điệp rõ | Tóm được trong một câu không? Có đoạn nào lạc khỏi thông điệp đó? |
| 7 | Liên quan đến người xem ("thì sao?") | Người xem mục tiêu được gì? Bài học có áp dụng được ngoài hoàn cảnh của người kể? |
| 8 | Chân thực và mức độ tổn thương vừa phải | Có thật không, người kể có là nhân vật chính không? Phần chia sẻ riêng tư có phục vụ người xem hay chỉ là trút lòng? |
| 9 | Nhịp và độ dài theo định dạng | Phần dẫn có cân với phần chính không? Có chậm lại ở cao trào và lướt nhanh phần còn lại? Độ dài có hợp định dạng? |
| 10 | CTA phù hợp | Lời kêu gọi có đi ra tự nhiên từ thông điệp, không xin tương tác kiểu mồi (engagement bait)? |

Với bài mẹo/kiến thức: "rủi ro" là cái giá người xem phải trả nếu không biết điều này, còn "chuyển hóa" là người xem hiểu hoặc làm khác đi ra sao sau khi xem.

Tổng điểm trên 50. Các mốc dưới đây là quy ước để dễ đọc, không phải chuẩn đo lường:
- **42–50 · Đăng được**: chỉ còn sửa nhẹ, tùy chọn.
- **33–41 · Sửa nhẹ**: cấu trúc ổn, cần làm sắc vài chỗ.
- **24–32 · Sửa cấu trúc**: có chất liệu tốt nhưng cần sắp xếp lại.
- **dưới 24 · Viết lại**: nên quay lại bước tìm khoảnh khắc và thông điệp.

Nếu có bất kỳ vấn đề 🔴 nào ở bước 5 thì bài chưa đăng được, dù tổng điểm cao.

### 4. Kiểm tra theo định dạng

Đọc phần tương ứng trong `references/format-checks.md`. Những điểm thường quyết định nhất:
- **Video ngắn**: người xem hiểu bài nói về gì trong khoảng 3 giây đầu; số âm tiết khớp thời lượng (ước tính 4,5–5,5 âm tiết/giây); chữ trên màn hình ngắn và xem không bật tiếng vẫn hiểu; không mở đầu bằng "Xin chào mọi người, hôm nay…".
- **YouTube dài**: tiêu đề, thumbnail và 30 giây đầu cùng nói một lời hứa (câu đầu khớp tiêu đề, khung hình đầu khớp thumbnail); vào nội dung trong khoảng 20–30 giây; thân bài chia chu kỳ năng lượng, có móc lại (re-hook) và tương phản ở các điểm chuyển; kết ở cao trào, không báo hiệu kết thúc trước khi trả phần chính.
- **Bài viết chữ**: dòng đầu tự đứng được trước nút "Xem thêm"; đọc trên điện thoại không bị thành bức tường chữ; không lạm dụng kiểu mỗi câu một dòng (broetry).
- **Carousel**: slide 1 đủ mạnh để dừng lướt, slide 2 đứng riêng được; mỗi slide một ý; có mạch nối qua các slide; slide cuối chốt ý và chỉ một CTA.

Các con số về nền tảng (điểm cắt "Xem thêm", giới hạn ký tự, số slide) đều là ước lượng và hay thay đổi, nên khi nhắc đến thì nói là "khoảng".

### 5. Gắn cờ lằn ranh đỏ

Những vấn đề sau luôn được xếp 🔴, bất kể điểm, vì chúng làm hại người dùng (mất niềm tin, bị nền tảng giảm phân phối, làm tổn thương người khác) chứ không chỉ làm bài kém hay:
- **Dấu hiệu bịa hoặc phóng đại**: con số khó tin, thoại dài như ghi âm từ nhiều năm trước, "người lạ dạy mình bài học", dòng thời gian mâu thuẫn.
- **Mồi tương tác (engagement bait)**: "comment 'có' để nhận…", "share nếu bạn đồng ý", "tag 3 người bạn".
- **Tiêu đề, hook hoặc thumbnail hứa điều nội dung không trả.**
- **Thông tin riêng tư của người khác**: tên, ảnh, tin nhắn chụp màn hình, chi tiết nhận diện được về người thân, người yêu cũ, sếp, khách hàng, trẻ em, khi chưa có sự đồng ý.
- **Phơi bày quá mức (floodlighting)**: chuyện đau còn quá mới, chia sẻ để kéo phản ứng hơn là để phục vụ bài học.

Khi không kiểm chứng được, hỏi thay vì kết luận ("Con số 300 triệu này là doanh thu hay lợi nhuận, trong bao lâu?"). Cách diễn đạt và các phương án xử lý nằm trong `references/red-flags.md`.

### 6. Trả kết quả

Viết bằng tiếng Việt theo khung dưới đây. Mỗi mức độ chỉ nêu tối đa 3–5 vấn đề quan trọng nhất; nếu không có vấn đề ở mức nào thì bỏ mục đó.

```markdown
> Giả định: [định dạng · nền tảng · mục tiêu · người xem], chỉ khi phải tự suy ra

## Tổng điểm: [x]/50 · [Đăng được / Sửa nhẹ / Sửa cấu trúc / Viết lại]
[2–3 câu nhận định: bài đang làm tốt điều gì, điều gì đang cản nó, thông điệp một câu mình đọc ra được]

| Tiêu chí | Điểm | Bằng chứng |
|---|---|---|
| Câu móc | 3 | "…trích ngắn…" — [lý do một dòng] |
| … | | |

## 🔴 Nghiêm trọng (sửa trước khi đăng)
**1. [Tên vấn đề]**
- Bản nháp: "…trích nguyên văn…"
- Vì sao: [một câu]
- Đề xuất: "…câu viết lại…" (hoặc câu hỏi cần người dùng trả lời)

## 🟠 Cấu trúc
…cùng khung; với vấn đề sắp xếp lại, đưa dàn ý mới dạng danh sách…

## 🟡 Câu chữ
…cùng khung, trước → sau…

## ✅ Điểm tốt nên giữ
- [1–3 điểm, có trích dẫn, để khi sửa không làm mất]

## Làm trước 3 việc này
1. …
2. …
3. …
```

Kết thúc bằng một câu hỏi ngắn mời làm tiếp: áp các sửa đổi vào bản nháp, viết lại toàn bài, hay chỉ sửa phần mở đầu.

### 7. Sau khi review

- **Áp sửa đổi**: sửa đúng những mục người dùng đồng ý, giữ nguyên phần còn lại và giữ chỗ trống `[cần bổ sung: …]` cho chi tiết họ chưa cung cấp. Sau đó chấm lại nhanh những tiêu chí bị ảnh hưởng.
- **Viết lại toàn bài**: chỉ làm khi người dùng yêu cầu. Giữ giọng, chất liệu thật và thông điệp của họ; nói rõ đã đổi gì về cấu trúc.
- Nếu điểm yếu nhất là câu móc hoặc tiêu đề, gợi ý dùng `story-hook-writer` (nếu đã cài) để có nhiều phương án đã được soát mồi nhấp chuột (clickbait). Nếu kết luận là "Viết lại", có thể gợi ý `story-content-writer`.
- Kết quả để trong chat. Nếu người dùng muốn, lưu bản review hoặc bản đã sửa thành file trong dự án của họ.

## Trường hợp đặc biệt

- **Bản nháp chỉ là ý tưởng vài dòng**: chưa đủ để chấm. Nhận xét nhanh về khoảnh khắc và thông điệp, hỏi thêm chất liệu, hoặc gợi ý `story-content-writer`.
- **Người dùng chỉ muốn điểm hoặc chỉ muốn góp ý nhanh**: trả bảng điểm, hoặc chỉ mục "Làm trước 3 việc này", rồi dừng.
- **Nhiều bản nháp hoặc một series**: review từng bài theo khung rút gọn, rồi thêm một đoạn về điểm chung lặp lại giữa các bài (cùng một kiểu hook, cùng một lỗi CTA).
- **Bản nháp viết bằng tiếng Anh**: góp ý bằng tiếng Việt (trừ khi người dùng viết bằng tiếng Anh), còn câu viết lại giữ ngôn ngữ của bản nháp.
- **Bài có dấu hiệu người viết đang trong khủng hoảng thật** (tuyệt vọng, ý nghĩ tự hại): ưu tiên con người trước nội dung. Hỏi han nhẹ nhàng, gợi ý họ tìm người tin cậy hoặc hỗ trợ chuyên môn, và đừng chấm điểm câu chuyện ấy như một sản phẩm.
