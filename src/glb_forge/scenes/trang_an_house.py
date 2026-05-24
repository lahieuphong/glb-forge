from __future__ import annotations

import math
from random import Random

from glb_forge.scene import SceneMesh, Vec3, v_add, v_cross, v_dot, v_len, v_lerp, v_mul, v_norm, v_sub


# Scene này dùng Y-up:
# x = trái/phải, y = cao/thấp, z = trước/sau.
# Phía trước nhà nằm ở z âm, nền cảnh quan/núi nằm ở z dương.


def create_trang_an_house(seed: int = 42) -> SceneMesh:
    """Tạo mẫu 04: nhà cổ Ninh Bình/Tràng An dạng procedural.

    Model cố ý dùng hình học đơn giản + nhiều chi tiết nhỏ thay cho texture ảnh:
    - nhà 1 tầng, bố cục ngang 5 gian
    - mái ngói đỏ nâu có nhiều viên ngói riêng
    - hiên rộng, cột gỗ, nền đá, bậc tam cấp
    - cửa bức bàn gỗ nhiều cánh
    - sân gạch đỏ, chum nước, cau, cây xanh, tường đá thấp
    - núi đá vôi và cây xanh phía sau để gợi Tràng An
    """
    rng = Random(seed)
    scene = SceneMesh("Trang_An_Heritage_House")
    mat = _make_materials(scene)

    _add_ground_and_courtyard(scene, mat, rng)
    _add_low_walls_and_fence(scene, mat, rng)
    _add_house_base(scene, mat, rng)
    _add_house_body_and_doors(scene, mat, rng)
    _add_roof(scene, mat, rng)
    _add_columns_and_wood_frame(scene, mat, rng)
    _add_jars_and_garden(scene, mat, rng)
    _add_background_karst(scene, mat, rng)

    return scene


def _make_materials(scene: SceneMesh) -> dict[str, int | list[int]]:
    materials: dict[str, int | list[int]] = {}

    materials["earth"] = scene.add_material("warm earth base", (0.45, 0.34, 0.23, 1.0), roughness=0.95)
    materials["shadow"] = scene.add_material("dark interior shadow", (0.015, 0.012, 0.009, 1.0), roughness=1.0)

    materials["wood_dark"] = scene.add_material("old dark lim wood", (0.25, 0.12, 0.045, 1.0), roughness=0.86)
    materials["wood"] = scene.add_material("aged brown wood", (0.42, 0.22, 0.09, 1.0), roughness=0.82)
    materials["wood_light"] = scene.add_material("worn golden wood edge", (0.58, 0.34, 0.14, 1.0), roughness=0.78)
    materials["wood_black"] = scene.add_material("nearly black carved wood", (0.08, 0.035, 0.014, 1.0), roughness=0.9)

    materials["stone"] = scene.add_material("old grey limestone", (0.45, 0.45, 0.40, 1.0), roughness=0.92)
    materials["stone_dark"] = scene.add_material("dark stone gaps", (0.20, 0.21, 0.19, 1.0), roughness=0.96)
    materials["stone_light"] = scene.add_material("light worn stone edge", (0.63, 0.62, 0.56, 1.0), roughness=0.88)

    materials["moss"] = scene.add_material("soft green moss", (0.10, 0.30, 0.07, 1.0), roughness=0.96)
    materials["leaf"] = scene.add_material("deep village green leaves", (0.10, 0.36, 0.07, 1.0), roughness=0.9)
    materials["leaf_light"] = scene.add_material("young leaf highlights", (0.25, 0.55, 0.12, 1.0), roughness=0.9)
    materials["bamboo"] = scene.add_material("dry bamboo", (0.64, 0.45, 0.20, 1.0), roughness=0.88)
    materials["jar"] = scene.add_material("old brown ceramic jar", (0.48, 0.20, 0.08, 1.0), roughness=0.72)
    materials["jar_dark"] = scene.add_material("dark jar mouth", (0.06, 0.03, 0.015, 1.0), roughness=0.95)

    materials["roof_base"] = scene.add_material("old red brown roof base", (0.42, 0.13, 0.045, 1.0), roughness=0.9)
    roof_variants: list[int] = []
    roof_colors = [
        (0.46, 0.15, 0.055, 1.0),
        (0.56, 0.20, 0.075, 1.0),
        (0.36, 0.10, 0.040, 1.0),
        (0.64, 0.26, 0.090, 1.0),
        (0.31, 0.085, 0.035, 1.0),
        (0.50, 0.18, 0.065, 1.0),
        (0.42, 0.19, 0.085, 1.0),
        (0.62, 0.30, 0.12, 1.0),
    ]
    for i, color in enumerate(roof_colors):
        roof_variants.append(scene.add_material(f"individual roof tile {i + 1}", color, roughness=0.94))
    materials["roof_tiles"] = roof_variants

    brick_variants: list[int] = []
    brick_colors = [
        (0.55, 0.22, 0.11, 1.0),
        (0.63, 0.27, 0.13, 1.0),
        (0.45, 0.16, 0.08, 1.0),
        (0.70, 0.34, 0.16, 1.0),
        (0.50, 0.20, 0.10, 1.0),
    ]
    for i, color in enumerate(brick_colors):
        brick_variants.append(scene.add_material(f"old courtyard brick {i + 1}", color, roughness=0.96))
    materials["bricks"] = brick_variants
    materials["brick_gap"] = scene.add_material("dark red mortar gaps", (0.18, 0.10, 0.075, 1.0), roughness=1.0)

    return materials


def _mat(materials: dict[str, int | list[int]], name: str) -> int:
    value = materials[name]
    if isinstance(value, list):
        raise TypeError(f"Material {name!r} là list, không phải int.")
    return value


def _mat_list(materials: dict[str, int | list[int]], name: str) -> list[int]:
    value = materials[name]
    if not isinstance(value, list):
        raise TypeError(f"Material {name!r} là int, không phải list.")
    return value


