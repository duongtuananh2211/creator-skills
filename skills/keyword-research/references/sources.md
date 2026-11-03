# Nguồn từ khoá: đo gì, lấy được không, tin tới đâu

Trạng thái dưới đây được kiểm tra ngày 03/11/2026 bằng `curl` và chính `scripts/kw.py`. Endpoint công khai đổi không báo trước, nên khi một nguồn lỗi, coi bảng này là "đã từng chạy" chứ không phải bảo đảm.

Mức bằng chứng: **chính thức** (trang trợ giúp hoặc newsroom của nền tảng), **đã thử** (gọi thật trong phiên kiểm tra), **người làm nghề** (blog, công cụ SEO, chưa có nguồn chính thức), **suy luận** (nhận định của người viết skill).

Điều quan trọng nhất: **không nguồn nào script đọc được cho ra lượt tìm.** Gợi ý tìm kiếm chỉ cho biết một cụm có người gõ; kết quả tìm kiếm chỉ cho biết ai đang chiếm chỗ. Con số lượt tìm (nếu có) chỉ đến từ công cụ người dùng tự mở, và cũng là ước lượng.

---

## Nguồn script đọc được

| Nguồn | Lệnh | Đo gì | Lưu ý |
|---|---|---|---|
| Gợi ý tìm kiếm YouTube | `expand --platform yt` | Cụm người ta gõ trên YouTube ở VN, tối đa 10 gợi ý mỗi truy vấn | `suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=vi&gl=VN`. Không chính thức. Thứ tự gợi ý không phải thứ hạng lượt tìm [suy luận], nhưng một cụm hiện lên ở nhiều truy vấn (`hits` cao) là dấu hiệu nó phổ biến. |
| Gợi ý tìm kiếm Google | `expand --platform google` | Như trên nhưng của Google Search | Hữu ích để thấy người ta còn tìm chủ đề này dạng bài viết, hướng dẫn. Gợi ý có ngày cụ thể ("giá vàng hôm nay") là truy vấn lặp hằng ngày, báo làm tốt hơn creator [suy luận]. |
| Gợi ý tìm kiếm TikTok | `expand --platform tiktok` | Cụm người ta gõ trong ô tìm kiếm TikTok, `region=VN&lang=vi` | `www.tiktok.com/api/search/general/sug/?keyword=…&aid=1988&region=VN&lang=vi` [đã thử, không cần đăng nhập]. Không chính thức, dễ bị chặn nhất trong ba nguồn. **TikTok trả rỗng cho "nghiện cờ bạc", "cờ bạc", "cá độ bóng đá"** trong khi YouTube vẫn gợi ý [đã thử]: nền tảng chặn gợi ý cho chủ đề nhạy cảm. Script ghi những hạt giống trả rỗng vào `empty_seed`. Với chủ đề như vậy, hashtag và từ khoá thẳng trên TikTok có rủi ro bị giảm phân phối; dùng cách gọi gián tiếp hoặc thiên về YouTube [suy luận]. |
| Trang kết quả tìm kiếm YouTube | `serp --q` | Khoảng 20 video đầu: tiêu đề, kênh, lượt xem, tuổi, thời lượng | Đọc `ytInitialData` trong HTML của `youtube.com/results?gl=VN&hl=vi` [đã thử]. Kết quả không cá nhân hoá vì không đăng nhập, nên có thể khác thứ người dùng thấy. Tuổi video là chữ ("3 tháng trước") đổi ra ngày gần đúng. Nếu YouTube hiện trang đồng ý cookie hoặc đổi bố cục, lệnh báo `ytInitialData not found`. Không lấy được số người đăng ký kênh. |

Giới hạn script tự đặt: tối đa 30 truy vấn mỗi hạt giống mỗi nền tảng, nghỉ 0,3 giây giữa các lần gọi, dừng một nền tảng sau 3 lỗi liên tiếp. `--alphabet` với 3 nền tảng mất khoảng 30–40 giây cho mỗi hạt giống, nên chỉ dùng cho 1–3 hạt giống quan trọng nhất.

## Nguồn người dùng tự mở (phải đăng nhập hoặc chạy bằng JavaScript)

Skill không đọc được các trang này. Đưa link (lệnh `links` tạo sẵn) và nói rõ cần dán gì về; không có cũng làm tiếp được.

### Google Trends, bộ lọc YouTube Search

