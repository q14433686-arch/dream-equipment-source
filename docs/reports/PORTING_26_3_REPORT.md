# Dream Equipment — Minecraft 26.3 移植与 CI 部署报告

- **日期**：2026-10-13
- **分支**：`arena/413a9699-dream-equipment-source`
- **基线版本**：Minecraft `26.2` → **`26.3`**

---

## 1. 目标与背景

按照与同组织仓库 `{UN}TACZR`（`TaCZ_Refabricated_Unofficial`）、`TaCZTweaks_Unofficial`、`chiseled-enchanting-table-26.1.2-source` 对齐的 26.3 移植规范：

1. **先行部署 `{UN}TACZR` 同款 CI 基础设施**：在 `docs/ci/` 下预置 `compile-check.yml`、`build.yml`、`consistency.yml` 与 `docs/ci/README.md`，并提供本地与 CI 共用的静态门禁脚本 `scripts/check_release_consistency.sh`。
2. **完成 Minecraft 26.3 源码与构建矩阵升级**：对照 Minecraft 26.3 反编译源码（`0khs/minecraft_source_26.3`）、Fabric API `0.160.7+26.3` 源码与 NeoForge 26.3 Primer，逐一修复全部 26.3 破坏性 API 变更。

---

## 2. 依赖与构建矩阵升级

| 配置项 | 26.2 基线 | 26.3 迁移后 |
|---|---|---|
| `minecraft_version` | `26.2` | `26.3` |
| `loader_version` | `0.19.3` | `0.19.5` |
| `loom_version` | `1.17.13` | `1.17.20` |
| `fabric_api_version` | `0.153.0+26.2` | `0.160.7+26.3` |
| Gradle Wrapper | `9.5.1` | `9.5.1` |
| Java Toolchain | `25` | `25` |

同步更新了 `gradle.properties` 与 `src/main/resources/fabric.mod.json` 的 `depends` 声明。

---

## 3. Minecraft 26.3 & Fabric API `0.160.7+26.3` 破坏性变更适配

### 3.1 原版 `AxeItem` / `ShovelItem` / `HoeItem` 移除 → `Item.Properties#axe` / `#shovel` / `#hoe`
- **原因**：Minecraft 26.3 将斧剥皮/除锈/除蜡、锹压径/熄灭营火、锄耕地行为统一抽象为 `DataComponents.BLOCK_TRANSFORMER`（`BlockTransformers.AXE` / `SHOVEL` / `HOE`），并移除了 `net.minecraft.world.item.AxeItem`、`ShovelItem`、`HoeItem` 三个子类。
- **修复**（`DreamEquipmentItems.java`）：移除已删除的 `AxeItem`、`ShovelItem`、`HoeItem` 导入，在 `registerTools` 中直接调用 `new Item.Properties().axe(toolMaterial, 5.0f, -3.0f)`、`.shovel(toolMaterial, 1.5f, -3.0f)`、`.hoe(toolMaterial, -3.0f, 0.0f)` 注册标准 `Item`。

### 3.2 Fabric API `FuelValueEvents` 移除 → 原版 `DataComponents.COOKING_FUEL` (`CookingFuel`)
- **原因**：Minecraft 26.3 将熔炉燃料值迁移为物品数据组件 `DataComponents.COOKING_FUEL`（`net.minecraft.world.item.component.CookingFuel`），Fabric API `0.160.7+26.3` 随之移除了 `net.fabricmc.fabric.api.registry.FuelValueEvents`。
- **修复**（`DreamEquipmentFuelValues.java`）：改为通过 `DefaultItemComponentEvents.MODIFY` 为所有正燃料值材质家族的护甲（`perMaterial * 5/8/7/4`）与盾牌（`perMaterial * 6`）挂载 `DataComponents.COOKING_FUEL`：
  ```java
  CookingFuel fuel = new CookingFuel(
          new ResolvableInt.Constant(burnTime),
          ResolvableFloat.fromKey(ContextFloatProviders.COOKING_DEFAULT_SPEED_MULTIPLIER)
  );
  context.modify(item, builder -> builder.set(DataComponents.COOKING_FUEL, fuel));
  ```