def _roof_axes(y_eave: float, y_ridge: float, start_z: float, ridge_z: float) -> tuple[Vec3, Vec3, Vec3, Vec3, float]:
    """Trả về trục cho một mặt mái.

    Giá trị trả về:
    - u: trục ngang theo chiều dài nhà.
    - v: trục đi từ mép mái lên sống mái, dùng để đặt vị trí hàng ngói.
    - n: normal hướng lên ngoài mặt mái, dùng để đẩy ngói nổi lên khỏi nền mái.
    - tile_v: trục dọc viên ngói, cùng phương với v nhưng được chọn để hệ trục hộp đúng chiều.
    - slope_len: chiều dài dốc mái.

    FIX 05: Với mặt mái sau, nếu lấy trực tiếp v_cross(v, u) thì normal bị hướng xuống dưới,
    làm các viên ngói bị đặt ở mặt dưới roof_base. Vì vậy ép n luôn có thành phần Y dương.
    """
    u = (1.0, 0.0, 0.0)
    v = v_norm((0.0, y_ridge - y_eave, ridge_z - start_z))
    n = v_norm(v_cross(v, u))
    if n[1] < 0.0:
        n = v_mul(n, -1.0)

    # Giữ hệ trục local của hộp ngói đúng chiều để normal/shading ổn hơn.
    tile_v = v_norm(v_cross(u, n))
    slope_len = math.sqrt((y_ridge - y_eave) ** 2 + (ridge_z - start_z) ** 2)
    return u, v, n, tile_v, slope_len


# -----------------------------------------------------------------------------
# Nền, sân gạch, tường, hàng rào
# -----------------------------------------------------------------------------


def _add_ground_and_courtyard(scene: SceneMesh, mat: dict[str, int | list[int]], rng: Random) -> None:
    earth = _mat(mat, "earth")
    brick_gap = _mat(mat, "brick_gap")
    bricks = _mat_list(mat, "bricks")

    # Đế lớn để model có cảm giác giống một mô hình sa bàn.
    scene.add_box((0.0, -0.12, -2.05), (18.6, 0.24, 11.8), earth)

    # Lớp vữa tối nằm dưới những viên gạch.
    scene.add_box((0.0, 0.015, -4.95), (17.2, 0.05, 5.55), brick_gap)

    x_min, x_max = -8.35, 8.35
    z_min, z_max = -7.45, -2.55
    brick_w = 0.62
    brick_d = 0.34
    gap = 0.035
    y = 0.065

    row = 0
    z = z_min + brick_d / 2.0
    while z < z_max:
        offset = 0.0 if row % 2 == 0 else brick_w * 0.5
        x = x_min + brick_w / 2.0 - offset
        col = 0
        while x < x_max:
            if x_min + 0.12 < x < x_max - 0.12:
                color_mat = bricks[(row * 3 + col + rng.randrange(len(bricks))) % len(bricks)]
                h = 0.035 + rng.random() * 0.012
                scene.add_box((x, y + h * 0.5, z), (brick_w - gap, h, brick_d - gap), color_mat)
            x += brick_w
            col += 1
        z += brick_d
        row += 1

    # Viền sân thấp màu đất/đá.
    scene.add_box((0.0, 0.12, -7.80), (18.6, 0.28, 0.28), earth)
    scene.add_box((-9.18, 0.12, -2.05), (0.28, 0.28, 11.5), earth)
    scene.add_box((9.18, 0.12, -2.05), (0.28, 0.28, 11.5), earth)


def _add_low_walls_and_fence(scene: SceneMesh, mat: dict[str, int | list[int]], rng: Random) -> None:
    stone = _mat(mat, "stone")
    stone_dark = _mat(mat, "stone_dark")
    stone_light = _mat(mat, "stone_light")
    bamboo = _mat(mat, "bamboo")
    moss = _mat(mat, "moss")

    # Tường đá thấp hai bên và phía sau.
    wall_specs = [
        ((-8.55, 0.62, 0.55), (0.38, 1.24, 6.9)),
        ((8.55, 0.62, 0.55), (0.38, 1.24, 6.9)),
        ((0.0, 0.70, 3.90), (17.4, 1.40, 0.38)),
    ]
    for center, size in wall_specs:
        scene.add_box(center, size, stone)

    # Trụ tường ở các góc, nhìn giống cột đá làng quê.
    for x in (-8.55, 8.55):
        for z in (-2.75, 3.90):
            scene.add_box((x, 0.78, z), (0.62, 1.55, 0.62), stone)
            scene.add_box((x, 1.60, z), (0.78, 0.18, 0.78), stone_light)
            scene.add_box((x, 0.08, z), (0.78, 0.16, 0.78), stone_dark)

    # Vẽ mạch đá bằng các thanh tối rất mỏng trên mặt tường.
    for x in (-8.77, 8.77):
        for zi in range(12):
            z = -2.45 + zi * 0.55
            scene.add_box((x, 0.62, z), (0.035, 0.025, 0.42), stone_dark)
        for yi in range(4):
            y = 0.25 + yi * 0.28
            scene.add_box((x, y, 0.55), (0.035, 0.025, 6.55), stone_dark)

    for xi in range(28):
        x = -8.0 + xi * 0.60
        if abs(x) < 6.8:
            scene.add_box((x, 0.68, 3.68), (0.45, 0.025, 0.035), stone_dark)
    for yi in range(4):
        scene.add_box((0.0, 0.25 + yi * 0.30, 3.68), (16.4, 0.025, 0.035), stone_dark)

    # Một ít rêu trên tường đá, không quá dày để file nhẹ.
    for _ in range(38):
        side = rng.choice([-1.0, 1.0])
        x = side * 8.78
        y = rng.uniform(0.25, 1.15)
        z = rng.uniform(-2.3, 3.2)
        scene.add_box((x, y, z), (0.025, rng.uniform(0.08, 0.22), rng.uniform(0.12, 0.35)), moss)

    # Hàng rào tre thấp phía trước, chừa khoảng giữa cho bậc tam cấp.
    _add_bamboo_fence(scene, bamboo, x0=-8.05, x1=-2.05, z=-6.62)
    _add_bamboo_fence(scene, bamboo, x0=2.05, x1=8.05, z=-6.62)
    _add_bamboo_fence(scene, bamboo, x0=-8.15, x1=-5.4, z=-3.10)
    _add_bamboo_fence(scene, bamboo, x0=5.4, x1=8.15, z=-3.10)