- Link: `trends.google.com/trends/explore?geo=VN&gprop=youtube&q=<từ>`. Tham số `gprop=youtube` tương ứng với việc đổi "Web Search" sang "YouTube Search" trên giao diện; mặc định Trends hiện dữ liệu tìm kiếm web, không phải YouTube.
- Xem gì: đường quan tâm 12 tháng (đang lên, đi ngang, theo mùa), và khung **Related queries → Rising** (truy vấn tăng nhanh, nơi bắt từ mới nổi). "Breakout" là tăng hơn 5.000% [chính thức, trang trợ giúp Trends].
- Nhờ dán: 5–10 dòng Rising, và nhận xét hình dạng đường (lên/xuống/theo mùa, đỉnh vào tháng nào).
- Giới hạn [chính thức, FAQ Trends https://support.google.com/trends/answer/4365533]: chỉ số 0–100 là **mức quan tâm tương đối trên mẫu**, không phải lượt tìm. Từ ít người tìm ở VN thường hiện "không đủ dữ liệu"; đó không có nghĩa là không ai tìm.
- Script không gọi được API của Trends: endpoint `trends/api/explore` trả 429 [đã thử], thư viện pytrends cũng hay bị chặn.

### TikTok

- **Creator Search Insights** (trong app: tìm "Creator Search Insights", hoặc TikTok Studio → công cụ nhà sáng tạo) [chính thức, newsroom TikTok 13/3/2024 https://newsroom.tiktok.com/creator-search-insights]: chủ đề người dùng đang tìm, lọc được **content gap** (tìm nhiều nhưng ít video đáp ứng). Lúc ra mắt chỉ có ở một số khu vực; chưa xác nhận đã có ở VN. Nhờ dán: các cụm có nhãn content gap thuộc niche của kênh.
- **TikTok One Creative Suite** (tên mới của TikTok Creative Center), mục Trends → Hashtags, chọn khu vực VN: `ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en?region=VN`. Hashtag, bài nhạc, creator, video đang lên, lọc theo ngành. Dữ liệu tải bằng JavaScript nên script không đọc được.
- **Keyword Insights** trong Creative Center [chính thức, https://ads.tiktok.com/help/article/keyword-insights]: chỉ trên máy tính, dữ liệu **lấy từ quảng cáo**, không gồm bài đăng tự nhiên. Có ích để biết cụm nào nhà quảng cáo hay dùng trong ngành (mỹ phẩm, đồ ăn, giáo dục), không phản ánh người xem tìm gì. Chưa xác nhận có khu vực VN.
- **Ô tìm kiếm trong app**: gõ từ gốc rồi xem gợi ý và mục "Người khác cũng tìm". Gần giống `expand --platform tiktok` nhưng đã cá nhân hoá theo tài khoản.

### YouTube Studio (của chính kênh)

- Analytics → **Research / Nghiên cứu**: "Your viewers' searches" và "Searches across YouTube", có **content gap** [chính thức]. Đây là nguồn tốt nhất cho kênh đã có người xem. Tên và vị trí tab có thể đổi vì Studio đang thiết kế lại từ 7/2026.
- Analytics → Reach → Traffic source: **YouTube search**: từ người xem đã gõ để tới video của kênh. Từ nào đã mang người xem tới mà kênh chưa có video riêng là ứng viên tốt nhất.
- Nhờ dán hoặc chụp màn hình; đừng đoán số liệu.

### Công cụ bên thứ ba

| Công cụ | Có gì | Lưu ý |
|---|---|---|
| vidIQ (có bản miễn phí) | Điểm từ khoá (lượt tìm ước lượng, cạnh tranh), trang từ khoá YouTube đang lên | Cần tài khoản hoặc extension. Con số là ước lượng của vidIQ, mỗi công cụ ra một số khác nhau [người làm nghề]. Dùng để **so các từ với nhau**, không trích như lượt tìm thật. |
| Ahrefs YouTube Keyword Tool, Keyword Tool, Morningfame, TubeBuddy | Lượt tìm ước lượng, gợi ý từ dài | Phần lớn trả phí hoặc giới hạn lượt; dữ liệu tiếng Việt thường mỏng [suy luận]. |
| Google Ads Keyword Planner | Lượt tìm ước lượng theo khoảng | Của **Google Search**, không phải YouTube; cần tài khoản Ads. |

Khi người dùng dán số từ các công cụ này, ghi rõ nguồn cạnh con số trong bảng (ví dụ "vidIQ: ~2,1K/tháng"), không cộng hay trộn số của hai công cụ.

## Khi script không chạy

- Gợi ý YouTube/Google lỗi: thử lại sau vài phút; nếu vẫn lỗi, dùng WebFetch trên đúng URL `suggestqueries` ở bảng trên.
- TikTok lỗi hoặc trả rỗng hết: nhiều khả năng bị chặn; nhờ người dùng gõ thử trong app và dán gợi ý.
- `serp` lỗi: dùng WebSearch với `site:youtube.com <từ khoá>` để biết sơ bộ ai đang chiếm kết quả, hoặc nhờ người dùng chụp trang kết quả.
