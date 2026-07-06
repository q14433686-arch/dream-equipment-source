# Round 56 — 穿戴贴图重做准备报告
**日期：2026-07-06**  
**性质：准备工作 / 下一轮执行**

---

## 一、背景与问题陈述

用户反馈：石头类装备、红石、青金石（含黑曜石）的穿戴贴图与原料材质关联性极差，无法通过视觉辨别材料来源。

本轮完成全量诊断分析，**下一轮执行批量脚本重做**。

---

## 二、MC 26.1 装备穿戴贴图规范（通过原版 jar 逆向确认）

### 文件结构
```
assets/<mod>/textures/entity/equipment/
  humanoid/<family>.png          64×32  RGBA  —— 头盔 + 胸甲 + 双臂
  humanoid_leggings/<family>.png 64×32  RGBA  —— 护腿
  humanoid_baby/<family>.png     64×64  RGBA  —— 幼体缩放版
```

### humanoid.png UV 分区（64×32，逆向自原版 iron.png）

```
 y= 0-7   x= 8-15   →  头盔正面 (8×8 px)
 y= 8-15  x= 0-31   →  头盔完整面组（含侧/顶/底，带 helmet "visor" 形状）
 y=16-19  x= 8-47   →  双臂上部（左右各 4px 宽）
 y=20-25  x=16-55   →  胸甲正面 + 双臂下部
 y=26-31  x= 0-39   →  腰部/前摆
```

### 关键设计规律（原版手工像素画风格）
- 每张贴图只有 **5–10 种颜色**（不需要也不应该梯度过渡）
- 颜色来自 **原版 block 材质调色板**，直接采用或轻微明暗调整
- UV 形状边缘 1px 使用调色板中**最深色**做轮廓
- 内部 2–3 级明暗变化模拟**立体感**（上/前面亮，侧/下面暗）
- **不做 tiling 纹理平铺**，整块填充 + 少量高光点/深色缝隙

---

## 三、当前穿戴贴图诊断结果

### 3.1 UV 形状 — 全部正确 ✅

所有家族穿戴贴图的非透明像素布局与原版 iron 完全一致，UV 模板正确，无需修改形状/模板。

### 3.2 颜色保真度诊断

以下颜色分析基于：  
`avg_nearest_dist` = 穿戴贴图每像素到原版 block 调色板最近色的平均距离  
`unique_colors` = 穿戴贴图中不重复颜色数

| 家族 | 状态 | avg_dist | 核心问题 |
|---|---|---|---|
| **obsidian（黑曜石）** | 🔴 严重 | 34.8 | B 通道严重偏高（≈81 vs 原版≈24），整体偏蓝紫而非近黑 |
| **lapis（青金石）** | 🔴 严重 | 23.0 | 蓝色过亮（B≈183 vs 原版≈140），缺少金色高光点 |
| **quartz（石英）** | 🔴 严重 | 30.1 | 偏黄暖调（avg #ddd2bd），原版石英是冷白（avg #ebe5de） |
| **redstone（红石）** | 🟡 中等 | 23.0 | 颜色梯度集中在中红，缺少原版 redstone_block 的深暗红对比 |
| **amethyst（紫晶）** | 🟡 中等 | 30.0 | 偏洋红（R偏高），原版紫晶块是蓝紫均衡的中饱和紫 |
| **stone（石头）** | 🟢 颜色OK | 5.8 | 颜色贴近，但纹理细节过少（lum_std=7.1 vs 原版建议>12） |
| **cobblestone（圆石）** | 🟢 颜色OK | 10.2 | 颜色尚可，但圆石特有的不规则石块图案完全缺失 |
| **blackstone（黑石）** | 🟢 颜色OK | 7.3 | 颜色合理，但黑石独特的紫色底纹/纹路视觉缺失 |
| **granite（花岗岩）** | 🟢 颜色OK | 7.3 | 颜色贴近，但花岗岩的粉红矿点质感缺失 |
| **andesite（安山岩）** | 🟢 颜色OK | 5.9 | 颜色近似，andesite 独特的冷灰色调略有丢失 |
| **diorite（闪长岩）** | 🟡 中等 | 10.4 | 闪长岩的白灰斑驳感缺失，整体偏均匀灰 |
| **basalt（玄武岩）** | 🟢 颜色OK | 8.3 | 颜色可接受，玄武岩条带纹路视觉不明显 |
| **smooth_basalt（光滑玄武岩）** | 🟢 颜色OK | 7.3 | 颜色可接受，与 basalt 区分度不足 |
| **netherrack（地狱岩）** | 🟢 颜色OK | 4.7 | 颜色贴近，但肉色/腐烂质感缺失 |
| **sandstone（砂岩）** | 🟢 颜色OK | — | 整体表现尚可，准确度较高 |
| **red_sandstone（红砂岩）** | 🟢 颜色OK | — | 整体尚可 |
| **end_stone（末地石）** | 🟢 颜色OK | — | 整体尚可 |
| **tuff（凝灰岩）** | 🟢 颜色OK | — | 整体尚可 |
| **calcite（方解石）** | 🟢 颜色OK | — | 整体尚可 |
| **dripstone_block（滴水石块）** | 🟢 颜色OK | — | 整体尚可 |
| **mossy_cobblestone（苔石圆石）** | 🟢 颜色OK | — | 绿色苔藓调色存在，尚可 |
| **cobbled_deepslate（深板岩圆石）** | 🟢 颜色OK | — | 整体尚可 |

