package com.dreamequipment.client;

import com.dreamequipment.DreamEquipment;
import com.dreamequipment.DreamEquipmentFamilyRules;
import com.dreamequipment.DreamEquipmentSetEffectRules;
import com.dreamequipment.DreamEquipmentShieldEffectRules;
import net.fabricmc.fabric.api.client.item.v1.ItemTooltipCallback;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.ItemStack;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public final class DreamEquipmentTooltips {
    private DreamEquipmentTooltips() {}

    public static void register() {
        ItemTooltipCallback.EVENT.register((stack, context, tooltipFlag, lines) -> append(stack, lines));
    }

    private static void append(ItemStack stack, List<Component> lines) {
        Identifier id = BuiltInRegistries.ITEM.getKey(stack.getItem());
        if (id == null) return;
        if ("minecraft".equals(id.getNamespace()) && "turtle_helmet".equals(id.getPath())) {
            DreamEquipmentFamilyRules.Family family = familyById("turtle_shell");
            if (family == null) return;
            lines.add(Component.translatable("tooltip.dream_equipment.header").withStyle(ChatFormatting.DARK_AQUA));
            lines.add(Component.translatable("tooltip.dream_equipment.material", materialName("turtle_shell")).withStyle(ChatFormatting.GRAY));
            appendSetEffects(lines, "turtle_shell", "turtle_helmet", true, false);
            return;
        }
        if (!DreamEquipment.MOD_ID.equals(id.getNamespace())) return;
        String path = id.getPath();
        DreamEquipmentFamilyRules.Family family = familyFor(path);
        if (family == null) return;

        lines.add(Component.translatable("tooltip.dream_equipment.header").withStyle(ChatFormatting.DARK_AQUA));
        String suffix = path.substring(family.id().length() + 1);
        boolean isArmor = family.armor() != null && family.armor().pieces().contains(suffix);
        boolean isTool = family.tools() != null && family.tools().types().contains(suffix);
        boolean isShield = family.shield() != null && family.shield().enabled() && "shield".equals(suffix);
        if (isArmor) appendArmor(lines, family, suffix);
        if (isTool) appendTool(lines, family, suffix);
        if (isShield) appendShield(lines, family);
        appendSetEffects(lines, family.id(), path, isArmor, isTool);
        if (isShield) appendShieldEffects(lines, family.id());
    }

    private static DreamEquipmentFamilyRules.Family familyFor(String itemPath) {
        return DreamEquipmentFamilyRules.current().families.stream()
            .filter(f -> itemPath.startsWith(f.id() + "_"))
            .max(Comparator.comparingInt(f -> f.id().length()))
            .orElse(null);
    }

    private static DreamEquipmentFamilyRules.Family familyById(String id) {
        return DreamEquipmentFamilyRules.current().families.stream()
            .filter(f -> f.id().equals(id))
            .findFirst()
            .orElse(null);
    }

    private static void appendArmor(List<Component> lines, DreamEquipmentFamilyRules.Family family, String piece) {
        DreamEquipmentFamilyRules.Armor armor = family.armor();
        int defense = switch (piece) {
            case "helmet" -> armor.helmetDefense();
            case "chestplate" -> armor.chestplateDefense();
            case "leggings" -> armor.leggingsDefense();
            case "boots" -> armor.bootsDefense();
            default -> 0;
        };
        lines.add(Component.translatable("tooltip.dream_equipment.material", materialName(family.id())).withStyle(ChatFormatting.GRAY));
        lines.add(Component.translatable("tooltip.dream_equipment.armor", defense, armorDurability(piece, armor.durabilityMultiplier())).withStyle(ChatFormatting.GRAY));
        if (armor.toughness() > 0.0f || armor.knockbackResistance() > 0.0f) {
            lines.add(Component.translatable("tooltip.dream_equipment.toughness", trim(armor.toughness()), trim(armor.knockbackResistance())).withStyle(ChatFormatting.GRAY));
        }
        lines.add(Component.translatable("tooltip.dream_equipment.enchantability", armor.enchantmentValue()).withStyle(ChatFormatting.DARK_GRAY));
    }

    private static void appendShield(List<Component> lines, DreamEquipmentFamilyRules.Family family) {
        DreamEquipmentFamilyRules.Shield shield = family.shield();
        lines.add(Component.translatable("tooltip.dream_equipment.material", materialName(family.id())).withStyle(ChatFormatting.GRAY));
        lines.add(Component.translatable("tooltip.dream_equipment.shield", shield.durability()).withStyle(ChatFormatting.GRAY));
    }

    private static void appendTool(List<Component> lines, DreamEquipmentFamilyRules.Family family, String toolType) {
        DreamEquipmentFamilyRules.Tools tools = family.tools();
        lines.add(Component.translatable("tooltip.dream_equipment.material", materialName(family.id())).withStyle(ChatFormatting.GRAY));
        lines.add(Component.translatable("tooltip.dream_equipment.tool", toolName(toolType), tools.durability()).withStyle(ChatFormatting.GRAY));
        lines.add(Component.translatable("tooltip.dream_equipment.tool_stats", trim(tools.speed()), trim(tools.attackDamageBonus())).withStyle(ChatFormatting.GRAY));
        lines.add(Component.translatable("tooltip.dream_equipment.enchantability", tools.enchantmentValue()).withStyle(ChatFormatting.DARK_GRAY));
    }

    private static void appendSetEffects(List<Component> lines, String material, String itemPath, boolean isArmor, boolean isTool) {
        DreamEquipmentSetEffectRules rules = DreamEquipmentSetEffectRules.current();
        List<Component> effects = new ArrayList<>();
        if (isArmor) {
            for (DreamEquipmentSetEffectRules.PassiveEffectRule rule : rules.passiveEffects) {
                if (rule.material().equals(material)) {
                    effects.add(Component.translatable("tooltip.dream_equipment.effect", condition(rule.condition()), effectName(rule.effect()), roman(rule.amplifier() + 1)).withStyle(ChatFormatting.BLUE));
                }
            }
            if (rules.cactus.enabled() && material.equals("cactus")) effects.add(Component.translatable("tooltip.dream_equipment.cactus", trim(rules.cactus.damagePerPiece())).withStyle(ChatFormatting.GREEN));
            if (rules.slime.enabled() && material.equals("slime")) {
                effects.add(Component.translatable("tooltip.dream_equipment.slime_decay").withStyle(ChatFormatting.GREEN));
                effects.add(Component.translatable("tooltip.dream_equipment.slime_cancel", percent(rules.slime.damageCancelChance())).withStyle(ChatFormatting.GREEN));
                if (itemPath.endsWith("_boots")) effects.add(Component.translatable("tooltip.dream_equipment.slime_boots", trim(rules.slime.bootsSafeFallDistance())).withStyle(ChatFormatting.GREEN));
            }
        if (itemPath.equals("armadillo_shell_boots")) effects.add(Component.translatable("tooltip.dream_equipment.armadillo_terrain").withStyle(ChatFormatting.GREEN));
        if (material.equals("lapis") && isArmor) effects.add(Component.translatable("tooltip.dream_equipment.lapis_enchanting").withStyle(ChatFormatting.BLUE));
        if (material.equals("redstone") && itemPath.endsWith("_boots")) effects.add(Component.translatable("tooltip.dream_equipment.redstone_signal", rules.redstoneSignal.bootsSignal(), rules.redstoneSignal.bootsPulseTicks(), rules.redstoneSignal.fullSetSignal(), rules.redstoneSignal.fullSetPulseTicks()).withStyle(ChatFormatting.RED));
            for (DreamEquipmentSetEffectRules.WetDurabilityRule rule : rules.wetDurabilityRules) {
                if (rule.material().equals(material)) effects.add(Component.translatable("tooltip.dream_equipment.wet_weakness", rule.damage(), rule.intervalTicks()).withStyle(ChatFormatting.YELLOW));
            }
            for (DreamEquipmentSetEffectRules.WetRepairRule rule : rules.wetRepairRules) {
                if (rule.material().equals(material)) effects.add(Component.translatable("tooltip.dream_equipment.wet_repair", rule.repair(), rule.intervalTicks()).withStyle(ChatFormatting.GREEN));
            }
            for (DreamEquipmentSetEffectRules.BrittleRule rule : rules.brittleRules) {
                if (rule.material().equals(material) && !hasStonePhysicsRule(rules, material)) effects.add(Component.translatable("tooltip.dream_equipment.brittle", trim(rule.damageThreshold()), percent(rule.shatterChance())).withStyle(ChatFormatting.RED));
            }
            for (DreamEquipmentSetEffectRules.StoneArmorPhysicsRule rule : rules.stoneArmorPhysicsRules) {
                if (rule.material().equals(material)) effects.add(Component.translatable("tooltip.dream_equipment.stone_physics", percent(rule.cancelChancePerPiece() * 4.0f), trim(rule.shatterDamageThreshold()), trim(rule.slownessPerPiece() * 4.0f)).withStyle(ChatFormatting.DARK_GRAY));
            }
            for (DreamEquipmentSetEffectRules.DamageImmunityRule rule : rules.damageImmunities) {
                if (rule.material().equals(material)) effects.add(Component.translatable("tooltip.dream_equipment.damage_immunity", damageTypeName(rule.damageType())).withStyle(ChatFormatting.LIGHT_PURPLE));
            }
        }
        if (isTool) {
            for (DreamEquipmentSetEffectRules.BrittleWeaponRule rule : rules.brittleWeaponRules) {
                if (rule.material().equals(material)) effects.add(Component.translatable("tooltip.dream_equipment.brittle_weapon", percent(rule.breakChance())).withStyle(ChatFormatting.RED));
            }
            for (DreamEquipmentSetEffectRules.HeldEffectRule rule : rules.heldEffects) {
                if (itemPath.equals(rule.item().contains(":") ? rule.item().substring(rule.item().indexOf(':') + 1) : rule.item())) {
                    effects.add(Component.translatable("tooltip.dream_equipment.held_effect", condition(rule.condition()), effectName(rule.effect()), roman(rule.amplifier() + 1)).withStyle(ChatFormatting.BLUE));
                }
            }
        }
        if (!effects.isEmpty()) {
            lines.add(Component.translatable("tooltip.dream_equipment.effects_header").withStyle(ChatFormatting.GOLD));
            lines.addAll(effects);
        }
    }

    private static void appendShieldEffects(List<Component> lines, String material) {
        DreamEquipmentShieldEffectRules rules = DreamEquipmentShieldEffectRules.current();
        List<Component> effects = new ArrayList<>();
        if ("cactus".equals(material) && rules.cactus.enabled()) effects.add(Component.translatable("tooltip.dream_equipment.shield_cactus", trim(rules.cactus.retaliateDamage()), rules.cactus.cooldownTicks()).withStyle(ChatFormatting.GREEN));
        if ("glass".equals(material) && rules.glass.enabled()) effects.add(Component.translatable("tooltip.dream_equipment.shield_glass", trim(rules.glass.shatterThreshold()), percent(rules.glass.shatterChance())).withStyle(ChatFormatting.RED));
        if ("redstone".equals(material) && rules.redstone.enabled()) effects.add(Component.translatable("tooltip.dream_equipment.shield_redstone", rules.redstone.pulseSignal(), rules.redstone.pulseTicks()).withStyle(ChatFormatting.RED));
        if ("slime".equals(material) && rules.slime.enabled()) effects.add(Component.translatable("tooltip.dream_equipment.shield_slime", trim(rules.slime.knockbackStrength())).withStyle(ChatFormatting.GREEN));
        if ("paper".equals(material) && rules.paper.enabled()) effects.add(Component.translatable("tooltip.dream_equipment.shield_paper", rules.paper.wetDamage(), rules.paper.wetDamageInterval()).withStyle(ChatFormatting.YELLOW));
        if ("obsidian".equals(material) && rules.obsidian.enabled()) effects.add(Component.translatable("tooltip.dream_equipment.shield_obsidian", rules.obsidian.refundDamage()).withStyle(ChatFormatting.DARK_GRAY));
        if ("prismarine".equals(material) && rules.prismarine.enabled()) effects.add(Component.translatable("tooltip.dream_equipment.shield_prismarine", rules.prismarine.waterRefundDamage()).withStyle(ChatFormatting.AQUA));
        if ("amethyst".equals(material) && rules.amethyst.enabled()) effects.add(Component.translatable("tooltip.dream_equipment.shield_amethyst", rules.amethyst.sonicBoomDamageCost()).withStyle(ChatFormatting.LIGHT_PURPLE));
        if ("bone".equals(material) && rules.bone.enabled()) effects.add(Component.translatable("tooltip.dream_equipment.shield_bone", rules.bone.undeadRefundDamage()).withStyle(ChatFormatting.GRAY));
        if ("coal".equals(material) && rules.coal.enabled()) effects.add(Component.translatable("tooltip.dream_equipment.shield_coal", rules.coal.fireRefundDamage()).withStyle(ChatFormatting.DARK_GRAY));
        if ("quartz".equals(material) && rules.quartz.enabled()) effects.add(Component.translatable("tooltip.dream_equipment.shield_quartz", rules.quartz.projectileRefundDamage()).withStyle(ChatFormatting.WHITE));
        if (!effects.isEmpty()) {
            lines.add(Component.translatable("tooltip.dream_equipment.effects_header").withStyle(ChatFormatting.GOLD));
            lines.addAll(effects);
        }
    }

    private static boolean hasStonePhysicsRule(DreamEquipmentSetEffectRules rules, String material) {
        for (DreamEquipmentSetEffectRules.StoneArmorPhysicsRule rule : rules.stoneArmorPhysicsRules) if (rule.material().equals(material)) return true;
        return false;
    }

    private static Component damageTypeName(String id) {
        String path = id.contains(":") ? id.substring(id.indexOf(':') + 1) : id;
        return switch (path) {
            case "sonic_boom" -> Component.translatable("damage_type.minecraft.sonic_boom");
            default -> Component.literal(path);
        };
    }

    private static int armorDurability(String piece, int multiplier) {
        return switch (piece) {
            case "helmet" -> 11 * multiplier;
            case "chestplate" -> 16 * multiplier;
            case "leggings" -> 15 * multiplier;
            case "boots" -> 13 * multiplier;
            default -> multiplier;
        };
    }

    private static Component materialName(String id) { return Component.translatable("material.dream_equipment." + id); }
    private static Component toolName(String toolType) { return Component.translatable("tooltip.dream_equipment.tool." + toolType); }
    private static Component condition(String condition) { return Component.translatable("tooltip.dream_equipment.condition." + condition); }
    private static Component effectName(String id) {
        String path = id.contains(":") ? id.substring(id.indexOf(':') + 1) : id;
        return Component.translatable("effect.minecraft." + path);
    }
    private static String roman(int level) { return switch (level) { case 1 -> "I"; case 2 -> "II"; case 3 -> "III"; case 4 -> "IV"; case 5 -> "V"; default -> String.valueOf(level); }; }
    private static String trim(float value) { return Math.abs(value - Math.round(value)) < 0.001f ? String.valueOf(Math.round(value)) : String.format(java.util.Locale.ROOT, "%.2f", value); }
    private static String percent(float chance) { return Math.round(chance * 100.0f) + "%"; }
}
