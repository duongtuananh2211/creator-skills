---
name: script-review
description: Mở giao diện HTML cục bộ để người dùng review kịch bản hoặc bài viết theo từng đoạn (bôi đen chữ, nhận xét, đề xuất câu thay thế, đánh dấu đoạn ổn) rồi gửi phản hồi về cho agent sửa theo từng vòng. Dùng khi người dùng nói "review kịch bản trên giao diện", "mở trang review", "cho tôi bôi và góp ý từng đoạn", "review trên html", "review UI", "tôi muốn tự đọc và comment từng câu", kể cả khi họ chỉ đưa một file kịch bản và muốn góp ý trực tiếp trên đó. Nhận được bản kịch bản từ story-content-writer hoặc story-content-review đều dùng được. Không dùng để tự chấm điểm kịch bản (dùng story-content-review) hay viết kịch bản mới (dùng story-content-writer).
---

# Script review

Skill này mở một trang HTML trên máy người dùng để họ đọc kịch bản, bôi đen từng câu và góp ý ngay tại chỗ. Khi họ bấm "Gửi cho agent", phản hồi được lưu thành file, và agent sửa kịch bản theo từng nhận xét. Lý do làm bằng giao diện thay vì gõ trong chat: người dùng tự quyết câu nào cần sửa, câu nào giữ, và nhận xét luôn gắn với đúng đoạn chữ nên agent không phải đoán "câu thứ ba ở đoạn giữa" là câu nào.

Skill không chấm điểm và không viết mới. Người dùng muốn một bản đánh giá theo tiêu chí thì dùng `story-content-review`, muốn viết từ ý tưởng thì dùng `story-content-writer`. Đầu ra của hai skill đó đều đưa thẳng vào đây được.

Mọi thao tác đi qua `scripts/review_server.py` (chỉ dùng thư viện chuẩn của Python). `HELPER` là đường dẫn tuyệt đối tới script, nằm trong thư mục chứa file SKILL.md này. Chạy từ **thư mục gốc dự án của người dùng** để đường dẫn file kịch bản ngắn gọn và các file review nằm cạnh kịch bản:

```bash
HELPER="<thư-mục-skill>/scripts/review_server.py"
```

## Quy trình

### 1. Có kịch bản dưới dạng file

Máy chủ đọc file markdown, nên kịch bản chỉ có trong chat thì phải ghi ra file trước. Dùng một đường dẫn hợp lý như `scripts/<slug>.md` (hoặc thư mục kịch bản dự án đang dùng), nói rõ trong một dòng đường dẫn đã chọn rồi làm tiếp, không cần hỏi.

Trang hiển thị tốt các dạng: tiêu đề, đoạn văn, gạch đầu dòng, và bảng kịch bản `| Thời gian | Lời thoại | Hình ảnh / chữ trên màn hình | Âm tiết |` (mỗi dòng của bảng thành một thẻ, nhận xét gắn được vào đúng ô). Dàn ý YouTube có chương cũng dùng được.

### 2. Mở trang và chờ

```bash
python3 "$HELPER" serve scripts/ten-kich-ban.md
```

Chạy lệnh này bằng Bash với `run_in_background: true`. Máy chủ phải sống cho tới khi người dùng đọc xong, có thể vài chục phút, nên không thể chạy ở foreground; khi người dùng bấm gửi, máy chủ tự thoát và agent được báo là tác vụ nền đã kết thúc. Đọc dòng `REVIEW_URL http://127.0.0.1:<port>/` trong file output của tác vụ nền, gửi URL cho người dùng (trình duyệt thường tự mở) và dặn: đọc, bôi đen chỗ cần góp ý, xong thì bấm "Gửi cho agent". Sau đó dừng lượt và đợi. Đừng poll, vì mỗi lần poll chỉ tốn lượt mà không làm trang chạy nhanh hơn.

Các tuỳ chọn: `--no-open` (không tự mở trình duyệt), `--port N` (cố định cổng; trình duyệt lưu bản nháp theo cổng, nên mở lại cùng cổng thì bản nháp chưa gửi vẫn còn), `--timeout-min N` (mặc định 120 phút), `--round N`.

### 3. Khi được báo tác vụ nền kết thúc

Đọc output: dòng `FEEDBACK_SAVED <đường dẫn>` trỏ tới `<tên>.review-r<N>.json`. Mở file đó (và file `.md` cùng tên nếu muốn đọc tóm tắt). Nếu thấy `REVIEW_TIMEOUT` hoặc lỗi, báo người dùng và đề nghị mở lại; nếu họ đã gõ dở thì bản nháp còn trong trình duyệt nếu mở lại đúng cổng.