---

## 四、根本问题分类

当前穿戴贴图的生成方式是**对 UV mask 内部像素做原版 block 调色板的线性插值平铺**，存在两类根本问题：

### 问题 A：颜色来源错误（高优先级）
影响：obsidian、lapis、quartz、redstone、amethyst

这几种材质的贴图颜色不是从正确的原版 block 材质提取，导致穿着时视觉上辨识不出材料。

| 家族 | 现有穿戴主色 | 应有主色（原版 block 实测） | 差异描述 |
|---|---|---|---|
| obsidian | `#190751` 亮紫蓝 | `#0f0a18` 近黑微紫 | **B 通道比原版高 57**，蓝得不像黑曜石 |
| lapis | `#224fb7` 亮蓝 | `#1e438c` 深海蓝 | **亮度偏高**，缺少原版 lapis_block 的金色小亮点 |
| quartz | `#ddd2bd` 暖米黄 | `#ebe5de` 冷白灰 | **偏黄**，原版石英是近乎纯白的冷调 |
| redstone | `#c9201c` 中红 | `#af1805` 暗红+`#e62008` 亮红 | **缺少深暗色**，原版 redstone_block 有强对比的暗红区域 |
| amethyst | `#9e55d9` 洋红紫 | `#8561bf` 蓝紫 | **R 偏高 25，B 偏高 26**，偏洋红而非蓝紫 |

### 问题 B：纹理细节不足（中优先级）
影响：stone、cobblestone、blackstone、diorite、granite、netherrack，以及几乎全部石质材质

这些材质颜色勉强接近，但贴图内部只有 2–3 级亮度的平滑梯度，缺少原版材质的**石纹/矿脉/斑驳感**。

原版穿戴贴图虽然只有 5–10 种颜色，但排布方式是**非均匀的像素画图案**，呈现出材质特征：
- iron → 金属板缝/铆钉感
- chainmail → 链环图案
- diamond → 宝石棱面反光

我们的石质贴图缺少的是：
- stone → 自然裂缝/岩石纹理感
- cobblestone → 不规则鹅卵石块分割线
- blackstone → 紫色基岩纹/层纹
- granite → 粉色矿点
- netherrack → 不规则腐肉/孔洞感

---

## 五、下一轮执行方案

### 方案选择

采用**基于原版 block 材质采样的确定性重新生成**，新增 `scripts/generate_rock_worn_textures.py`，逻辑类比 `generate_wood_worn_textures.py` 但针对石质/矿物特性定制。

**不手工绘制**：维持架构分工原则，纹理由脚本从原版 jar 材质确定性生成。

### 生成策略（按材质分类）

#### 策略 1：完整色板映射（高置信度直接采样）
适用：sandstone、red_sandstone、end_stone、tuff、calcite、granite、diorite、andesite、basalt、smooth_basalt、dripstone_block、netherrack、mossy_cobblestone、cobbled_deepslate、cobblestone、stone、blackstone

做法：
1. 从 MC jar 加载对应 block 材质（16×16）
2. 用 **Floyd-Steinberg 量化** 将材质色板压缩到 5–8 色
3. 保留原 UV mask 形状（alpha 不变）
4. 对每个非透明像素，按其在 UV 区域内的相对坐标映射到 block 材质对应位置采样
5. 叠加边缘暗化（最深色，1px 轮廓）和立体感（上/前亮化 × 1.15，下/侧暗化 × 0.85）

特殊纹理处理规则：

| 家族 | block 纹理 | 附加处理 |
|---|---|---|
| cobblestone | `cobblestone` | 找石块边界（颜色跳变）→ 保留分割线 |
| blackstone | `blackstone` | 保留紫色基岩层纹，区分 R/G/B 各通道比例 |
| granite | `granite` | 保留粉色矿点高亮 |
| diorite | `diorite` | 保留黑白斑驳（不均匀分布） |
| mossy_cobblestone | `mossy_cobblestone` | 双区块混采：石色 + 苔藓绿色分开处理 |
| netherrack | `netherrack` | 保留深红和腐蚀孔洞暗点 |
| smooth_basalt | `smooth_basalt` | 与 basalt 明度对比区分 |

