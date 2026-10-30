---
name: thumbnail-designer
description: Thiết kế thumbnail YouTube dài (16:9) cho creator thương hiệu cá nhân và kênh nhân vật đại diện. Bắt đầu từ điều người xem sẽ thắc mắc và cảm thấy (không phải "cho hình gì"), gom 10–15 thumbnail tham khảo từ 5 nguồn (video vượt trội của chính kênh, của kênh khác, kênh cùng định dạng khác chủ đề, thumbnail đã lưu, nguồn ngoài YouTube) bằng script tính điểm outlier, rút cơ chế của từng mẫu, phác 3 concept khác góc tiếp cận để Test & Compare, viết prompt ảnh cho Google Flow và chữ đè, rồi kiểm tra ảnh thật (phép thử 50% cho TV, cỡ điện thoại, ảnh xám, góc nhãn thời lượng, đặt cạnh feed đối thủ). Dùng khi người dùng nói "làm thumbnail cho video này", "thiết kế thumbnail", "ý tưởng thumbnail", "thumbnail này ổn chưa", "góp ý thumbnail", "tìm mẫu thumbnail tham khảo", "concept thumbnail để A/B test", "design a thumbnail", "review my thumbnail". Không dùng để viết tiêu đề hay chữ thumbnail từ đầu (dùng `story-hook-writer`), bấm tạo ảnh trong trình duyệt (dùng `google-flow-image-generation`), ảnh bìa video ngắn hay slide bìa carousel.
---

# Thumbnail designer

Skill này lo phần hình của "gói" YouTube: từ một combo tiêu đề và chữ thumbnail đã chọn, nó cho ra bộ tham khảo có phân tích, 3 concept khác nhau để thử, prompt ảnh, và bản kiểm tra ảnh thật. Skill không tự vẽ ảnh. Ảnh được tạo bằng `google-flow-image-generation` hoặc người dùng tự làm trong Canva, CapCut, Photoshop.

Ba nguyên tắc chạy xuyên suốt:

- **Thumbnail phải tự gây tò mò được.** Giao diện YouTube ngày càng cho thumbnail to và chữ tiêu đề nhỏ, nên mắt người xem lướt thumbnail trước, chỉ đọc tiêu đề khi đã chú ý. Vì vậy bắt đầu bằng câu hỏi "người xem sẽ thắc mắc gì, cảm thấy gì", rồi mới tới "cho hình gì". Mỗi chi tiết trên ảnh phải phục vụ thắc mắc hoặc cảm xúc đó.
- **Thắc mắc và cảm xúc phải có thật trong video.** Người làm nghề hay nói "thắc mắc và cảm xúc thắng sự liên quan". Skill dùng thắc mắc và cảm xúc, nhưng không đổi lấy sự thật: Test & Compare chọn phương án thắng theo thời gian xem chứ không theo CTR, YouTube phạt thumbnail lừa người xem, và với thương hiệu cá nhân thì lòng tin là tài sản chính.
- **Không bắt đầu từ con số 0, nhưng cũng không chép.** Kỹ năng ảnh hưởng nhiều nhất là tìm đúng thumbnail tham khảo và hiểu vì sao nó hiệu quả. Thứ được mượn là cơ chế (cách nó gợi thắc mắc hay cảm xúc), không phải bố cục, nhân vật hay chữ của người khác.

## Script hỗ trợ

`scripts/thumb_tools.py` (thư viện chuẩn Python, gọi `ffmpeg`, và `yt-dlp` để đọc dữ liệu công khai của YouTube; nếu máy không có `yt-dlp` thì script chạy qua `uvx yt-dlp`, không có cả hai thì hỏi người dùng trước khi cài). `HELPER` là đường dẫn tuyệt đối tới script, nằm trong thư mục chứa file SKILL.md này. Chạy từ thư mục gốc dự án người dùng:

