# Nhân vật: nguồn, chuẩn bị, nhép miệng

Engine nhận `.glb`, `.gltf` (kể cả nén Draco, Meshopt) và `.fbx`. GLB là định dạng nên dùng: một file gồm lưới, vật liệu, texture, xương, animation, blendshape. Luôn chạy `npm run inspect -- models/<file>` trước khi viết tập.

Các dịch vụ bên thứ ba dưới đây thay đổi tính năng, giá và điều khoản thường xuyên; trước khi khuyên người dùng trả tiền hay dùng thương mại, mở trang của dịch vụ để kiểm tra lại.

## 1. Chọn hướng khi chưa có nhân vật

| Người dùng có gì | Hướng | Ghi chú |
|---|---|---|
| Chưa có gì, cần thử nhanh | Robot mẫu, hoặc nhân vật có sẵn trên Mixamo | Mixamo có sẵn nhân vật đã rig và kho animation |
| Ảnh nhân vật 2D (vẽ tay, ảnh tạo bằng Flow) | Dịch vụ tạo 3D từ ảnh (Meshy, Tripo, Hunyuan3D…) → tự rig hình người → animation Mixamo | Chất lượng mặt và tay thay đổi nhiều; thường không có blendshape miệng |
| Muốn nhân vật anime, có biểu cảm | VRoid Studio | Có sẵn blendshape miệng, mắt; rig khác Mixamo (mục 3) |
| Có hoạ sĩ 3D hoặc tự làm Blender | Xuất GLB từ Blender (mục 4) | Kiểm soát được blendshape và tên xương |
| Nhân vật không phải người (rắn, cá, quả cầu) | Rig + animation trong Blender, hoặc chuyển động thủ tục bằng code (mục 6) | Mixamo chỉ tự rig hình người hai tay hai chân |

Nhân vật đại diện của kênh nên giữ nhất quán qua mọi tập: một file model cố định, đặt ở `public/models/`, các tập đều trỏ vào nó.

## 2. Mixamo (Adobe)

Miễn phí với tài khoản Adobe. Có nhân vật dựng sẵn, tự rig nhân vật hình người bạn tải lên, và kho animation lớn (idle, nói chuyện, vẫy tay, gật đầu, đi, ngồi…).

Tải về:

- **Nhân vật**: chọn nhân vật (hoặc tải model của bạn lên để tự rig), Download → Format **FBX Binary**, Pose **T-pose**, có skin. Đặt vào `public/models/`.
- **Animation**: chọn animation trên đúng nhân vật đó, Download → FBX Binary, **Without Skin** (file nhẹ, chỉ có chuyển động), 30 fps. Animation đi lại thì tick **In Place**. Đặt vào `public/anims/`.

Dùng trong tập:

```ts
xa: {
  model: 'models/xa.fbx',
  animations: { idle: 'anims/Idle.fbx', talk: 'anims/Talking.fbx', wave: 'anims/Waving.fbx' },
}
```

Model FBX từ Mixamo tính bằng centimet; engine tự thu về 1,7 m và cảnh báo, đặt `height` để chỉnh đúng. Mọi animation Mixamo dùng cùng tên xương nên khớp với nhau (`inspect` báo `matched: 53/53` hoặc tương tự). Nhiều file FBX nặng; khi đã ổn định, có thể gộp nhân vật và animation thành một GLB trong Blender (mục 4) cho tải nhanh hơn.

Nhân vật của Mixamo không có blendshape miệng: nhép miệng bằng `bone: 'Head'` (gật nhẹ) hoặc thêm shape key trong Blender.

## 3. Animation và rig không khớp

Engine đổi tên track theo tên xương (bỏ tiền tố `mixamorig`, dấu `:`, chữ hoa thường) và quy đổi tỉ lệ dịch chuyển của hông. Engine **không** retarget giữa hai bộ xương khác cấu trúc hay khác tư thế gốc.

- `matched` gần bằng tổng: ổn.
- `matched` thấp hoặc 0: hai rig khác nhau. Ví dụ VRoid dùng tên `J_Bip_C_Hips`, rig tự làm dùng `spine.001`. Cách xử lý, từ dễ tới khó:
  1. Tải model lên Mixamo để rig lại theo chuẩn Mixamo (mất blendshape VRoid nếu xuất qua FBX không cẩn thận; kiểm tra lại bằng `inspect`).
  2. Retarget trong Blender bằng add-on retarget (ví dụ Rokoko Studio Live có chức năng retarget miễn phí), rồi xuất GLB có sẵn animation.
  3. Dùng animation đi kèm model (nhiều model tạo bằng AI có sẵn vài clip).
- Clip làm méo lưới dù khớp tên: tư thế gốc khác nhau (A-pose với T-pose). Retarget trong Blender.

## 4. Xuất GLB từ Blender

File → Export → glTF 2.0 (.glb):

