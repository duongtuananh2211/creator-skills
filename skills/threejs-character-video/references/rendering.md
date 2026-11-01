# Render và bàn giao

## 1. Render hoạt động thế nào

`npm run render -- <tập>` bật Vite trên `127.0.0.1:5199` (hoặc cổng trống kế tiếp), mở Chrome chạy ngầm tới `?ep=<tập>&render=1`, đợi mọi model, ảnh, audio tải xong, rồi với mỗi khung `i` gọi `renderAt(i / fps)`, lấy ảnh PNG của canvas và đẩy vào ffmpeg qua pipe. ffmpeg mã hoá H.264 (`-crf 18`, `yuv420p`, `+faststart`) và ghép đoạn audio tương ứng (AAC 192k). Không có bước nào phụ thuộc thời gian thực, nên máy chậm chỉ render lâu hơn chứ không rớt khung.

Tuỳ chọn:

| Cờ | Tác dụng |
|---|---|
| `--from 5 --to 9` | Chỉ render đoạn 5–9 s (audio cắt theo). Tên file thêm `-5.0-9.0` |
| `--scale 0.5` | Nửa độ phân giải để nháp. Đo trên tập demo: 6 giây video mất 2,6 s thay vì 4,2 s (khoảng 1,5 s là thời gian khởi động cố định), nên lợi nhiều hơn với tập dài |
| `--jpeg` | Truyền khung bằng JPEG thay PNG; nhanh hơn, chất lượng giảm chút trước khi H.264 nén lại |
| `--crf 16` | Chất lượng cao hơn (số nhỏ = nét hơn, file to hơn). 18 là đủ cho bản đưa vào CapCut |
| `--alpha` | Nền trong suốt → `.mov` ProRes 4444 (cần `background: 'transparent'` trong tập) |
| `--no-audio` | Không ghép audio |
| `--out đường/dẫn.mp4` | Đổi tên file |
| `--headful` | Mở cửa sổ Chrome thật (khi chạy ngầm không có GPU) |

Đo trên Mac M2 Pro: 1080×1920, một nhân vật, khoảng 60 khung/giây (18 giây video trong ~10 giây). Cảnh nhiều nhân vật, bóng đổ lớn, model nặng sẽ chậm hơn.

## 2. Lỗi thường gặp

| Hiện tượng | Nguyên nhân và cách sửa |
|---|---|
| `Không tìm thấy Chrome` | Cài Chrome, hoặc `CHROME_PATH=/đường/dẫn npm run render -- ...`, hoặc `npx @puppeteer/browsers install chrome-headless-shell@stable` rồi trỏ `CHROME_PATH` vào file vừa tải |
| `gpu` có `SwiftShader`/`llvmpipe`, render rất chậm | Chrome chạy ngầm không lấy được GPU (hay gặp trên Linux không màn hình, máy ảo). Thử `--headful`. Linux server: chấp nhận chậm, hoặc đặt `RENDER_SWIFTSHADER=1` để ép dùng CPU ổn định |
| `Trang không sẵn sàng` / hết thời gian | Model quá nặng hoặc lỗi JavaScript. Chạy `npm run dev`, mở `?ep=<tập>`, xem lỗi trên trang và trong console trình duyệt |
| Lỗi `không có clip "X"`, `morph "Y"` | Sai tên; thông báo lỗi liệt kê tên đúng. Chạy `npm run inspect -- <tập>` |
| Khung đen hoặc nhân vật biến mất | Camera ở trong model (kiểm tra `height`), `target` sai, hoặc NaN trong `update`. Chụp `still` ở thời điểm đó |
| Video không có tiếng | Cảnh báo `Không tìm thấy audio` → đường dẫn sai (tính từ `public/`). File `.m4a`/`.mp3`/`.wav` đều được; định dạng Chrome không giải mã được thì đổi sang WAV: `ffmpeg -i in.ogg out.wav` |
| Nhép miệng lệch tiếng | Audio có khoảng lặng bị cắt sau khi tạo `.srt`, hoặc fps của tập khác 30 mà CapCut ép lại. Giữ nguyên audio gốc |
| Nhân vật trượt chân khi đi | Tốc độ `moves` không khớp nhịp bước của clip: chỉnh `dur` hoặc `speed` của clip; clip không In Place thì đặt `inPlace: true` |
| Cổng 5199 bận | Vite tự lấy cổng kế tiếp; không cần làm gì |
| `ffmpeg lỗi` | Đọc dòng lỗi ngay phía trên. Ổ đĩa đầy, hoặc đường dẫn `--out` không ghi được |

Lần chạy đầu tiên sau `npm install`, Vite đóng gói lại thư viện và có thể tải lại trang một lần; script tự thử lại.

## 3. Kiểm tra trước khi giao

1. `npm run still -- <tập> --at <4–6 mốc>`: đầu mỗi cảnh, giữa cử chỉ lớn, câu cuối. Xem `renders/<tập>-sheet.png`.
2. Nhìn: nhân vật nằm trong khung và không bị cắt đầu, không xuyên sàn hay lơ lửng, bóng đổ hợp lý, vùng phụ đề trống.
3. Kiểm tra file: `ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,duration -of compact renders/<tập>.mp4`. Độ dài video và audio phải bằng nhau (lệch dưới một khung).
4. Nhép miệng và nhịp chỉ đánh giá được khi nghe: nhờ người dùng xem preview hoặc file MP4.

## 4. Bàn giao sang CapCut

- **Phụ đề**: nhập chính file `.srt` đã dùng cho tập (đã khớp audio), hoặc dùng phụ đề tự động của CapCut. Không in phụ đề vào render: để CapCut làm kiểu chữ đồng bộ với các video khác của kênh.
- **Vùng an toàn khung dọc**: giao diện TikTok, Reels, Shorts che khoảng 1/8 trên và 1/4–1/3 dưới, cùng một dải bên phải (nút thả tim, bình luận). Giữ mặt nhân vật ở khoảng 1/3 giữa trên của khung.
- **Nhạc nền**: thêm trong CapCut, không trộn vào `audio` của tập (nhép miệng sẽ bám cả theo nhạc).
- **Nền trong suốt**: render `--alpha` ra ProRes 4444 `.mov` để đặt nhân vật lên cảnh quay hoặc ảnh khác. File rất nặng (vài trăm MB mỗi phút ở 1080p). Thử nhập một đoạn ngắn vào CapCut trước để chắc phiên bản CapCut đang dùng giữ được kênh trong suốt; nếu không, cách chắc chắn hơn là render với nền ảnh ngay trong tập (`background: 'images/...'`).
- **Tốc độ khung**: giữ project CapCut cùng fps với tập (mặc định 30) để không bị lặp hay rớt khung.

## 5. Hiệu năng khi tập dài hoặc nặng

- Model trên ~20 MB: nén bằng `npx @gltf-transform/cli optimize in.glb out.glb --texture-compress webp` (giảm texture, nén lưới). Engine đọc được Draco và Meshopt.
- Bóng đổ: `lights: { shadows: false }` khi nền là ảnh và không cần bóng.
- Video dài (5–15 phút): render theo đoạn bằng `--from/--to` để kiểm tra dần, rồi render cả tập một lần cho bản cuối (đừng ghép các đoạn trong CapCut nếu không cần: dễ lệch một khung ở chỗ nối).
