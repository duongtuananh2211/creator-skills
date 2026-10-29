---
name: story-content-writer
description: Viết nội dung kể chuyện cho creator thương hiệu cá nhân từ một ý tưởng hoặc khoảnh khắc có thật, thành kịch bản video ngắn (TikTok, Reels, Shorts), kịch bản/outline YouTube dài, bài viết chữ (Facebook, Threads, LinkedIn, X) hoặc carousel. Skill kiểm tra chất liệu câu chuyện và hỏi lại thay vì bịa, chọn cấu trúc hợp định dạng rồi viết bản dùng được ngay. Dùng khi người dùng nói "viết kịch bản TikTok từ chuyện này", "biến trải nghiệm này thành bài Facebook", "kể chuyện mình nghỉ việc thành video", "lên kịch bản YouTube về hành trình của mình", "làm carousel kể chuyện", "turn this story into a Reels script", "write a LinkedIn story post", kể cả khi họ chỉ kể một chuyện rồi hỏi "đăng cái này lên thế nào". Không dùng để chỉ sinh nhiều phương án hook/tiêu đề/thumbnail (dùng `story-hook-writer`), chấm điểm hay góp ý bản nháp có sẵn (dùng `story-content-review`), quảng cáo doanh nghiệp hay truyện hư cấu.
---

# Story content writer

Skill này biến chuyện thật của người dùng (một trải nghiệm, một bài học, một đoạn hành trình, một góc hậu trường) thành một nội dung đăng được ngay. Người dùng là creator xây thương hiệu cá nhân, nên tài sản lớn nhất của họ là sự thật trong câu chuyện. Một câu chuyện bịa có thể hay hơn trên giấy, nhưng khi lộ ra nó phá đúng thứ khiến người xem tin họ. Vì vậy mọi quyết định trong skill này ưu tiên chất liệu thật hơn văn hay.

## Đọc reference nào, khi nào

Các file trong `references/` nằm cạnh file SKILL.md này. Chỉ đọc file cần cho lượt viết hiện tại:

| Khi nào | Đọc file |
| --- | --- |
| Bước 3, chọn cấu trúc (mọi định dạng) | `references/frameworks.md` |
| Định dạng là video ngắn (TikTok, Reels, Shorts) | `references/short-video.md` |
| Định dạng là video YouTube dài (khoảng 8–30 phút) | `references/youtube-long.md` |
| Định dạng là bài viết dạng chữ (Facebook, Threads, LinkedIn, X) | `references/text-post.md` |
| Định dạng là carousel (Instagram, LinkedIn, TikTok photo mode, album Facebook) | `references/carousel.md` |

Khi người dùng muốn chuyển một câu chuyện sang định dạng khác, đọc file của định dạng mới và viết lại theo khuôn của nó. Chép nguyên văn từ định dạng này sang định dạng kia hầu như luôn hỏng nhịp.

## Hồ sơ kênh (nếu có)

Trước bước 1, kiểm tra file `channel-profile.md` ở thư mục gốc dự án (thư mục mở Claude Code). File này do skill `channel-profile` tạo và là nguồn đúng nhất về kênh của người dùng. Nếu có, đọc nó trước và dùng như sau:

- **Khán giả** (mục 3) và **trụ cột nội dung** (mục 5): dùng để chọn góc kể và bài học hợp người xem.
- **Người dẫn / nhân vật đại diện** (mục 4) và **giọng văn** (mục 7): xưng hô, tính cách, câu cửa miệng, những điều người dẫn không bao giờ nói.
- **Định dạng** (mục 6): độ dài mặc định, khung kịch bản cố định của kênh nếu có.
- **Quy tắc nội dung** (mục 8): quy tắc về nguồn, ví dụ giả định, chủ đề nhạy cảm. Quy tắc này cộng thêm vào nguyên tắc không bịa của skill, không thay thế nó.

Những gì hồ sơ đã trả lời thì đừng hỏi lại. Nếu yêu cầu của người dùng trong lượt này khác hồ sơ (ví dụ đổi xưng hô cho một video), làm theo yêu cầu hiện tại và nhắc một dòng rằng nó khác hồ sơ. Nếu không có file, làm như bình thường; có thể nhắc một lần rằng `channel-profile` (nếu đã cài) giúp các lần sau không phải khai lại.

## Quy trình

### 1. Gom đầu vào

Cần sáu thứ:

1. **Định dạng và nền tảng**: video ngắn, YouTube dài, bài chữ hay carousel, đăng ở đâu.
2. **Chất liệu câu chuyện**: chuyện gì đã xảy ra, càng cụ thể càng tốt.
3. **Thông điệp**: một điều người xem mang về sau khi xem hoặc đọc xong.
4. **Người xem**: họ là ai, đang gặp chuyện gì giống người kể.
5. **Độ dài**: số giây, số phút, số chữ hoặc số slide.
6. **Mục tiêu CTA (lời kêu gọi hành động)**: muốn người xem làm gì tiếp theo, ví dụ theo dõi để xem phần sau, lưu lại, kể trải nghiệm của họ, ghé link.