def _add_bamboo_fence(scene: SceneMesh, bamboo: int, *, x0: float, x1: float, z: float) -> None:
    step = 0.72
    x = x0
    posts: list[float] = []
    while x <= x1 + 1e-6:
        posts.append(x)
        scene.add_frustum_between((x, 0.12, z), (x, 0.88, z), 0.035, 0.028, bamboo, segments=8)
        x += step

    for y in (0.42, 0.70):
        scene.add_box_between((x0, y, z), (x1, y, z), 0.045, bamboo, width=0.055)

    # Thanh chéo vài đoạn cho cảm giác thủ công.
    for i in range(0, max(0, len(posts) - 1), 2):
        scene.add_box_between((posts[i], 0.18, z + 0.02), (posts[i + 1], 0.78, z + 0.02), 0.035, bamboo, width=0.045)


# -----------------------------------------------------------------------------
# Nhà chính: nền đá, thân nhà, cửa, mái, cột
# -----------------------------------------------------------------------------


def _add_house_base(scene: SceneMesh, mat: dict[str, int | list[int]], rng: Random) -> None:
    stone = _mat(mat, "stone")
    stone_dark = _mat(mat, "stone_dark")
    stone_light = _mat(mat, "stone_light")
    moss = _mat(mat, "moss")

    # Nền nhà cao bằng đá tảng.
    scene.add_box((0.0, 0.30, -0.10), (13.75, 0.60, 4.65), stone)
    scene.add_box((0.0, 0.64, -1.50), (13.55, 0.12, 1.45), stone_light)

    # Mặt trước nền đá: các khối đá riêng để nhìn cổ hơn.
    x_min, x_max = -6.75, 6.75
    z_front = -2.43
    rows = 3
    cols = 25
    for r in range(rows):
        for c in range(cols):
            w = (x_max - x_min) / cols
            x = x_min + w * (c + 0.5)
            y = 0.14 + r * 0.18
            h = 0.14
            block_mat = stone if (r + c + rng.randrange(3)) % 3 else stone_light
            scene.add_box((x, y, z_front - 0.025), (w - 0.035, h, 0.06), block_mat)

    # Mạch ngang/dọc tối.
    for r in range(rows + 1):
        y = 0.055 + r * 0.18
        scene.add_box((0.0, y, z_front - 0.065), (13.35, 0.018, 0.035), stone_dark)
    for c in range(cols + 1):
        x = x_min + (x_max - x_min) * c / cols
        scene.add_box((x, 0.32, z_front - 0.07), (0.018, 0.48, 0.035), stone_dark)

    # Bậc tam cấp bằng đá.
    scene.add_box((0.0, 0.11, -3.42), (3.35, 0.22, 0.72), stone)
    scene.add_box((0.0, 0.27, -3.10), (2.85, 0.22, 0.62), stone_light)
    scene.add_box((0.0, 0.43, -2.80), (2.35, 0.22, 0.52), stone)
    for i, z in enumerate((-3.42, -3.10, -2.80)):
        scene.add_box((0.0, 0.23 + i * 0.16, z - 0.36), (3.15 - i * 0.45, 0.035, 0.045), stone_dark)

    # Rêu xanh nhẹ ở mép bậc và chân nền.
    for _ in range(28):
        x = rng.uniform(-6.2, 6.2)
        y = rng.uniform(0.47, 0.68)
        z = rng.choice([-2.47, -1.95]) + rng.uniform(-0.015, 0.015)
        scene.add_box((x, y, z), (rng.uniform(0.10, 0.28), 0.018, 0.035), moss)


def _add_house_body_and_doors(scene: SceneMesh, mat: dict[str, int | list[int]], rng: Random) -> None:
    wood = _mat(mat, "wood")
    wood_dark = _mat(mat, "wood_dark")
    wood_light = _mat(mat, "wood_light")
    wood_black = _mat(mat, "wood_black")
    shadow = _mat(mat, "shadow")

    # Thân nhà gỗ thấp, dài ngang.
    scene.add_box((0.0, 1.42, 0.10), (12.55, 1.65, 3.25), wood_dark)
    scene.add_box((0.0, 1.50, 1.69), (12.55, 1.80, 0.20), wood)
    scene.add_box((-6.38, 1.42, 0.05), (0.22, 1.75, 3.35), wood)
    scene.add_box((6.38, 1.42, 0.05), (0.22, 1.75, 3.35), wood)

    # Vách bên dạng ván ngang.
    for side_x in (-6.52, 6.52):
        for i in range(8):
            y = 0.78 + i * 0.19
            scene.add_box((side_x, y, 0.12), (0.05, 0.035, 3.05), wood_light if i % 3 == 0 else wood_dark)

    # Dải xà ngang mặt trước.
    scene.add_box((0.0, 2.40, -1.72), (12.75, 0.22, 0.18), wood_black)
    scene.add_box((0.0, 0.78, -1.73), (12.75, 0.18, 0.18), wood_black)
    scene.add_box((0.0, 2.16, -1.74), (12.40, 0.10, 0.14), wood_light)

    # 5 gian cửa bức bàn, nhiều cánh.
    bay_centers = [-4.95, -2.48, 0.0, 2.48, 4.95]
    for bay_i, cx in enumerate(bay_centers):
        open_middle = bay_i in (1, 3)
        _add_door_bay(
            scene,
            cx=cx,
            y_base=0.83,
            z=-1.86,
            width=1.78,
            height=1.34,
            open_middle=open_middle,
            wood=wood,
            wood_dark=wood_dark,
            wood_light=wood_light,
            shadow=shadow,
        )

    # Các mảng vách gỗ giữa cửa/cột.
    for x in (-6.00, -3.72, -1.22, 1.22, 3.72, 6.00):
        scene.add_box((x, 1.48, -1.83), (0.18, 1.32, 0.08), wood_black)
        scene.add_box((x, 2.05, -1.87), (0.32, 0.16, 0.10), wood_light)
        # Ô trang trí nhỏ phía trên như chạm khắc đơn giản.
        scene.add_box((x, 2.31, -1.90), (0.28, 0.24, 0.08), wood)
        scene.add_box((x, 2.31, -1.955), (0.18, 0.14, 0.03), wood_dark)

    # Vì kèo gợi hình ở hai đầu hồi.
    for x in (-6.25, 6.25):
        sign = 1 if x > 0 else -1
        scene.add_box_between((x, 2.00, -1.58), (x, 3.32, -0.02), 0.09, wood_black, width=0.12, up_hint=(sign, 0.0, 0.0))
        scene.add_box_between((x, 2.00, 1.58), (x, 3.32, -0.02), 0.09, wood_black, width=0.12, up_hint=(sign, 0.0, 0.0))
        scene.add_box_between((x, 2.18, -1.20), (x, 2.18, 1.20), 0.075, wood_light, width=0.10, up_hint=(sign, 0.0, 0.0))


