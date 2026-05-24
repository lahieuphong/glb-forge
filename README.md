# GLB Forge

**GLB Forge** là project Python thuần để tạo file `.glb` procedural cho scene nhà cổ Tràng An/Ninh Bình.

Project không cần Blender và không cần thư viện ngoài. Code tự tạo hình học, normal, material, scene rồi ghi trực tiếp ra file GLB.

## Cấu trúc project

```text
glb-forge/
├─ pyproject.toml
├─ README.md
├─ output/
│  ├─ .gitkeep
│  └─ 35-Ninh-Binh/
│     └─ Nha-co-Trang-An.glb
├─ src/
│  └─ glb_forge/
│     ├─ __init__.py
│     ├─ catalog.py
│     ├─ scene.py
│     ├─ scene_writer.py
│     └─ scenes/
│        ├─ __init__.py
│        └─ trang_an_house.py
├─ examples/
│  └─ 04_trang_an_house/
│     └─ generate.py
└─ scripts/
   └─ generate_all.py
```

## Chạy nhanh

Đứng ở thư mục gốc `glb-forge`, chạy:

```bash
python3.12 examples/04_trang_an_house/generate.py
```

Hoặc dùng script tổng:

```bash
python3.12 scripts/generate_all.py
```

Kết quả:

```text
output/35-Ninh-Binh/Nha-co-Trang-An.glb
```

## Chạy kiểu package chuyên nghiệp

Tạo môi trường ảo:

```bash
python3.12 -m venv .venv
```

Kích hoạt trên macOS/Linux:

```bash
source .venv/bin/activate
```

Cài project ở chế độ editable:

```bash
pip install -e .
```

Sau đó chạy:

```bash
python examples/04_trang_an_house/generate.py
```

## Luồng tạo GLB

```text
src/glb_forge/scenes/trang_an_house.py
→ SceneMesh nhiều material
→ write_scene_glb()
→ output/35-Ninh-Binh/Nha-co-Trang-An.glb
```

## Quy ước quản lý output

Mỗi di tích được khai báo trong:

```text
src/glb_forge/catalog.py
```

Output dùng dạng:

```text
output/<ma-tinh>-<ten-tinh>/<Ten-di-tich>.glb
```

Ví dụ:

```text
output/35-Ninh-Binh/Nha-co-Trang-An.glb
```

## Scene Tràng An

File scene chính:

```text
src/glb_forge/scenes/trang_an_house.py
```

File chạy:

```text
examples/04_trang_an_house/generate.py
```

Scene hiện có:

```text
- nhà một tầng bố cục ngang, thấp, dạng nhà cổ 5 gian
- mái ngói đỏ nâu cũ, hiên rộng, cột gỗ, chân tảng đá
- nền đá cao, bậc tam cấp
- cửa gỗ kiểu bức bàn nhiều cánh
- khung gỗ, xà ngang, vì kèo gợi hình nhà cổ
- sân gạch đỏ cũ, chum nước, cây cau, hàng rào tre, tường đá thấp
- núi đá vôi xám và cây xanh phía sau gợi Tràng An
```

## Import mẫu

```python
from glb_forge import TRANG_AN_HERITAGE_HOUSE, write_scene_glb

scene = TRANG_AN_HERITAGE_HOUSE.create_scene()
write_scene_glb(scene, TRANG_AN_HERITAGE_HOUSE.output_path("output"))
```