### 3.3 `Player#drop(ItemStack, boolean)` 移除 → `drop(ItemStack, boolean, Prediction.SERVER_ONLY)`
- **原因**：Minecraft 26.3 移除了二参 `Player#drop(ItemStack, boolean)`，统一使用三参 `LivingEntity#drop(ItemStack, boolean, net.minecraft.util.Prediction)`。
- **修复**：
  - `DreamEquipmentEnchantingSupport.java`：青金石退还背包满时掉落改为 `player.drop(refund, false, Prediction.SERVER_ONLY)`。
  - `DreamEquipmentSetEffects.java`：易碎护甲碎裂返还材料及粘液护甲碎裂返还粘液球改为 `player.drop(returned, false, Prediction.SERVER_ONLY)`。

### 3.4 `Entity#hurtMarked` 重命名为 `Entity#syncVelocity`
- **原因**：Minecraft 26.3 将实体速度同步标记字段 `Entity.hurtMarked` 重命名为 `Entity.syncVelocity`。
- **修复**：
  - `DreamEquipmentSetEffects.java`：`bounceLikeSlime` 中 `player.hurtMarked = true` → `player.syncVelocity = true`。
  - `DreamEquipmentShieldEffects.java`：`slimeBounce` 中 `living.hurtMarked = true` → `living.syncVelocity = true`。

### 3.5 `RedStoneWireBlock` 重命名为 `RedstoneWireBlock`
- **原因**：Minecraft 26.3 将 `net.minecraft.world.level.block.RedStoneWireBlock` 规范化重命名为 `net.minecraft.world.level.block.RedstoneWireBlock`（小写 `s`），`getBlockSignal(Level, BlockPos)` 方法签名保持不变。
- **修复**（`RedStoneWireBlockMixin.java`）：更新导入与 `@Mixin(RedstoneWireBlock.class)` 目标类，保留 Mixin 类名 `RedStoneWireBlockMixin` 以兼容 `dream_equipment.mixins.json`。

---

## 4. Mixin 目标逐项核验（Minecraft 26.3）

| Mixin 类 | 目标类（26.3） | 注入目标与签名 | 26.3 状态 |
|---|---|---|---|
| `EnchantmentMenuAccessor` | `net.minecraft.world.inventory.EnchantmentMenu` | `@Accessor("enchantSlots") Container` | 字段未变，完全兼容 |
| `EnchantmentMenuMixin` | `net.minecraft.world.inventory.EnchantmentMenu` | `clickMenuButton(Player, int)` | 方法签名未变，完全兼容 |
| `RedStoneWireBlockMixin` | `net.minecraft.world.level.block.RedstoneWireBlock` | `getBlockSignal(Level, BlockPos)` | 目标类名更新为 `RedstoneWireBlock`，方法签名未变 |
| `RedstoneWireEvaluatorMixin` | `net.minecraft.world.level.redstone.RedstoneWireEvaluator` | `getBlockSignal(Level, BlockPos)` | 类名与签名未变，完全兼容 |
| `SignalGetterMixin` | `net.minecraft.world.level.SignalGetter` | `getSignal` / `getDirectSignal` / `getBestNeighborSignal` / `hasNeighborSignal` | 接口与签名未变，完全兼容 |
| `ShieldSpecialRendererMixin` | `net.minecraft.client.renderer.special.ShieldSpecialRenderer` | `submit(DataComponentMap, PoseStack, SubmitNodeCollector, int, int, boolean, int)` | 签名与 `SpriteId` 局部变量槽位未变，完全兼容 |

---

## 5. Minecraft 26.2 / 26.3 新方块与新物品内容适配（`60 → 69` 家族，`372 → 426` 物品）

围绕 Minecraft 26.2 / 26.3 新增的硫磺洞穴（Sulfur Caves）、白杨木（Poplar）、朱砂（Cinnabar）、层架菌（Shelf Mushroom）、草床（Straw Bed）与 16 色软垫（Cushions）以及生态材料树脂（Resin）与鹦鹉螺壳（Nautilus Shell），新增 **9 个装备家族、54 件新装备**：