```bash
HELPER="<thư-mục-skill>/scripts/thumb_tools.py"
R=thumbnails/<slug-video>/refs
python3 "$HELPER" channel @kenhcuaban --source internal --download $R     # video vượt trội của chính kênh
python3 "$HELPER" channel @kenhdoithu --source external --download $R     # của một kênh cùng chủ đề
python3 "$HELPER" channel @kenhmau --source model --download $R           # kênh cùng định dạng, khác chủ đề
python3 "$HELPER" search "từ khoá chủ đề" --outlier --download $R         # tìm kiếm, chấm theo trung vị từng kênh
python3 "$HELPER" fetch <link1> <link2> --download $R                     # thumbnail người dùng đã lưu
python3 "$HELPER" sheet $R                                                # ghép tất cả thành một ảnh để xem
python3 "$HELPER" check thumbnails/<slug>/candidates/a.png                # ảnh kiểm tra một ứng viên
python3 "$HELPER" sheet $R --highlight thumbnails/<slug>/candidates/a.png # ứng viên đặt giữa feed đối thủ
```

`channel` và `search` in JSON gồm lượt xem, trung vị của kênh và điểm `outlier` (lượt xem chia trung vị). Ảnh tải về tên dạng `<nguồn>-<lượt xem>-<id>.jpg`, kèm `refs.json` lưu tiêu đề, kênh, điểm. Mỗi lệnh `channel`/`search` mất vài giây; `--outlier` quét thêm từng kênh nên lâu hơn. Nếu YouTube trả lỗi 429 thì đợi vài phút rồi chạy lại, đừng chạy dồn dập. Xem ảnh `sheet` và `check` bằng Read.

## Đọc reference nào, khi nào

- `references/principles.md`: luôn đọc trước bước 4. Vì sao thumbnail phải tự gây tò mò, phép thử 50% cho TV, ba sửa nhanh, thông số chính thức, kinh nghiệm người làm nghề, ranh giới trung thực, và checklist dùng ở bước 6.
- `references/references-and-mechanisms.md`: đọc ở bước 3 và 4. Năm nguồn tham khảo và cách lấy, giới hạn của điểm outlier, mẫu phân tích, thư viện cơ chế kèm ví dụ cho kênh người thật và kênh nhân vật, cách chuyển cơ chế sang video của mình.
- `references/image-prompts.md`: đọc ở bước 5 và 7. Cách viết prompt ảnh thumbnail cho Flow, giữ nhân vật nhất quán, quy cách chữ đè tiếng Việt, xuất file.
- Nếu đã cài `story-hook-writer`: `story-hook-writer/references/titles-thumbnails.md` (combo tiêu đề, chữ thumbnail, 30 giây đầu, Test & Compare) và `policy-redflags.md` (mẫu thumbnail đỏ).

## Hồ sơ kênh (nếu có)

Trước bước 1, kiểm tra file `channel-profile.md` ở thư mục gốc dự án. File này do skill `channel-profile` tạo. Nếu có, đọc và dùng:

- **Khán giả** (mục 3): họ đã biết gì, để đặt thắc mắc đúng tầm.
- **Người dẫn / nhân vật đại diện** (mục 4): người thật hay nhân vật; với nhân vật, phần "nhận diện hình ảnh" (bảng màu, dáng, biểu cảm cố định, đạo cụ, kiểu thumbnail, reference sheet) là nguồn để viết prompt nhất quán.
- **Định dạng** (mục 6): để chọn kênh "cùng định dạng, khác chủ đề" ở nguồn tham khảo thứ ba.
- **Quy tắc nội dung** (mục 8): những gì không được hứa, không được cho thấy (ví dụ kênh về cờ bạc không cho thấy cảnh thắng tiền hấp dẫn).
- **Đối thủ** (mục 9): link kênh để chạy `channel --source external`.

Những gì hồ sơ đã trả lời thì đừng hỏi lại. Nếu yêu cầu lượt này khác hồ sơ, làm theo yêu cầu hiện tại và nhắc một dòng. Không có file thì làm như bình thường.

## Quy trình

### 1. Nắm video và lời hứa

Cần biết:

- **Tiêu đề** (đã chọn hoặc tạm) và **chữ thumbnail** nếu đã có. Chưa có tiêu đề thì gợi ý chạy `story-hook-writer` trước, hoặc xin một tiêu đề tạm, vì thumbnail và tiêu đề phải bổ sung cho nhau.
- **Phần thưởng** của video trong một câu, và **những hình ảnh có thật** trong video dùng được cho thumbnail: cảnh, đồ vật, con số, biểu cảm, khoảnh khắc chuyển biến, kèm mốc thời gian nếu có kịch bản.
- **Ai xuất hiện**: người dẫn thật (có ảnh chụp không), nhân vật minh hoạ, hay không có người.
- **Kênh của người dùng** (link hoặc @handle) để lấy video vượt trội của chính kênh, nếu kênh đã có khoảng 10 video trở lên.
- **Tỉ lệ xem trên TV**: Analytics → Audience → Device type. Không bắt buộc; nếu người dùng không biết, cứ áp phép thử 50% vì nó rẻ và hiếm khi làm hại.

Nếu người dùng dán kịch bản hay bản nháp, tự rút ra các điều trên rồi tóm 2–3 dòng để họ kiểm tra. Thiếu gì thì hỏi gộp một lần. Không hỏi những thứ không làm thay đổi kết quả; ghi giả định một dòng rồi làm tiếp.

Nếu người dùng chỉ đưa một thumbnail có sẵn để góp ý, nhảy tới bước 6 (vẫn cần biết tiêu đề và video nói gì).

### 2. Thắc mắc và cảm xúc trước, hình sau

Viết 3–5 cặp **thắc mắc + cảm xúc** mà thumbnail có thể gợi ra khi người xem chưa đọc tiêu đề. Mỗi cặp gắn với một chỗ có thật trong video:

```
1. Thắc mắc: "Con rắn này đang đặt cược cái gì?"  · Cảm xúc: căng thẳng, lo cho nhân vật
   Có trong video: cảnh Xa đặt cả tổ trứng lên bàn (phút 3:10)
```

Thắc mắc phải cụ thể đủ để người xem gọi tên được (khoảng trống có điểm bám), và video phải trả lời nó. Cảm xúc thường dùng: tò mò, mới lạ, căng thẳng hay nguy hiểm, đồng cảm hay tổn thương, ngưỡng mộ hay khao khát, buồn cười, tin cậy. Cặp nào video không trả được thì bỏ.

### 3. Gom 10–15 tham khảo từ 5 nguồn

Lưu vào `thumbnails/<slug-video>/refs/`. Đọc `references/references-and-mechanisms.md` để biết cách chọn từ khoá, kênh mẫu và giới hạn của điểm outlier. Tóm tắt:

1. **Video vượt trội của chính kênh**: `channel <kênh của người dùng> --source internal`.
2. **Video vượt trội của kênh khác** cùng chủ đề: `search "<từ khoá>" --outlier` và `channel <đối thủ trong mục 9> --source external`. Người dùng có YouTube Studio → Trends → Breakout videos thì nhờ họ chụp hoặc dán link vào.
3. **Kênh cùng định dạng, khác chủ đề**: đề xuất 2–3 kênh (ví dụ kênh giải thích bằng hoạt hình nếu kênh người dùng cũng vậy) và hỏi người dùng duyệt, rồi `channel --source model`.
4. **Thumbnail người dùng đã lưu** (playlist riêng hay link): `fetch`.
5. **Nguồn ngoài YouTube** (poster phim, bìa sách, bìa album, biển quảng cáo): nhờ người dùng thả ảnh vào thư mục `refs/`. Skill không tự lấy ảnh từ các trang này.

Không cần đúng chủ đề video; đang gom **cách làm**, không gom nội dung. Chạy `sheet` rồi xem một lượt. Ít hơn 10 mẫu vẫn làm tiếp được, nhưng nói rõ là bộ tham khảo mỏng. Nếu người dùng không muốn tra web, làm bước 4 với những mẫu họ đưa.

### 4. Rút cơ chế của từng mẫu

