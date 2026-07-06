# 玻璃装备半透明效果技术调研报告
**日期：2026-07-06 | Round 57 附属调研**

---

## 一、调研目标

调查在 MC 26.1.2 / Fabric Loader 0.19.3 / Fabric API 0.152.1 环境下，实现玻璃装备**全套半透明视觉**的可行方案，涵盖：

- 穿戴贴图（worn layer，人物身上的装备渲染）
- 物品栏图标（item texture，背包/手持显示）
- 手持/使用状态（handheld / in-hand）

---

## 二、当前玻璃装备状态

### 贴图文件

| 文件 | 尺寸 | 当前 alpha | 状态 |
|---|---|---|---|
| `textures/entity/equipment/humanoid/glass.png` | 64×32 | 全不透明（255） | ❌ 无半透明 |
| `textures/entity/equipment/humanoid_leggings/glass_leggings.png` | 64×32 | 全不透明（255） | ❌ 无半透明 |
| `textures/entity/equipment/humanoid_baby/glass.png` | 64×64 | 全不透明（255） | ❌ 无半透明 |
| `textures/item/glass_helmet.png` | 128×128 | 全不透明（255） | ❌ 无半透明 |
| `textures/item/glass_chestplate.png` | 128×128 | 全不透明（255） | ❌ 无半透明 |
| `textures/item/glass_sword.png` | 128×128 | 全不透明（255） | ❌ 无半透明 |
| （其余 item 贴图同上） | | | |

### 现有 equipment.json

```json
{
  "layers": {
    "humanoid": [ { "texture": "dream_equipment:glass" } ],
    "humanoid_baby": [ { "texture": "dream_equipment:glass" } ],
    "humanoid_leggings": [ { "texture": "dream_equipment:glass_leggings" } ]
  }
}
```

无任何渲染类型控制字段。

---

## 三、原版渲染管线分析（逆向 MC 26.1.2 jar）

### 3.1 EquipmentLayerRenderer 固定使用 armorCutoutNoCull

反编译分析确认：`EquipmentLayerRenderer.renderLayers()` 固定调用：

```java
RenderTypes.armorCutoutNoCull(identifier)
```

- `armorCutoutNoCull` = **CUTOUT 模式**：alpha 非 0 即 255，无中间值。
- 所有装备穿戴贴图天然走 CUTOUT 渲染管线。
- **结论：原版装备渲染管线不支持半透明穿戴层。**

### 3.2 armorTranslucent 存在但未被装备渲染器使用

`RenderTypes.class` 中存在 `armorTranslucent()` 方法（无参，返回 `RenderType`），但：
- `EquipmentLayerRenderer` **没有调用** `armorTranslucent`
- Fabric API 0.152.1 没有提供装备渲染注入 hook
- `armorTranslucent` 仅作为备用 RenderType 定义，供 Mixin 手动使用

### 3.3 EquipmentClientInfo.Layer CODEC 字段清单

```
textureId  (必填)
dyeable    (可选，皮革染色机制)
use_player_texture (可选，仅鞘翅用)
```

**没有 `render_type` / `translucent` / `alpha` 等字段** → 无法通过 JSON 单独配置渲染模式。

### 3.4 原版玻璃材质本身的 alpha 情况

| 材质 | alpha 值 | 说明 |
|---|---|---|
| `block/glass` | 0 或 255 | **CUTOUT**，中心完全透明，边框不透明 |
| `block/white_stained_glass` | 102 / 155 / 163 | **TRANSLUCENT**，真正半透明 |
| `block/tinted_glass` | 110 / 200 | **TRANSLUCENT**，半透明 |

→ 染色玻璃是真正的半透明材质，但不能直接用于装备渲染（管线不支持）。

---

## 四、item 贴图（物品栏/手持）的半透明情况

### 4.1 原版 item/generated 模型的渲染管线

物品栏和手持状态使用 `minecraft:item/generated` 父模型，渲染管线由**物品的 item model JSON** 决定：

- 默认走 `item_cutout`（CUTOUT），alpha 0/255 二值化
- 可通过 `items/*.json` 中的 `tint_source` 等机制着色
- **item 贴图原生支持半透明**：物品渲染走 `item_translucent` 通道（`RenderTypes.itemTranslucent()`），条件是贴图 PNG 中存在中间 alpha 值

#### 关键结论

