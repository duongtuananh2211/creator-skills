---
name: keyword-research
description: Tìm từ khoá tốt cho kênh và cho từng nội dung trên YouTube, Shorts và TikTok ở Việt Nam. Đọc `channel-profile.md` nếu có, lập hạt giống từ trụ cột nội dung và cách khán giả gọi vấn đề, mở rộng bằng gợi ý tìm kiếm YouTube, Google và TikTok, kiểm tra trang kết quả YouTube để đo cạnh tranh và khoảng trống (bao nhiêu tiêu đề khớp đúng, video cũ hay mới, lượt xem), nhận thêm dữ liệu người dùng dán từ Google Trends (bộ lọc YouTube Search), TikTok Creative Center, Creator Search Insights, YouTube Studio, vidIQ, rồi gom cụm theo ý định, chấm theo độ hợp kênh, nhu cầu, cạnh tranh, khoảng trống. Làm được hai việc, lập bản đồ từ khoá cho cả kênh theo trụ cột, hoặc chọn từ khoá chính, từ phụ và chỗ đặt (tiêu đề, chữ trên màn hình, chú thích, hashtag, chương) cho một video hay bài. Có thể lưu vào `keyword-bank.md`. Dùng khi người dùng nói "tìm từ khoá", "keyword cho kênh", "từ khoá nào dễ lên top", "người ta hay tìm gì về chủ đề này", "nghiên cứu từ khoá YouTube/TikTok", "SEO cho video này", "keyword research", "find keywords for my channel". Không dùng để tìm chủ đề đang hot theo tin tức (dùng `trending-topic-finder`), viết mô tả YouTube hoàn chỉnh (dùng `youtube-description-writer`), làm kỹ tiêu đề, câu móc, thumbnail (dùng `story-hook-writer`), hay đọc số liệu analytics thay người dùng.
---

# Keyword research

Skill này trả lời hai câu hỏi: "kênh mình nên nhắm những cụm từ nào" và "video này nên dùng từ khoá gì, đặt ở đâu". Kết quả là các cụm từ người ta gõ thật, đã được lọc qua hồ sơ kênh và xếp theo cơ hội, kèm nguồn của từng tín hiệu.

Ba nguyên tắc chạy xuyên suốt:

- **Hợp kênh trước, nhiều người tìm sau.** Từ khoá đúng là câu người xem gõ mà video của kênh này trả lời tốt. Người tới từ một từ khoá lệch sẽ bỏ đi sớm, kéo tương tác xuống, và YouTube xếp hạng tìm kiếm theo cả mức liên quan, tương tác và chất lượng chứ không chỉ chữ khớp (theo trang "How YouTube search works").
- **Không có lượt tìm thì đừng nói có.** Gợi ý tìm kiếm chỉ cho biết một cụm có người gõ; trang kết quả chỉ cho biết ai đang chiếm chỗ. Google Trends là chỉ số tương đối trên mẫu. Số của vidIQ hay Ahrefs là ước lượng của từng công cụ. Luôn ghi nguồn cạnh tín hiệu, và viết "có trong gợi ý YouTube và TikTok" thay vì "nhiều người tìm".
- **Kênh nhỏ thắng bằng cụm hẹp.** "tiết kiệm tiền cho sinh viên" có cơ hội hơn "tiết kiệm tiền"; một câu hỏi dài mà trang đầu toàn video cũ, khớp một phần là cơ hội tốt hơn một cụm lớn đã có chủ.

## Script hỗ trợ

`scripts/kw.py` (chỉ dùng thư viện chuẩn Python) in JSON gọn. `HELPER` là đường dẫn tuyệt đối tới script, nằm trong thư mục chứa file SKILL.md này. Chạy từ thư mục gốc dự án người dùng:

```bash
HELPER="<thư-mục-skill>/scripts/kw.py"
python3 "$HELPER" expand --seed "tiết kiệm tiền" --seed "quản lý chi tiêu"      # YouTube + Google + TikTok, ~5 giây
python3 "$HELPER" expand --seed "tiết kiệm tiền" --alphabet --no-accent --limit 60  # mở rộng sâu, ~30–40 giây mỗi hạt giống
python3 "$HELPER" expand --seed "..." --platform yt,tiktok                         # chọn nền tảng
python3 "$HELPER" serp --q "cách tiết kiệm tiền" --q "tiết kiệm tiền cho sinh viên" --brief
python3 "$HELPER" links --q "tiết kiệm tiền" --q "quản lý chi tiêu"               # link Trends (YouTube Search), YouTube, TikTok để người dùng tự mở
```

