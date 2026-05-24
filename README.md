# GLB Forge

**GLB Forge** là project Python thuần để tạo file `.glb` procedural cho các di tích Việt Nam.

Project hiện có một di tích:

```text
output/35-Ninh-Binh/Nha-co-Trang-An.glb
```

Code không cần Blender và không cần thư viện ngoài. Toàn bộ mesh, normal, material và scene được tạo bằng Python rồi ghi trực tiếp ra GLB.

## Cấu Trúc

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

## Vai Trò Các Phần

```text
src/glb_forge/scene.py
```

Chứa các primitive và helper hình học dùng chung: box, quad, triangle, frustum, lathe, vector math.

```text
src/glb_forge/scene_writer.py
```

Ghi `SceneMesh` ra file `.glb`.

```text
src/glb_forge/build.py
```

Đóng gói luồng generate chung: lấy một di tích, tạo scene, ghi GLB, trả về thông tin kết quả.

```text
src/glb_forge/scenes/
```

Chứa source dựng hình của từng di tích. Hiện tại:

```text
src/glb_forge/scenes/trang_an_house.py
```

Đây là source chính tạo model nhà cổ Tràng An.

```text
src/glb_forge/sites/
```

Chứa metadata để phân biệt di tích, tỉnh, registry key và tên file output. Phần này giúp nhiều di tích sau này không bị trùng tên hoặc ghi nhầm output.

```text
generators/
```

Chứa lệnh chạy riêng cho từng di tích. Đây là lớp tiện dụng, không phải nơi chứa logic dựng hình chính.

## Chạy Code

Đứng ở thư mục gốc `glb-forge`, chạy riêng nhà cổ Tràng An:

```bash
python3.12 generators/35_ninh_binh/nha_co_trang_an.py
```

Hoặc chạy theo registry key:

```bash
python3.12 scripts/generate_site.py 35-ninh-binh/nha-co-trang-an
```

Hoặc generate toàn bộ di tích đã đăng ký:

```bash
python3.12 scripts/generate_all.py
```

Kết quả:

```text
output/35-Ninh-Binh/Nha-co-Trang-An.glb
```

## Quy Ước Source Và Output

Source code dùng tên Python-friendly:

```text
src/glb_forge/scenes/trang_an_house.py
generators/35_ninh_binh/nha_co_trang_an.py
```

Output dùng tên đẹp để quản lý asset:

```text
output/35-Ninh-Binh/Nha-co-Trang-An.glb
```

Không cần bọc source theo đúng tên output như `35-Ninh-Binh/Nha-co-Trang-An`, vì tên có dấu gạch ngang không phù hợp để import trong Python. Source nên giữ dạng `snake_case`, còn output giữ dạng dễ đọc.

## Di Tích Hiện Có

Registry key:

```text
35-ninh-binh/nha-co-trang-an
```

Scene source:

```text
src/glb_forge/scenes/trang_an_house.py
```

Metadata:

```text
src/glb_forge/sites/provinces/ninh_binh.py
```

Output:

```text
output/35-Ninh-Binh/Nha-co-Trang-An.glb
```

## Thêm Di Tích Mới

Mỗi di tích nên có một source scene riêng trong:

```text
src/glb_forge/scenes/
```

Sau đó khai báo di tích trong đúng file tỉnh:

```text
src/glb_forge/sites/provinces/
```

Nếu cần lệnh chạy riêng, thêm file tương ứng trong:

```text
generators/
```

Luồng thêm di tích:

```text
1. Tạo hàm dựng scene mới trong src/glb_forge/scenes/
2. Import hàm đó trong file tỉnh tương ứng ở src/glb_forge/sites/provinces/
3. Khai báo HeritageSite với site_id, name, province, output_name, create_scene
4. Thêm di tích vào danh sách <TINH>_SITES
5. Chạy scripts/generate_all.py hoặc scripts/generate_site.py
```

`src/glb_forge/sites/registry.py` sẽ kiểm tra trùng registry key và trùng output path trước khi generate.

## Dùng Trong Code

```python
from glb_forge import generate_site, get_site

site = get_site("35-ninh-binh/nha-co-trang-an")
result = generate_site(site, "output")
print(result.path)
```