def _add_door_bay(
    scene: SceneMesh,
    *,
    cx: float,
    y_base: float,
    z: float,
    width: float,
    height: float,
    open_middle: bool,
    wood: int,
    wood_dark: int,
    wood_light: int,
    shadow: int,
) -> None:
    # Khoảng tối phía sau cửa.
    scene.add_box((cx, y_base + height * 0.50, z - 0.055), (width, height, 0.045), shadow)

    leaves = 4
    leaf_w = width / leaves
    for i in range(leaves):
        # Mở hờ 2 cánh giữa ở một số gian để tạo nhịp tối/sáng như hình mẫu.
        if open_middle and i in (1, 2):
            continue
        lx = cx - width / 2.0 + leaf_w * (i + 0.5)
        scene.add_box((lx, y_base + height * 0.50, z), (leaf_w - 0.045, height, 0.055), wood)
        # Khung cánh cửa.
        scene.add_box((lx - leaf_w * 0.39, y_base + height * 0.50, z - 0.04), (0.035, height, 0.035), wood_dark)
        scene.add_box((lx + leaf_w * 0.39, y_base + height * 0.50, z - 0.04), (0.035, height, 0.035), wood_dark)
        scene.add_box((lx, y_base + 0.12, z - 0.045), (leaf_w - 0.09, 0.035, 0.035), wood_dark)
        scene.add_box((lx, y_base + height - 0.12, z - 0.045), (leaf_w - 0.09, 0.035, 0.035), wood_dark)

        # Hai ô pano nổi.
        scene.add_box((lx, y_base + height * 0.35, z - 0.075), (leaf_w - 0.16, height * 0.32, 0.030), wood_light)
        scene.add_box((lx, y_base + height * 0.72, z - 0.075), (leaf_w - 0.16, height * 0.25, 0.030), wood_light)
        scene.add_box((lx, y_base + height * 0.35, z - 0.100), (leaf_w - 0.24, height * 0.22, 0.025), wood_dark)
        scene.add_box((lx, y_base + height * 0.72, z - 0.100), (leaf_w - 0.24, height * 0.15, 0.025), wood_dark)

    # Khung bao cửa.
    scene.add_box((cx, y_base - 0.03, z - 0.02), (width + 0.16, 0.07, 0.08), wood_dark)
    scene.add_box((cx, y_base + height + 0.03, z - 0.02), (width + 0.16, 0.07, 0.08), wood_dark)
    scene.add_box((cx - width / 2.0 - 0.05, y_base + height / 2.0, z - 0.02), (0.07, height + 0.08, 0.08), wood_dark)
    scene.add_box((cx + width / 2.0 + 0.05, y_base + height / 2.0, z - 0.02), (0.07, height + 0.08, 0.08), wood_dark)


def _add_roof(scene: SceneMesh, mat: dict[str, int | list[int]], rng: Random) -> None:
    roof_base = _mat(mat, "roof_base")
    roof_tiles = _mat_list(mat, "roof_tiles")
    stone = _mat(mat, "stone")
    stone_light = _mat(mat, "stone_light")
    wood_dark = _mat(mat, "wood_dark")
    wood = _mat(mat, "wood")
    moss = _mat(mat, "moss")

    width = 14.70
    z_front = -2.82
    z_back = 2.82
    z_ridge = 0.00
    y_eave = 2.55
    y_ridge = 4.02

    # Hai mặt mái chính.
    _add_roof_plane(
        scene,
        start_z=z_front,
        ridge_z=z_ridge,
        y_eave=y_eave,
        y_ridge=y_ridge,
        width=width,
        roof_base=roof_base,
        roof_tiles=roof_tiles,
        rng=rng,
    )
    _add_roof_plane(
        scene,
        start_z=z_back,
        ridge_z=z_ridge,
        y_eave=y_eave,
        y_ridge=y_ridge,
        width=width,
        roof_base=roof_base,
        roof_tiles=roof_tiles,
        rng=rng,
    )

    # Diềm mái trước/sau hơi cong nhẹ ở hai đầu, không tạo cảm giác chùa.
    # Chia làm 3 đoạn: giữa thẳng, hai đầu nâng nhẹ.
    for z in (z_front, z_back):
        scene.add_box_between((-6.45, y_eave - 0.03, z), (6.45, y_eave - 0.03, z), 0.16, stone, width=0.22)
        scene.add_box_between((-7.35, y_eave + 0.13, z), (-6.45, y_eave - 0.03, z), 0.16, stone_light, width=0.22)
        scene.add_box_between((6.45, y_eave - 0.03, z), (7.35, y_eave + 0.13, z), 0.16, stone_light, width=0.22)
        scene.add_box_between((-7.20, y_eave - 0.20, z + (0.08 if z < 0 else -0.08)), (7.20, y_eave - 0.20, z + (0.08 if z < 0 else -0.08)), 0.10, wood_dark, width=0.16)

    # Đỉnh mái và bờ chảy hai đầu hồi.
    scene.add_box_between((-7.20, y_ridge + 0.06, z_ridge), (7.20, y_ridge + 0.06, z_ridge), 0.18, stone_light, width=0.24)
    for x in (-7.32, 7.32):
        scene.add_box_between((x, y_eave + 0.03, z_front), (x, y_ridge + 0.08, z_ridge), 0.16, stone_light, width=0.24, up_hint=(1.0, 0.0, 0.0))
        scene.add_box_between((x, y_ridge + 0.08, z_ridge), (x, y_eave + 0.03, z_back), 0.16, stone_light, width=0.24, up_hint=(1.0, 0.0, 0.0))

    # Mặt hồi tam giác bằng gỗ.
    for x in (-6.45, 6.45):
        sign = 1.0 if x > 0 else -1.0
        normal = (sign, 0.0, 0.0)
        p0 = (x, 2.18, z_front + 0.20)
        p1 = (x, 2.18, z_back - 0.20)
        p2 = (x, 3.74, z_ridge)
        if x > 0:
            scene.add_triangle(p0, p1, p2, wood, normal=normal)
        else:
            scene.add_triangle(p1, p0, p2, wood, normal=normal)
        # Ván dọc trên hồi.
        for i in range(7):
            z = -1.35 + i * 0.45
            y_mid = 2.45 + (1.0 - abs(z) / 1.55) * 0.65
            scene.add_box((x + sign * 0.035, y_mid, z), (0.06, 0.95, 0.035), wood_dark)

    # Rui mè dưới mái hiên trước.
    for i in range(27):
        x = -6.6 + i * 0.51
        scene.add_box_between((x, 2.33, -1.70), (x, 2.50, -2.62), 0.055, wood_dark, width=0.070)

    # Rêu nhẹ trên mái, làm bằng các hộp mỏng nằm theo mặt mái.
    for _ in range(42):
        front = rng.choice([True, False])
        start_z = z_front if front else z_back
        u, v, n, tile_v, slope_len = _roof_axes(y_eave, y_ridge, start_z, z_ridge)
        x = rng.uniform(-6.4, 6.4)
        dist = rng.uniform(0.35, slope_len - 0.30)
        center = v_add((x, y_eave, start_z), v_add(v_mul(v, dist), v_mul(n, 0.045)))
        scene.add_box(center, (rng.uniform(0.18, 0.50), 0.018, rng.uniform(0.05, 0.12)), moss, x_axis=u, y_axis=n, z_axis=tile_v)