Đọc kết quả `expand`: `platforms` là số nền tảng có gợi ý này, `hits` là số truy vấn trả ra nó, `best_rank` là thứ hạng gợi ý tốt nhất, `question` đánh dấu cụm dạng câu hỏi. `empty_seed` liệt kê hạt giống mà một nền tảng trả rỗng: với TikTok thường là chủ đề bị chặn gợi ý (cờ bạc, cá độ). Đọc kết quả `serp`: phần `summary` (`title_exact`, `title_most_words`, `under_1y`, `median_age_days`, `median_views`, `median_views_under_1y`, `top_channel_share`) là thứ dùng để chấm; `--brief` chỉ giữ 5 video đầu cho khỏi tràn ngữ cảnh.

Nền tảng nào lỗi sẽ nằm trong `errors` và `failed_platforms`, các nền tảng khác vẫn chạy.

## Khi nào đọc reference nào

- `references/sources.md`: đọc khi một nguồn lỗi, khi cần hướng dẫn người dùng mở Google Trends, TikTok Creative Center, Creator Search Insights, YouTube Studio, vidIQ, hoặc khi người dùng hỏi số liệu tin được tới đâu.
- `references/scoring.md`: luôn đọc trước bước 3. Có danh sách loại bỏ, bảng ý định, thang chấm bốn tín hiệu, ví dụ đã chấm và các biến thể tiếng Việt cần thử.
- `references/platforms.md`: đọc ở bước 6 chế độ B, và khi người dùng hỏi đặt từ khoá ở đâu trên YouTube, Shorts, TikTok, Reels.

## Hồ sơ kênh (nếu có)

Trước bước 1, kiểm tra file `channel-profile.md` ở thư mục gốc dự án (thư mục mở Claude Code). File này do skill `channel-profile` tạo. Nếu có, dùng như sau:

- **Định vị** (mục 1) và **niche, góc nhìn** (mục 2): phạm vi làm gì / không làm gì là bộ lọc đầu tiên; góc nhìn riêng quyết định cụm nào kênh trả lời tốt hơn người khác.
- **Khán giả** (mục 3): cách họ gọi vấn đề, vùng miền, độ tuổi. Đây là nguồn hạt giống quan trọng nhất, quan trọng hơn cách người làm kênh gọi.
- **Trụ cột** (mục 5): mỗi trụ cột một nhóm hạt giống; mỗi từ khoá phải gắn với một trụ cột.
- **Định dạng, nền tảng** (mục 6): kênh làm YouTube dài, Shorts hay TikTok, để biết nền tảng nào cần chạy và cụm nào hợp định dạng nào.
- **Giọng văn** (mục 7): tiêu đề gợi ý phải đúng xưng hô, đúng từ hay dùng.
- **Quy tắc nội dung** (mục 8): chủ đề nhạy cảm và cách kênh xử lý đè lên mọi gợi ý.
- **Đối thủ, khoảng trống** (mục 9): kênh đối thủ hiện trong `serp` là tín hiệu cạnh tranh trực tiếp; khoảng trống đã ghi là nơi tìm hạt giống.

Những gì hồ sơ đã trả lời thì đừng hỏi lại. Nếu không có file, hỏi gộp một lần: kênh nói về gì, cho ai (tuổi, vùng miền nếu liên quan), 3–5 chủ đề chính, làm trên nền tảng nào. Có thể nhắc một dòng rằng `channel-profile` (nếu đã cài) giúp các lần sau không phải khai lại. Nếu người dùng muốn làm luôn, ghi giả định trong một dòng rồi chạy tiếp.

## Hai chế độ

- **A. Bản đồ từ khoá cho kênh**: người dùng hỏi chung ("kênh mình nên nhắm từ khoá gì", "lập danh sách từ khoá"). Chạy cho mọi trụ cột, ra bảng theo trụ cột và 5 video nên làm trước.
- **B. Từ khoá cho một nội dung**: người dùng đưa ý tưởng, tiêu đề nháp, kịch bản hoặc link video. Ra 1 từ khoá chính, 3–6 từ phụ và chỗ đặt trên từng nền tảng.

Không rõ thì hỏi một câu. Đang có một ý tưởng cụ thể trong cuộc trò chuyện thì mặc định chế độ B.

## Quy trình

### 0. Đọc bối cảnh

