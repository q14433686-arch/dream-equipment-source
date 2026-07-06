package com.dreamequipment;

import com.google.gson.Gson;
import com.google.gson.JsonObject;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

public final class DreamEquipmentShieldEffectRules {
    private static final Gson GSON = new Gson();
    private static DreamEquipmentShieldEffectRules CURRENT = defaults();

    public final CactusShield cactus;
    public final GlassShield glass;
    public final RedstoneShield redstone;
    public final SlimeShield slime;
    public final PaperShield paper;
    public final ObsidianShield obsidian;
    public final PrismarineShield prismarine;
    public final AmethystShield amethyst;
    public final BoneShield bone;
    public final CoalShield coal;
    public final QuartzShield quartz;

    private DreamEquipmentShieldEffectRules(CactusShield cactus, GlassShield glass, RedstoneShield redstone, SlimeShield slime, PaperShield paper,
                                            ObsidianShield obsidian, PrismarineShield prismarine, AmethystShield amethyst,
                                            BoneShield bone, CoalShield coal, QuartzShield quartz) {
        this.cactus = cactus;
        this.glass = glass;
        this.redstone = redstone;
        this.slime = slime;
        this.paper = paper;
        this.obsidian = obsidian;
        this.prismarine = prismarine;
        this.amethyst = amethyst;
        this.bone = bone;
        this.coal = coal;
        this.quartz = quartz;
    }

    public static DreamEquipmentShieldEffectRules current() {
        return CURRENT;
    }

    public static void load() {
        try (var stream = DreamEquipmentShieldEffectRules.class.getClassLoader().getResourceAsStream("data/dream_equipment/set_effects.json")) {
            if (stream == null) {
                CURRENT = defaults();
                return;
            }
            try (var reader = new InputStreamReader(stream, StandardCharsets.UTF_8)) {
                JsonObject root = GSON.fromJson(reader, JsonObject.class);
                CURRENT = parse(object(root, "shield_effects"));
            }
        } catch (Exception ex) {
            CURRENT = defaults();
            System.err.println("[Dream Equipment] Failed to load shield_effects from set_effects.json: " + ex.getMessage());
        }
    }

    private static DreamEquipmentShieldEffectRules parse(JsonObject root) {
        JsonObject cactus = object(root, "cactus");
        JsonObject glass = object(root, "glass");
        JsonObject redstone = object(root, "redstone");
        JsonObject slime = object(root, "slime");
        JsonObject paper = object(root, "paper");
        JsonObject obsidian = object(root, "obsidian");
        JsonObject prismarine = object(root, "prismarine");
        JsonObject amethyst = object(root, "amethyst");
        JsonObject bone = object(root, "bone");
        JsonObject coal = object(root, "coal");
        JsonObject quartz = object(root, "quartz");
        return new DreamEquipmentShieldEffectRules(
            new CactusShield(bool(cactus, "enabled", true), flt(cactus, "retaliate_damage", 1.0f), integer(cactus, "cooldown_ticks", 20)),
            new GlassShield(bool(glass, "enabled", true), flt(glass, "shatter_threshold", 5.0f), flt(glass, "shatter_chance", 0.25f)),
            new RedstoneShield(bool(redstone, "enabled", true), integer(redstone, "pulse_signal", 15), integer(redstone, "pulse_ticks", 8)),
            new SlimeShield(bool(slime, "enabled", true), flt(slime, "knockback_strength", 0.60f), flt(slime, "vertical_boost", 0.10f)),
            new PaperShield(bool(paper, "enabled", true), integer(paper, "wet_damage_interval", 20), integer(paper, "wet_damage", 1)),
            new ObsidianShield(bool(obsidian, "enabled", true), integer(obsidian, "refund_damage", 2), integer(obsidian, "slowness_duration_ticks", 40), integer(obsidian, "slowness_amplifier", 0)),
            new PrismarineShield(bool(prismarine, "enabled", true), integer(prismarine, "water_refund_damage", 1)),
            new AmethystShield(bool(amethyst, "enabled", true), integer(amethyst, "sonic_boom_damage_cost", 8)),
            new BoneShield(bool(bone, "enabled", true), integer(bone, "undead_refund_damage", 1)),
            new CoalShield(bool(coal, "enabled", true), integer(coal, "fire_refund_damage", 2)),
            new QuartzShield(bool(quartz, "enabled", true), integer(quartz, "projectile_refund_damage", 1))
        );
    }

    private static DreamEquipmentShieldEffectRules defaults() {
        return new DreamEquipmentShieldEffectRules(
            new CactusShield(true, 1.0f, 20),
            new GlassShield(true, 5.0f, 0.25f),
            new RedstoneShield(true, 15, 8),
            new SlimeShield(true, 0.60f, 0.10f),
            new PaperShield(true, 20, 1),
            new ObsidianShield(true, 2, 40, 0),
            new PrismarineShield(true, 1),
            new AmethystShield(true, 8),
            new BoneShield(true, 1),
            new CoalShield(true, 2),
            new QuartzShield(true, 1)
        );
    }

    private static JsonObject object(JsonObject root, String key) {
        return root != null && root.has(key) && root.get(key).isJsonObject() ? root.getAsJsonObject(key) : new JsonObject();
    }

    private static boolean bool(JsonObject obj, String key, boolean fallback) { return obj != null && obj.has(key) ? obj.get(key).getAsBoolean() : fallback; }
    private static int integer(JsonObject obj, String key, int fallback) { return obj != null && obj.has(key) ? obj.get(key).getAsInt() : fallback; }
    private static float flt(JsonObject obj, String key, float fallback) { return obj != null && obj.has(key) ? obj.get(key).getAsFloat() : fallback; }

    public record CactusShield(boolean enabled, float retaliateDamage, int cooldownTicks) {}
    public record GlassShield(boolean enabled, float shatterThreshold, float shatterChance) {}
    public record RedstoneShield(boolean enabled, int pulseSignal, int pulseTicks) {}
    public record SlimeShield(boolean enabled, float knockbackStrength, float verticalBoost) {}
    public record PaperShield(boolean enabled, int wetDamageInterval, int wetDamage) {}
    public record ObsidianShield(boolean enabled, int refundDamage, int slownessDurationTicks, int slownessAmplifier) {}
    public record PrismarineShield(boolean enabled, int waterRefundDamage) {}
    public record AmethystShield(boolean enabled, int sonicBoomDamageCost) {}
    public record BoneShield(boolean enabled, int undeadRefundDamage) {}
    public record CoalShield(boolean enabled, int fireRefundDamage) {}
    public record QuartzShield(boolean enabled, int projectileRefundDamage) {}
}