Chọn 6–8 mẫu đáng chú ý nhất (không chỉ những mẫu điểm cao) và với mỗi mẫu trả lời ba câu: nó khiến mình **thắc mắc** gì, **cảm thấy** gì, và **bằng cách nào** (cơ chế). Câu thứ ba là quan trọng nhất. Đối chiếu với thư viện cơ chế trong reference, nhưng đừng ép mẫu vào một ô có sẵn nếu cơ chế của nó mới.

Rồi hỏi: cơ chế này áp vào video của mình thì trông thế nào, và có phục vụ cặp thắc mắc + cảm xúc nào ở bước 2 không? Ghi vào bảng:

| # | Mẫu (nguồn, điểm) | Thắc mắc | Cảm xúc | Cơ chế | Áp vào video này |
|---|---|---|---|---|---|
| 3 | model-…-TOHQ… (kênh mẫu, ×11.5) | Intro "killer" trông thế nào? | tò mò | Một vật thể duy nhất phát sáng giữa nền xám, người chỉ tay vào nó | Tổ trứng phát sáng giữa bàn cược tối, Xa nhìn nó |

### 5. Phác 3 concept khác góc tiếp cận

Ba concept phải khác nhau về **thắc mắc, cảm xúc hoặc cơ chế**, không chỉ khác màu hay chữ, vì YouTube khuyên các phương án Test & Compare khác nhau rõ rệt. Mỗi concept gồm:

- **Ý tưởng một câu**, cặp thắc mắc + cảm xúc (từ bước 2), cơ chế mượn từ mẫu nào.
- **Nhân vật chính** (một thứ duy nhất mắt thấy đầu tiên) và cách làm nó nổi: màu tách khỏi nền, kích thước, viền, nhãn chữ.
- **Bố cục**: nửa trên chứa gì (phải đủ để hiểu chủ đề khi nửa dưới bị che), nửa dưới chứa gì, góc dưới bên phải để trống cho nhãn thời lượng. Bỏ mọi thứ không phục vụ ý tưởng.
- **Chữ**: 3–5 phương án, mỗi phương án 0–4 từ, không lặp tiêu đề, đặt ở 1/3 trên nếu được. Một phương án không chữ cũng hợp lệ.
- **Có trong video**: cảnh hoặc mốc thời gian chứng minh hình ảnh và cảm xúc là thật.
- **Prompt ảnh** theo `references/image-prompts.md`.
- **Mức**: 🟢 ổn · 🟡 cần người dùng xác nhận (cảnh này có thật không, biểu cảm có quá tay không) · 🔴 hình hoặc cảm xúc video không có. Concept 🔴 phải sửa hoặc thay trước khi đưa ra.

### 6. Kiểm tra

Trên giấy, chạy checklist trong `references/principles.md` cho từng concept trước khi tạo ảnh. Khi đã có ảnh (từ Flow, từ người dùng, hay thumbnail cũ cần góp ý):

1. `check <ảnh>` rồi xem: ảnh gốc, chỉ nửa trên (TV), nhãn thời lượng và thanh tiến trình, ảnh xám, hai cỡ điện thoại thật.
2. `sheet refs --highlight <ảnh>` để xem ứng viên đứng giữa feed đối thủ: nó có khác hẳn về màu nền, bố cục, độ sáng không, hay hoà lẫn vào?
3. Ghi kết quả theo checklist, mỗi mục ✅ hoặc ⚠️ kèm cách sửa cụ thể ("bỏ ba thanh vịn hồ bơi", "đổi áo nhân vật sang đỏ để tách khỏi nền xanh", "đưa chữ lên 1/3 trên").

Đánh giá hình là phán đoán, không phải đo lường. Nói rõ chỗ nào chắc (chữ không đọc được ở cỡ 168 px) và chỗ nào là gu.

### 7. Bàn giao để tạo ảnh và thử