Đọc `channel-profile.md` như trên. Nếu có `keyword-bank.md`, đọc để không đề xuất lại cụm đã có và biết cụm nào đã dùng; nếu có `content-ideas.md` (do `trending-topic-finder` tạo), đọc để gắn từ khoá vào ý tưởng sẵn có. Ở chế độ B, viết **lời hứa của nội dung trong một câu** trước: video này giúp ai biết hoặc làm được gì. Từ khoá phải nằm trong lời hứa đó.

### 1. Lập hạt giống

3–5 hạt giống mỗi trụ cột (chế độ A) hoặc 3–5 cho nội dung (chế độ B), lấy từ:

- cách khán giả gọi vấn đề (mục 3 hồ sơ), không phải thuật ngữ của người làm kênh;
- lời hứa của nội dung và chủ đề của trụ cột;
- biến thể tiếng Việt trong `references/scoring.md` mục 6: vùng miền, từ mượn, người trong cuộc và người ngoài;
- cụm người dùng đã có từ Studio (Traffic source: YouTube search, tab Research) nếu họ dán.

Hạt giống nên ngắn (2–3 chữ); gợi ý tìm kiếm sẽ tự kéo dài ra.

### 2. Mở rộng

Chạy `expand` cho tất cả hạt giống trên các nền tảng kênh làm. Chạy thêm `--alphabet --no-accent` cho 1–3 hạt giống quan trọng nhất (mỗi lần khoảng 30 lượt gọi mỗi nền tảng, đừng chạy cho mọi hạt giống).

Cùng lúc, hỏi người dùng **một lần** có muốn bổ sung dữ liệu tự xem không, đưa link từ lệnh `links` và nói rõ cần dán gì (chi tiết trong `references/sources.md`):

- Google Trends với bộ lọc **YouTube Search** (link đã có `gprop=youtube`): hình dạng đường 12 tháng và 5–10 dòng **Related queries → Rising**.
- TikTok: **Creator Search Insights** (cụm có nhãn content gap), **TikTok Creative Center** → Trends → Hashtags, khu vực Việt Nam.
- YouTube Studio → Analytics → **Research** và Traffic source: YouTube search.
- vidIQ hoặc công cụ khác nếu họ có: điểm từ khoá, ghi nguồn cạnh số.

Không có cũng làm tiếp; đừng chờ.

### 3. Lọc và gom cụm

Đọc `references/scoring.md`. Bỏ các cụm lệch niche, lệch ý định, truy vấn hằng ngày, tên người hay thương hiệu không liên quan, cụm buộc video hứa điều không trả được. Gom các biến thể cùng ý định thành **cụm**, mỗi cụm gắn một nhãn ý định (cách làm, giải thích, cân nhắc, tình huống, cảm hứng) và một trụ cột. Với chủ đề nằm trong `empty_seed` của TikTok, ghi chú ngay để bước 6 không đặt cụm đó lên TikTok.

Cụm nào thật ra là tin nóng thì chuyển gợi ý sang `trending-topic-finder`, đừng chấm như từ khoá bền.

### 4. Đo cạnh tranh

Chạy `serp --brief` cho 8–15 cụm có triển vọng nhất (chế độ A) hoặc 3–5 cụm (chế độ B), dùng biến thể đại diện của mỗi cụm. Không chạy cho mọi gợi ý. Nhìn thêm 5 video đầu: kênh lớn, báo đài hay creator cỡ vừa; tiêu đề có thật sự trả lời câu hỏi không (khớp một phần thường là cơ hội).

### 5. Chấm và xếp hạng

Chấm bốn tín hiệu theo `references/scoring.md`: **hợp kênh** (cửa), **nhu cầu**, **cạnh tranh**, **khoảng trống**, rồi xếp **Ưu tiên / Thử / Kho / Bỏ**. Ghi lý do ngắn bằng số liệu thật ("0/20 tiêu đề khớp đúng, 4/20 dưới 1 năm"), không ghi điểm trơ.

Nói rõ với người dùng giới hạn: không có lượt tìm tuyệt đối, kết quả `serp` là bản không đăng nhập (có thể khác thứ họ thấy), Trends là chỉ số tương đối.

### 6. Trình bày

Mở đầu bằng 2–3 dòng: ngày lấy dữ liệu, nền tảng đã chạy, nguồn nào lỗi hoặc trả rỗng, giả định về kênh, dữ liệu người dùng đã dán (nếu có).

**Chế độ A**: bảng theo trụ cột, mỗi trụ cột 3–8 cụm, xếp theo hạng. Sau bảng, chọn **5 video nên làm trước** (ưu tiên cụm Ưu tiên, trải trên nhiều trụ cột, trộn ý định), mỗi video một dòng: cụm chính, định dạng, một tiêu đề nháp đúng giọng kênh.

