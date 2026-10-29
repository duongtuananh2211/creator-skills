# Nguồn xu hướng: đo gì, truy cập được không, tin tới đâu

Trạng thái dưới đây được kiểm tra ngày 29/10/2026 bằng `curl` và chính `scripts/trends.py`. Endpoint công khai thay đổi không báo trước, nên khi một nguồn lỗi, hãy coi bảng này là "đã từng chạy" chứ không phải bảo đảm.

Mức bằng chứng: **chính thức** (trang trợ giúp của nền tảng), **đã thử** (gọi thật trong phiên kiểm tra), **suy luận** (nhận định của người viết skill, chưa có nguồn).

---

## Nguồn script dùng được

| Nguồn | URL | Đo gì | Lưu ý |
|---|---|---|---|
| Google Trends "Trending now" RSS | `https://trends.google.com/trending/rss?geo=VN` | Từ khoá tìm kiếm đang tăng đột biến ở VN, mỗi mục có `approx_traffic` và 1–3 bài báo liên quan | Khoảng 10 mục, phần lớn là bóng đá, vụ án, người nổi tiếng. Dùng làm hạt giống và cầu nối sang tin, không phải danh sách ý tưởng. Đường dẫn cũ `/trends/trendingsearches/daily/rss` đã 404. |
| Google News RSS | `https://news.google.com/rss?hl=vi&gl=VN&ceid=VN:vi` | Tin nổi bật do Google News chọn | Link là link chuyển hướng của Google News; tên báo nằm ở trường `source`. |
| VnExpress xem nhiều | `https://vnexpress.net/tin-xem-nhieu` (HTML) | Bài được đọc nhiều nhất hiện tại, theo thứ hạng | **RSS `rss/tin-xem-nhieu.rss` vẫn trả 200 nhưng các bài trong đó dừng ở tháng 11/2021** (đã thử), nên script đọc trang HTML. Trang HTML không có ngày đăng. Nếu VnExpress đổi bố cục, script sẽ báo lỗi "no articles found". |
| VnExpress nổi bật | `https://vnexpress.net/rss/tin-noi-bat.rss` | Bài biên tập viên chọn | Từ máy kiểm tra, vnexpress.net mất khoảng 20 giây chỉ để mở kết nối (các báo khác dưới 1 giây), nên script cho VnExpress thời gian chờ 35 giây. |
| Kenh14 | `https://kenh14.vn/rss/home.rss` | Tin mới, thiên về giới trẻ, showbiz, chuyện lan truyền | `kenh14.vn/home.rss` là 404. |
| Tuổi Trẻ | `https://tuoitre.vn/rss/tin-moi-nhat.rss` | Tin mới nhất (không phải xem nhiều) | Ngày đăng dạng `10/29/2026 12:21:00 PM`, script đổi sang ISO. |
| Thanh Niên | `https://thanhnien.vn/rss/home.rss` | Tin mới nhất | Năm hai chữ số trong ngày đăng, script đã xử lý. |
| Wikipedia tiếng Việt, top lượt xem | `https://wikimedia.org/api/rest_v1/metrics/pageviews/top/vi.wikipedia/all-access/YYYY/MM/DD` | Số lượt xem tuyệt đối theo ngày (UTC) | Trễ khoảng 1 ngày; dữ liệu hôm qua lúc có lúc 404 tuỳ thời điểm, script tự lùi một ngày. Script bỏ trang chính, trang đặc biệt, tập tin. Hay có bài 18+ hoặc bài tăng vọt do bot, crawler: bỏ qua, đừng biến thành ý tưởng. Hữu ích để thấy *thực thể* đằng sau trend (người, địa danh, khái niệm), là điểm xuất phát tốt cho video giải thích. |
| Gợi ý tìm kiếm Google / YouTube | `https://suggestqueries.google.com/complete/search?client=firefox&hl=vi&gl=VN&q=...` (thêm `ds=yt` cho YouTube) | Cách người ta thật sự gõ | Endpoint không chính thức, có thể đổi. Không có số lượng, chỉ cho biết truy vấn có tồn tại. Gợi ý có ngày cụ thể ("giá vàng ngày 29 tháng 10") là truy vấn lặp hằng ngày: lượng lớn nhưng hết hạn ngay, báo làm tốt hơn creator (suy luận). Script giới hạn khoảng 30 lượt gọi cho mỗi lần `--alphabet`. |

## Google Trends đo gì (chính thức)

