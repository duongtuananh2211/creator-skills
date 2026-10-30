# Tham khảo và cơ chế

Phương pháp trong file này theo Aprilynne Alter (https://www.youtube.com/watch?v=KE4zqD0ONDI, 2026) [người làm nghề]: gom nhiều mẫu, từ nhiều nguồn khác nhau, rồi rút ra cơ chế thay vì chép hình. Thư viện cơ chế ở mục 4 là tổng hợp của skill này, không phải danh sách đã được kiểm chứng.

---

## 1. Năm nguồn

Mục tiêu: **10–15 mẫu, từ nhiều nguồn**. Một bộ toàn thumbnail cùng ngách sẽ cho ra concept giống đối thủ.

| Nguồn | Là gì | Cách lấy | Lưu ý |
|---|---|---|---|
| Nội bộ | Video của chính kênh vượt trung vị của kênh | `channel <kênh người dùng> --source internal` | Cần khoảng 10 video trở lên. Hỏi: kiểu thumbnail đó có áp được cho video mới không? |
| Bên ngoài | Video cùng chủ đề của kênh khác, vượt trung vị của kênh đó | `search "<từ khoá>" --outlier`, `channel <đối thủ> --source external`, YouTube Studio → Trends → Breakout videos (người dùng tự xem) | Thử cả từ khoá tiếng Việt và tiếng Anh. |
| Kênh mẫu | Cùng định dạng, khác chủ đề (ví dụ kênh giải thích bằng hoạt hình về khoa học khi kênh mình giải thích tâm lý bằng nhân vật) | Đề xuất 2–3 kênh, người dùng duyệt, rồi `channel --source model` | Nguồn hay bị bỏ qua nhất nhưng cho nhiều cơ chế mới nhất. |
| Đã lưu | Thumbnail người dùng thấy bắt mắt khi lướt | `fetch <link>...` hoặc một playlist riêng tên kiểu "thumbnail hay" | Gợi ý người dùng lập playlist này nếu chưa có. |
| Ngoài YouTube | Poster phim, khung hình phim hay intro series, bìa sách, bìa album, biển quảng cáo, quảng cáo vừa thấy | Người dùng thả ảnh vào `refs/`; có thể dùng các thư viện khung hình phim như FRAMESET (frameset.app) | Khó chuyển nhất, nhưng dễ cho ra thứ feed chưa ai làm. |

Không cần đúng chủ đề video. Đang gom **cách làm**.

## 2. Đọc điểm outlier cho đúng

- `outlier` = lượt xem của video chia trung vị lượt xem các video gần đây của chính kênh đó. Khoảng ≥2 là đáng xem, ≥5 là hiếm [kinh nghiệm, không có ngưỡng chuẩn].
- Danh sách video của kênh thường không kèm ngày đăng, nên script bỏ qua 2 video mới nhất (`--skip-newest`) vì chúng chưa kịp có lượt xem. Video cũ hơn nhiều năm có lợi thế thời gian; để ý cột lượt xem.
- Kênh nhỏ có trung vị thấp nên một video vài chục nghìn view đã cho điểm rất cao. Điểm cao ở kênh nhỏ vẫn là tín hiệu, chỉ là nhiễu hơn.
- **Điểm outlier không chứng minh thumbnail tốt.** Video có thể vượt trội nhờ chủ đề, thời điểm, tiêu đề, được kênh lớn nhắc tới hay chia sẻ ngoài YouTube. Dùng điểm để lọc mẫu đáng xem, rồi tự đánh giá thumbnail.
- Kết quả tìm kiếm của `yt-dlp` không giống hệt những gì người dùng thấy (không cá nhân hoá, khu vực có thể khác). Đủ để gom mẫu, không đủ để kết luận về "thị trường".

## 3. Mẫu phân tích

Với mỗi mẫu chọn ra (6–8 mẫu, không chỉ lấy mẫu điểm cao nhất), trả lời:

1. Nó khiến mình **thắc mắc** gì? (Có thể là không gì cả.)
2. Nó khiến mình **cảm thấy** gì? (Có thể là không gì cả.)
3. **Bằng cách nào?** Chỉ ra chi tiết cụ thể tạo ra thắc mắc hoặc cảm xúc đó: màu, vị trí, tỉ lệ, biểu cảm, thứ bị che, font, ánh sáng. Đây là cơ chế.
4. Cơ chế đó áp vào video của mình thì thành gì, và phục vụ cặp thắc mắc + cảm xúc nào ở bước 2?

Nếu một mẫu gây cảm giác mạnh mà khó gọi tên vì sao, mô tả thật kỹ những gì thấy rồi so với thư viện bên dưới; đôi khi phải thử vài cách diễn đạt mới ra. Ví dụ của Alter: một khung hình intro phim không gợi thắc mắc nào nhưng có cảm giác "chưa từng thấy". Nhìn kỹ thì cơ chế là phá kỳ vọng: thứ vốn 2D được làm thành 3D. Áp vào video về thumbnail: thumbnail vốn phẳng, vậy làm một thumbnail trông như khối 3D nhô ra khỏi màn hình.

## 4. Thư viện cơ chế

Mỗi cơ chế ghi: gợi ra gì, ví dụ cho kênh người thật và kênh nhân vật, rủi ro. Ví dụ là minh hoạ, không phải chuyện thật của ai.

**1. Phá kỳ vọng.** Một thứ quen thuộc xuất hiện sai chỗ, sai chất liệu, sai kích thước hay sai chiều (2D thành 3D, đồ vật nhỏ thành khổng lồ).
Gợi: mới lạ, "cái gì thế này". Người thật: cuốn sổ nợ to bằng cánh cửa đè lên người dẫn. Nhân vật: con rắn cuộn quanh một con xúc xắc to hơn nó. Rủi ro: lạ mà không liên quan thì thành gây nhiễu.

**2. Lạc loài.** Một thứ khác biệt giữa nhiều thứ giống nhau (thumbnail của chính Alter: một ô màu cầu vồng giữa hàng ô xám).
Gợi: chú ý ngay vào cái khác, "vì sao nó khác". Người thật: một cái ví rỗng giữa hàng ví dày. Nhân vật: một con rắn tỉnh táo giữa đám đông mắt đỏ nhìn máy đánh bạc. Rủi ro: thấp.

**3. Trước và sau.** Hai trạng thái đặt cạnh nhau, khoảng giữa bị giấu.
Gợi: "chuyện gì đã xảy ra ở giữa". Người thật: bàn làm việc bừa bộn và gọn gàng. Nhân vật: Xa béo tròn và Xa gầy rộc. Rủi ro: trạng thái "sau" phải có thật; đừng phóng đại khoảng cách.

**4. Ngay trước hậu quả.** Đóng băng một khoảnh khắc trước khi chuyện xảy ra.
Gợi: căng thẳng, "rồi sao nữa". Người thật: ngón tay sắp bấm "Gửi" email xin nghỉ việc. Nhân vật: đuôi rắn sắp đẩy cả tổ trứng lên bàn cược. Rủi ro: video phải kể đúng khoảnh khắc đó.

**5. Một vật thể, nền trống.** Tối giản, một thứ duy nhất được chiếu sáng.
Gợi: tò mò về chính vật đó, cảm giác cao cấp. Người thật: một tờ hoá đơn trên nền đen. Nhân vật: một con chip casino phát sáng. Rủi ro: vật phải đủ gợi chuyện; vật quá bình thường thì không ai thắc mắc.

**6. Phóng to một chi tiết.** Khoanh, mũi tên hoặc phóng đại một phần nhỏ của cảnh.
Gợi: "chi tiết đó có gì". Người thật: khoanh dòng phí ẩn trên hợp đồng. Nhân vật: kính lúp lên con mắt đổi màu của nhân vật. Rủi ro: chi tiết khoanh phải được giải thích trong video.

**7. Khung chưa lộ nội dung.** Thấy cấu trúc mà không thấy nội dung: "5 quy tắc", danh sách bị làm mờ, hộp hé mở.
Gợi: muốn biết nội dung. Người thật: 3 tờ giấy úp, chữ "3 SAI LẦM". Nhân vật: tủ có 5 ngăn khoá. Rủi ro: thứ bị che phải lộ ra trong video, và sớm.

**8. Phản ứng thay cho đối tượng.** Thấy mặt người hay nhân vật nhìn vào một thứ nằm ngoài khung hoặc bị che.
Gợi: tò mò về thứ họ đang thấy, đồng cảm với cảm xúc của họ. Người thật: người dẫn nhìn màn hình điện thoại, mặt sững lại. Nhân vật: Xa tròn mắt nhìn xuống bàn. Rủi ro: biểu cảm phải tương xứng với chuyện thật.

**9. Tổn thương, thú nhận.** Cho thấy sự trần trụi, thất bại, xấu hổ (người đàn ông mặc đồ lót trong ví dụ của Alter).
Gợi: đồng cảm, cảm giác "người thật việc thật". Người thật: ảnh chụp tài khoản âm. Nhân vật: nhân vật ôm mặt giữa đống vỏ vé số. Rủi ro: chuyện riêng của người thứ ba; quá tay thành bi kịch hoá.

**10. Mượn thẩm mỹ để mượn uy tín.** Font tạp chí, ánh sáng điện ảnh, bố cục poster phim hay bìa sách.
Gợi: tin cậy, gu, "video này được làm kỹ". Người thật: ảnh chân dung ánh sáng studio, chữ serif. Nhân vật: bố cục poster phim noir. Rủi ro: thẩm mỹ phải khớp chất lượng video thật.

**11. Đối lập quy mô hay giá trị.** Hai thứ chênh nhau rất xa đặt cạnh nhau (rẻ và đắt, nhỏ và to, một và một triệu).
Gợi: "sao lại chênh vậy". Người thật: tô phở 40 nghìn cạnh hoá đơn 4 triệu. Nhân vật: con rắn nhỏ cạnh núi tiền. Rủi ro: con số phải có thật.

**12. Con người đặt vào tình huống.** Người dẫn hay nhân vật đang ở giữa hành động, không đứng tạo dáng.
Gợi: nhập vai, "mình mà ở đó thì sao". Người thật: đang đóng thùng đồ rời văn phòng. Nhân vật: đang trèo ra khỏi hố sâu. Rủi ro: cảnh phải có trong video, ít nhất dưới dạng hình minh hoạ.

Cơ chế có thể kết hợp (lạc loài + phóng to chi tiết), nhưng một thumbnail chỉ nên có một ý chính.

## 5. Chuyển cơ chế sang video của mình

- Bước khó nhất, nhất là với mẫu ngoài YouTube hoặc ngoài ngách. Mô tả cơ chế bằng một câu không nhắc tới chủ đề của mẫu ("một thứ vốn phẳng được làm thành khối"), rồi hỏi: trong video của mình, cái gì "vốn phẳng", "vốn nhỏ", "vốn bị giấu"...?
- Viết 2–3 cách áp khác nhau cho cùng một cơ chế trước khi chọn.
- Nếu không hình dung được, phác bố cục bằng chữ (nửa trên có gì, nửa dưới có gì) hoặc tạo nhanh một ảnh nháp bằng Flow để nhìn. Ảnh nháp chỉ để quyết định hướng, chưa phải bản cuối.
- Không mượn: nhân vật, khuôn mặt, chữ, logo, ảnh gốc của mẫu. Concept cuối cùng phải nhìn không giống bản sao của mẫu nào.