**Chế độ B**: từ khoá chính, từ phụ, câu hỏi dùng làm chương, rồi chỗ đặt trên từng nền tảng kênh làm theo mẫu trong `references/platforms.md`. Kèm 2–3 tiêu đề nháp có từ khoá chính gần đầu; mỗi tiêu đề phải **đúng sự thật**, **video trả được lời hứa**, **không xin tương tác**. Nói rõ đây là nháp; làm kỹ với `story-hook-writer`.

Cuối cùng hỏi gọn:

- Có muốn lưu vào `keyword-bank.md` không (định dạng bên dưới).
- Bước tiếp, nếu đã cài: `story-hook-writer` cho tiêu đề, câu móc, thumbnail; `youtube-description-writer` cho mô tả (đưa luôn từ khoá chính và từ phụ đã chốt); `story-content-writer` để viết kịch bản bám lời hứa.

## Định dạng đầu ra

Chế độ A, mỗi trụ cột một bảng:

```
### Trụ cột: <tên>

| Cụm (biến thể đại diện) | Ý định | Nền tảng có gợi ý | Cạnh tranh YouTube | Hạng | Vì sao |
|---|---|---|---|---|---|
| <cụm> | giải thích | YT #2, Google #1, TikTok rỗng | 0/20 khớp đúng, 4/20 dưới 1 năm | Ưu tiên | <một câu, có số> |
```

Chế độ B:

```
Lời hứa: <một câu>
Từ khoá chính: <cụm>  — <nguồn tín hiệu> · <tóm tắt serp>
Từ phụ: <cụm>, <cụm>, <cụm>
Câu hỏi cho chương / Shorts: <câu>, <câu>
Lưu ý nền tảng: <ví dụ: TikTok chặn gợi ý "cờ bạc", không dùng trong hashtag>

<khối "đặt ở đâu" theo references/platforms.md>

Tiêu đề nháp:
- <phương án 1>
- <phương án 2>
```

Phần trong ngoặc nhọn là chỗ điền từ dữ liệu thật; đừng điền khi không có nguồn.

## `keyword-bank.md`

Chỉ ghi khi người dùng đồng ý, ở thư mục gốc dự án. Chưa có file thì tạo; có rồi thì thêm dòng vào cuối bảng, không sửa dòng cũ trừ cột Trạng thái khi người dùng nhờ:

```markdown
# Kho từ khoá

| Ngày | Cụm | Trụ cột | Ý định | Tín hiệu (nguồn) | Cạnh tranh YouTube | Hạng | Dùng cho | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| 2026-11-03 | <cụm> | <trụ cột> | <ý định> | YT #2, TikTok #1 | 3/20 khớp đúng, cũ | Ưu tiên | <video/ý tưởng hoặc để trống> | mới |
```

Trạng thái gợi ý: mới / đã dùng / bỏ. Cùng một cụm chạy lại sau vài tháng thì thêm dòng mới với ngày mới, để thấy cạnh tranh thay đổi.

## Những chỗ dễ sai

- **Chọn cụm vì to, không vì hợp.** Một cụm lớn mà kênh không có gì riêng để nói thì xếp Bỏ hoặc Kho, dù gợi ý nhiều.
- **Coi gợi ý tìm kiếm là lượt tìm.** Thứ hạng gợi ý và số `hits` chỉ cho biết cụm có người gõ và hay xuất hiện; không nói "X nghìn người tìm" khi người dùng chưa dán số từ công cụ có ước lượng.
- **Trộn số của các công cụ.** vidIQ, Ahrefs, Keyword Planner mỗi nơi ước lượng một kiểu; ghi nguồn cạnh từng số, không cộng.
- **Chạy `serp` cho mọi gợi ý.** Chậm, dễ bị chặn, và tràn ngữ cảnh. Gom cụm trước, đo cạnh tranh sau.
- **Đặt cụm bị TikTok chặn vào hashtag hay chữ trên màn hình.** Kiểm tra `empty_seed` và quy tắc mục 8 hồ sơ kênh.
- **Nhồi từ khoá.** Mỗi từ phụ ở đúng một chỗ tự nhiên (một câu mô tả, một tên chương). Danh sách từ khoá trần trong mô tả vi phạm chính sách spam của YouTube.
- **Tiêu đề hứa nhiều hơn video.** Từ khoá kéo người tới; video không trả lời được thì họ bỏ đi và kênh bị đánh giá thấp hơn.