| 家族 ID | 核心材料 | 新增装备（件数） | 26.3 专属机制与套装/盾牌特性 |
|---|---|---|---|
| `poplar` | `minecraft:poplar_planks` | 头盔、胸甲、护腿、靴子、盾牌（5） | 整套缓降 I + 速度 I；移动/缓降飘落三色白杨秋叶粒子（`RED/ORANGE/YELLOW_POPLAR_LEAVES`）；格挡卷起落叶气流推开攻击者；可作熔炉燃料（300 tick/单位） |
| `poplar_log` | `minecraft:poplar_log` | 头盔、胸甲、护腿、靴子、盾牌（5） | 整套缓降 I + 抗性提升 I；移动/缓降飘落三色白杨秋叶粒子；支持 `#minecraft:poplar_logs` 修复；可作熔炉燃料（300 tick/单位） |
| `sulfur` | `minecraft:sulfur` | 4 护甲 + 剑/镐/斧/锹/锄/矛 + 盾牌（11） | **间歇泉热力弹射 + 易碎爆燃岩石融合流**：整套水中抗火并净除反胃/中毒；受火焰/爆炸、水中受击、护甲碎裂或举盾格挡时喷发 `SULFUR_BUBBLES` + `GEYSER_ERUPTION_START` 硫磺间歇泉，向上弹飞近战敌人并附加反胃与缓慢；支持 `potent_sulfur` / `sulfur_spike` 修复；可作高热燃料（400 tick/单位） |
| `cinnabar` | `minecraft:cinnabar` | 4 护甲 + 剑/镐/斧/锹/锄/矛 + 盾牌（11） | **丹砂辟邪流**：高附魔（18）石质护甲与工具，整套常驻生命恢复 I 并持续净除中毒与凋零；手持朱砂剑获得生命恢复 I；朱砂盾牌格挡魔法/亡灵伤害返还耐久并使亡灵虚弱 |
| `shelf_mushroom` | `minecraft:shelf_mushroom` | 层架菌靴子、层架菌盾牌（2） | 还原 26.3 `ShelfMushroomBlock` 弹性机制：≤8 格摔落免伤并播放 `SHELF_MUSHROOM_BOUNCE` 弹性弹跳（>8 格减免 50% 摔落伤害，无粘液套的时间自耗）；盾牌格挡弹反近战攻击者 |
| `resin` | `minecraft:resin_brick` | 4 护甲 + 剑/矛 + 盾牌（7） | **琥珀粘滞流**：整套常驻抗性提升 I；近战受击或举盾格挡时为攻击者附加 `Slowness II` 并伴随 `FALLING_HONEY` 粒子 |
| `nautilus_shell` | `minecraft:nautilus_shell` | 4 护甲 + 矛 + 盾牌（6） | **深海螺壳流**：整套常驻 26.x 原版 `minecraft:breath_of_the_nautilus`（鹦鹉螺之息）及水中海豚的恩惠 I + 潮涌能量 I；手持鹦鹉螺壳矛在水中获得海豚的恩惠；盾牌水中格挡返还耐久并喷射水流推开目标 |
| `straw` | `minecraft:straw_bed` | 草帽、草编蓑衣、草编护腿、草鞋、草编盾牌（5） | **草编轻装**：整套常驻速度 I，干燥环境下额外获得急迫 I；支持草床/干草块/小麦修复；可作燃料（150 tick/单位） |
| `cushion` | `#minecraft:cushions` | 软垫靴子、软垫盾牌（2） | **软垫缓冲**：支持全部 16 色 `#minecraft:cushions` 合成与修复；靴子提供 0.1 击退抗性并减免 40% 摔落伤害（播放 `CUSHION_SIT` 音效）；盾牌格挡缓和冲击并返还 1 点耐久 |

---

## 6. CI 部署与门禁自检结果

- 已新增 `.gitignore`、`docs/ci/README.md`、`docs/ci/compile-check.yml`、`docs/ci/build.yml`、`docs/ci/consistency.yml` 与 `scripts/check_release_consistency.sh`。
- 已为 `scripts/validate_dream_equipment_assets.py` 补充无 `Pillow` 环境下的标准 PNG `IHDR` 尺寸解析回退与 26.3 源码断言支持。
- 本地运行 `bash scripts/check_release_consistency.sh --strict` 及全部 5 个 Python 校验脚本全部通过（`families=69, items=426`），且对 `src/main/java` 全部 19 个源文件针对 Minecraft 26.3 与 Fabric API `0.160.7+26.3` 源码树的导入/符号扫描缺失数为 `0`。
