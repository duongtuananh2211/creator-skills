---
name: story-voice-script
description: Chuyển một kịch bản video đã viết xong (video ngắn TikTok/Reels/Shorts hoặc YouTube dài, từ `story-content-writer` hay tự viết) thành lời đọc dán thẳng vào ElevenLabs hoặc Vbee, theo giọng điệu người dùng chọn cho cả bài hoặc từng đoạn (vui vẻ, hào hứng, thủ thỉ, trầm lắng, kể chuyện, hồi hộp, nghiêm túc, hài hước, hoặc tự mô tả). Skill viết lại câu cho hợp miệng đọc mà không đổi nội dung, chuẩn hoá số, ngày giờ, tiền, từ viết tắt và từ tiếng Anh cho TTS tiếng Việt, gắn audio tag và khoảng nghỉ đúng cú pháp từng công cụ, chia khối theo giới hạn ký tự, kèm bảng cách đọc và cài đặt gợi ý. Dùng khi người dùng nói "chuyển kịch bản thành voice script", "làm lời đọc cho ElevenLabs", "đọc bằng Vbee", "voice-over giọng vui vẻ", "thêm cảm xúc cho giọng AI", "TTS script", "voiceover script". Không dùng để viết kịch bản từ ý tưởng (dùng `story-content-writer`), tạo file âm thanh qua API hay tự động hoá, hoặc cho công cụ TTS khác trừ khi người dùng yêu cầu (khi đó chỉ đưa bản dựa trên dấu câu).
---

# Story voice script

Skill này nhận một kịch bản video đã xong và trả về lời đọc để người dùng dán vào ElevenLabs hoặc Vbee, đọc theo giọng điệu họ chọn. Người dùng là creator thương hiệu cá nhân kể chuyện của chính mình, nên việc của skill là đổi **hình thức** cho hợp tai nghe (câu ngắn hơn, nhịp rõ hơn, số viết thành chữ, chỗ nghỉ đúng chỗ) chứ không đổi **nội dung**. Giọng AI đọc một chi tiết bịa nghe vẫn rất thật, và chính điều đó làm nó nguy hiểm cho người kể.

Một điều cần nói rõ với người dùng ngay từ đầu: chưa có tài liệu chính thức nào xác nhận audio tag của ElevenLabs hoạt động tốt với chữ tiếng Việt, và Vbee không có tag cảm xúc. Vì vậy mọi bản dán ra đều đi kèm bước nghe thử một đoạn ngắn trước khi tạo cả bài.

## Đọc reference nào, khi nào

Các file trong `references/` nằm cạnh file SKILL.md này. Chỉ đọc file cần cho lượt hiện tại:

| Khi nào | Đọc file |
| --- | --- |
| Bước 3, viết lại theo giọng điệu (mọi công cụ) | `references/voicings.md`, chỉ phần của giọng điệu đã chọn |
| Bước 4, chuẩn hoá số, từ viết tắt, tiếng Anh | `references/vietnamese-normalization.md` |
| Công cụ là ElevenLabs | `references/elevenlabs.md` |
| Công cụ là Vbee | `references/vbee.md` |

Thông tin về công cụ được nghiên cứu ngày 29/10/2026. Hai hãng đổi tính năng thường xuyên (ElevenLabs vừa ra v4 cuối tháng 9/2026), nên khi người dùng thấy giao diện khác mô tả, tin vào thứ họ đang thấy và điều chỉnh theo.

## Hồ sơ kênh (nếu có)

Trước bước 1, kiểm tra file `channel-profile.md` ở thư mục gốc dự án (thư mục mở Claude Code). File này do skill `channel-profile` tạo và là nguồn đúng nhất về kênh của người dùng. Nếu có, đọc nó trước và dùng như sau:

- **Người dẫn / nhân vật đại diện** (mục 4): giọng đọc AI đã chọn cho kênh (công cụ, model, tên giọng, cài đặt) và giọng điệu mặc định. Dùng làm mặc định thay vì hỏi.
- **Giọng văn** (mục 7): xưng hô, tiểu từ nói hay dùng, từ cần tránh.
- **Bảng cách đọc** trong hồ sơ, nếu có: áp dụng luôn và chỉ bổ sung từ mới vào bảng của lượt này.

