# ElevenLabs cho lời đọc tiếng Việt

Nghiên cứu ngày 29/10/2026. Ba mức bằng chứng: **[chính thức]** là tài liệu hoặc blog của ElevenLabs; **[kinh nghiệm]** là hướng dẫn bên thứ ba hoặc cộng đồng; **[chưa kiểm chứng]** là suy luận hoặc thông tin cũ không tìm lại được nguồn. ElevenLabs đổi model và giao diện thường xuyên. Eleven v4 ra cuối tháng 9/2026 và trang hướng dẫn v3 cũ đã bị gộp vào trang "Best practices" mới, nên mẹo v3 trên các blog năm 2025 có thể đã lỗi thời.

## 1. Model nào đọc được tiếng Việt

| Model | Mã API | Tiếng Việt | Giới hạn ký tự mỗi lần tạo | Ghi chú |
| --- | --- | --- | --- | --- |
| Eleven v4 | `eleven_v4` | Có | 10.000 (~10 phút) | Mới nhất, có audio tag. Mặc định của skill |
| Eleven v4 Turbo | `eleven_v4_turbo` | Có | Không công bố | Độ trễ thấp, cũng nhận audio tag |
| Eleven v3 | `eleven_v3` | Có | 5.000 (~5 phút) | Ghi là "thế hệ trước", cùng cú pháp tag với v4 |
| Flash v2.5 | `eleven_flash_v2_5` | Có | 40.000 (~40 phút) | Không có audio tag, có `<break>` |
| Multilingual v2 | `eleven_multilingual_v2` | **Không** | 10.000 | 29 ngôn ngữ, không có `vi` |

