# Nguyên tắc thumbnail, bằng chứng và checklist

Mỗi ý được gắn mức bằng chứng: **[chính thức]** là tài liệu của YouTube, **[người làm nghề]** là kinh nghiệm của người làm thumbnail chuyên nghiệp, **[suy luận]** là hệ quả rút ra từ hai loại trên. Giao diện YouTube đổi thường xuyên, nên các mô tả giao diện có thể đã cũ khi bạn đọc.

Nguồn người làm nghề chính của file này: Aprilynne Alter, *give me 9 minutes, I'll make your thumbnails 81% better* (27/08/2026), https://www.youtube.com/watch?v=KE4zqD0ONDI. Tác giả là người góp ý thumbnail cho nhiều creator. Video được 1of10 tài trợ, và con số "81%" trong tiêu đề không được chứng minh trong video, nên file này chỉ giữ phương pháp, không giữ con số hay tên công cụ.

---

## 1. Vì sao thumbnail phải tự gây tò mò

- **Thumbnail to lên, tiêu đề nhỏ đi** [người làm nghề]. Alter so giao diện cũ và mới của cột video đề xuất: thumbnail lớn hơn hẳn, cỡ chữ tiêu đề nhỏ hơn. Mắt người xem mặc định lướt thumbnail, chỉ đọc tiêu đề khi đã chủ động chú ý. Trước đây tiêu đề hay đủ gánh, thumbnail chỉ cần liên quan; giờ thumbnail phải tự tạo được sự quan tâm.
- **Cách tạo sự quan tâm: gợi thắc mắc, gợi cảm xúc, tốt nhất là cả hai** [người làm nghề]. Ví dụ Alter đưa ra: cùng một video về phong cách ăn mặc nam, thumbnail bày quần áo và phụ kiện thì đúng chủ đề nhưng nhạt; thumbnail người đàn ông mặc đồ lót, font kiểu tạp chí, chữ "5 quy tắc" thì khiến người xem thắc mắc (5 quy tắc là gì, bộ đồ cuối cùng trông thế nào), cảm thấy tin cậy (font, ánh sáng) và hơi bị chạm (sự trần trụi).
- **Thứ tự khi brainstorm**: muốn người xem thắc mắc gì và cảm thấy gì → rồi mới chọn hình [người làm nghề]. Nhờ vậy mỗi chi tiết trên ảnh đều có mục đích tâm lý.
- **Cơ sở tâm lý của thắc mắc** là lý thuyết khoảng trống thông tin (Loewenstein 1994): tò mò cần người xem biết đủ về chủ đề để thấy mình thiếu một mảnh, và dễ biến thành thất vọng nếu đáp án không xứng. Chi tiết trong `story-hook-writer/references/evidence.md` nếu đã cài.
- **Giới hạn của "thắc mắc và cảm xúc thắng sự liên quan"** [suy luận]: câu này nói về lượt click. Test & Compare chọn phương án thắng theo **thời gian xem**, không theo CTR [chính thức, https://support.google.com/youtube/answer/13861714], nên thumbnail kéo click mà video không trả được vẫn có thể thua. Thắc mắc và cảm xúc phải là thứ video có.

## 2. Phép thử 50% cho TV

- **TV quan trọng hơn trước.** Trong thư thường niên tháng 2/2025, CEO YouTube Neal Mohan cho biết TV đã vượt điện thoại thành thiết bị chính để xem YouTube ở Mỹ, tính theo thời gian xem [chính thức, qua báo chí: https://www.hollywoodreporter.com/business/business-news/youtube-tv-viewing-overtakes-mobile-ceo-neal-mohan-1236132074/ và https://au.variety.com/2025/digital/global/youtube-tv-viewing-surpasses-mobile-ceo-neal-mohan-creators-hollywood-startups-20202/]. Đây là số liệu Mỹ; kênh Việt cần tự xem Analytics → Audience → Device type.
- **Giao diện TV chỉ hiện nửa trên** [người làm nghề, quan sát giao diện năm 2026]. Ở trang chủ và mục đề xuất trên TV, các hàng video bên dưới chỉ lộ phần trên của thumbnail; người xem phải bấm xuống trên remote mới thấy toàn bộ thumbnail và tiêu đề. Nếu chữ và nhân vật chính nằm ở nửa dưới, với người xem TV thumbnail gần như trống.
- **Phép thử** [người làm nghề]: che nửa dưới. Phần còn lại có đủ để người xem đoán được video nói về gì và muốn bấm xuống không? Nếu không: đưa thứ quan trọng nhất lên trên, hoặc đặt chữ ở 1/3 trên cùng. Alter áp dụng khi TV chiếm từ khoảng 10% lượt xem trở lên; skill này áp mặc định vì cách sửa thường không làm hại thumbnail trên điện thoại [suy luận].
- `thumb_tools.py check` tạo sẵn ô "chỉ nửa trên".

## 3. Ba sửa nhanh

[người làm nghề] Phần lớn thumbnail được cải thiện rõ chỉ với ba thay đổi nhỏ:

1. **Bỏ chi tiết thừa.** Ngoài đời trông thế nào không quan trọng. Thứ gì trên thumbnail không giúp ý tưởng thì đang cản nó. Ví dụ của Alter: các thanh vịn ở hồ bơi là thật nhưng làm rối mắt khỏi vận động viên; xoá đi thì mắt tìm ngay được chỗ cần nhìn.
2. **Làm nhân vật chính hiển nhiên.** Nhân vật chính (người, con vật, đồ vật) phải là thứ mắt thấy đầu tiên. Làm nó tách khỏi phần còn lại: đổi màu cho tương phản với nền, phóng to, thêm viền hoặc một nhãn chữ ngắn. Ví dụ: vận động viên nhảy cầu lẫn vào nền; đổi màu đồ bơi và thêm nhãn chữ là thấy ngay.
3. **Viết nhiều phương án chữ.** Mỗi lần đặt chữ lên thumbnail, bỏ thêm vài phút nghĩ các từ khác có thể dùng, rồi đưa vào thử. Đây là cách ít công nhất để cải thiện.

## 4. Thông số chính thức

[chính thức, https://support.google.com/youtube/answer/72431, kiểm tra 30/10/2026]

- Video thường: tỉ lệ 16:9, độ phân giải khuyến nghị 3840×2160, chiều rộng tối thiểu 640 px. Shorts: 9:16, 2160×3840, chiều cao tối thiểu 640 px.
- Định dạng ảnh như JPG hoặc PNG. Dung lượng tối đa: 2 MB khi tải từ điện thoại (10 MB với podcast), 50 MB trên máy tính.
- Cần tài khoản đã xác minh để tải thumbnail tuỳ chỉnh. Có giới hạn số thumbnail tải lên mỗi ngày.
- Thumbnail phải tuân thủ Nguyên tắc cộng đồng; vi phạm có thể bị từ chối và bị cảnh cáo (strike).
- Test & Compare: tối đa 3 phương án, ảnh nên từ 1280×720 trở lên, chỉ trên YouTube Studio bản máy tính, thường kết thúc trong khoảng hai tuần, đổi tiêu đề hay thumbnail giữa chừng sẽ dừng thử nghiệm [chính thức, https://support.google.com/youtube/answer/13861714].

## 5. Kinh nghiệm người làm nghề khác

[người làm nghề; không có nghiên cứu công khai đo riêng từng mẹo cho thumbnail YouTube]

- **Chữ**: khoảng 0–4 từ, to, đậm, tương phản cao, đọc được ở cỡ nhỏ nhất trên điện thoại (khoảng 168×94 px ở danh sách đề xuất). Chữ không lặp tiêu đề; tiêu đề nói lời hứa, thumbnail nói cảm xúc, cái giá phải trả, hoặc một mảnh của câu hỏi.
- **Một điểm nhìn**: một nhân vật chính, nền đơn giản. Hai ba thứ cùng tranh sự chú ý thì ở cỡ nhỏ không thứ nào thắng.
- **Khuôn mặt hoặc biểu cảm rõ** khi có người hay nhân vật, và biểu cảm phải khớp với cảm xúc thật của video.
- **Tránh góc dưới bên phải** vì nhãn thời lượng che mất; với video đã xem dở, thanh tiến trình đỏ chạy dọc mép dưới [quan sát giao diện].
- **Ảnh xám**: chuyển sang đen trắng mà nhân vật chính vẫn tách khỏi nền thì độ tương phản sáng tối đủ; nếu chỉ tách được nhờ màu thì yếu hơn ở cỡ nhỏ và với người mù màu.
- **Đứng giữa feed**: đặt thumbnail cạnh thumbnail của các kênh cùng chủ đề. Nếu cùng tông màu, cùng bố cục "mặt to bên trái, chữ vàng bên phải" thì nó hoà lẫn. Khác biệt về nền, độ sáng hoặc bố cục giúp mắt dừng lại.
- **Nhận diện kênh**: kênh nhân vật nên giữ vài yếu tố cố định (màu, dáng nhân vật, vị trí chữ) để người xem quen nhận ra, nhưng đừng để khuôn mẫu làm mọi video trông giống nhau.

## 6. Ranh giới trung thực

- YouTube cấm "malicious clickbait": dùng tiêu đề, thumbnail, mô tả hay hình ảnh gây hiểu lầm có chủ ý để lừa người xem bấm vào video không có những gì đã hứa. Hậu quả có thể là gỡ video, cảnh cáo hoặc gậy [chính thức, https://support.google.com/youtube/answer/2801973].
- Kênh dùng hình AI: hình hoạt hình hay rõ ràng không thật thì không cần nhãn; hình trông như thật về người thật hay sự kiện thật thì có thể cần nhãn nội dung thay đổi hoặc tổng hợp [chính thức, https://support.google.com/youtube/answer/14328491]. Thumbnail AI vẽ người thật trông như ảnh chụp, làm điều họ không làm, là 🔴.
- Mức 🟢🟡🔴 dùng chung với `story-hook-writer`: 🔴 khi thumbnail cho thấy người, vật, cảnh, con số hay cảm xúc mà video không có, hoặc mức cảm xúc vượt xa câu chuyện (mặt khóc cho một video bình thản).

---

## Checklist cho từng concept hoặc ảnh

Ghi ✅ hoặc ⚠️ kèm cách sửa cụ thể. Hai mục đầu là điều kiện bắt buộc; các mục sau là chất lượng.

1. **Có thật**: mọi người, vật, cảnh, con số và cảm xúc trên ảnh đều có trong video, và video trả lời thắc mắc mà ảnh gợi ra.
2. **Không lừa, không vi phạm**: không thuộc mẫu đỏ, không có hình như thật về người thật mà chưa được phép hoặc chưa gắn nhãn khi cần.
3. **Tự gây tò mò**: che tiêu đề đi, ảnh vẫn gợi được một thắc mắc cụ thể hoặc một cảm xúc rõ.
4. **Phép thử 50%**: che nửa dưới, vẫn hiểu chủ đề và muốn xem tiếp.
5. **Nhân vật chính**: nhận ra trong chưa tới một giây, tách khỏi nền cả khi chuyển ảnh xám.
6. **Không thừa**: chỉ ra được vai trò của từng chi tiết; thứ không có vai trò thì bỏ.
7. **Chữ**: 0–4 từ, đọc được ở cỡ 168 px, không lặp tiêu đề, dấu tiếng Việt đúng.
8. **Góc và mép dưới**: không có gì quan trọng ở góc dưới phải hay sát mép dưới.
9. **Giữa feed**: khác rõ với thumbnail đối thủ về nền, độ sáng hoặc bố cục.
10. **Bổ sung tiêu đề**: tiêu đề và thumbnail cùng một lời hứa, mỗi bên nói một phần.