- **Tạo ảnh**: nếu đã cài `google-flow-image-generation`, đưa prompt của từng concept sang skill đó với tỉ lệ ngang 16:9 và `--output-dir thumbnails/<slug>/candidates`, mỗi concept 2–4 ảnh. Mặc định tạo ảnh **không chữ** rồi đè chữ trong Canva/CapCut/Photoshop theo quy cách trong `image-prompts.md`, vì AI hay viết sai dấu tiếng Việt. Ảnh về thì quay lại bước 6.
- **Xuất file** theo thông số chính thức trong `principles.md`.
- **Test & Compare**: đưa 3 concept (hoặc 3 cặp tiêu đề + thumbnail) vào thử. Phương án thắng là phương án có thời gian xem cao nhất; đừng đổi thumbnail giữa lúc đang thử. Kết quả "Performed same" hay "Inconclusive" là bình thường.

## Lưu kết quả

Ghi `thumbnails/<slug-video>/brief.md` (tóm tắt video, các cặp thắc mắc + cảm xúc, bảng phân tích tham khảo, 3 concept, prompt, kết quả kiểm tra). Thư mục: `refs/` (ảnh tham khảo + `refs.json`), `candidates/` (ảnh tạo ra, kèm `*-check.jpg` cạnh từng ảnh), còn `contact-sheet.jpg` và `feed-check.jpg` nằm ngay trong `thumbnails/<slug-video>/`. Nếu dự án là git repo, nhắc một lần rằng `refs/` chứa thumbnail của người khác, chỉ dùng để tham khảo nội bộ, có thể thêm vào `.gitignore`.

## Định dạng trả lời

Mở đầu 2–3 dòng: video, lời hứa, ai xuất hiện, giả định. Tiếp theo là bảng phân tích tham khảo (bước 4), rồi 3 concept dạng danh sách đánh số:

```
1. [Phá kỳ vọng · mượn từ mẫu #3] 🟢 Tổ trứng có thật ở phút 3:10
   Thắc mắc / cảm xúc: "Nó đặt cược cả tổ trứng à?" · căng thẳng
   Nhân vật chính: tổ trứng phát sáng vàng giữa bàn cược tối
   Bố cục: trứng và mặt Xa ở nửa trên; tay Xa đẩy trứng ở nửa dưới; góc dưới phải trống
   Chữ: TẤT TAY · CẢ TỔ? · (không chữ)
   Prompt: …
```

Cuối cùng là **Đề xuất**: concept nào nên làm trước và vì sao (gắn với khán giả và feed đối thủ), 3 phương án nên đưa vào Test & Compare, và những điểm cần người dùng xác nhận.

Ví dụ trên chỉ minh hoạ định dạng. Khi làm thật, mọi cảnh, con số và nhân vật phải lấy từ video của người dùng.

## Những chỗ dễ sai

- **Bắt đầu bằng "cho hình gì".** Kết quả là thumbnail đúng chủ đề nhưng không gây tò mò, kiểu bày đồ vật liên quan ra rồi thôi. Quay lại bước 2.
- **Chép mẫu thay vì mượn cơ chế.** Bố cục, nhân vật, chữ của kênh khác không được bê sang. Nếu concept nhìn như bản sao của một mẫu, đổi cách thể hiện.
- **Coi điểm outlier là bằng chứng.** Video vượt trội có thể nhờ chủ đề, thời điểm hay tiêu đề, không phải nhờ thumbnail. Điểm outlier chỉ để lọc mẫu đáng xem.
- **Cái quan trọng nằm ở nửa dưới.** Trên TV, nửa dưới bị che ở trang chủ và mục đề xuất. Chữ và nhân vật chính nên nằm ở nửa trên.
- **Nhồi chi tiết vì "ngoài đời nó như vậy".** Thứ gì không giúp ý tưởng thì đang làm loãng nó. Thumbnail không phải ảnh chụp tài liệu.
- **Ba concept chỉ khác màu chữ.** Test & Compare khó ra kết quả khi các phương án quá giống nhau.
- **Biểu cảm hay cảnh không có trong video.** Mặt khóc, cháy nổ, người hay vật không xuất hiện trong video là 🔴. Xem `story-hook-writer/references/policy-redflags.md`.
- **Con số hiệu quả không có nguồn.** Đừng hứa "thumbnail này tăng CTR 81%". Không ai đoán trước được phương án thắng; đó là lý do phải thử.