def _add_roof_plane(
    scene: SceneMesh,
    *,
    start_z: float,
    ridge_z: float,
    y_eave: float,
    y_ridge: float,
    width: float,
    roof_base: int,
    roof_tiles: list[int],
    rng: Random,
) -> None:
    # Plane từ mép mái lên sống mái.
    half_w = width / 2.0
    p0 = (-half_w, y_eave, start_z)
    p1 = (half_w, y_eave, start_z)
    p2 = (half_w, y_ridge, ridge_z)
    p3 = (-half_w, y_ridge, ridge_z)

    u, v, n, tile_v, slope_len = _roof_axes(y_eave, y_ridge, start_z, ridge_z)
    scene.add_quad(p0, p1, p2, p3, roof_base, normal=n)

    cols = 42
    rows = 14
    tile_w = width / cols * 0.96
    tile_d = slope_len / rows * 0.92
    step_x = width / cols
    step_d = slope_len / rows

    for row in range(rows):
        row_offset = 0.0 if row % 2 == 0 else step_x * 0.5
        dist = step_d * (row + 0.5)
        for col in range(cols):
            x = -half_w + step_x * (col + 0.5) + row_offset
            if x > half_w - step_x * 0.35:
                continue
            # Ngói hơi không đều để nhìn cũ.
            mat_index = roof_tiles[(row * 5 + col + rng.randrange(len(roof_tiles))) % len(roof_tiles)]
            jitter_x = rng.uniform(-0.018, 0.018)
            jitter_d = rng.uniform(-0.014, 0.014)
            center = v_add((x + jitter_x, y_eave, start_z), v_add(v_mul(v, dist + jitter_d), v_mul(n, 0.035)))
            scene.add_box(center, (tile_w * rng.uniform(0.90, 1.02), 0.040, tile_d * rng.uniform(0.82, 1.05)), mat_index, x_axis=u, y_axis=n, z_axis=tile_v)

    # Một số hàng ngói âm/dương nổi nhẹ theo chiều ngang.
    for row in range(1, rows, 3):
        dist = step_d * row
        center = v_add((0.0, y_eave, start_z), v_add(v_mul(v, dist), v_mul(n, 0.060)))
        scene.add_box(center, (width - 0.55, 0.045, 0.045), roof_tiles[row % len(roof_tiles)], x_axis=u, y_axis=n, z_axis=tile_v)


def _add_columns_and_wood_frame(scene: SceneMesh, mat: dict[str, int | list[int]], rng: Random) -> None:
    wood = _mat(mat, "wood")
    wood_dark = _mat(mat, "wood_dark")
    wood_light = _mat(mat, "wood_light")
    stone = _mat(mat, "stone")
    stone_light = _mat(mat, "stone_light")

    column_xs = [-6.05, -4.55, -3.05, -1.52, 0.0, 1.52, 3.05, 4.55, 6.05]
    for x in column_xs:
        # Chân tảng đá vuông + đế tròn.
        scene.add_box((x, 0.70, -2.05), (0.42, 0.18, 0.42), stone_light)
        scene.add_frustum((x, 0.84, -2.05), 0.17, 0.14, 0.16, stone, segments=16)
        # Cột gỗ hơi thuôn.
        scene.add_frustum((x, 1.56, -2.05), 0.105, 0.085, 1.55, wood, segments=18)
        scene.add_frustum((x, 2.37, -2.05), 0.14, 0.12, 0.16, wood_dark, segments=18)
        scene.add_box((x, 2.52, -2.05), (0.38, 0.16, 0.30), wood_light)

    # Xà ngang trước, xà hiên.
    scene.add_box((0.0, 2.48, -2.05), (12.55, 0.16, 0.18), wood_dark)
    scene.add_box((0.0, 2.25, -2.07), (12.30, 0.10, 0.14), wood_light)
    scene.add_box((0.0, 0.72, -2.04), (12.40, 0.10, 0.12), wood_dark)

    # Thanh xà dọc từ tường ra cột hiên.
    for x in column_xs:
        scene.add_box_between((x, 2.28, -1.72), (x, 2.38, -2.52), 0.065, wood_dark, width=0.085)

    # Một vài chi tiết đầu dư gỗ dưới mái.
    for x in [-5.35, -4.00, -2.68, -1.35, 1.35, 2.68, 4.00, 5.35]:
        scene.add_box((x, 2.18, -2.18), (0.20, 0.22, 0.20), wood_light)
        scene.add_box((x, 2.18, -2.33), (0.13, 0.14, 0.08), wood_dark)


# -----------------------------------------------------------------------------
# Đồ sân vườn: chum nước, cau, bụi cây
# -----------------------------------------------------------------------------