- Include: Selected Objects nếu file Blender có nhiều thứ ngoài nhân vật.
- Transform: **+Y Up** (mặc định).
- Data → Mesh: Apply Modifiers; **Shape Keys** bật (để có blendshape); Data → Armature: Export Deformation Bones Only nếu rig có nhiều xương điều khiển.
- Animation: bật; mỗi Action thành một clip mang tên Action. Dùng NLA hoặc "Actions" mode để xuất nhiều clip. Đặt tên Action rõ ràng (`idle`, `talk`, `wave`).
- Áp scale trước khi xuất (Object → Apply → All Transforms) để model cao đúng mét.

Mặc định nhân vật nhìn về `-Y` trong Blender, tương ứng `+Z` trong Three.js: đúng hướng camera mặc định của engine.

## 5. Quyền sử dụng

- Ghi nguồn mọi model, animation, texture vào `public/models/CREDITS.md` (tên, tác giả, giấy phép, link).
- Robot mẫu: CC0, dùng thoải mái.
- Mixamo: Adobe cho phép dùng nhân vật và animation trong dự án thương mại; không được phân phối lại file Mixamo dưới dạng tài nguyên rời. Đọc lại điều khoản hiện hành của Adobe khi người dùng làm kênh kiếm tiền.
- Model tải từ Sketchfab, kho miễn phí: kiểm tra giấy phép từng model (CC-BY cần ghi tên tác giả trong mô tả video; CC-NC không dùng cho kênh kiếm tiền).
- Model tạo bằng AI: quyền thương mại tuỳ gói đăng ký của dịch vụ.
- Không dựng nhân vật thuộc bản quyền người khác (nhân vật hoạt hình, game, người nổi tiếng) để đăng lên kênh.

## 6. Nhân vật không phải người

Mixamo không rig được rắn, cá, sinh vật nhiều chân. Hai cách:

**Rig và animation trong Blender**: chuỗi xương dọc thân, animation uốn lượn, xuất GLB có clip. Cách này đẹp nhất và tái sử dụng được.

**Chuyển động thủ tục bằng code** khi model đã có chuỗi xương nhưng chưa có animation. Ví dụ con rắn có xương `Spine_0` … `Spine_N`:

```ts
update({ characters }, t) {
  const snake = characters.xa;
  for (let i = 0; i < 12; i++) {
    const b = snake.bone(`Spine_${i}`);
    if (b) b.rotation.y = Math.sin(t * 3 - i * 0.6) * 0.25 * (i / 12);   // sóng chạy dọc thân
  }
  const head = snake.bone('Head');
  if (head) head.rotation.x = -0.15 + Math.sin(t * 1.2) * 0.05;          // ngẩng đầu, thở
},
```

Giá trị đặt tuyệt đối theo `t` (không cộng dồn) để render lặp lại được. Model không có xương nào thì vẫn làm được chuyển động cả khối (nhún, lắc, xoay) qua `characters.xa.holder`, hoặc `moves`.

## 7. Nhép miệng và biểu cảm

Engine nhép miệng theo **độ to** giọng đọc, đủ cho nhân vật hoạt hình. Thứ tự ưu tiên khi chọn cách:

1. **Blendshape miệng có sẵn.** Tên thường gặp:
   - Bộ ARKit (52 blendshape, nhiều model tạo bằng các công cụ nhân vật dùng): `jawOpen`, `mouthFunnel`, `mouthSmileLeft`/`Right`, `eyeBlinkLeft`/`Right`, `browInnerUp`.
   - Bộ viseme kiểu Oculus: `viseme_aa`, `viseme_O`, `viseme_E`…; dùng `viseme_aa` cho mở miệng.
   - VRoid (khi xuất ra glTF/GLB thường): dạng `Fcl_MTH_A`, `Fcl_EYE_Close`, `Fcl_ALL_Joy`; kiểm tra bằng `inspect` vì tên thay đổi theo cách xuất.
   - Tự đặt: `mouthOpen`, `MouthOpen`, `A`.
   Phối nhiều morph cho tự nhiên hơn: `morph: { jawOpen: 0.7, mouthFunnel: 0.2 }`.
2. **Xương hàm** (`Jaw`, `jaw`, `mixamorigJaw` nếu rig có): `bone: 'Jaw', axis: 'x', amount: 0.3`. Thử dấu và trục.
3. **Không có miệng**: gật đầu rất nhẹ theo giọng (`bone: 'Head', amount: 0.08–0.12`) kết hợp một clip "talking" để thân người cử động. Người xem chấp nhận tốt với nhân vật cách điệu, nhất là khi camera không cận mặt.

Biểu cảm (`face`) dùng blendshape như vui, buồn, ngạc nhiên. Model chỉ có vài biểu cảm thì đẩy cảm xúc bằng cử chỉ thân người và góc máy thay vì mặt.

Thêm blendshape cho model chưa có: Blender → Shape Keys → thêm key "jawOpen", chỉnh lưới miệng mở, xuất GLB có Shape Keys. Việc này cần người biết Blender; đừng hứa với người dùng là skill tự làm được.