Nguồn [chính thức]: [Models](https://elevenlabs.io/docs/overview/models), [Eleven v4](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4). Turbo v2.5 đã ngừng phát triển và được ElevenLabs coi là tương đương Flash v2.5.

- Nhiều hướng dẫn cũ khuyên dùng Multilingual v2 cho tiếng nước ngoài. Với tiếng Việt thì không được, vì model này không có tiếng Việt.
- [chính thức] v4 "có thể nghe khác hẳn v3", nên kịch bản đã chỉnh cho v3 cần nghe lại trên v4 ([Eleven v4](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4)).
- Chưa có tài liệu chính thức nào đánh giá chất lượng dấu thanh tiếng Việt của từng model. Trang v4 chỉ nói "một số ngôn ngữ được xử lý trôi chảy hơn những ngôn ngữ khác".
- Một kịch bản video ngắn 60–90 giây thường chỉ khoảng 800–1.500 ký tự, nằm gọn trong một lần tạo. YouTube dài thì chia khối theo chương.

## 2. Audio tag (v4, v4 Turbo, v3)

### Cú pháp

[chính thức] Audio tag là một chỉ dẫn ngắn bằng tiếng Anh, đặt trong **ngoặc vuông**, ngay trước đoạn cần đổi cách đọc. Ngoặc tròn hoặc ngoặc nhọn có thể làm tag bị đọc thành tiếng. v3 và v4 dùng chung tag ([Audio tags với v3 và v4](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-do-audio-tags-work-with-eleven-v3-and-v4), [Danh sách tag v4](https://elevenlabs.io/blog/elevenlabs-audio-tags-list)).

```text
[thoughtful] Hồi đó mình nghĩ, chắc chỉ là một buổi họp bình thường.
[softly] Nhưng hết buổi, sếp gọi mình lại.
```

### Danh sách tag chính thức của v4

Theo [blog danh sách tag v4](https://elevenlabs.io/blog/elevenlabs-audio-tags-list):

| Nhóm | Tag |
| --- | --- |
| Năng lượng cao | excited, playful, amazed, powerful, proud, optimistic, startled |
| Gay gắt | mad, aggressive, bitter, critical, repelled |
| Căng thẳng | anxious, stressed, scared, threatened, vulnerable, confused, busy |
| Năng lượng thấp | tired, bored, distant, despair, let down |
| Bình thản, suy ngẫm | peaceful, content, curious, thoughtful, trusting |
| Cách nói, âm lượng | whispers, shouts, softly, quietly, low threatening, hushed, barely audible, booming, disbelief |
| Nhịp | slowly, rushed, pause, drawn out, long pause, snappy, speedy |
| Phản ứng | laughs, sighs, gasps, clears throat, crying, starts crying, gulp |
| Giọng vùng, nhân vật | British accent, French accent, Australian accent, Irish accent, pirate voice |
| Hiệu ứng âm thanh | thunder rumbling, footsteps, door creaking, clapping, owl hooting, twig snapping, zipper opening, dog barking |

Trang [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices) còn liệt kê thêm (áp dụng cho cả v3): `[laughs harder]`, `[starts laughing]`, `[wheezing]`, `[exhales]`, `[sarcastic]`, `[snorts]`, `[mischievously]`.

### Tag tự viết và kết hợp

[chính thức] Danh sách là mở. Có thể tự viết tag mô tả cách nói, tình huống hoặc nhân vật, và gộp bằng dấu phẩy: `[whispering, fearful]`. Hướng dẫn chính thức: **một tag cho mỗi mệnh đề, thêm tag mới ở chỗ cảm xúc đổi**, bắt đầu từ tag có sẵn rồi thêm chi tiết.

Các tag như `[cheerful]`, `[serious]`, `[warm]` không có trong danh sách chính thức. Chúng dùng được như tag tự viết, nhưng chưa ai kiểm chứng với tiếng Việt. Trong `voicings.md`, tag tự viết được đánh dấu *(tự viết)*.

### Những điều cần nhớ khi dùng

- **Luôn dùng tag tiếng Anh.** Mọi ví dụ chính thức đều bằng tiếng Anh; không tài liệu nào nói `[thì thầm]` được hiểu. [chưa kiểm chứng] Tag tiếng Anh đi với chữ tiếng Việt có lẽ hoạt động vì tag ở mức model và v3/v4 có tiếng Việt, nhưng chưa có xác nhận chính thức. Đây là lý do bắt buộc nghe thử.
- **Tag hợp với giọng thì mới ăn.** [chính thức] "Một giọng nghiêm túc, chuyên nghiệp có thể không đáp ứng tốt với tag tinh nghịch như `[giggles]`", và tag ăn dễ hơn khi cách đọc đó đã có trong dữ liệu của giọng.
- **Tag có thể thành tiếng động.** [chính thức] Vì model cũng học hiệu ứng âm thanh, một tag đôi khi bị hiểu là yêu cầu tạo âm thanh. Tag mô tả rõ như `[low, gravelly voice]` giúp giảm lỗi này. Với lời đọc, tránh hẳn nhóm tag hiệu ứng âm thanh trừ khi người dùng muốn.
- **Không viết chỉ dẫn bằng lời.** [chính thức] Câu kiểu "cô nói đầy hào hứng" sẽ bị đọc thành tiếng.
- **Tag chưa hoàn hảo.** [chính thức] ElevenLabs tự nhận khả năng làm theo chỉ dẫn "chưa hoàn hảo", và khuyên tạo nhiều lần rồi chọn bản tốt nhất khi kết quả không đều.
- **Giọng clone và Voice Design.** [chính thức] Với v3, giọng clone chuyên nghiệp (PVC) "chưa được tối ưu hoàn toàn". Với v4, PVC được hỗ trợ đầy đủ (có thanh Clone Strength, nên bắt đầu ở 0%), còn giọng tạo bằng Voice Design "có thể không biểu cảm bằng".
- **Đoạn quá ngắn.** [chưa kiểm chứng] Hướng dẫn v3 năm 2025 từng nói đoạn dưới khoảng 250 ký tự cho kết quả thiếu ổn định. Không tìm lại được câu này trên trang hiện tại. Khi nghe thử, lấy đoạn 2–4 câu thay vì một câu lẻ.
- Không có con số chính thức về số tag tối đa mỗi lần tạo.

## 3. Khoảng nghỉ theo model

| Model | Cách tạo khoảng nghỉ | Không dùng |
| --- | --- | --- |
| v4, v4 Turbo, v3 | `[pause]`, `[long pause]`, dấu ba chấm `...`, gạch ngang `—`, xuống dòng, tách đoạn | `<break>` (không hỗ trợ SSML) |
| Flash v2.5 | `<break time="0.8s" />`, tối đa 3 giây; dấu câu | Audio tag |

Nguồn [chính thức]: [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices), [Eleven v4](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4).

- [chính thức] "Eleven v4 và Eleven v3 không hỗ trợ thẻ SSML break." Tài liệu không nói `<break>` trên v3/v4 bị bỏ qua hay bị đọc thành tiếng, nên không bao giờ đưa nó vào bản v3/v4.
- [chính thức] Dùng quá nhiều `<break>` trong một lần tạo có thể làm giọng mất ổn định: đọc nhanh lên hoặc có tiếng lạ. Không có con số tối đa. Skill dùng mức thưa, khoảng một break cho mỗi 2–3 câu là nhiều [kinh nghiệm, suy luận].
- [chính thức] Gạch ngang cho nghỉ ngắn, dấu ba chấm cho giọng ngập ngừng, nhưng hai cách này được mô tả là "kém nhất quán" hơn.
- [chưa kiểm chứng] `[short pause]` hay gặp trong tài liệu v3 năm 2025 nhưng không có trong danh sách v4. Dùng được như tag tự viết.

## 4. Nhấn mạnh

- [chính thức] Viết hoa làm tăng độ nhấn; dấu ba chấm thêm khoảng nghỉ và sức nặng; dấu câu thường tạo nhịp tự nhiên. Ví dụ chính thức: `It was a VERY long day [sigh] … nobody listens anymore.` Trên v4, "dấu câu ảnh hưởng đáng kể tới cách đọc".
- [chưa kiểm chứng] Viết hoa chữ có dấu ("RẤT", "KHÔNG") giữ nguyên dấu nên có lẽ dùng được, nhưng chưa ai thử có hệ thống. Tối đa một hai từ mỗi đoạn.
- Vì viết hoa mang nghĩa nhấn, từ viết tắt viết hoa (KPI, CEO) dễ bị đọc lẫn. Luôn chuẩn hoá từ viết tắt trước (xem `vietnamese-normalization.md`).
- Không có hướng dẫn chính thức về dấu ngoặc kép, in đậm, in nghiêng.

## 5. Cài đặt giọng

| Cài đặt | Điều đã kiểm chứng | Nguồn |
| --- | --- | --- |
| Speed | Mặc định 1.0, từ 0.7 đến 1.2, "giá trị cực đoan có thể ảnh hưởng chất lượng" | [chính thức] [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices) |
| v4: Style, Speed | **Không có** thanh Style và Speed trên v4. Nhịp trên v4 điều khiển bằng tag (`[slowly]`, `[rushed]`) và độ dài câu | [chính thức] [Eleven v4](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4) |
| v4: Stability | Thấp hơn = biểu cảm, đa dạng hơn; cao hơn = gần giọng gốc, đều hơn giữa các lần tạo | [chính thức] [Eleven v4](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4) |
| v3: chế độ Stability | Creative (biểu cảm nhất, dễ "ảo giác"), Natural (gần bản ghi gốc nhất), Robust (ổn định nhất nhưng ít nghe theo tag). Nên dùng Creative hoặc Natural khi cần tag | [chính thức nhưng từ trang cũ đã bị thay, có thể lỗi thời] |
| Stability, Similarity, Style dạng số (Flash) | [chưa kiểm chứng] Thường thấy dải 0–1 cho cả ba, cùng Speaker Boost bật/tắt. Không xác minh được trong lần nghiên cứu này | — |

Chưa rõ v4 có thanh Similarity hay Speaker Boost không. Khi đưa thông số cho người dùng, chỉ nêu những dòng đã kiểm chứng, phần còn lại ghi "chỉnh theo tai nghe".

Hướng chung theo giọng điệu [kinh nghiệm, suy luận từ mô tả chính thức]: giọng điệu cần biểu cảm (hào hứng, hài hước, hồi hộp, xúc động) dùng Stability thấp hơn trên v4 hoặc Creative/Natural trên v3; giọng điệu cần đều (nghiêm túc, kể chuyện dài) dùng Stability cao hơn hoặc Natural/Robust.

## 6. Từ điển phát âm (Pronunciation Dictionary)

- [chính thức] Từ điển dạng TXT hoặc .PLS, chỉ gồm hai loại quy tắc: **alias** (thay chữ bằng chữ khác) và **phoneme** (phiên âm IPA/CMU). Phân biệt hoa thường, quy tắc khớp đầu tiên được dùng. Dùng được trong Studio, Dubbing Studio và API ([Pronunciation dictionaries](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/pronunciation-dictionaries), [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)).
- [chính thức] **Alias dùng được với mọi model.** Ví dụ chính thức: `UN` → `United Nations`. Với tiếng Việt, alias là cách thực tế nhất: `KPI` → `kê pê i`, `deadline` → `đét lai`.
- [chính thức] Phoneme chỉ chạy trên `eleven_v4`, `eleven_v4_turbo`, `eleven_flash_v2` và `eleven_v3`. **IPA cho ngôn ngữ không phải tiếng Anh chỉ chạy trên v4 và v4 Turbo.**
- [chính thức] v4 đọc được IPA viết thẳng trong câu, đặt giữa hai dấu gạch chéo (`/ˌbaɪoʊˈkemɪstri/`), nên dùng chọn lọc và có dấu trọng âm. [chưa kiểm chứng] IPA tiếng Việt viết thẳng trong câu chưa ai thử.
- Nếu đã viết sẵn cách đọc ngay trong bản dán thì không cần từ điển. Từ điển có ích khi một từ lặp lại qua nhiều video (tên thương hiệu cá nhân, tên sản phẩm).

## 7. Chuẩn hoá văn bản và mã ngôn ngữ

- [chính thức] Chuẩn hoá văn bản bật mặc định cho mọi model nhưng chất lượng khác nhau. Ví dụ chính thức: "$1,000,000" được Multilingual v2 đọc đúng nhưng Flash v2.5 đọc thành "one thousand thousand dollars" ([Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)).
- [chính thức] ElevenLabs khuyên "viết số, từ viết tắt, ngày tháng và ký hiệu đầy đủ bằng chữ". Trên API, `language_code: "vi"` giúp bộ chuẩn hoá áp quy tắc tiếng Việt; `apply_text_normalization` nhận `on` / `off` / `auto` và làm tăng độ trễ. Số như "11" có thể bị đọc sai ngôn ngữ ([Vì sao số, ngày, ký hiệu đọc sai](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/why-are-numbers-dates-symbols-and-acronyms-not-properly-pronounced-or-spoken-in-the-correct-language)).
- Mọi ví dụ chuẩn hoá chính thức đều là tiếng Anh. Không có tài liệu nào cho thấy "1.800.000đ" hay "15/10" được đọc đúng kiểu Việt. Skill tự chuẩn hoá trước, không trông vào bộ chuẩn hoá của ElevenLabs.
- [chưa kiểm chứng] Từ tiếng Anh thông dụng trong câu tiếng Việt (podcast, deadline) có thể được giọng đa ngôn ngữ đọc đúng kiểu tiếng Anh. Mặc định giữ nguyên chữ gốc, ghi vào bảng cách đọc, và kiểm ở bước nghe thử; nếu sai thì đổi sang phiên âm kiểu Việt hoặc thêm alias.