Tự suy ra những gì đã rõ, rồi nêu giả định trong một dòng ("Mình viết cho TikTok, khoảng 60 giây, xưng 'mình'"). Mặc định hợp lý khi người dùng không nói: video ngắn 45–60 giây, YouTube 10–12 phút, bài Facebook 250–450 chữ, carousel 8 slide, CTA mềm là một câu hỏi thật về trải nghiệm của người xem.

Chỉ hỏi những gì làm đổi kết quả, và hỏi gộp một lần bằng AskUserQuestion. Định dạng thường phải hỏi nếu chưa rõ, vì nó quyết định gần như mọi thứ phía sau. Xưng hô (mình, tôi, em, anh/chị) nên lấy theo cách người dùng tự kể; nếu họ có bài cũ thì bám theo giọng đó.

### 2. Kiểm tra chất liệu câu chuyện trước khi viết

Trước khi viết một chữ nào, đối chiếu chất liệu với bảy câu hỏi sau. Đây là lõi chung của hầu hết các khung kể chuyện: nhân vật muốn điều gì, gặp trở ngại, và thay đổi.

| Yếu tố | Câu hỏi | Chất liệu đủ trông như thế nào |
| --- | --- | --- |
| Nhân vật | Ai kể, lúc đó họ là người thế nào? | "Mình, năm hai đại học, đi làm thêm ở quán trà sữa" |
| Mong muốn | Lúc đó muốn gì? | "Muốn đủ tiền trả trọ mà không xin bố mẹ" |
| Trở ngại | Cái gì cản? | "Quản lý cắt ca vì mình hay đi trễ" |
| Rủi ro | Mất gì nếu thất bại? | "Hết tháng là phải dọn khỏi phòng" |
| Khoảnh khắc thay đổi | Lúc nào mọi thứ đổi hướng, hoặc mình nhận ra điều gì? | "Lúc chị quản lý nói 'em không thiếu thời gian, em thiếu ưu tiên'" |
| Trước / sau | Trước và sau khoảnh khắc đó khác nhau ra sao? | "Trước: làm theo hứng. Sau: lịch cố định, 6 tháng không trễ buổi nào" |
| Chi tiết cụ thể | Con số, nơi chốn, câu nói, đồ vật nào chứng minh? | "Tiền trọ 1,8 triệu, tin nhắn lúc 23h47" |

Khi thiếu chi tiết thật, hãy hỏi người dùng, đừng tự điền. Bịa ở đây gồm: sự kiện, lời thoại trình bày như nguyên văn, con số, mốc thời gian, tên người, và cả cảm xúc người dùng chưa hề nói. Những thứ được phép: sắp lại thứ tự kể (ví dụ đưa kết quả lên đầu), rút gọn, diễn đạt lại bằng lời khác, gộp vài lần tương tự thành một lần nhưng phải ghi rõ cho người dùng biết.

Hỏi tối đa khoảng 3–5 câu, cụ thể ("Lúc bị cắt ca, chị quản lý nói gì với bạn?" tốt hơn "Kể thêm chi tiết đi"). Nếu người dùng muốn có bản nháp ngay, cứ viết nhưng để chỗ trống dễ thấy dạng `[cần bổ sung: câu chị quản lý nói lúc đó]`. Câu chuyện thiếu rủi ro hoặc thiếu khoảnh khắc thay đổi thì nói thẳng: lúc này nó mới là một sự kiện, chưa phải một câu chuyện. Gợi ý người dùng tìm lại khoảnh khắc đó thay vì đắp thêm cảm xúc.

Kiểm tra thêm hai điều nhạy cảm. Nếu chuyện nhắc đến người thứ ba (gia đình, người yêu cũ, khách hàng, sếp), hỏi xem có cần ẩn danh không. Nếu chuyện còn quá đau và chưa rút ra được bài học, nhắc nhẹ rằng chia sẻ khi vết thương còn mở dễ thành trút bỏ hơn là kể, và người xem thường lùi lại.

### 3. Chọn cấu trúc

Đọc `references/frameworks.md` rồi chọn một cấu trúc hợp với định dạng, độ dài và chất liệu. Gợi ý nhanh:

- Video ngắn dưới 30 giây: ABT hoặc kết quả trước.
- Video ngắn 45–90 giây: kết quả trước (flashback), mini hành trình, hoặc cảnh rồi suy ngẫm kiểu The Moth.
- YouTube dài: mini hành trình làm khung lớn, mỗi chương là một vòng ABT, mở bằng kết quả trước hoặc cảnh cao trào.
- Bài chữ: cảnh rồi suy ngẫm, Story Spine, BAB, hoặc PAS khi chuyện là một sai lầm có cách sửa.
- Carousel: Story Spine hoặc BAB, chia đều mỗi slide một nhịp.

Ghi cho người dùng một dòng vì sao chọn ("Dùng kết quả trước vì con số 40 triệu đủ mạnh để giữ người xem ngay giây đầu").

### 4. Viết theo khuôn của định dạng

Dùng template trong file reference của định dạng. Các nguyên tắc chung cho mọi định dạng:

- **Câu mở đầu vào thẳng chuyện.** Câu đầu (hoặc 1–3 giây đầu) phải là cảnh, con số, lời thú nhận hoặc mâu thuẫn. Bỏ hết "Xin chào mọi người, hôm nay mình muốn chia sẻ…", vì người xem lướt qua trước khi tới phần hay.
- **Một câu chuyện, một ý, một CTA.** Nhiều bài học trong một bài khiến bài học nào cũng nhạt.
- **Nối các nhịp bằng "nhưng" hoặc "vì vậy", không bằng "và rồi".** Nếu giữa hai nhịp chỉ đặt được "và rồi" thì đó là danh sách sự kiện; cắt bớt hoặc tìm nguyên nhân nối chúng lại.
- **Cụ thể hơn chung chung.** "Tháng 3/2023, tài khoản còn 2,3 triệu" thay cho "có thời điểm mình rất khó khăn". Dùng lại đúng chữ người dùng đã kể khi có thể, vì đó là giọng thật của họ.
- **Bài học phải được khoảnh khắc chứng minh.** Nói bài học một lần, ngắn, gắn với tình huống của người xem. Tránh giọng dạy đời.
- **Tránh giọng máy.** Không dùng các câu sáo như "Trong thời đại 4.0…", "Hãy cùng mình khám phá…", "Và đó là lúc mình nhận ra…", không gom mọi thứ thành bộ ba cho tròn, không lặp mẫu "không phải X mà là Y" ở mỗi đoạn.
- **CTA thật, không mồi tương tác.** Một câu hỏi thật về trải nghiệm của người xem, một lời mời lưu lại, hay một gợi ý xem phần sau đều ổn. "Comment 'có' để nhận…", "share nếu đồng ý", "tag 3 người bạn" là mồi tương tác (engagement bait); Meta và LinkedIn đều công bố là giảm phân phối loại này (chi tiết trong `references/text-post.md`).

### 5. Tự kiểm tra rồi sửa trước khi đưa

Đọc lại bản viết và trả lời từng câu. Câu nào "chưa" thì sửa luôn, không để người dùng tự phát hiện:

1. **Rủi ro**: người xem có biết người kể sẽ mất gì nếu thất bại không?
2. **Thay đổi**: có một khoảnh khắc rõ ràng và một trước/sau khác biệt không?
3. **Nhân quả**: các nhịp có nối bằng "nhưng / vì vậy" không, còn chỗ nào "và rồi" không?
4. **Cụ thể**: có ít nhất 2–3 chi tiết cụ thể (con số, nơi chốn, câu nói, đồ vật) lấy từ chất liệu thật không?
5. **Trung thực**: có chi tiết nào mình tự thêm mà người dùng chưa cung cấp không? Nếu có, xoá hoặc đổi thành `[cần bổ sung: …]`.
6. **Vừa độ dài**: đã đếm âm tiết, chữ hoặc slide theo ngân sách trong reference chưa?
7. **Câu mở đầu và CTA**: câu đầu có hứa đúng điều nội dung trả được không, CTA có phải mồi tương tác không?

### 6. Trình bày

Trình bày trong chat theo thứ tự này:

```
**Cấu trúc:** <tên cấu trúc> — <một dòng vì sao>
**Giả định:** <nền tảng, độ dài, xưng hô… nếu có>

<Bản hoàn chỉnh theo template của định dạng>

**Câu mở đầu thay thế:**
1. <hook khác góc, ví dụ vào thẳng cảnh>
2. <hook khác góc, ví dụ con số / kết quả>
3. <tuỳ chọn: hook thú nhận hoặc câu hỏi>

**Cần bổ sung:** <liệt kê các [cần bổ sung: …] còn trong bài, hoặc "Không có">
```

Các câu mở đầu thay thế phải khác góc nhau, không chỉ đổi vài chữ, và cũng phải đúng sự thật như bài chính. Cuối cùng, nhắc ngắn hai bước tiếp theo nếu phù hợp: cần thêm nhiều phương án hook, tiêu đề hoặc chữ trên thumbnail thì dùng `story-hook-writer` (nếu đã cài); muốn chấm điểm và nhận góp ý theo mức độ thì dùng `story-content-review` (nếu đã cài). Nếu người dùng muốn lưu, đề nghị ghi bài ra một file trong dự án của họ.

## Khi người dùng sửa hoặc phản hồi

- **"Dài quá / ngắn quá"**: cắt hoặc thêm nhịp theo bảng nhịp trong reference, đừng chỉ nén câu chữ. Thêm nhịp thì hỏi thêm chất liệu thật.
- **"Chưa giống giọng mình"**: xin một bài cũ hoặc một đoạn họ tự viết rồi bám theo cách xưng hô, độ dài câu, từ hay dùng.
- **"Thêm kịch tính đi"**: tăng kịch tính bằng cách đưa rủi ro lên sớm hơn, kể chậm lại ở khoảnh khắc thay đổi, cắt bớt bối cảnh. Không thêm tình tiết không có thật.
