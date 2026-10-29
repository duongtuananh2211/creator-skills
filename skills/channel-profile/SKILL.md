---
name: channel-profile
description: Phỏng vấn để lập hồ sơ kênh nội dung mới, cả kênh người thật lẫn kênh faceless dùng nhân vật/mascot, gồm chọn niche và định vị (2–3 phương án kèm đánh đổi), chân dung khán giả, hồ sơ người dẫn hoặc character bible cho nhân vật, trụ cột nội dung, định dạng, nhịp đăng, giọng văn, quy tắc nội dung (kèm checklist cho chủ đề nhạy cảm như cờ bạc, tài chính, y tế), tra kênh cùng chủ đề trên web nếu người dùng đồng ý, rồi ghi `channel-profile.md` ở thư mục gốc dự án cho các skill story-* đọc. Cũng cập nhật hồ sơ đã có. Dùng khi người dùng nói "xây dựng profile kênh", "tạo hồ sơ kênh", "mới lập kênh", "khởi tạo dự án kênh", "chọn niche", "định vị kênh YouTube", "character bible cho nhân vật", "cập nhật hồ sơ kênh", "channel profile", "find my niche", hoặc kể về kênh sắp làm. Không dùng để viết kịch bản, hook, chấm bản nháp hay làm lời đọc (dùng `story-content-writer`, `story-hook-writer`, `story-content-review`, `story-voice-script`), audit số liệu analytics của kênh lớn đang chạy, hay thiết kế logo, hình ảnh.
---

# Channel profile

Skill này giúp người dùng đặt nền móng cho một kênh mới: kênh nói về gì, cho ai, ai dẫn, đăng gì và theo nhịp nào, và những gì kênh không làm. Kết quả là file `channel-profile.md` ở thư mục gốc dự án (thư mục mở Claude Code). Bốn skill `story-content-writer`, `story-hook-writer`, `story-content-review`, `story-voice-script` đọc file này trước mỗi lượt, nên hồ sơ càng cụ thể thì người dùng càng ít phải khai lại.

Người dùng có thể là creator kể chuyện của chính mình, hoặc một kênh faceless dùng nhân vật đại diện (ví dụ một con vật hoạt hình giải thích vì sao người ta nghiện cờ bạc). Hai kiểu kênh cần những câu hỏi khác nhau ở phần người dẫn, còn phần niche, khán giả, trụ cột thì dùng chung.

Hồ sơ là thứ các skill khác tin là đúng, nên mọi thứ ghi vào đó phải đến từ người dùng, từ nguồn đã kiểm chứng, hoặc được ghi rõ là đề xuất. Chỗ nào chưa biết thì ghi "Chưa xác định". Một ô để trống trung thực có ích hơn một ô điền cho đủ, vì chỗ điền bừa sẽ bị các skill sau dùng như sự thật. Riêng kênh đối thủ và số liệu thì không được bịa: không tìm thấy thì nói là không tìm thấy.

## Đọc reference nào, khi nào

Các file nằm cạnh SKILL.md này. Chỉ đọc file cần cho bước đang làm:

| Khi nào | Đọc file |
| --- | --- |
| Vòng (b), chọn niche và viết câu định vị | `references/niche-positioning.md` |
| Vòng (c), khán giả | `references/audience.md` |
| Vòng (d), người dẫn hoặc nhân vật, giọng đọc AI, chính sách nội dung AI | `references/host-persona.md` |
| Vòng (e), trụ cột, series, nhịp đăng, mục tiêu và chỉ số | `references/pillars-formats.md` |
| Người dùng đồng ý tra đối thủ trên web | `references/competitor-research.md` |
| Niche đụng tới cờ bạc, sức khoẻ tinh thần, nghiện, tài chính, y tế | `references/sensitive-niches.md` |
| Bước soạn hồ sơ (luôn luôn) | `assets/channel-profile-template.md` |

Thông tin chính sách và pháp lý trong references được nghiên cứu ngày 29/10/2026. Trang trợ giúp của YouTube và văn bản pháp luật đều thay đổi, nên khi người dùng thấy khác thì tin vào văn bản hiện hành họ đang đọc.

## Bước 0. Tạo mới hay cập nhật

Kiểm tra `channel-profile.md` ở thư mục làm việc hiện tại. Nếu thư mục đó trông không giống một dự án (ví dụ thư mục home), hỏi người dùng muốn đặt hồ sơ ở đâu trước khi ghi, vì các skill khác chỉ tìm ở thư mục gốc dự án.