Theo FAQ của Google Trends (https://support.google.com/trends/answer/4365533):

- Mỗi điểm dữ liệu là lượt tìm của từ khoá chia cho tổng lượt tìm ở nơi và thời điểm đó, rồi quy về thang 0–100. Đây là **mức quan tâm tương đối, không phải số lượt tìm**.
- Dữ liệu là **mẫu**, có thêm nhiễu để bảo vệ quyền riêng tư; đột biến ở từ khoá ít người tìm có thể chỉ là nhiễu.
- Lượt tìm từ AI Mode và AI Overviews của Google bị loại ra.
- Google khuyên so với vài từ khoá phổ biến làm mốc, và coi Trends là "một điểm dữ liệu trong nhiều điểm".

Vì vậy `approx_traffic` "200+" chỉ là một khoảng ước lượng. Ở VN các khoảng này thường nhỏ, cho thấy RSS đưa lên cả những đột biến nhỏ (suy luận). Trước khi gọi một chủ đề là "lớn", đối chiếu với lượt xem Wikipedia và gợi ý tìm kiếm.

## Nguồn cần người dùng tự xem (phải đăng nhập)

- **YouTube Studio → Analytics → tab Trends** (chính thức, https://support.google.com/youtube/answer/11962757): Top searches (khán giả của kênh tìm gì, 28 ngày), Breakout videos (video đang chạy tốt của kênh tương tự), Recent videos, Content gaps cho Shorts. Khi tìm một chủ đề, Studio cho mức "Audience interest" từ rất thấp tới rất cao. **Content gap** là khi người xem không tìm được kết quả chất lượng cho một truy vấn (không có kết quả, không khớp, hoặc chỉ có video cũ, kém). Một số dữ liệu bị giới hạn theo quốc gia, ngôn ngữ. Studio đang được thiết kế lại từ tháng 7/2026 nên vị trí tab có thể khác.
- **YouTube Studio → Content → "Get inspired" (tab Inspiration)**: ý tưởng, tiêu đề, dàn ý do AI gợi ý; chỉ trên máy tính và chỉ tiếng Anh (chính thức, theo đoạn trích tìm kiếm, https://support.google.com/youtube/answer/15575509).
- **TikTok One Creative Suite** (tên mới của TikTok Creative Center), mục Trends → Hashtags, chọn khu vực VN: `https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en?region=VN`. Dữ liệu tải bằng JavaScript nên script không đọc được. Các nguồn mâu thuẫn về việc có cần đăng nhập không, và một nguồn người làm nghề nói dữ liệu hashtag nay chỉ còn bảng xếp hạng theo ngành.
- **Google Trends Explore** (`trends.google.com/trends/explore?geo=VN&q=...`): so sánh từ khoá theo thời gian; người dùng xem trên trình duyệt.
- **Facebook**: không có trang xu hướng công khai; CrowdTangle đã đóng (8/2024). Người dùng tự quan sát.

## Nguồn đã chết hoặc không dùng được

| Nguồn | Tình trạng |
|---|---|
| Trang YouTube Trending (`youtube.com/feed/trending`) | YouTube gỡ khoảng 21–22/7/2025 vì lượt truy cập giảm liên tục; trang giờ chỉ trả về feed trang chủ. Thay bằng YouTube Charts theo danh mục và trang Gaming Explore. |
| YouTube Charts (`charts.youtube.com/...`) | Trang chỉ là khung JavaScript, không có dữ liệu trong HTML. Chưa xác nhận có bảng cho VN ở mọi danh mục. |
| VnExpress `rss/tin-xem-nhieu.rss` | Còn trả 200 nhưng nội dung đứng ở năm 2021. Dùng trang HTML. |
| Google Trends daily RSS cũ | 404. |
| Reddit r/VietNam JSON | 403. |
| Znews `xem-nhieu-nhat.html` | 404. |
| Threads search | Khung đăng nhập / JavaScript. |
| AnswerThePublic, Exploding Topics, Glimpse | Cần tài khoản hoặc trả phí, ít dữ liệu VN; gợi ý tìm kiếm ở trên thay được phần lớn nhu cầu. |
| X/Twitter qua trends24.in | Truy cập được nhưng giá trị thấp cho VN: chủ yếu fandom K-pop, T-pop và hashtag quảng cáo. Script không dùng. |
| pytrends (thư viện không chính thức cho Google Trends) | Hay bị chặn 429; không dùng. |

## Khi script không chạy

Dùng WebFetch trên các URL RSS ở bảng đầu, và WebSearch cho câu hỏi cụ thể. WebFetch chuyển trang thành markdown rồi tóm tắt, nên với RSS dài có thể mất mục; yêu cầu nó liệt kê nguyên tiêu đề, link và ngày đăng. Với trang VnExpress xem nhiều, yêu cầu liệt kê tiêu đề theo thứ tự xuất hiện.