Những gì hồ sơ đã trả lời thì đừng hỏi lại. Nếu yêu cầu của người dùng trong lượt này khác hồ sơ (ví dụ đổi xưng hô cho một video), làm theo yêu cầu hiện tại và nhắc một dòng rằng nó khác hồ sơ. Nếu không có file, làm như bình thường; có thể nhắc một lần rằng `channel-profile` (nếu đã cài) giúp các lần sau không phải khai lại.

## Quy trình

### 1. Gom đầu vào

Cần các thứ sau:

1. **Kịch bản**: thường là bảng `Thời gian | Lời thoại | Hình ảnh / chữ trên màn hình | Âm tiết` của `story-content-writer`, hoặc kịch bản/dàn ý YouTube, hoặc đoạn văn người dùng tự viết.
2. **Công cụ**: ElevenLabs hay Vbee.
3. **Model ElevenLabs**: Eleven v4, Eleven v3 hay Flash v2.5. Model quyết định cú pháp khoảng nghỉ (v3/v4 dùng tag, Flash dùng `<break>`). Người dùng không biết thì mặc định v4 và ghi giả định một dòng. Nếu họ đang dùng Multilingual v2, báo rằng model này không hỗ trợ tiếng Việt theo tài liệu chính thức và đề nghị đổi sang v4.
4. **Giọng điệu**: một cho cả bài, hoặc khác nhau theo đoạn (ví dụ mở đầu hồi hộp, giữa tâm sự, kết vui vẻ). Tám mẫu có sẵn: vui vẻ; hào hứng / năng lượng; thủ thỉ / tâm sự; trầm lắng / xúc động; kể chuyện (người dẫn); hồi hộp / bí ẩn; nghiêm túc / chuyên gia; hài hước. Nếu người dùng tự mô tả ("ấm mà hơi tinh nghịch"), quy về một hoặc hai mẫu gần nhất và nói rõ đã quy về mẫu nào.
5. **Với Vbee**: vùng miền và giới tính giọng nếu đã chọn (ảnh hưởng cách đọc số như "linh/lẻ", "nghìn/ngàn").
6. **Thời lượng mục tiêu**: lấy từ cột thời gian của kịch bản nếu có.

Nếu thiếu công cụ hoặc giọng điệu, hỏi một lần bằng AskUserQuestion, có danh sách lựa chọn (công cụ: ElevenLabs / Vbee; giọng điệu: tám mẫu, cho chọn nhiều). Những thứ còn lại tự suy ra rồi nêu giả định trong một dòng.

Nếu kịch bản còn chỗ trống `[cần bổ sung: …]`, dừng lại hỏi người dùng điền trước. Chỗ trống đó mà lọt vào bản dán sẽ bị đọc thành tiếng, còn trên ElevenLabs thì ngoặc vuông còn bị hiểu thành một chỉ dẫn giọng.

### 2. Tách phần được đọc

Chỉ giữ lời thoại. Bỏ cột hình ảnh, dòng `CHỮ:`, ghi chú `[B-roll]`, emoji, hashtag, link, @tên tài khoản và mọi chỉ dẫn quay. Giữ cột thời gian cho bản duyệt để người dùng khớp lời với hình khi dựng. Kịch bản YouTube dài thì tách theo chương; mỗi chương thường thành một khối riêng.

### 3. Viết lại cho miệng đọc theo giọng điệu

Đọc `references/voicings.md`, phần của giọng điệu đã chọn. Mỗi giọng điệu có cách chỉnh riêng về độ dài câu, nhịp và chọn từ. Nguyên tắc chung:

- **Đổi hình thức, không đổi sự thật.** Được: tách câu dài, đảo trật tự trong một câu cho thuận miệng, đổi từ viết sang từ nói ("tuy nhiên" → "nhưng"), thêm dấu câu để tạo nhịp. Không được: thêm sự kiện, con số, cảm xúc, lời thoại hay câu mới mà kịch bản không có, kể cả một câu cảm thán cho "có cảm xúc". Cảm xúc phải đến từ cách đọc, không từ chữ mới.
- **Tag và cảm xúc phải khớp với chữ đã có.** Tag phản ứng như `[sighs]`, `[laughs]`, `[crying]` tạo ra âm thanh thật, tức là thêm một cảm xúc vào câu chuyện. Chỉ dùng khi kịch bản đã nói rõ cảm xúc đó ở chỗ đó.
- **Tiểu từ nói (nha, nè, à, nhé) dùng ít.** Chỉ khi giọng điệu hợp và cách người dùng tự viết cũng có kiểu đó. Giọng nghiêm túc hay trầm lắng gần như không cần.
- **Giữ xưng hô và từ quen của người dùng.** "Mình" vẫn là "mình", từ địa phương vẫn giữ.

