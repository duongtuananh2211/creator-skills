---
name: trending-topic-finder
description: Tìm chủ đề đang hot ở Việt Nam và biến chúng thành ý tưởng video hợp với kênh của người dùng. Đọc `channel-profile.md` nếu có, kéo xu hướng hiện tại từ Google Trends, Google News, báo điện tử (VnExpress, Kenh14, Tuổi Trẻ, Thanh Niên), Wikipedia tiếng Việt và gợi ý tìm kiếm YouTube, lọc theo độ hợp kênh, vòng đời xu hướng, mức cạnh tranh và rủi ro, rồi đề xuất 5–10 ý tưởng. Mỗi ý tưởng có xu hướng gốc kèm link và ngày, góc riêng của kênh, 2–3 tiêu đề đúng giọng kênh, định dạng gợi ý, độ gấp và lưu ý rủi ro. Có thể lưu vào `content-ideas.md`, tránh lặp ý cũ. Dùng khi người dùng nói "tìm chủ đề hot", "đang trend gì", "ý tưởng video theo xu hướng", "tiêu đề đang hot hợp kênh", "bắt trend", "tuần này làm video gì", "trending topics", "what's trending for my channel". Không dùng để viết kịch bản (dùng `story-content-writer`), làm kỹ hook, tiêu đề, thumbnail (dùng `story-hook-writer`), dựng hồ sơ kênh (dùng `channel-profile`), hay phân tích số liệu analytics của kênh người dùng.
---

# Trending topic finder

Skill này trả lời câu hỏi "tuần này kênh mình nên làm video gì" bằng dữ liệu xu hướng thật ở Việt Nam, rồi lọc qua hồ sơ kênh để chỉ giữ những gì kênh có lý do để nói. Kết quả là 5–10 ý tưởng có nguồn, có góc, có tiêu đề, để người dùng chọn.

Hai nguyên tắc chạy xuyên suốt:

- **Xu hướng là hạt giống, chưa phải ý tưởng.** Danh sách trend ở Việt Nam phần lớn là bóng đá, vụ án, người nổi tiếng. Giá trị nằm ở câu hỏi bên dưới trend ("vì sao chuyện này cứ lặp lại", "nó ảnh hưởng gì tới mình") và góc mà chỉ kênh này nói được. Một trend không gắn được với trụ cột nào thì bỏ, dù nó đang hot, vì người xem tới vì trend lạc đề thường không quay lại.
- **Chỉ nói những gì nguồn đã nói.** Mọi chi tiết về sự kiện phải lấy từ tiêu đề và bài báo đã kéo về. Chỗ nào cần thêm chi tiết thì ghi rõ "cần kiểm tra: …" thay vì tự suy ra. Một video dựng trên chi tiết sai về tin nóng vừa mất uy tín vừa có thể vướng quy định về thông tin sai sự thật.

## Script hỗ trợ

`scripts/trends.py` (chỉ dùng thư viện chuẩn Python) kéo dữ liệu từ các nguồn công khai và in JSON gọn. `HELPER` là đường dẫn tuyệt đối tới script, nằm trong thư mục chứa file SKILL.md này. Chạy từ thư mục gốc dự án người dùng:

```bash
HELPER="<thư-mục-skill>/scripts/trends.py"
python3 "$HELPER" all --seeds "từ khoá 1,từ khoá 2,từ khoá 3"   # mọi nguồn cùng lúc, ~20–40 giây
python3 "$HELPER" suggest --q "vì sao nghiện cờ bạc" --yt --alphabet  # mở rộng một từ khoá
python3 "$HELPER" news --source vnexpress-most-read
python3 "$HELPER" wiki-top --limit 30
python3 "$HELPER" google-trends --geo VN
```

Nguồn nào lỗi sẽ trả `{"source": ..., "error": ...}` và được liệt kê trong `failed_sources`, các nguồn khác vẫn chạy. `all` mặc định lấy 20 mục mỗi nguồn (`--limit` để đổi) cho khỏi tràn ngữ cảnh.

## Khi nào đọc reference nào