def _add_jars_and_garden(scene: SceneMesh, mat: dict[str, int | list[int]], rng: Random) -> None:
    jar = _mat(mat, "jar")
    jar_dark = _mat(mat, "jar_dark")
    moss = _mat(mat, "moss")
    leaf = _mat(mat, "leaf")
    leaf_light = _mat(mat, "leaf_light")
    bamboo = _mat(mat, "bamboo")

    _add_water_jar(scene, (-7.05, 0.07, -4.55), 0.95, jar, jar_dark, moss)
    _add_water_jar(scene, (-4.95, 0.07, -4.12), 0.58, jar, jar_dark, moss)
    _add_water_jar(scene, (5.00, 0.07, -4.35), 0.82, jar, jar_dark, moss)
    _add_water_jar(scene, (6.25, 0.07, -4.05), 0.54, jar, jar_dark, moss)

    _add_areca_palm(scene, (-7.65, 0.08, -3.18), height=2.85, trunk=bamboo, leaf=leaf, leaf_light=leaf_light, rng=rng)
    _add_areca_palm(scene, (7.45, 0.08, -2.90), height=3.05, trunk=bamboo, leaf=leaf, leaf_light=leaf_light, rng=rng)

    # Bụi cây quanh chân tường và hai bên hiên.
    for center, scale, count in [
        ((-7.20, 0.16, -2.30), 0.55, 22),
        ((7.15, 0.16, -2.20), 0.55, 22),
        ((-5.05, 0.18, -3.40), 0.36, 14),
        ((5.60, 0.18, -3.35), 0.36, 14),
        ((-6.85, 0.18, 2.90), 0.75, 24),
        ((6.85, 0.18, 2.90), 0.75, 24),
    ]:
        _add_leaf_cluster(scene, center, scale, count, leaf, leaf_light, rng)


def _add_water_jar(scene: SceneMesh, center: Vec3, scale: float, jar: int, jar_dark: int, moss: int) -> None:
    profile = [
        (0.18 * scale, 0.00 * scale),
        (0.33 * scale, 0.10 * scale),
        (0.44 * scale, 0.34 * scale),
        (0.39 * scale, 0.62 * scale),
        (0.24 * scale, 0.78 * scale),
        (0.30 * scale, 0.86 * scale),
        (0.23 * scale, 0.93 * scale),
    ]
    scene.add_lathe(center, profile, jar, segments=24)
    top_y = center[1] + 0.93 * scale
    scene.add_frustum((center[0], top_y + 0.012, center[2]), 0.24 * scale, 0.21 * scale, 0.035 * scale, jar_dark, segments=24)
    # Vài vệt rêu nhỏ trên chum.
    scene.add_box((center[0] + 0.24 * scale, center[1] + 0.45 * scale, center[2] - 0.15 * scale), (0.025 * scale, 0.12 * scale, 0.18 * scale), moss)
    scene.add_box((center[0] - 0.20 * scale, center[1] + 0.32 * scale, center[2] + 0.18 * scale), (0.025 * scale, 0.10 * scale, 0.13 * scale), moss)


def _add_areca_palm(
    scene: SceneMesh,
    base: Vec3,
    *,
    height: float,
    trunk: int,
    leaf: int,
    leaf_light: int,
    rng: Random,
) -> None:
    lean_x = rng.uniform(-0.16, 0.16)
    lean_z = rng.uniform(-0.10, 0.10)
    top = (base[0] + lean_x, base[1] + height, base[2] + lean_z)
    scene.add_frustum_between(base, top, 0.060, 0.038, trunk, segments=10)

    # Đốt cau mảnh.
    for i in range(7):
        t = (i + 1) / 8.0
        p = v_lerp(base, top, t)
        scene.add_frustum_between((p[0] - 0.035, p[1], p[2]), (p[0] + 0.035, p[1], p[2]), 0.010, 0.010, trunk, segments=6)

    # Tán lá cau dạng cánh quạt.
    for i in range(14):
        angle = math.tau * i / 14.0 + rng.uniform(-0.08, 0.08)
        length = rng.uniform(0.72, 1.05)
        droop = rng.uniform(0.15, 0.38)
        dir_vec = v_norm((math.cos(angle), -droop, math.sin(angle)))
        side = v_norm(v_cross(dir_vec, (0.0, 1.0, 0.0)))
        if v_len(side) < 0.01:
            side = (1.0, 0.0, 0.0)
        p0 = v_add(top, v_mul(side, -0.06))
        p1 = v_add(top, v_mul(side, 0.06))
        p2 = v_add(top, v_mul(dir_vec, length))
        p_mid = v_add(top, v_mul(dir_vec, length * 0.45))
        leaf_mat = leaf_light if i % 3 == 0 else leaf
        scene.add_triangle(p0, p1, p_mid, leaf_mat)
        scene.add_triangle(p1, p2, p_mid, leaf_mat)
        scene.add_triangle(p2, p0, p_mid, leaf_mat)


def _add_leaf_cluster(
    scene: SceneMesh,
    center: Vec3,
    scale: float,
    count: int,
    leaf: int,
    leaf_light: int,
    rng: Random,
) -> None:
    for i in range(count):
        angle = rng.random() * math.tau
        radius = rng.random() * scale
        c = (
            center[0] + math.cos(angle) * radius,
            center[1] + rng.uniform(0.00, scale * 0.65),
            center[2] + math.sin(angle) * radius,
        )
        length = rng.uniform(0.16, 0.34) * scale
        width = rng.uniform(0.05, 0.12) * scale
        direction = v_norm((math.cos(angle + rng.uniform(-0.8, 0.8)), rng.uniform(0.05, 0.35), math.sin(angle + rng.uniform(-0.8, 0.8))))
        side = v_norm(v_cross(direction, (0.0, 1.0, 0.0)))
        if v_len(side) < 0.01:
            side = (1.0, 0.0, 0.0)
        p0 = v_add(c, v_mul(side, -width))
        p1 = v_add(c, v_mul(side, width))
        p2 = v_add(c, v_mul(direction, length))
        scene.add_triangle(p0, p1, p2, leaf_light if i % 5 == 0 else leaf)


# -----------------------------------------------------------------------------
# Nền sau: núi đá vôi Tràng An nhẹ file
# -----------------------------------------------------------------------------