Khi viết lại làm thay đổi đáng kể một câu (gộp hai câu, đảo ý), đánh dấu câu đó trong bản duyệt để người dùng kiểm.

### 4. Chuẩn hoá tiếng Việt cho TTS

Đọc `references/vietnamese-normalization.md`. Cả hai hãng đều khuyên viết số, ngày, ký hiệu, từ viết tắt thành chữ, và bộ chuẩn hoá tự động của cả hai đều chưa có tài liệu nào cho thấy đọc đúng kiểu viết tiếng Việt. Vì vậy tự chuẩn hoá trước: số, tiền, phần trăm, ngày, giờ, khoảng, số thứ tự, đơn vị, số điện thoại, từ viết tắt, từ tiếng Anh. Cách đọc số theo vùng của giọng ("một trăm linh năm" giọng Bắc, "một trăm lẻ năm" giọng Nam).

Gom mọi từ đã đổi cách viết vào **Bảng cách đọc**: từ gốc → cách đọc đã dùng → gợi ý thêm vào Pronunciation Dictionary (ElevenLabs, dạng alias) hoặc "Cách đọc" (Vbee). Bảng này có ích khi từ đó lặp lại ở các video sau.

### 5. Gắn markup theo công cụ

Đọc reference của công cụ. Tóm tắt:

**ElevenLabs v4 / v3**
- Audio tag là chỉ dẫn tiếng Anh trong ngoặc vuông, đặt ngay trước cụm từ đổi cảm xúc. Một tag cho mỗi chỗ đổi cảm xúc, không gắn vào mọi câu. Luôn dùng tag tiếng Anh; chưa có tài liệu nào nói tag tiếng Việt được hiểu.
- Khoảng nghỉ: `[pause]`, `[long pause]`, dấu ba chấm, gạch ngang, xuống dòng. v3/v4 không hỗ trợ `<break>`.
- Nhấn: VIẾT HOA một hai từ mỗi đoạn là nhiều. Hiệu quả với chữ có dấu chưa được kiểm chứng.
- Không viết chỉ dẫn bằng lời ("cô ấy nói đầy hào hứng") hay dùng ngoặc tròn, ngoặc nhọn: chúng sẽ bị đọc thành tiếng.

**ElevenLabs Flash v2.5**
- Không dùng audio tag. Khoảng nghỉ bằng `<break time="0.8s" />`, tối đa 3 giây, dùng thưa vì quá nhiều break làm giọng mất ổn định. Giọng điệu dựa vào dấu câu và nhịp câu.

**Vbee**
- Không có tag cảm xúc. Giọng điệu đến từ chọn giọng (giọng "nhấn nhá" cho đoạn cần biểu cảm), tốc độ, mức nhấn `emphasisIntensity` (với giọng có hỗ trợ), khoảng nghỉ và dấu câu.
- Bản dán **không chứa bất kỳ ký hiệu nào** ngoài chữ và dấu câu thường. Khoảng nghỉ thủ công ghi dạng `[nghỉ 1s]` **chỉ trong bản duyệt**; người dùng tự chèn bằng "Thêm khoảng nghỉ" trong studio tại đúng chỗ đó.

**Công cụ khác** (chỉ khi người dùng yêu cầu): bản thuần chữ đã chuẩn hoá, giọng điệu chỉ bằng dấu câu và nhịp câu, không tag, không `<break>`.

### 6. Kiểm tra trước khi đưa

