# Chuẩn hoá tiếng Việt cho TTS

File này dùng ở bước 4. Mục tiêu: bản dán chỉ còn chữ tiếng Việt (hoặc từ tiếng Anh đã chủ ý giữ) và dấu câu, để giọng AI không phải đoán cách đọc.

**Vì sao tự chuẩn hoá.** [chính thức] ElevenLabs khuyên "viết số, từ viết tắt, ngày tháng và ký hiệu đầy đủ bằng chữ", và mọi ví dụ chuẩn hoá của họ là tiếng Anh ([ElevenLabs Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)). [chính thức] Vbee có chuẩn hoá tự động nhưng changelog ghi nhận lỗi với "10.000 tỷ đồng", "0 giờ 0 phút 0 giây", "°C", và từ viết tắt lạ bị đánh vần từng chữ cái ([Vbee Help Center](https://help.vbee.vn/llms-full.txt)). Chưa có tài liệu nào cho thấy công cụ nào đọc đúng "1,8 triệu" hay "23h47" hôm nay. Nghiên cứu ngày 29/10/2026; công cụ có thể đã cải thiện, nhưng viết sẵn thành chữ vẫn là cách chắc nhất.

Phần lớn quy tắc dưới đây là quy ước tiếng Việt thông thường, không phải tài liệu của hãng. Các cách phiên âm tiếng Anh ngoài ví dụ chính thức của Vbee là gợi ý, cần nghe thử.

## Nguyên tắc chọn cách đọc

1. **Đọc như creator nói ngoài đời.** "Một triệu tám" hay "một triệu tám trăm nghìn", "ca-pê-i" hay "kê-pi-ai", người dùng nói kiểu nào thì viết kiểu đó. Không biết thì chọn cách phổ biến nhất, ghi vào bảng cách đọc để họ sửa.
2. **Theo vùng của giọng.** Giọng Bắc: "nghìn", "linh", "cân". Giọng Nam: "ngàn", "lẻ", "ký". Giọng Huế: thường theo cách viết chuẩn, tuỳ người dùng.
3. **Nhất quán trong cả bài.** Đã chọn "ca-pê-i" thì cả bài đều là "ca-pê-i".
4. **Không đổi nghĩa.** "23h47" thành "mười một giờ bốn mươi bảy tối" vẫn đúng sự thật; "khoảng mười hai giờ" thì không.
5. **Đếm lại âm tiết sau khi chuẩn hoá.** "15/10/2025" có 5 ký hiệu nhưng thành hơn 10 âm tiết khi đọc.

## Bảng quy tắc và ví dụ

### Số và tiền

| Viết | Đọc | Ghi chú |
| --- | --- | --- |
| 1,8 triệu | một triệu tám trăm nghìn / một triệu tám / một phẩy tám triệu | Dấu phẩy là phần thập phân theo kiểu Việt. "Một triệu tám" tự nhiên nhất khi nói chuyện |
| 1.800.000đ | một triệu tám trăm nghìn đồng | Dấu chấm là phân cách hàng nghìn. Viết thành chữ để không bị đọc "một chấm tám trăm" |
| 2.5 (kiểu Anh) | hai phẩy năm | Kịch bản trộn kiểu Anh và kiểu Việt rất hay gây đọc sai; hỏi lại nếu không chắc là 2,5 hay 2.500 |
| 120 triệu | một trăm hai mươi triệu | |
| 10.000 | mười nghìn (Bắc) / mười ngàn (Nam) | |
| 15, 25, 45 | mười lăm, hai mươi lăm, bốn mươi lăm (khẩu ngữ: hai lăm, bốn lăm) | Hàng đơn vị 5 sau hàng chục đọc "lăm" |
| 21, 31 | hai mươi mốt, ba mươi mốt | Hàng đơn vị 1 sau "mươi" đọc "mốt" |
| 24 | hai mươi tư / hai mươi bốn | "Tư" phổ biến hơn khi nói |
| 105 | một trăm linh năm (Bắc) / một trăm lẻ năm (Nam) | |
| 1.005 | một nghìn không trăm linh năm | |
| 50k | năm mươi nghìn | "k" là nghìn |
| 2tr, 3 tỷ | hai triệu, ba tỷ | |
| 30% | ba mươi phần trăm | |
| 2,5% | hai phẩy năm phần trăm | |
| $500, 500 USD | năm trăm đô / năm trăm đô la Mỹ | Chọn theo giọng điệu: "đô" thân mật, "đô la Mỹ" trang trọng |
| x2 | gấp đôi | |

### Ngày, giờ, khoảng

| Viết | Đọc | Ghi chú |
| --- | --- | --- |
| 15/10/2025 | ngày mười lăm tháng mười năm hai nghìn không trăm hai mươi lăm | Khẩu ngữ: "năm hai không hai lăm" |
| 5/3 | ngày mùng năm tháng ba | Ngày 1–10 thường đọc "mùng" (hoặc "mồng") |
| tháng 4 | tháng tư | Không đọc "tháng bốn" |
| tháng 1, tháng 12 | tháng một, tháng mười hai | "Tháng giêng", "tháng chạp" chỉ khi kịch bản nói về âm lịch |
| năm 2019 | năm hai nghìn không trăm mười chín | |
| thứ 2, CN | thứ hai, chủ nhật | |
| 23h47 | hai mươi ba giờ bốn mươi bảy phút / mười một giờ bốn mươi bảy tối | Cách sau dễ nghe hơn, nghĩa như nhau |
| 7h30 | bảy giờ ba mươi / bảy rưỡi | |
| 0h | không giờ | Vbee từng có lỗi với "0 giờ" |
| 2-3 tháng | hai, ba tháng / hai đến ba tháng | Gạch nối có thể bị đọc "trừ" |
| 5–7 triệu | năm đến bảy triệu | |
| 2020–2023 | từ năm hai nghìn không trăm hai mươi đến năm hai nghìn không trăm hai mươi ba | Dài; cân nhắc khẩu ngữ "hai không hai mươi đến hai không hai ba" |

### Số thứ tự, đơn vị, số điện thoại

| Viết | Đọc | Ghi chú |
| --- | --- | --- |
| lần thứ 1, lần thứ 4 | lần thứ nhất, lần thứ tư | |
| hạng 1, hạng 2 | hạng nhất, hạng nhì | |
| top 1 | tốp một | |
| thế kỷ XXI | thế kỷ hai mươi mốt | Số La Mã luôn viết ra |
| 5km | năm ki-lô-mét / năm cây số | |
| 3kg | ba ki-lô-gam / ba cân (Bắc) / ba ký (Nam) | |
| 30m² | ba mươi mét vuông | |
| 38°C | ba mươi tám độ xê | Vbee từng không đọc được "°C" |
| 500ml | năm trăm mi-li-lít | |
| 0912 345 678 | không chín một hai, ba bốn năm, sáu bảy tám | Đọc theo nhóm, dấu phẩy giữa nhóm. Cân nhắc có nên đọc số điện thoại riêng tư trong video không |

### Từ viết tắt

Ba cách đọc: **viết ra đầy đủ**, **đánh vần chữ cái** (kiểu Việt hoặc kiểu Anh), hoặc **đọc như một từ**. Chọn theo cách creator nói.

| Viết | Đọc | Kiểu |
| --- | --- | --- |
| TP.HCM | Thành phố Hồ Chí Minh | Viết ra đầy đủ |
| HN, ĐH, SV, NV | Hà Nội, đại học, sinh viên, nhân viên | Viết ra đầy đủ |
| QL4H | Quốc lộ 4-hát → Quốc lộ bốn hát | Ví dụ chính thức của Vbee |
| VHVN | văn hóa Việt Nam | Ví dụ chính thức của Vbee; không thêm thì bị đọc "vê hát vê nờ" |
| KPI | ca-pê-i (kiểu Việt) / kê-pi-ai (kiểu Anh) | Đánh vần; hỏi creator hay nói kiểu nào |
| CEO | xi-i-ô | Đánh vần kiểu Anh, phổ biến |
| AI | ây-ai / a-i | Cả hai đều gặp |
| MC | em-xi | |
| IELTS | ai-eo | Đọc như một từ |
| COVID | cô-vít | Đọc như một từ |
| ASEAN | a-xê-an | Đọc như một từ |

Trên ElevenLabs, viết hoa còn mang nghĩa nhấn mạnh, nên từ viết tắt để nguyên chữ hoa dễ bị đọc lệch. Luôn đổi sang cách đọc đã chọn.

### Từ tiếng Anh

- **ElevenLabs:** [chưa kiểm chứng] giọng đa ngôn ngữ có thể đọc đúng từ tiếng Anh thông dụng nằm giữa câu tiếng Việt. Mặc định giữ chữ gốc (podcast, deadline), ghi vào bảng cách đọc kèm phiên âm dự phòng, và kiểm ở bước nghe thử. Nếu sai, thay bằng phiên âm kiểu Việt ngay trong câu hoặc thêm alias vào Pronunciation Dictionary.
- **Vbee:** [chính thức] nên phiên âm kiểu Việt. Viết thẳng phiên âm vào bản dán, rồi gợi ý thêm vào "Cách đọc" nếu từ lặp lại.

Quy tắc phiên âm chính thức của Vbee: s/x → "x"; sh và -tion → "s"; d/z → "d"; gi/j → "gi"; cụm phụ âm giữ phụ âm đầu và tách bằng gạch nối.

| Từ | Phiên âm kiểu Việt | Nguồn |
| --- | --- | --- |
| resort | ri-xót | Vbee chính thức |
| bad | bát-đ | Vbee chính thức |
| brain | b-rên | Vbee chính thức |
| six | xích-x | Vbee chính thức |
| deadline | đét-lai | Gợi ý, nghe thử |
| podcast | pót-cát | Gợi ý, nghe thử |
| content | con-ten | Gợi ý, nghe thử |
| feedback | phít-bách | Gợi ý, nghe thử |
| marketing | ma-két-tinh | Gợi ý, nghe thử |
| freelancer | phri-lan-xơ | Gợi ý, nghe thử |
| startup | xtát-ắp | Gợi ý, nghe thử |
| TikTok | tíc-tóc | Gợi ý, nghe thử |
| YouTube | diu-túp | Gợi ý, nghe thử |
| Facebook | phây-búc | Gợi ý, nghe thử |

Tên riêng (tên người, tên thương hiệu cá nhân, tên sản phẩm) thì hỏi creator đọc thế nào, đừng đoán.

### Trường hợp dễ đọc nhầm

| Viết | Có thể bị hiểu là | Cách viết an toàn |
| --- | --- | --- |
| 1/2 | ngày một tháng hai, hoặc một phần hai | Viết rõ theo nghĩa: "ngày mùng một tháng hai" hoặc "một nửa" |
| 2-3 | hai đến ba, hoặc hai trừ ba | "hai, ba" hoặc "hai đến ba" |
| Q1 | quận một, hoặc quý một | Viết ra theo nghĩa |
| k, ko | nghìn, hoặc "không" (kiểu viết tắt chat) | "nghìn" hoặc "không" |
| h | giờ | "giờ" |
| đ, tr | đồng, triệu | Viết ra |
| 1.800 | một nghìn tám trăm, hoặc một phẩy tám | Viết ra |
| / | trên, hoặc hoặc | "năm mươi nghìn một tháng" thay cho "50k/tháng" |
| &, + | và, cộng | Viết ra |
| vs | với, đấu với | Viết ra |

### Dấu thanh và mã hoá

[chưa kiểm chứng, kiến thức nền] Dùng Unicode dựng sẵn (NFC). Văn bản dán từ một số trình soạn thảo có thể ở dạng tổ hợp (NFD) hoặc bảng mã cũ (TCVN3, VNI), dễ làm mất dấu hoặc đọc sai. Giữ một kiểu đặt dấu trong cả bài ("hoà" hay "hòa"), vì từ điển phát âm của cả hai công cụ khớp theo chuỗi chính xác.

## Dấu câu là công cụ tạo nhịp

[chính thức] Vbee tự nghỉ sau `.` `,` `;` và xuống dòng; trên ElevenLabs v4 "dấu câu ảnh hưởng đáng kể tới cách đọc". Phần dưới là cách dùng thực tế [kinh nghiệm, cần nghe thử]:

| Dấu | Tác dụng | Dùng khi |
| --- | --- | --- |
| `.` | Nghỉ rõ, giọng hạ | Kết một ý. Tách câu dài thành hai câu là cách tạo nhịp chắc nhất |
| `,` | Nghỉ ngắn | Chia nhóm hơi trong câu; chuỗi phẩy quá dài làm giọng đều đều |
| `...` | Nghỉ, ngập ngừng, thêm sức nặng | ElevenLabs: trước chi tiết quan trọng. Vbee: chưa rõ có nghỉ thêm không, ưu tiên dấu chấm |
| `—` | Nghỉ ngắn, chuyển ý | ElevenLabs; được mô tả là kém nhất quán hơn tag |
| `?` | Lên giọng | Câu hỏi tu từ ở hook, nếu kịch bản đã có |
| `!` | Tăng năng lượng | Vui vẻ, hào hứng; tránh với thủ thỉ, trầm lắng, nghiêm túc |
| `:` | Nghỉ trước lời dẫn | Thay cho ngoặc kép khi dẫn lời ai đó |
| Xuống dòng | Nghỉ dài hơn dấu chấm | Giữa các nhịp kể, trước câu chốt |

Không đưa vào bản dán: ngoặc tròn, ngoặc nhọn, dấu sao, dấu thăng, gạch dưới, emoji, link, @tên tài khoản. Ngoặc kép không có hướng dẫn chính thức nào; an toàn nhất là dẫn lời bằng dấu hai chấm.