> **item 贴图（背包图标/手持）天然支持半透明 PNG，只要贴图有半透明像素，MC 会自动切换为 `item_translucent` 渲染路径。**
> 这与穿戴层不同，不需要任何 Mixin。

验证：`RenderTypes.class` 中 `itemTranslucent` 与 `itemCutout` 并存，且 item 渲染器会根据贴图内容自动选择。

### 4.2 item model 中的 gui_light 对半透明的影响

```json
{
  "parent": "minecraft:item/generated",
  "gui_light": "front",
  "textures": { "layer0": "dream_equipment:item/glass_helmet" }
}
```

`gui_light: front` = 正面光照，适合半透明玻璃物品。改为 `side` 会有侧面阴影，不适合玻璃。

---

## 五、穿戴层半透明的实现路径

### 方案 A：Mixin 注入 EquipmentLayerRenderer（推荐，技术上可行）

**原理**：拦截 `renderLayers` 方法，对 glass 材质改用 `RenderTypes.armorTranslucent()` 渲染。

```java
@Mixin(EquipmentLayerRenderer.class)
public abstract class GlassEquipmentRenderMixin {
    @Inject(
        method = "renderLayers(...)",
        at = @At(value = "INVOKE", 
                 target = "Lnet/minecraft/client/renderer/rendertype/RenderTypes;armorCutoutNoCull(...)"),
        cancellable = true
    )
    private void dream_equipment$useTranslucentForGlass(
        EquipmentClientInfo.LayerType type,
        ResourceKey<EquipmentAsset> key,
        Model model,
        ItemStack stack,
        PoseStack poseStack,
        SubmitNodeCollector collector,
        int light,
        CallbackInfo ci
    ) {
        // 检测是否为 glass 家族装备
        if (DreamEquipmentItems.isGlassArmor(stack)) {
            // 改用 armorTranslucent，绕过 CUTOUT
            // ... 渲染逻辑
            ci.cancel();
        }
    }
}
```

**难点**：
1. `armorTranslucent()` 不接受贴图参数（无参方法），需要独立绑定贴图 → 可能需要额外的渲染状态管理
2. 透明渲染顺序问题：半透明物体需要从后往前渲染（depth sorting），装备套穿在人物上时排序会有边缘重叠 artifact
3. 深度写入（depth write）问题：半透明层写深度会导致层叠闪烁
4. MC 26.1 渲染管线重构（Render Graph），mixin 注入点可能不稳定

**评估**：技术上可行，但实现复杂度高，且可能有视觉 artifact。

---

### 方案 B：修改穿戴贴图使用 CUTOUT 模拟玻璃感（无需 Mixin，推荐优先试）

**原理**：不做真正的半透明，而是在装备 UV mask 内画出玻璃边框 + 高光线，中间镂空（alpha=0），模拟玻璃的视觉语言。

与原版 `block/glass` 一致：边框可见，内部全透明。

```
UV mask 当前（全填充）:
██████████
██████████
██████████

改为玻璃风格（仅边框+高光）:
██▒░░░░░░█  ← 边框 alpha=255, 高光 alpha=200
█░░░░░░░░█
█░░░░░░░░█  ← 内部全透明 alpha=0
█░░░░░░░░█
██████████
```

**效果**：穿戴时肤色/衣服在玻璃"格子"缝隙中透出，视觉上类似玻璃板。

**优点**：
- **零 Mixin，零 Java 改动**
- 纯贴图修改，完全数据驱动
- 和原版 CUTOUT 管线完全兼容
- 不会有半透明排序 artifact

**缺点**：
- 不是"真"半透明，内部完全镂空而非半透明叠色
- 视觉效果为"玻璃格/窗框"而非"染色玻璃"

---

### 方案 C：双层贴图（外框 CUTOUT + 内层染色，模拟染色玻璃）

**原理**：
1. 外层：原有 UV 形状，使用 CUTOUT，仅保留边框像素（边缘 2px）
2. 内层：附加一个 `dyeable` 染色层，整体半色调染色

**实现**：
```json
{
  "layers": {
    "humanoid": [
      { "texture": "dream_equipment:glass" },
      { "texture": "dream_equipment:glass_inner", "dyeable": { "color_when_undyed": "#b0d8ff66" } }
    ]
  }
}
```

但问题：`dyeable` 机制仍走 CUTOUT，不支持真正的半透明叠色。

---

### 方案 D：Fabric Rendering API + 自定义渲染层（最完整，最复杂）