#### 策略 2：颜色校正（高偏差材质优先修正）
适用：obsidian、lapis、redstone、quartz、amethyst

做法：
1. 同上采样流程，但对采样结果做**色彩空间校正**，确保最终均值落在原版 block avg ±10 以内
2. 具体校正参数（下一轮执行时写入脚本）：

| 家族 | 目标 avg_rgb | 颜色空间操作 |
|---|---|---|
| obsidian | `#0f0a18` | B 通道从 ≈81 压到 ≈24，提升 R/G 微弱紫调 |
| lapis | `#1e438c` | 降低 B 通道约 43，保留少量金色高光点（原版 lapis_block 实测有 `#8f8a00` 金色） |
| quartz | `#ebe5de` | 向冷白偏移：减少 R-B 差值（原版 R-B≈13，我们 R-B≈32） |
| redstone | 双色对比 | 保留 `#e62008` 高亮 + `#730c00` 暗红的强对比，中间不插值 |
| amethyst | `#8561bf` | G 通道加 12，R 通道减 25，向蓝紫方向偏移 |

#### 策略 3：区分度增强
适用：basalt vs smooth_basalt、stone vs cobblestone vs cobbled_deepslate

现状：basalt 和 smooth_basalt 穿戴层几乎无视觉区别。

做法：
- basalt：保留 `basalt_side` 的**竖条纹**特征（dark stripes）
- smooth_basalt：使用 `smooth_basalt` 的**均匀暗色**，饱和度略高于 basalt
- cobbled_deepslate：比 cobblestone 整体暗 30–40 亮度单位，添加蓝灰冷色调

---

## 六、原版 block 材质调色板整理（供下一轮直接使用）

以下为从 MC 26.1.2 客户端 jar 提取的每种材质调色板（top-5 颜色，按出现频率排序）：

| 家族 | 来源 block | 颜色 1 | 颜色 2 | 颜色 3 | 颜色 4 | 颜色 5 |
|---|---|---|---|---|---|---|
| stone | stone | `#7f7f7f` | `#747474` | `#8f8f8f` | `#686868` | — |
| cobblestone | cobblestone | `#888788` | `#616161` | `#6e6d6d` | `#a6a6a6` | `#b5b5b5` |
| cobbled_deepslate | cobbled_deepslate | `#4a4a4f` | `#3f3f45` | `#353539` | `#5a5a5a` | `#7a7a7a` |
| blackstone | blackstone | `#27221c` | `#20131c` | `#312c36` | `#3c3947` | `#160f10` |
| sandstone | sandstone | `#dad2a3` | `#d1ba8a` | `#e7e4bb` | `#c6ae71` | `#e3dbb0` |
| red_sandstone | red_sandstone | `#c06822` | `#ac5712` | `#d2752b` | `#9f4e0b` | `#cb6e24` |
| end_stone | end_stone | `#d5da94` | `#eef6b4` | `#dee6a4` | `#cdc68b` | `#c5be8b` |
| tuff | tuff | `#6a6e6f` | `#5d5d52` | `#85837b` | `#4d5046` | `#a0a297` |
| calcite | calcite | `#d9dbd7` | `#edece6` | `#c9c9c4` | `#f0f5f4` | `#ffffff` |
| granite | granite | `#9f6b58` | `#7f5646` | `#a97764` | `#926251` | `#5f4034` |
| diorite | diorite | `#e9e9e9` | `#a4a2a2` | `#bebfc1` | `#8b8b8b` | `#cececf` |
| andesite | andesite | `#8a8a8e` | `#7f7f7f` | `#9c9c9c` | `#747474` | `#a8aa9a` |
| basalt | basalt_side | `#4f4b4f` | `#5c5c5c` | `#3a3b48` | `#32333d` | `#1b2632` |
| smooth_basalt | smooth_basalt | `#4f4b4f` | `#5c5c5c` | `#3a3b48` | `#32333d` | `#1b2632` |
| dripstone_block | dripstone_block | `#927965` | `#836356` | `#735450` | `#a08d71` | `#634a47` |
| netherrack | netherrack | `#652828` | `#723232` | `#501b1b` | `#511515` | `#572121` |
| mossy_cobblestone | mossy_cobblestone | `#525d39` | `#888788` | `#627941` | `#6e6d6d` | `#5a6d41` |
| **redstone** | redstone_block | `#e62008` | `#730c00` | `#a41808` | `#941400` | `#bd2008` |
| **lapis** | lapis_block | `#1e4285` | `#204a8a` | `#1c3890` | `#20509c` | `#1b3588` |
| **obsidian** | obsidian | `#06030b` | `#100c1c` | `#000001` | `#271e3d` | `#3b2754` |
| **amethyst** | amethyst_block | `#7a5bb5` | `#64479e` | `#8d6acc` | `#a678f1` | `#5d3a9a` |
| **quartz** | quartz_block_side | `#eeeae6` | `#eee6de` | `#eae2da` | `#f2efed` | `#ddd9cb` |

