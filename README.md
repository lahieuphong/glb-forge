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
│     ├─ build.py
│     ├─ scene.py
│     ├─ scene_writer.py
│     ├─ scenes/
│     │  ├─ __init__.py
│     │  └─ trang_an_house.py
│     └─ sites/
│        ├─ __init__.py
│        ├─ models.py
│        ├─ registry.py
│        └─ provinces/
│           ├─ __init__.py
│           └─ ninh_binh.py
├─ generators/
│  └─ 35_ninh_binh/
│     └─ nha_co_trang_an.py
└─ scripts/
   ├─ generate_all.py
   └─ generate_site.py
```

## Chạy nhanh

Đứng ở thư mục gốc `glb-forge`, chạy:

```bash
python3.12 generators/35_ninh_binh/nha_co_trang_an.py
```

Hoặc dùng script tổng:

```bash
python3.12 scripts/generate_all.py
```

Hoặc build theo registry key:

```bash
python3.12 scripts/generate_site.py 35-ninh-binh/nha-co-trang-an
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
python generators/35_ninh_binh/nha_co_trang_an.py
```

## Luồng tạo GLB

```text
src/glb_forge/scenes/trang_an_house.py
→ SceneMesh nhiều material
→ generate_site()
→ write_scene_glb()
→ output/35-Ninh-Binh/Nha-co-Trang-An.glb
```

## Quy ước quản lý di tích

Mỗi di tích có 3 phần tách riêng:

```text
src/glb_forge/scenes/<ten_scene>.py                 # geometry/procedural model
src/glb_forge/sites/provinces/<ten_tinh>.py         # province + site metadata
generators/<ma_tinh>_<ten_tinh>/<ten_di_tich>.py    # entrypoint riêng nếu cần
```

Output dùng dạng:

```text
output/<ma-tinh>-<ten-tinh>/<Ten-di-tich>.glb
```

Trường hợp hiện tại:

```text
output/35-Ninh-Binh/Nha-co-Trang-An.glb
```

Registry key trong code dùng dạng slug thường:

```text
35-ninh-binh/nha-co-trang-an
```

`src/glb_forge/sites/registry.py` sẽ kiểm tra trùng registry key và trùng output path trước khi generate.

Khi thêm di tích mới:

```text
1. Tạo hàm scene mới trong src/glb_forge/scenes/
2. Khai báo HeritageSite trong đúng file tỉnh ở src/glb_forge/sites/provinces/
3. Thêm site vào danh sách <TINH>_SITES
4. Nếu muốn có lệnh chạy riêng, thêm file trong generators/<ma_tinh>_<ten_tinh>/
```

## Scene Tràng An

File scene chính:

```text
src/glb_forge/scenes/trang_an_house.py
```

File chạy:

```text
generators/35_ninh_binh/nha_co_trang_an.py
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

## Dùng Trong Code

```python
from glb_forge import generate_site, get_site

site = get_site("35-ninh-binh/nha-co-trang-an")
result = generate_site(site, "output")
print(result.path)
```