def _add_background_karst(scene: SceneMesh, mat: dict[str, int | list[int]], rng: Random) -> None:
    stone = _mat(mat, "stone")
    stone_dark = _mat(mat, "stone_dark")
    moss = _mat(mat, "moss")
    leaf = _mat(mat, "leaf")
    leaf_light = _mat(mat, "leaf_light")
    trunk = _mat(mat, "wood_dark")

    clusters = [
        ((-5.4, 0.10, 4.65), 3.35, 1.05, 5),
        ((-1.2, 0.10, 5.05), 4.25, 1.20, 6),
        ((3.6, 0.10, 4.85), 3.85, 1.10, 5),
        ((6.2, 0.10, 4.15), 2.65, 0.80, 3),
    ]
    for center, height, radius, count in clusters:
        _add_karst_cluster(scene, center, height, radius, count, stone, stone_dark, moss, leaf, leaf_light, rng)

    # FIX 04: thêm cây xanh thật sự phía sau nhà.
    # Trước đó chỉ có tam giác lá rải rác trên núi nên nhìn xa giống rêu,
    # chưa ra cảm giác cây. Đoạn này tạo thân/cành + tán lá dạng khối thấp-poly.
    _add_background_tree_belt(scene, trunk, leaf, leaf_light, rng)

    # Bụi cây thấp sát chân tường để nối cảnh quan với tường đá.
    for i in range(22):
        x = -7.8 + i * 0.74 + rng.uniform(-0.16, 0.16)
        z = rng.uniform(3.15, 3.82)
        _add_leaf_cluster(scene, (x, 1.10, z), rng.uniform(0.32, 0.52), rng.randint(8, 13), leaf, leaf_light, rng)



def _add_background_tree_belt(
    scene: SceneMesh,
    trunk: int,
    leaf: int,
    leaf_light: int,
    rng: Random,
) -> None:
    """Thêm hàng cây phía sau nhà và quanh chân núi.

    Cây ở xa nên dùng hình học thấp-poly: thân nhỏ, vài cành, nhiều cụm tán lá.
    Như vậy nhìn trong GLB rõ là cây xanh nhưng file vẫn nhẹ.
    """
    # Hàng cây ngay sau tường: tán cao hơn tường đá để nhìn rõ từ phía trước.
    front_row = [
        (-7.55, 3.58, 2.35, 0.72),
        (-6.80, 3.76, 1.85, 0.58),
        (-5.95, 3.52, 2.15, 0.66),
        (-4.75, 3.78, 2.55, 0.76),
        (-3.65, 3.45, 1.95, 0.60),
        (-2.55, 3.85, 2.40, 0.70),
        (-1.45, 3.58, 1.85, 0.56),
        (-0.35, 3.92, 2.75, 0.80),
        (0.85, 3.50, 2.10, 0.63),
        (1.95, 3.80, 2.45, 0.72),
        (3.10, 3.58, 1.95, 0.60),
        (4.20, 3.88, 2.65, 0.78),
        (5.35, 3.48, 2.15, 0.66),
        (6.45, 3.76, 2.30, 0.70),
        (7.35, 3.50, 1.90, 0.58),
    ]
    for x, z, height, canopy_scale in front_row:
        _add_background_tree(
            scene,
            base=(x + rng.uniform(-0.12, 0.12), 0.12, z + rng.uniform(-0.10, 0.10)),
            height=height * rng.uniform(0.92, 1.08),
            canopy_scale=canopy_scale * rng.uniform(0.92, 1.12),
            trunk=trunk,
            leaf=leaf,
            leaf_light=leaf_light,
            rng=rng,
        )

    # Một số cây cao hơn chen giữa núi đá vôi để tạo cảm giác có rừng phía sau.
    back_row = [
        (-6.20, 4.85, 2.90, 0.82),
        (-4.20, 5.10, 3.20, 0.90),
        (-2.20, 5.35, 2.80, 0.78),
        (0.30, 5.48, 3.25, 0.95),
        (2.35, 5.25, 2.95, 0.82),
        (4.80, 5.05, 3.10, 0.88),
        (6.80, 4.65, 2.70, 0.76),
    ]
    for x, z, height, canopy_scale in back_row:
        _add_background_tree(
            scene,
            base=(x + rng.uniform(-0.20, 0.20), 0.10, z + rng.uniform(-0.18, 0.18)),
            height=height * rng.uniform(0.88, 1.10),
            canopy_scale=canopy_scale * rng.uniform(0.90, 1.15),
            trunk=trunk,
            leaf=leaf,
            leaf_light=leaf_light,
            rng=rng,
        )


def _add_background_tree(
    scene: SceneMesh,
    *,
    base: Vec3,
    height: float,
    canopy_scale: float,
    trunk: int,
    leaf: int,
    leaf_light: int,
    rng: Random,
) -> None:
    """Cây nền phía sau nhà: thân mảnh, cành thấp-poly, tán lá thành cụm rõ ràng."""
    top = (
        base[0] + rng.uniform(-0.18, 0.18),
        base[1] + height,
        base[2] + rng.uniform(-0.12, 0.12),
    )

    scene.add_frustum_between(
        base,
        top,
        0.055 * canopy_scale,
        0.030 * canopy_scale,
        trunk,
        segments=8,
    )

    # Cành chính để khi xoay model vẫn thấy là cây, không phải bụi lá nổi.
    branch_tips: list[Vec3] = []
    branch_count = rng.randint(3, 5)
    for i in range(branch_count):
        angle = math.tau * i / branch_count + rng.uniform(-0.35, 0.35)
        start = v_lerp(base, top, rng.uniform(0.58, 0.82))
        length = canopy_scale * rng.uniform(0.38, 0.72)
        tip = (
            start[0] + math.cos(angle) * length,
            start[1] + canopy_scale * rng.uniform(0.15, 0.42),
            start[2] + math.sin(angle) * length,
        )
        branch_tips.append(tip)
        scene.add_frustum_between(
            start,
            tip,
            0.025 * canopy_scale,
            0.012 * canopy_scale,
            trunk,
            segments=6,
        )

    # Tán chính và tán phụ. Dùng lathe để tạo khối lá bo tròn thấp-poly.
    _add_leaf_blob(scene, (top[0], top[1] - 0.18 * canopy_scale, top[2]), canopy_scale * 0.72, leaf, rng, segments=10)
    _add_leaf_blob(scene, (top[0] - 0.28 * canopy_scale, top[1] - 0.08 * canopy_scale, top[2] + 0.12 * canopy_scale), canopy_scale * 0.50, leaf_light, rng, segments=9)
    _add_leaf_blob(scene, (top[0] + 0.30 * canopy_scale, top[1] - 0.12 * canopy_scale, top[2] - 0.10 * canopy_scale), canopy_scale * 0.52, leaf, rng, segments=9)

    for tip_i, tip in enumerate(branch_tips):
        blob_mat = leaf_light if tip_i % 2 == 0 else leaf
        _add_leaf_blob(scene, tip, canopy_scale * rng.uniform(0.34, 0.48), blob_mat, rng, segments=8)

    # Vài lá tam giác ló ra quanh rìa tán để nhìn tự nhiên hơn khi xem gần.
    for _ in range(12):
        c = (
            top[0] + rng.uniform(-0.75, 0.75) * canopy_scale,
            top[1] + rng.uniform(-0.18, 0.42) * canopy_scale,
            top[2] + rng.uniform(-0.55, 0.55) * canopy_scale,
        )
        _add_single_leaf(scene, c, canopy_scale * rng.uniform(0.16, 0.28), leaf_light if rng.random() < 0.25 else leaf, rng)


