# creator-skills

Bộ agent skill cho Claude Code phục vụ công việc sáng tạo nội dung.

| Skill | Mô tả |
| --- | --- |
| [`google-flow-image-generation`](skills/google-flow-image-generation/SKILL.md) | Tạo ảnh bằng Google Flow qua Claude in Chrome, tải ảnh về và chuyển vào thư mục dự án. |

## Cài đặt bằng npx

Cần có Node.js (để chạy `npx`) và Python 3.

Cài vào dự án hiện tại (skill nằm ở `./.claude/skills/`):

```bash
npx skills add duongtuananh2211/creator-skills --skill google-flow-image-generation --agent claude-code
```

Cài cho mọi dự án (skill nằm ở `~/.claude/skills/`):

```bash
npx skills add duongtuananh2211/creator-skills --skill google-flow-image-generation --agent claude-code --global
```

Một số lệnh khác:

```bash
npx skills add duongtuananh2211/creator-skills --list   # xem các skill có trong repo
npx skills list                                          # xem các skill đã cài
npx skills update google-flow-image-generation           # cập nhật bản mới
npx skills remove google-flow-image-generation           # gỡ cài đặt
```

Bỏ `--agent claude-code` nếu muốn tự chọn agent khi cài, hoặc dùng `--agent '*'` để cài cho mọi agent được hỗ trợ.

### Cài thủ công

```bash
git clone https://github.com/duongtuananh2211/creator-skills.git
ln -s "$PWD/creator-skills/skills/google-flow-image-generation" ~/.claude/skills/
```

## google-flow-image-generation

### Yêu cầu

- Đã cài extension Claude in Chrome, đã kết nối với Claude Code và đã cấp quyền cho `flow.google.com`.
- Chrome đã đăng nhập tài khoản Google có quyền dùng Flow.
- Nên tắt tuỳ chọn hỏi nơi lưu mỗi lần tải trong Chrome (Settings → Downloads). Hộp thoại lưu file của hệ thống sẽ chặn bước tải tự động.

### Cách dùng

Nhờ Claude Code tạo ảnh như bình thường, ví dụ:

> Tạo ảnh bằng Flow: một chú mèo đội nón lá đứng giữa đồng lúa, phong cách Ghibli

Nếu bạn chưa nói rõ ảnh ngang (16:9) hay dọc (9:16), Claude sẽ hỏi lại trước khi tạo. Sau đó Claude sẽ:

1. mở dự án Flow ghi trong `skill-config.json`, hoặc tạo dự án mới nếu chưa có và lưu id vào file;
2. sinh ảnh với tỉ lệ đã chọn;
3. tải ảnh về `~/Downloads`;
4. chuyển ảnh sang thư mục của dự án, đặt tên dạng `20261023-115506-meo-doi-non-la-....png`.

### Cấu hình

File `skill-config.json` nằm ở thư mục gốc của dự án bạn đang làm (thư mục mở Claude Code). Mỗi dự án có cấu hình riêng, và lần đầu dùng skill sẽ tự tạo file này:

```json
{
  "flow_project_id": "",
  "output_dir": "./flow-images",
  "downloads_dir": "~/Downloads"
}
```

| Khoá | Ý nghĩa |
| --- | --- |
| `flow_project_id` | Id dự án trong `https://flow.google.com/project/{id}`. Để trống thì skill sẽ tự tạo dự án và điền vào. |
| `output_dir` | Thư mục lưu ảnh. Đường dẫn tương đối được tính từ thư mục chứa `skill-config.json`. |
| `downloads_dir` | Thư mục tải xuống của Chrome. |

Bạn có thể sửa file trực tiếp, nhờ Claude đổi, hoặc chạy script từ thư mục gốc của dự án:

```bash
SKILL=.claude/skills/google-flow-image-generation   # hoặc ~/.claude/skills/... nếu cài global
python3 $SKILL/scripts/flow_helper.py config                         # xem cấu hình hiện tại
python3 $SKILL/scripts/flow_helper.py set-project https://flow.google.com/project/<id>
python3 $SKILL/scripts/flow_helper.py set-output-dir assets/images
```

File này chứa id dự án Flow của riêng bạn. Nếu không muốn đưa nó lên git, hãy thêm `skill-config.json` vào `.gitignore` của dự án.
