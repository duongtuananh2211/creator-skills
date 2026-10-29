# creator-skills

Bộ agent skill cho Claude Code phục vụ công việc sáng tạo nội dung.

| Skill | Mô tả |
| --- | --- |
| [`google-flow-image-generation`](skills/google-flow-image-generation/SKILL.md) | Tạo ảnh bằng Google Flow qua Claude in Chrome, tải ảnh về và chuyển vào thư mục dự án. |
| [`channel-profile`](skills/channel-profile/SKILL.md) | Dựng hồ sơ kênh khi khởi tạo dự án: niche, định vị, khán giả, người dẫn hoặc nhân vật đại diện, trụ cột nội dung, quy tắc; tuỳ chọn tra kênh cùng chủ đề trên web. |
| [`story-content-writer`](skills/story-content-writer/SKILL.md) | Biến chuyện thật của bạn thành kịch bản video ngắn, kịch bản YouTube dài, bài viết hoặc carousel kể chuyện. |
| [`story-hook-writer`](skills/story-hook-writer/SKILL.md) | Viết 8–10 phương án câu mở đầu, tiêu đề, chữ thumbnail, có gắn nhãn loại và lọc giật tít, mồi tương tác. |
| [`story-content-review`](skills/story-content-review/SKILL.md) | Chấm bản nháp theo 10 tiêu chí kể chuyện và kiểm tra riêng từng định dạng, trả về sửa đổi theo mức độ ưu tiên. |
| [`story-voice-script`](skills/story-voice-script/SKILL.md) | Chuyển kịch bản thành lời đọc dán thẳng vào ElevenLabs hoặc Vbee, theo giọng điệu chọn (vui vẻ, tâm sự, hồi hộp…). |

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

Cài cả bộ skill kể chuyện (kèm `channel-profile`) một lần:

```bash
npx skills add duongtuananh2211/creator-skills --skill channel-profile story-content-writer story-hook-writer story-content-review story-voice-script --agent claude-code
```

## Bộ skill kể chuyện cho mạng xã hội

Bốn skill dành cho creator xây thương hiệu cá nhân, kể chuyện của chính mình trên TikTok, Reels, Shorts, YouTube, Facebook, Threads, LinkedIn, X và carousel. Mỗi skill cài và dùng riêng được, nhưng dùng cùng nhau thì thành một vòng: viết, chọn câu mở đầu, chấm và sửa, rồi chuyển thành lời đọc cho giọng AI.

| Skill | Bạn nói gì | Bạn nhận được gì |
| --- | --- | --- |
| `story-content-writer` | "Viết kịch bản TikTok 60 giây từ chuyện mình nghỉ việc" | Kịch bản hoặc bài hoàn chỉnh theo khuôn của định dạng, cấu trúc đã chọn, 2–3 câu mở đầu thay thế |
| `story-hook-writer` | "Đặt tiêu đề và chữ thumbnail cho video này" | Bảng phương án theo loại câu móc, mỗi phương án được gắn 🟢/🟡/🔴, kèm 2–3 đề xuất và cách A/B test |
| `story-content-review` | "Review giúp bài này, đăng được chưa?" | Điểm /50, vấn đề xếp theo 🔴 nghiêm trọng → 🟠 cấu trúc → 🟡 câu chữ, có trích nguyên văn và câu viết lại |
| `story-voice-script` | "Chuyển kịch bản này thành voice script cho Vbee, giọng tâm sự" | Bản dán sạch theo đúng cú pháp công cụ (tag ElevenLabs v3/v4, `<break>` cho Flash, chỉ chữ và dấu câu cho Vbee), cài đặt gợi ý, bảng cách đọc, checklist nghe thử |

Nguyên tắc chung của cả bộ:

- **Không bịa chuyện của bạn.** Thiếu chi tiết thật thì skill hỏi lại hoặc để chỗ trống `[cần bổ sung: …]`, không tự thêm sự kiện, lời thoại hay con số.
- **Không mồi tương tác, không giật tít.** Các câu kiểu "comment 'có' để nhận…" hay tiêu đề hứa nhiều hơn nội dung đều bị lọc, vì Meta, LinkedIn và YouTube đều giảm phân phối hoặc phạt loại này.
- **Phân biệt bằng chứng.** Hướng dẫn chính thức của nền tảng được dẫn nguồn. Mẹo của người làm nghề và các con số ước lượng (như ngưỡng "Xem thêm", tốc độ nói 4,5–5,5 âm tiết/giây) được ghi rõ là ước lượng.

Kiến thức chi tiết của từng skill nằm trong thư mục `references/` của skill đó và chỉ được đọc khi cần.

### Hồ sơ kênh: bắt đầu từ `channel-profile`

Khi mở một dự án kênh mới, chạy `channel-profile` trước (ví dụ: "Tạo hồ sơ kênh: kênh YouTube, nhân vật Xa hình con rắn, giải thích vì sao người ta nghiện cờ bạc"). Skill phỏng vấn theo từng vòng ngắn, đề xuất 2–3 hướng niche và định vị, hỏi bạn có muốn tra các kênh cùng chủ đề trên web không, rồi ghi file `channel-profile.md` ở thư mục gốc dự án với 10 mục cố định:

1. Định vị · 2. Niche và góc nhìn · 3. Khán giả · 4. Người dẫn / nhân vật đại diện · 5. Trụ cột nội dung · 6. Định dạng và nhịp đăng · 7. Giọng văn và ngôn ngữ · 8. Quy tắc nội dung · 9. Đối thủ và khoảng trống · 10. Mục tiêu và chỉ số

Bốn skill `story-*` tự đọc file này trước mỗi lượt để bám đúng khán giả, xưng hô, giọng nhân vật, định dạng và giọng đọc AI của kênh. Muốn đổi gì (ví dụ đổi giọng AI sang Vbee), chỉ cần nhờ `channel-profile` cập nhật hồ sơ; skill chỉ sửa mục liên quan và ghi vào nhật ký thay đổi.

Lưu ý: hồ sơ không giữ đúng tên mục thì các skill khác sẽ không tìm thấy thông tin. Bạn sửa tay thoải mái, miễn giữ nguyên 10 tiêu đề đánh số.

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