- **Đã có file** → chế độ cập nhật (xem phần cuối).
- **Chưa có** → chế độ tạo mới, làm từ bước 1.

## Bước 1. Bắt đầu từ điều người dùng đã nói

Người dùng thường mở đầu bằng một câu như "kênh YouTube, nhân vật Xa hình con rắn, giải thích các vấn đề cuộc sống như vì sao nghiện cờ bạc". Câu đó đã trả lời được nền tảng, kiểu kênh (nhân vật đại diện), tên và hình dạng nhân vật, loại nội dung (giải thích) và một chủ đề mẫu. Rút hết những gì đã có, tóm lại trong 3–5 dòng ("Mình hiểu thế này: …"), rồi chỉ hỏi phần còn thiếu. Hỏi lại điều người dùng vừa nói làm họ thấy mình không được nghe.

## Bước 2. Phỏng vấn theo vòng ngắn

Chia thành các vòng, mỗi vòng 2–4 câu, xong vòng này mới sang vòng sau. Câu có lựa chọn rõ (nền tảng, người thật hay nhân vật, vùng giọng) thì dùng AskUserQuestion; câu cần người dùng tự kể (vì sao làm kênh, khán giả là ai) thì hỏi bằng lời thường. Một danh sách 30 câu hỏi một lúc khiến người dùng trả lời qua loa hoặc bỏ dở.

Mỗi vòng, nếu đã đủ dữ kiện để đề xuất thì đề xuất luôn cho người dùng sửa, thay vì hỏi trống. Người dùng trả lời "chưa biết" thì ghi "Chưa xác định" và đi tiếp. Nếu họ muốn làm nhanh, gộp còn vòng (a), (b), (d) rồi soạn hồ sơ với các mục còn lại đánh dấu "Chưa xác định" hoặc "Đề xuất, chưa xác nhận".

**(a) Cơ bản.** Ai làm kênh (một người, nhóm), vì sao làm, nền tảng chính và phụ, thời gian và nguồn lực mỗi tuần (quay, dựng, vẽ, công cụ AI), người thật xuất hiện hay nhân vật đại diện, kênh đã có video nào chưa.

**(b) Niche và định vị.** Đọc `references/niche-positioning.md`. Hỏi theo bộ câu trong đó: người dùng giỏi gì, có thể nói về gì suốt 100 video, người xem cụ thể là ai, hôm nay họ đang xem gì thay cho kênh này, kênh làm được gì mà các lựa chọn đó không làm. Sau đó, trước khi đề xuất phương án, hỏi có muốn tra đối thủ trên web không (bước 3). Rồi đưa 2–3 phương án niche và định vị, mỗi phương án có câu định vị, cái được, cái mất, và nêu một khuyến nghị kèm lý do. Người dùng chọn hoặc trộn.

**(c) Khán giả.** Đọc `references/audience.md`. Chốt 1–2 chân dung và khoảng 10 câu hỏi của người xem bằng chính lời họ.

**(d) Người dẫn hoặc nhân vật.** Đọc `references/host-persona.md`. Người thật thì hỏi vai trò với người xem, điều gì làm nên uy tín, ranh giới riêng tư. Nhân vật thì đi qua character bible: tính cách, giá trị, xưng hô, vùng giọng, câu cửa miệng, danh sách những điều nhân vật không bao giờ làm, nhận diện hình ảnh. Hỏi giọng đọc: tự đọc, người lồng tiếng hay giọng AI (công cụ, model, tên giọng, cài đặt).

