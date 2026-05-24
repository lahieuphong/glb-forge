# 35 Ninh Bình - Nhà Cổ Tràng An GLB

Project Python thuần để tạo file `.glb` procedural cho **nhà cổ Tràng An, Ninh Bình**.

Output hiện tại:

```text
output/35_ninh_binh/nha_co_trang_an.glb
```

Project không cần Blender và không cần thư viện ngoài. Mesh, normal, material và scene đều được tạo bằng Python.

## Cấu Trúc Chính

```text
src/glb_forge/
├─ scene.py                 # primitive + helper hình học
├─ scene_writer.py          # ghi SceneMesh ra GLB
├─ build.py                 # luồng generate dùng chung
├─ scenes/
│  └─ trang_an_house.py     # source dựng nhà cổ Tràng An
└─ sites/
   ├─ models.py             # model Province, HeritageSite
   ├─ registry.py           # đăng ký + kiểm tra trùng di tích
   └─ provinces/
      └─ ninh_binh.py       # metadata Ninh Bình / Tràng An

generators/
└─ 35_ninh_binh/
   └─ nha_co_trang_an.py    # lệnh chạy riêng di tích này

scripts/
├─ generate_site.py         # generate theo registry key
└─ generate_all.py          # generate toàn bộ di tích đã đăng ký
```

## Chạy Code

Sau khi clone project về máy khác, chạy theo các bước sau.

1. Vào thư mục project:

```bash
cd 35-ninh-binh-nha-co-trang-an-glb
```

2. Kiểm tra Python. Project cần Python `>= 3.10`:

```bash
python3.12 --version
```

Nếu máy không có `python3.12`, có thể thử:

```bash
python3 --version
```

3. Tạo môi trường ảo nếu muốn chạy gọn trong project:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

4. Cài project ở chế độ editable:

```bash
pip install -e .
```

5. Generate file GLB:

```bash
python3.12 generators/35_ninh_binh/nha_co_trang_an.py
```

Hoặc generate theo registry key:

```bash
python3.12 scripts/generate_site.py 35-ninh-binh/nha-co-trang-an
```

Hoặc generate toàn bộ di tích đã đăng ký:

```bash
python3.12 scripts/generate_all.py
```

Kết quả nằm tại:

```text
output/35_ninh_binh/nha_co_trang_an.glb
```

## Thông Tin Di Tích

```text
Registry key: 35-ninh-binh/nha-co-trang-an
Scene source: src/glb_forge/scenes/trang_an_house.py
Metadata:     src/glb_forge/sites/provinces/ninh_binh.py
Output:       output/35_ninh_binh/nha_co_trang_an.glb
```