---

## 七、脚本计划：`scripts/generate_rock_worn_textures.py`

### 输入
- MC 客户端 jar（`~/.gradle/caches/fabric-loom/26.1.2/minecraft-client.jar`）
- 现有穿戴贴图（作为 UV alpha mask 模板）

### 输出
- `textures/entity/equipment/humanoid/<family>.png` — 重写（仅修改非透明像素颜色）
- `textures/entity/equipment/humanoid_leggings/<family>.png` — 同上
- `textures/entity/equipment/humanoid_baby/<family>.png` — 同上（64×64 版）

### 主要参数表（`ROCK_FAMILY_CONFIG`）
每个家族包含：
- `block_texture`：原版 block 纹理名称
- `strategy`：`"direct"`（直接采样）或 `"corrected"`（颜色校正）
- `color_correction`（可选）：RGB 偏移或目标 avg
- `enhance_features`（可选）：`"cobble_seams"` / `"stripe"` / `"speckle"` 等

### 核心逻辑
```python
def regen_rock_layer(mask_path, block_texture, strategy, config):
    mask = load_rgba(mask_path)          # 保留 alpha
    block = load_block_texture(block_name)
    palette = extract_palette(block, max_colors=8)
    
    for pixel in opaque_pixels(mask):
        x, y = pixel.pos
        # 1. 从 block 材质采样（按 UV 区域内相对坐标映射）
        raw = sample_block(block, map_uv(x, y, region))
        # 2. 颜色校正（如需）
        corrected = apply_correction(raw, config)
        # 3. 立体感阴影
        shaded = apply_shading(corrected, edge=is_edge(mask, x, y), 
                               side=uv_side(x, y))
        # 4. 特殊纹理增强
        final = apply_feature(shaded, x, y, config)
        mask.set_pixel(x, y, final)
    
    mask.save(mask_path)
```

---

## 八、优先级排序

| 优先级 | 家族 | 原因 |
|---|---|---|
| P0（必改） | obsidian、lapis、quartz | 颜色严重偏离，视觉完全无法辨认材料 |
| P1（必改） | redstone、amethyst | 颜色偏差中等但材料特征丢失 |
| P2（建议改） | cobblestone、blackstone、diorite、granite | 颜色OK但无材质感 |
| P3（可选） | stone、andesite、basalt、smooth_basalt、netherrack | 颜色接近，细节不足，不影响辨认 |
| 暂缓 | sandstone、red_sandstone、end_stone、tuff、calcite、dripstone_block、mossy_cobblestone、cobbled_deepslate | 当前表现可接受 |

---

## 九、不修改的内容（本次审计边界）

- **UV alpha 形状/模板**：与原版 iron 完全一致，无需改动
- **equipment/*.json**：装备定义文件无需改动
- **Java 源码**：纯资源文件改动，Java 零修改
- **木质/木板类穿戴贴图**：已由 `generate_wood_worn_textures.py` 专门管理，本次不动
- **盾牌贴图**：由 `generate_shield_textures.py` 管理，本次不动

---

## 十、执行后的验证清单

- [ ] `python3 scripts/generate_equipment_resources.py` — PASS
- [ ] `python3 scripts/validate_equipment_families_json.py` — PASS  
- [ ] `python3 scripts/validate_dream_equipment_assets.py` — PASS
- [ ] `python3 scripts/validate_set_effects_json.py` — PASS
- [ ] `python3 scripts/audit_equipment_balance.py` — PASS
- [ ] `python3 scripts/generate_rock_worn_textures.py` — 新脚本运行 PASS
- [ ] Gradle build — BUILD SUCCESSFUL
- [ ] 生成审计对比图（改前 vs 改后 vs 原版 block）
- [ ] 客户端：穿戴各套装确认颜色可辨认
- [ ] 客户端：obsidian 呈近黑色、lapis 呈深蓝、redstone 呈暗红+亮红对比

---

## 十一、审计图像

- `docs/reports/ROUND56_WORN_TEXTURE_AUDIT_PRE.png` — 当前所有石质穿戴贴图一览（4x放大）
- `docs/reports/ROUND56_WORN_VS_SOURCE_AUDIT.png` — 原版 block 材质 vs 当前穿戴贴图对比（全量）
- `docs/reports/ROUND56_WORN_DETAIL_AUDIT.png` — 三列详细对比（block源 | 当前worn | iron UV参考）

---

*本文档由 Round 56 诊断分析生成，供下一轮批量修改使用。*