def _add_leaf_blob(
    scene: SceneMesh,
    center: Vec3,
    scale: float,
    material: int,
    rng: Random,
    *,
    segments: int = 10,
) -> None:
    """Khối tán lá oval thấp-poly, đủ rõ hình cây nhưng không nặng file."""
    profile = [
        (0.10 * scale, -0.44 * scale),
        (0.38 * scale, -0.30 * scale),
        (0.56 * scale, -0.02 * scale),
        (0.47 * scale, 0.26 * scale),
        (0.24 * scale, 0.46 * scale),
        (0.05 * scale, 0.54 * scale),
    ]
    jittered_center = (
        center[0] + rng.uniform(-0.03, 0.03) * scale,
        center[1] + rng.uniform(-0.02, 0.02) * scale,
        center[2] + rng.uniform(-0.03, 0.03) * scale,
    )
    scene.add_lathe(jittered_center, profile, material, segments=segments)


def _add_single_leaf(scene: SceneMesh, center: Vec3, scale: float, material: int, rng: Random) -> None:
    angle = rng.random() * math.tau
    direction = v_norm((math.cos(angle), rng.uniform(-0.10, 0.35), math.sin(angle)))
    side = v_norm(v_cross(direction, (0.0, 1.0, 0.0)))
    if v_len(side) < 0.01:
        side = (1.0, 0.0, 0.0)
    p0 = v_add(center, v_mul(side, -0.35 * scale))
    p1 = v_add(center, v_mul(side, 0.35 * scale))
    p2 = v_add(center, v_mul(direction, 1.00 * scale))
    scene.add_triangle(p0, p1, p2, material)

def _add_karst_cluster(
    scene: SceneMesh,
    center: Vec3,
    height: float,
    radius: float,
    count: int,
    stone: int,
    stone_dark: int,
    moss: int,
    leaf: int,
    leaf_light: int,
    rng: Random,
) -> None:
    for i in range(count):
        angle = math.tau * i / count + rng.uniform(-0.45, 0.45)
        dist = rng.uniform(0.0, radius * 0.75)
        base = (
            center[0] + math.cos(angle) * dist,
            center[1],
            center[2] + math.sin(angle) * dist,
        )
        h = height * rng.uniform(0.62, 1.06)
        r = radius * rng.uniform(0.28, 0.55)
        _add_rock_pillar(scene, base, h, r, stone, rng)

        # Rãnh tối trên đá.
        for _ in range(3):
            groove_angle = rng.random() * math.tau
            x = base[0] + math.cos(groove_angle) * r * 0.88
            z = base[2] + math.sin(groove_angle) * r * 0.88
            scene.add_box_between((x, base[1] + h * 0.18, z), (x, base[1] + h * 0.78, z), 0.035, stone_dark, width=0.040)

        # Bụi cây/mảng rêu bám trên núi.
        for _ in range(3):
            ledge_angle = rng.random() * math.tau
            ledge_y = base[1] + h * rng.uniform(0.28, 0.82)
            ledge = (
                base[0] + math.cos(ledge_angle) * r * rng.uniform(0.45, 0.95),
                ledge_y,
                base[2] + math.sin(ledge_angle) * r * rng.uniform(0.45, 0.95),
            )
            _add_leaf_cluster(scene, ledge, rng.uniform(0.22, 0.42), rng.randint(8, 14), leaf, leaf_light, rng)
            scene.add_box((ledge[0], ledge[1] - 0.08, ledge[2]), (0.18, 0.035, 0.14), moss)


def _add_rock_pillar(scene: SceneMesh, base: Vec3, height: float, radius: float, material: int, rng: Random) -> None:
    segments = 10
    levels = 7
    rings: list[list[Vec3]] = []

    phase = rng.random() * math.tau
    for level in range(levels):
        t = level / (levels - 1)
        y = base[1] + height * t
        taper = (1.0 - 0.72 * t) * (1.0 + 0.10 * math.sin(t * math.tau + phase))
        ring_center_x = base[0] + math.sin(t * math.pi * 1.4 + phase) * radius * 0.12
        ring_center_z = base[2] + math.cos(t * math.pi * 1.1 + phase) * radius * 0.10
        ring: list[Vec3] = []
        for i in range(segments):
            angle = math.tau * i / segments
            rough = 0.80 + 0.28 * rng.random() + 0.12 * math.sin(angle * 3.0 + phase)
            r = radius * taper * rough
            ring.append((ring_center_x + math.cos(angle) * r, y, ring_center_z + math.sin(angle) * r))
        rings.append(ring)

    for level in range(levels - 1):
        for i in range(segments):
            j = (i + 1) % segments
            scene.add_quad(rings[level][i], rings[level][j], rings[level + 1][j], rings[level + 1][i], material)

    # Nắp đỉnh gồ ghề.
    top_center = (base[0], base[1] + height, base[2])
    for i in range(segments):
        j = (i + 1) % segments
        scene.add_triangle(top_center, rings[-1][i], rings[-1][j], material)