Cấu trúc file phản hồi: `verdict` ("duyệt" hoặc "sửa tiếp"), `overall` (nhận xét chung), `approved_blocks` (đoạn người dùng đã đánh dấu ổn), `comments` (mỗi nhận xét có `id`, `block_id`, `field` (tên cột nếu là ô trong bảng), `quote` (đoạn bôi đen nguyên văn), `type`, `note`, `suggestion`, kèm `context_before`/`context_after` để định vị).

### 4. Sửa theo từng nhận xét

Xử lý **mọi** nhận xét, không bỏ sót cái nào, vì người dùng sẽ kiểm tra từng cái ở vòng sau:

- `sửa`: áp dụng. Có `suggestion` thì dùng câu đó (chỉnh nhẹ cho khớp ngữ cảnh nếu cần); không có thì viết một bản sửa giữ đúng giọng của creator, đừng làm câu nghe "máy" hơn.
- `cắt`: bỏ đoạn đó và vá lại chỗ nối ở câu trước và sau để mạch không gãy.
- `hỏi`: trả lời trong ghi chú phản hồi. Chỉ đổi kịch bản khi câu trả lời kéo theo thay đổi.
- `giữ`: không đụng vào. Người dùng đánh dấu vậy thường để chặn agent sửa chỗ họ thích.
- `khác`: đọc `note` và tự diễn giải; nếu mơ hồ thì đánh trạng thái "cần bạn quyết" và hỏi lại, đừng đoán.
- Đoạn trong `approved_blocks`: giữ nguyên. Chỉ chạm vào khi một chỗ nối bắt buộc phải đổi, và nói rõ điều đó trong phần tóm tắt.
- `overall`: dùng để chọn hướng chung (nhịp, giọng) khi sửa, không coi là một nhận xét riêng cần "xử lý".

Đây là câu chuyện của chính người dùng, nên không bịa sự kiện, lời thoại, con số hay cảm xúc để làm cho bản sửa trơn tru. Thiếu chi tiết thì để chỗ trống nhìn thấy được `[cần bổ sung: …]` và hỏi người dùng. Nếu kịch bản có ngân sách thời lượng hoặc số âm tiết, tính lại sau khi sửa (khoảng 4,5–5,5 âm tiết mỗi giây là ước lượng, không phải số cứng) và báo nếu vượt.

### 5. Lưu bản mới và ghi phản hồi

Lưu bản sửa thành file mới cạnh bản cũ (ví dụ `<tên>.v2.md`), giữ nguyên bản cũ để người dùng so sánh. Ghi lời đáp cho từng nhận xét ra một file JSON tạm rồi gộp vào file review bằng lệnh `respond`, không tự sửa tay file review:

```json
{"c1": {"status": "đã sửa", "note": "Đổi thành 'bảng lương' theo đề xuất"},
 "c2": {"status": "giữ nguyên", "note": "Giữ vì ..."},
 "c3": {"status": "cần bạn quyết", "note": "Cần số tiền thật, đang để [cần bổ sung]"}}
```

```bash
python3 "$HELPER" respond scripts/ten-kich-ban.review-r1.json responses.json
```

`status` chỉ nhận ba giá trị: `đã sửa`, `giữ nguyên`, `cần bạn quyết`. Lệnh báo nếu còn nhận xét chưa trả lời.

Trong chat, tóm tắt theo dạng "nhận xét → đã đổi gì" (ngắn, mỗi nhận xét một dòng), nêu đường dẫn bản mới và những chỗ cần người dùng quyết.

### 6. Vòng tiếp theo hoặc kết thúc

- Verdict "sửa tiếp": đề nghị mở vòng sau. Chạy lại `serve` với bản mới và trỏ về file review vòng trước để trang hiện nhận xét cũ cùng lời đáp của agent (số vòng tự tăng):
  ```bash
  python3 "$HELPER" serve scripts/ten-kich-ban.v2.md --previous scripts/ten-kich-ban.review-r1.json
  ```
  Nếu vẫn sửa ngay trên cùng một file (không tạo `.v2`) thì không cần `--previous`, máy chủ tự tìm file review vòng trước.
- Verdict "duyệt": chúc mừng ngắn gọn và gợi ý bước sau, ví dụ `story-voice-script` để làm lời đọc voice-over (nếu đã cài), hoặc `story-hook-writer` để chọn tiêu đề và hook.

### 7. Khi không mở được trình duyệt

Nếu agent chạy trên máy từ xa hoặc qua SSH, máy chủ chỉ nghe ở `127.0.0.1` nên trình duyệt của người dùng không vào được trực tiếp. In URL ra và hướng dẫn chuyển cổng: `ssh -L <port>:127.0.0.1:<port> <máy-chủ>`, rồi mở `http://127.0.0.1:<port>/` trên máy mình (nên chạy `serve --port <port>` với cổng cố định để lệnh này khớp). Trong VS Code Remote thì cổng thường được tự chuyển tiếp.