**(e) Trụ cột và định dạng.** Đọc `references/pillars-formats.md`. Đề xuất 3–5 trụ cột từ niche và câu hỏi của người xem, mỗi trụ cột vài ý tưởng video. Với mỗi series lặp lại, ghi rõ "mỗi tập thay đổi gì". Giải thích ngắn cho người dùng lý do: chính sách kiếm tiền của YouTube (đổi tên thành "inauthentic content" từ 15/7/2025) không cho phép "videos where characters are put in the same situation over and over again with the same outcome" (nhân vật bị đặt vào cùng một tình huống lặp đi lặp lại với cùng một kết cục), nhưng vẫn cho phép intro, outro giống nhau nếu phần lớn nội dung khác nhau ([YouTube Help 1311392](https://support.google.com/youtube/answer/1311392)). Kênh nhân vật có khung cố định dễ rơi vào vùng này nhất. Cũng trong vòng này, hỏi nhịp đăng giữ được trong khoảng 6 tháng và mục tiêu 90 ngày.

**(f) Giọng văn và quy tắc nội dung.** Mức trang trọng, từ hay dùng, từ cấm, tiểu từ nói. Xin 2–3 câu người dùng thấy "đúng giọng" (hoặc mình viết thử để họ chọn). Quy tắc về nguồn và ví dụ giả định. Nếu niche nhạy cảm, đọc `references/sensitive-niches.md` và đi qua checklist cùng người dùng.

## Bước 3. Tra đối thủ trên web (tuỳ chọn)

Hỏi trước, vì bước này tốn thêm vài phút và nhiều lượt tìm kiếm: "Bạn muốn mình tìm thử các kênh cùng chủ đề trên YouTube/TikTok (tiếng Việt và nước ngoài) để thấy khoảng trống không?". Chỉ làm khi người dùng đồng ý. Đọc `references/competitor-research.md` rồi làm theo.

Khi tra, nói rõ giới hạn: tìm kiếm web không thấy được tỉ lệ giữ chân, CTR, nguồn lượt xem hay doanh thu của kênh khác; số người đăng ký và lượt xem là ước lượng, có thể đã cũ. Ghi ngày kiểm tra. Chỉ đưa vào bảng những kênh đã mở được trang thật; không tìm thấy kênh nào thì ghi đúng như vậy. Gợi ý người dùng tự xem thẻ Trends (Xu hướng) trong YouTube Studio, gồm "Content gaps" (khoảng trống nội dung, YouTube định nghĩa là lúc người xem không tìm được đủ kết quả chất lượng cho một lượt tìm kiếm) khi kênh đã có khán giả.

Nếu người dùng không muốn tra, mục 9 ghi "Chưa kiểm chứng" và các phương án định vị chỉ dựa trên phỏng vấn; nói rõ điều đó khi đề xuất.

## Bước 4. Chủ đề nhạy cảm và chính sách nội dung AI

Hai việc này cần làm trước khi soạn hồ sơ, vì chúng quyết định mục 4 và mục 8:

- **Niche nhạy cảm** (cờ bạc, nghiện, sức khoẻ tinh thần, tự hại, tài chính, đầu tư, y tế): dùng checklist trong `references/sensitive-niches.md`. Với cờ bạc, phần pháp lý Việt Nam có số liệu mâu thuẫn giữa các nguồn và luật sửa đổi 2025 mới chỉ đọc được qua trích đoạn, nên ghi vào hồ sơ là "cần kiểm tra lại văn bản hiện hành", không trình bày như kết luận. Không ghi số đường dây nóng nào chưa được kiểm chứng; để chỗ trống `[cần bổ sung: nguồn hỗ trợ đã kiểm chứng]`.
- **Kênh nhân vật hoặc dùng AI**: theo trang công khai nội dung thay đổi hoặc tổng hợp của YouTube ([Help 14328491](https://support.google.com/youtube/answer/14328491)), nội dung hoạt hình hoặc rõ ràng không thật không cần nhãn; dùng AI để lên ý tưởng, viết kịch bản, làm thumbnail, hay nhân bản giọng của chính mình để lồng tiếng cũng không cần nhãn. Cần nhãn khi nội dung trông như thật và khiến người thật nói hoặc làm điều họ không làm, sửa cảnh sự kiện thật, hay dựng cảnh thật chưa từng xảy ra. Chi tiết trong `references/host-persona.md`.

## Bước 5. Soạn, xác nhận, ghi file

1. Đọc `assets/channel-profile-template.md`. Giữ nguyên mười tiêu đề đánh số và thứ tự của chúng, kể cả khi một mục chỉ có "Chưa xác định", vì các skill khác tìm thông tin theo số mục ("mục 3", "mục 4"…). Thay các dòng hướng dẫn dưới mỗi tiêu đề bằng nội dung thật, viết ngắn, dạng gạch đầu dòng hoặc bảng.
2. Mục 1 phải có câu định vị theo công thức: "Kênh <tên> giúp <khán giả> <hiểu/làm được gì> bằng <cách/góc riêng>, khác <lựa chọn thay thế> ở chỗ <điểm khác>." Mỗi chỗ trống phải cụ thể; câu nào thay tên kênh khác vào vẫn đúng thì chưa phải định vị.
3. Ở mục 4, nếu dùng giọng AI, ghi đủ công cụ, model, tên giọng, cài đặt, giọng điệu mặc định, và một "Bảng cách đọc" (từ gốc → cách đọc) cho tên nhân vật, thuật ngữ lặp lại. `story-voice-script` dùng thẳng bảng này.
4. Ghi ngày hôm nay (YYYY-MM-DD) ở dòng "Cập nhật lần cuối" và dòng đầu "Nhật ký thay đổi". Điều gì là đề xuất của mình mà người dùng chưa xác nhận thì ghi kèm "(đề xuất)".
5. Trình bày trong chat. Nếu hồ sơ ngắn, đưa toàn văn. Nếu dài, đưa tóm tắt các quyết định chính (câu định vị, niche và phạm vi, khán giả, người dẫn/nhân vật, trụ cột, nhịp đăng, quy tắc quan trọng, các mục còn "Chưa xác định") rồi hỏi người dùng muốn sửa gì. Sửa theo phản hồi.
6. Khi người dùng đồng ý, dùng Write ghi `channel-profile.md` vào thư mục gốc dự án.

Sau khi ghi, báo cho người dùng:

- Đường dẫn file, và rằng bốn skill story-* (nếu đã cài) sẽ tự đọc file này, nên không cần khai lại kênh mỗi lần.
- Các mục còn "Chưa xác định" và khi nào nên quay lại điền (ví dụ sau 10 video đầu, khi đã có số liệu trong Studio).
- Bước tiếp theo gợi ý: dùng `story-hook-writer` để nghĩ tiêu đề và thumbnail cho vài video đầu, `story-content-writer` để viết kịch bản đầu tiên, `story-voice-script` nếu kênh dùng giọng AI.

## Chế độ cập nhật

Khi `channel-profile.md` đã có:

1. Đọc toàn bộ file. Tóm tắt cho người dùng trong 2–3 dòng (câu định vị, ngày cập nhật lần cuối) để hai bên cùng nhìn một bản.
2. Hỏi điều gì đã thay đổi. Nếu người dùng đã nói rõ (ví dụ "đổi giọng AI sang Vbee"), làm luôn. Nếu chưa, hỏi bằng AskUserQuestion với các nhóm: định vị và niche; khán giả; người dẫn, nhân vật, giọng đọc; trụ cột, định dạng, nhịp đăng (người dùng có thể chọn "khác" cho giọng văn, quy tắc, đối thủ, mục tiêu).
3. Phỏng vấn lại chỉ phần đã đổi, dùng reference tương ứng như ở chế độ tạo mới.
4. Dùng Edit sửa đúng những mục đó; giữ nguyên chữ của các mục khác, kể cả cách người dùng tự viết. Cập nhật ngày ở dòng "Cập nhật lần cuối" và thêm một dòng cuối "Nhật ký thay đổi": `- <YYYY-MM-DD>: <đổi gì, ở mục nào>`.
5. Nếu thay đổi kéo theo mục khác (đổi niche thường làm lệch khán giả, trụ cột, đối thủ), chỉ ra các mục có thể đã cũ và hỏi có sửa luôn không, thay vì tự viết lại.
6. Nếu file thiếu một số tiêu đề đánh số của template (ví dụ người dùng tự viết tay), thêm các tiêu đề còn thiếu đúng vị trí với nội dung "Chưa xác định" và báo cho người dùng, vì các skill khác dựa vào số mục.

Người dùng muốn tra lại đối thủ thì làm lại bước 3 và thay bảng ở mục 9 bằng bảng mới có ngày kiểm tra mới, ghi vào nhật ký.

## Nguyên tắc xuyên suốt

- **Đề xuất được, quyết thay thì không.** Mình đưa phương án và lý do; người dùng chọn. Hồ sơ phản ánh lựa chọn của họ.
- **Phân biệt mức bằng chứng khi giải thích.** "YouTube công bố" khác "người làm nghề hay khuyên" và khác "mình suy luận". Các con số kiểu "đăng 3 video/tuần mới lên" là kinh nghiệm truyền miệng; chưa tìm thấy bằng chứng chính thức nào cho thấy một tần suất cụ thể được thưởng.
- **Không bịa chất liệu cá nhân.** Với kênh người thật, không tự thêm trải nghiệm, bằng cấp hay thành tích mà người dùng chưa nói. Với nhân vật, phần tiểu sử là sáng tác nên được đề xuất, nhưng ghi rõ là đề xuất.
- **Giữ hồ sơ gọn.** Đây là tài liệu tra cứu cho người và cho skill khác đọc mỗi lượt, không phải bài luận. Mỗi mục nên đọc xong trong nửa phút.
