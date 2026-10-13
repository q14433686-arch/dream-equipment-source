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

## 5. CI 部署与门禁自检结果

- 已新增 `.gitignore`、`docs/ci/README.md`、`docs/ci/compile-check.yml`、`docs/ci/build.yml`、`docs/ci/consistency.yml` 与 `scripts/check_release_consistency.sh`。
- 已为 `scripts/validate_dream_equipment_assets.py` 补充无 `Pillow` 环境下的标准 PNG `IHDR` 尺寸解析回退与 26.3 源码断言支持。
- 本地运行 `bash scripts/check_release_consistency.sh --strict` 及全部 5 个 Python 校验脚本全部通过，且对 `src/main/java` 全部 19 个源文件针对 Minecraft 26.3 与 Fabric API `0.160.7+26.3` 源码树的导入/符号扫描缺失数为 `0`。