- `references/sources.md`: đọc khi một nguồn lỗi, khi người dùng hỏi số liệu lấy từ đâu và tin được tới mức nào, hoặc khi cần hướng dẫn họ xem YouTube Studio, TikTok Creative Center.
- `references/scoring.md`: luôn đọc trước bước 4. File có thang chấm, ví dụ đã chấm, và các mẫu chuyển tin nóng thành ý tưởng bền.
- `references/risk-checklist.md`: luôn đọc ở bước 5, và khi người dùng hỏi một chủ đề có "đụng" được không.

## Hồ sơ kênh (nếu có)

Trước bước 1, kiểm tra file `channel-profile.md` ở thư mục gốc dự án (thư mục mở Claude Code). File này do skill `channel-profile` tạo và là nguồn đúng nhất về kênh. Nếu có, đọc nó và dùng như sau:

- **Định vị** (mục 1) và **niche, góc nhìn** (mục 2): phạm vi làm gì / không làm gì là bộ lọc đầu tiên; góc nhìn khác biệt là chất liệu cho câu "góc của kênh".
- **Khán giả** (mục 3): trend phải là thứ họ quan tâm hoặc đang hỏi.
- **Người dẫn / nhân vật** (mục 4) và **giọng văn** (mục 7): tiêu đề phải nghe như chính người dẫn nói, đúng xưng hô, đúng từ hay dùng, tránh từ cấm. Với kênh nhân vật đại diện (ví dụ một con rắn giải thích vì sao người ta nghiện cờ bạc), giữ đúng tính cách nhân vật.
- **Trụ cột** (mục 5): mỗi ý tưởng phải gắn với một trụ cột, và cả danh sách nên trải trên nhiều trụ cột.
- **Định dạng, nhịp đăng** (mục 6): biết kênh làm Shorts hay video dài, làm nhanh được tới đâu, để so với vòng đời trend.
- **Quy tắc nội dung** (mục 8): chủ đề nhạy cảm và cách xử lý của kênh đè lên danh sách rủi ro chung.
- **Đối thủ, khoảng trống** (mục 9): tránh góc mà kênh khác đã làm kỹ, ưu tiên khoảng trống hồ sơ đã ghi.

Những gì hồ sơ đã trả lời thì đừng hỏi lại. Nếu không có file, hỏi gộp một lần 3–4 câu: kênh nói về gì, cho ai, 3–5 chủ đề chính, giọng xưng hô. Có thể nhắc một dòng rằng `channel-profile` (nếu đã cài) giúp các lần sau không phải khai lại. Nếu người dùng muốn làm luôn, ghi giả định trong một dòng rồi chạy tiếp.

## Quy trình

### 0. Đọc bối cảnh

Đọc `channel-profile.md` như trên. Nếu có `content-ideas.md` ở thư mục gốc dự án, đọc luôn để biết ý nào đã có, tránh đề xuất lặp. Một trend mới chạm vào ý cũ thì có thể gợi ý "ý #… có hook mới" thay vì tạo ý trùng.

### 1. Lập 5–15 từ khoá hạt giống

Rút từ trụ cột, niche và câu hỏi của khán giả. Chủ yếu tiếng Việt, thêm 2–3 từ tiếng Anh nếu niche có cộng đồng quốc tế. Trộn từ khoá rộng ("cờ bạc online") với dạng câu hỏi ("vì sao nghiện cờ bạc"), vì gợi ý tìm kiếm trả về đúng cách người xem gõ, rất hợp để đặt tiêu đề.

### 2. Kéo dữ liệu

Chạy `python3 "$HELPER" all --seeds "..."`. Với 2–3 từ khoá quan trọng nhất, chạy thêm `suggest --q "..." --yt --alphabet` để thấy nhiều cách hỏi hơn (khoảng 30 lượt gọi mỗi từ, đừng chạy cho mọi từ).

Nếu script không chạy được hoặc mạng lỗi toàn bộ, chuyển sang WebSearch và WebFetch trên cùng các URL trong `references/sources.md`. Hai tool này thường được nạp trễ trong Claude Code, nên nạp bằng ToolSearch (`select:WebSearch,WebFetch`) trước khi gọi. Báo cho người dùng nguồn nào lấy được, nguồn nào không.