1. **Thời lượng**: đếm âm tiết sau khi chuẩn hoá (số viết thành chữ làm tăng âm tiết). Ước tính khoảng 4,5–5,5 âm tiết/giây ở tốc độ thường, nhân với hệ số tốc độ nếu đổi speed. Đây chỉ là ước tính; tốc độ thật của từng giọng AI cần đo ở bước nghe thử. Nếu dư nhiều so với thời lượng, đừng tự cắt nội dung: đề xuất câu nào có thể bỏ hoặc tăng tốc độ, để người dùng quyết.
2. **Giới hạn ký tự**: ElevenLabs v4 tối đa 10.000 ký tự mỗi lần tạo, v3 5.000, Flash v2.5 40.000. Vbee: giữ mỗi khối dưới khoảng 1.000 ký tự. Vượt thì chia khối, cắt ở chỗ hết đoạn, đánh số `Khối 1/3`. Nhãn khối nằm ngoài code block.
3. **Soát ký tự lạ trong bản dán**: không còn `( ) { } * # _ / & % @`, emoji, chữ số, chữ viết tắt chưa chuẩn hoá, nhãn `CHỮ:`, `[cần bổ sung…]`. Ngoặc vuông chỉ được có ở ElevenLabs v3/v4 và chỉ chứa tag tiếng Anh hợp lệ; `<break time="…" />` chỉ được có ở Flash v2.5. Bản Vbee không có ngoặc vuông nào.
4. **Trung thực**: so từng câu bản dán với kịch bản gốc. Câu nào chứa thông tin mới thì bỏ.

### 7. Trình bày

Trình bày trong chat theo thứ tự này:

````
**Giả định:** <công cụ, model, giọng điệu theo đoạn, tốc độ đọc ước tính…>

**Cài đặt**
- Công cụ / model: …
- Giọng gợi ý: <đặc tính cần tìm; với Vbee nêu vùng miền, giới tính, giọng nhấn nhá nếu hợp>
- Thông số: <ElevenLabs: Stability hoặc chế độ v3, Speed nếu model có; Vbee: tốc độ, emphasisIntensity, độ dài khoảng nghỉ>

**Bản duyệt** (để người đọc, không dán)
| Thời gian | Lời đọc | Giọng điệu / ghi chú | Âm tiết |
Tổng âm tiết: … ≈ … giây ở tốc độ … (mục tiêu …)

**Bản dán vào <ElevenLabs v4 | Vbee | …>**
Khối 1/n
```text
<lời đọc sạch, sẵn để dán>
```

**Bảng cách đọc**
| Từ gốc | Cách đọc đã dùng | Thêm vào từ điển của công cụ |

**Nghe thử trước**
- [ ] Tạo thử một đoạn 2–4 câu có tag và có số trước khi tạo cả bài
- [ ] Tag và ký hiệu không bị đọc thành tiếng
- [ ] Dấu thanh đúng, không mất dấu
- [ ] Số, ngày giờ, tiền đọc đúng
- [ ] Từ tiếng Anh, từ viết tắt, tên riêng đọc đúng (Vbee: chạy thêm "Kiểm tra cách đọc" sau khi dán)
- [ ] Bấm giờ đoạn thử để chỉnh lại ước tính thời lượng
````

Thông số trong khối Cài đặt chỉ đưa những gì reference có cơ sở. Khi một con số là kinh nghiệm chưa kiểm chứng, ghi rõ "điểm bắt đầu, chỉnh theo tai nghe". Cuối cùng, đề nghị lưu ra file cạnh kịch bản gốc (ví dụ `<tên-kịch-bản>.voice-vbee.md`) nếu người dùng muốn.

## Khi người dùng phản hồi

- **"Tag bị đọc thành tiếng" / "nghe ra tiếng động lạ"**: bỏ tag đó hoặc thay bằng tag mô tả cách nói rõ hơn; tag có thể bị hiểu thành yêu cầu hiệu ứng âm thanh. Nếu vẫn lỗi, chuyển đoạn đó sang chỉ dùng dấu câu.
- **"Nghe đều đều, chưa có cảm xúc"**: ElevenLabs thì hạ Stability, thêm tag ở chỗ đổi cảm xúc, tạo lại vài lần rồi chọn bản tốt nhất. Vbee thì thử giọng nhấn nhá, tăng `emphasisIntensity`, tách câu ngắn hơn. Không thêm chữ cảm thán mới.
- **"Dài quá"**: tăng tốc độ trong giới hạn hoặc đề xuất câu bỏ được, để người dùng chọn.
- **"Đọc sai từ X"**: đổi cách viết trong bản dán và thêm dòng vào bảng cách đọc.
- **Muốn sửa nội dung kịch bản**: đó là việc của `story-content-writer` hoặc `story-content-review` (nếu đã cài). Sửa xong thì chuyển lại thành lời đọc.
