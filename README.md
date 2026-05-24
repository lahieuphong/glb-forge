# GLB Forge

**GLB Forge** là project Python thuần để học và tạo file `.glb` bằng code.
Project bắt đầu từ mesh đơn giản như cube, pyramid, triangle, rồi nâng dần lên scene procedural phức tạp như nhà cổ Tràng An/Ninh Bình.

Không cần Blender, không cần thư viện ngoài. Code tự tạo mesh, normal, material, scene rồi ghi trực tiếp ra file GLB.

## Cấu trúc project

```text
glb-forge/
├─ pyproject.toml
├─ README.md
├─ .gitignore
├─ output/
│  ├─ .gitkeep
│  ├─ cube.glb
│  ├─ pyramid.glb
│  ├─ custom_triangle.glb
│  └─ trang_an_heritage_house.glb
├─ src/
│  └─ glb_forge/
│     ├─ __init__.py
│     ├─ mesh.py
│     ├─ glb_writer.py
│     ├─ scene.py
│     ├─ scene_writer.py
│     ├─ shapes/
│     │  ├─ __init__.py
│     │  ├─ cube.py
│     │  └─ pyramid.py
│     └─ scenes/
│        ├─ __init__.py
│        └─ trang_an_house.py
├─ examples/
│  ├─ 01_cube/
│  │  └─ generate.py
│  ├─ 02_pyramid/
│  │  └─ generate.py
│  ├─ 03_custom_mesh/
│  │  └─ generate.py
│  └─ 04_trang_an_house/
│     └─ generate.py
└─ scripts/
   └─ generate_all.py
```

## Chạy nhanh

Đứng ở thư mục gốc `glb-forge`, chạy scene số 04:

```bash
python examples/04_trang_an_house/generate.py
```

Kết quả:

```text
output/trang_an_heritage_house.glb
```

Chạy tất cả ví dụ:

```bash
python scripts/generate_all.py
```

Kết quả:

```text
output/cube.glb
output/pyramid.glb
output/custom_triangle.glb
output/trang_an_heritage_house.glb
```

## Chạy kiểu package chuyên nghiệp

Tạo môi trường ảo:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Cài project ở chế độ editable:

```bash
pip install -e .
```

Sau đó vẫn chạy được các ví dụ như bình thường:

```bash
python examples/04_trang_an_house/generate.py
```

## Luồng tạo GLB

Với mesh đơn giản:

```text
shape Python file
→ MeshData
→ write_glb()
→ output/*.glb
```

Với scene lớn:

```text
scene Python file
→ SceneMesh nhiều material
→ write_scene_glb()
→ output/*.glb
```

## Scene 04: Trang An Heritage House

File chính:

```text
src/glb_forge/scenes/trang_an_house.py
```

File chạy:

```text
examples/04_trang_an_house/generate.py
```

Scene số 04 là bản cuối đã sửa:

```text
- có cây xanh thật sự phía sau nhà, gồm thân, cành và tán lá low-poly
- mái ngói phía sau đã giống mặt mái phía trước, không còn bị trơn/phẳng
- nhà một tầng bố cục ngang, thấp, dạng nhà cổ 5 gian
- mái ngói đỏ nâu cũ, hiên rộng, cột gỗ, chân tảng đá
- nền đá cao, bậc tam cấp
- cửa gỗ kiểu bức bàn nhiều cánh
- khung gỗ, xà ngang, vì kèo gợi hình nhà cổ
- sân gạch đỏ cũ, chum nước, cây cau, hàng rào tre, tường đá thấp
- núi đá vôi xám và cây xanh phía sau gợi Tràng An
```

Toàn bộ model được tạo bằng hình học procedural, không dùng texture ảnh thật, nên dễ học và dễ chỉnh code.

## Import mẫu

```python
from glb_forge import write_scene_glb
from glb_forge.scenes import create_trang_an_house

scene = create_trang_an_house(seed=42)
write_scene_glb(scene, "output/trang_an_heritage_house.glb")
```