使用 Fabric Rendering API（`fabric-rendering-v1`），自定义 `BlockEntityRenderer` / `EntityRenderer` 额外渲染通道，在玩家渲染完成后追加一个半透明装备层。

**成本极高，超出本项目当前范围。**

---

## 六、item 贴图半透明实现方案（无限制，直接可用）

**item 贴图（背包图标/手持/地面丢弃）完全支持半透明 PNG**，无需任何 Mixin。

### 实现步骤

1. 将 `textures/item/glass_*.png` 中的非边框像素改为半透明（alpha ≈ 80–140）
2. 使用染色玻璃的蓝灰色调（`#b0d8ff`）作为主色
3. 保留高光线（alpha=200）和边框（alpha=255）
4. `gui_light` 设为 `front`（已是当前设置）

**视觉参考**：参照原版 `block/white_stained_glass`（alpha 102/155/163）的半透明程度。

---

## 七、一致性策略建议

| 贴图类型 | 推荐方案 | 技术限制 | 视觉效果 |
|---|---|---|---|
| **item 图标**（背包/合成界面） | ✅ 直接半透明 PNG | 无 | 真半透明，效果最好 |
| **手持贴图**（item/generated handheld） | ✅ 直接半透明 PNG | 无 | 真半透明 |
| **穿戴层**（worn equipment） | ⚠️ 方案 B（镂空边框） | 管线限制 | 伪透明，玻璃格风格 |
| 穿戴层（真半透明） | 方案 A（Mixin） | 复杂，有 artifact 风险 | 真半透明，但有排序问题 |

**推荐执行顺序**：
1. 先做 item 贴图半透明（零风险，效果显著）
2. 再做穿戴贴图方案 B（镂空边框，CUTOUT 兼容）
3. 如果用户满意，停止；如果追求真穿戴半透明，再评估 Mixin 方案 A

---

## 八、颜色设计参考

### 原版玻璃色调

| 类型 | 主色 | alpha |
|---|---|---|
| 普通玻璃边框 | `#7baeb7` `#8bc1cd` `#d0eae9` | 255（不透明边框） |
| 白色染色玻璃 | `#ffffff` | 102 / 155 / 163 |
| 浅蓝染色玻璃 | `#74c4f5`（估算） | 102 / 163 |
| 青色染色玻璃 | `#158991`（估算） | 102 / 163 |

### 玻璃装备建议色调

- **主色（半透明填充）**：`#a8d4e8` alpha=110（参照白色染色玻璃）
- **高光线**：`#d8eff8` alpha=180
- **边框/棱线**：`#5f9aaa` alpha=255
- **阴影边**：`#3a7080` alpha=255

---

## 九、结论

| 问题 | 答案 |
|---|---|
| 穿戴贴图能否直接支持半透明 PNG？ | **否**。`EquipmentLayerRenderer` 固定使用 `armorCutoutNoCull`，CUTOUT 管线，alpha 二值化。 |
| item 贴图能否支持半透明 PNG？ | **是**。item 渲染器自动检测并使用 `item_translucent`。 |
| 最简单的穿戴视觉方案？ | 方案 B：镂空边框 CUTOUT 贴图，模拟玻璃格风格。 |
| 真穿戴半透明是否可行？ | 可行，但需要 Mixin 注入 `EquipmentLayerRenderer`，且有半透明排序 artifact 风险。 |
| 建议下一步做什么？ | 先做 item 贴图半透明（本轮可执行），再做穿戴层镂空边框，评估效果后决定是否追加 Mixin。 |

---

## 十、参考资料（逆向来源）

- `net/minecraft/client/renderer/entity/layers/EquipmentLayerRenderer.class` — 装备层渲染入口，确认 `armorCutoutNoCull` 调用
- `net/minecraft/client/renderer/rendertype/RenderTypes.class` — `armorTranslucent()` / `armorCutoutNoCull()` / `itemTranslucent()` 方法定义
- `net/minecraft/client/resources/model/EquipmentClientInfo$Layer.class` — equipment JSON 的 CODEC 字段（texture / dyeable / use_player_texture）
- `assets/minecraft/textures/block/white_stained_glass.png` — alpha=102/155/163，真半透明参考
- `assets/minecraft/textures/block/glass.png` — alpha=0/255，CUTOUT 参考

---

*本报告由 Round 57 技术调研生成，供下一轮实现决策使用。*