### 3. Mời người dùng dán dữ liệu cần đăng nhập (không bắt buộc)

Một câu, không chờ: nếu họ có thời gian, dán những gì thấy ở **YouTube Studio → Analytics → tab Trends** (Top searches, Breakout videos từ kênh tương tự, Content gaps) và **TikTok One Creative Suite** (tên mới của Creative Center, mục Trends, chọn khu vực VN). Dữ liệu Studio gắn với khán giả của chính kênh nên là tín hiệu hợp kênh nhất, nhưng chỉ người dùng xem được. YouTube định nghĩa "content gap" là khi người xem không tìm được kết quả chất lượng cho một truy vấn. Nếu họ không dán, cứ làm tiếp với dữ liệu công khai.

### 4. Lọc và chấm

Đọc `references/scoring.md`. Gom 20–40 ứng viên từ các nguồn, gộp những mục cùng một chuyện, rồi với mỗi cụm:

1. **Cửa hợp kênh** (đạt / không đạt): gắn được với trụ cột nào, khán giả có quan tâm không. Không đạt thì bỏ luôn.
2. **Vòng đời**: bùng nổ ngắn / đang lên / theo mùa / bền có móc thời sự.
3. **Cạnh tranh**: nhìn gợi ý YouTube (nhiều biến thể dài là có nhu cầu thật); nếu cần, tìm nhanh xem kết quả đầu là báo đài lớn hay creator. Kênh nhỏ không thắng được "tin", chỉ thắng được "giải thích" hoặc "góc riêng".
4. **Góc của kênh** trong một câu: điều kênh này nói được mà báo không nói. Không viết được câu này thì không có video.
5. **Thời gian sản xuất so với vòng đời**: nếu làm mất hơn khoảng nửa thời gian trend còn nóng, đổi sang định dạng nhanh hơn hoặc đổi sang góc bền.

Nói rõ với người dùng giới hạn của dữ liệu: Google Trends đo **mức quan tâm tương đối, dữ liệu lấy mẫu**, không phải số lượt tìm (theo FAQ chính thức của Google Trends); `approx_traffic` như "200+" chỉ là khoảng ước lượng. Lượt xem Wikipedia là số tuyệt đối nhưng có đột biến do bot.

### 5. Gắn cờ rủi ro

Đọc `references/risk-checklist.md`. Bỏ qua hoặc đổi góc với: tai nạn, thiên tai, cái chết; vụ án nêu tên người thường hoặc đang xét xử; tin đồn chưa kiểm chứng; chính trị và vấn đề nhà nước nhạy cảm; dùng hình ảnh, clip của báo đài (bản quyền); tiêu đề hứa điều video không trả được; quảng bá cờ bạc, đầu tư, chữa bệnh. Với kênh giải thích, cách đổi góc tốt nhất thường là chuyển từ "kể lại vụ việc" sang **cơ chế bên dưới** ("vì sao chuyện này cứ lặp lại"), vừa an toàn hơn vừa sống lâu hơn tin.

Bỏ qua các mục vô nghĩa hoặc nhạy cảm trong top Wikipedia (bài 18+, trang tăng đột biến do bot), không cần bình luận.

### 6. Viết ý tưởng

Chọn 5–10 ý, trải trên nhiều trụ cột và nhiều loại vòng đời (đừng để cả danh sách là tin nóng 48 giờ). Mỗi ý gồm:

- **Trend gốc**: tiêu đề mục gốc, link, ngày đăng, nguồn. Chỉ dùng link đã kéo về, không tự dựng link.
- **Vì sao hợp kênh**: trụ cột nào, khán giả nào.
- **Góc của kênh**: một câu.
- **2–3 tiêu đề** đúng giọng mục 4 và mục 7, trộn kiểu: gợi tò mò, nói lợi ích, sát từ khoá người ta gõ (lấy từ gợi ý tìm kiếm). Mỗi tiêu đề qua 4 câu hỏi: **đúng sự thật**, **video trả được lời hứa**, **không xin tương tác**, **cảm xúc tương xứng với câu chuyện**. Gắn 🟢 nếu qua cả bốn, 🟡 kèm lý do nếu cần người dùng xác nhận hoặc chỉnh. Tiêu đề không qua thì viết lại hoặc bỏ, đừng để trong danh sách. Ý chính nên nằm trong khoảng 50–60 ký tự đầu (kinh nghiệm người làm nghề, không phải quy định).
- **Định dạng gợi ý**: Shorts/TikTok, video dài, hay cả hai (ngắn trước để bắt trend, dài sau cho cơ chế).
- **Độ gấp**: làm trong 24–48 giờ / trong tuần / kho ý tưởng.
- **Rủi ro, lưu ý** và **cần kiểm tra** (chi tiết nào phải xác minh với ít nhất hai báo lớn trước khi viết kịch bản).

### 7. Trình bày và bước tiếp theo

Mở đầu bằng 2–3 dòng: ngày giờ lấy dữ liệu, nguồn nào lỗi, giả định về kênh. Sau đó là danh sách ý tưởng, xếp theo độ gấp. Cuối cùng hỏi gọn:

- Có muốn lưu ý tưởng nào vào `content-ideas.md` không (xem định dạng bên dưới).
- Bước tiếp, nếu đã cài: `story-hook-writer` để làm kỹ tiêu đề, thumbnail, câu mở đầu; `story-content-writer` để viết kịch bản.
- Có thể chạy định kỳ hằng tuần bằng `/loop` hoặc `/schedule`.

## Định dạng đầu ra

```
1. [Đang lên · Trụ cột: Tâm lý con bạc] Làm trong tuần · Video dài + 1 Shorts
   Trend gốc: "<tiêu đề bài gốc>" — <nguồn>, <ngày> — <link>
   Hợp kênh vì: khán giả đang hỏi "<cụm từ gợi ý tìm kiếm>"
   Góc của kênh: <một câu>
   Tiêu đề:
   - 🟢 <tiêu đề gợi tò mò>
   - 🟢 <tiêu đề sát từ khoá>
   - 🟡 <tiêu đề nói lợi ích> (cần số liệu có nguồn cho vế "…")
   Rủi ro: <ví dụ: vụ án đang xét xử, không nêu tên, không suy đoán>
   Cần kiểm tra: <chi tiết cần xác minh>
```

Phần trong ngoặc nhọn là chỗ điền từ dữ liệu thật; đừng điền khi không có nguồn.

## `content-ideas.md`

Chỉ ghi khi người dùng đồng ý, ở thư mục gốc dự án. Chưa có file thì tạo; có rồi thì thêm dòng vào cuối bảng, không sửa dòng cũ:

```markdown
# Kho ý tưởng nội dung

| Ngày | Ý tưởng | Trend gốc | Trụ cột | Định dạng | Độ gấp | Trạng thái |
|---|---|---|---|---|---|---|
| 2026-10-29 | <ý tưởng, một dòng> | [<nguồn>](<link>) | <trụ cột> | <định dạng> | <độ gấp> | mới |
```

Trạng thái gợi ý: mới / đang làm / đã đăng / bỏ. Người dùng tự cập nhật hoặc nhờ sửa.

## Những chỗ dễ sai

- **Đưa nguyên danh sách trend ra làm ý tưởng.** Người dùng cần góc, không cần bản tin. Mỗi ý phải qua cửa hợp kênh và có câu "góc của kênh".
- **Bịa chi tiết về sự kiện.** Tiêu đề bài báo không đủ để biết ai đúng ai sai, con số cụ thể, hay diễn biến. Ghi "cần kiểm tra" thay vì đoán.
- **Nói Google Trends như số lượt tìm.** Đó là chỉ số tương đối trên mẫu; nói "đang tăng" chứ đừng nói "100 nghìn người tìm".
- **Cả danh sách là tin 48 giờ.** Kênh nhỏ không kịp; trộn thêm ý đang lên, theo mùa và ý bền có móc thời sự.
- **Tiêu đề hay hơn video.** Tiêu đề phải mô tả đúng thứ video có. Chính sách YouTube cấm tiêu đề, thumbnail gây hiểu lầm có chủ ý.
