package com.dreamequipment;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.damagesource.DamageType;
import net.minecraft.world.effect.MobEffect;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class DreamEquipmentSetEffectRules {
    private static final Gson GSON = new Gson();
    private static DreamEquipmentSetEffectRules CURRENT = defaults();

    public final boolean enabled;
    public final List<PassiveEffectRule> passiveEffects;
    public final CactusRule cactus;
    public final SlimeRule slime;
    public final List<BrittleRule> brittleRules;
    public final List<WetDurabilityRule> wetDurabilityRules;
    public final RedstoneSignalRule redstoneSignal;
    public final List<WetRepairRule> wetRepairRules;
    public final List<BrittleWeaponRule> brittleWeaponRules;
    public final List<StoneArmorPhysicsRule> stoneArmorPhysicsRules;
    public final List<DamageImmunityRule> damageImmunities;
    public final ArmadilloBootsRule armadilloBoots;
    public final List<HeldEffectRule> heldEffects;

    private DreamEquipmentSetEffectRules(boolean enabled, List<PassiveEffectRule> passiveEffects, CactusRule cactus, SlimeRule slime, List<BrittleRule> brittleRules, List<WetDurabilityRule> wetDurabilityRules, RedstoneSignalRule redstoneSignal, List<WetRepairRule> wetRepairRules, List<BrittleWeaponRule> brittleWeaponRules, List<StoneArmorPhysicsRule> stoneArmorPhysicsRules, List<DamageImmunityRule> damageImmunities, ArmadilloBootsRule armadilloBoots, List<HeldEffectRule> heldEffects) {
        this.enabled = enabled;
        this.passiveEffects = List.copyOf(passiveEffects);
        this.cactus = cactus;
        this.slime = slime;
        this.brittleRules = List.copyOf(brittleRules);
        this.wetDurabilityRules = List.copyOf(wetDurabilityRules);
        this.redstoneSignal = redstoneSignal;
        this.wetRepairRules = List.copyOf(wetRepairRules);
        this.brittleWeaponRules = List.copyOf(brittleWeaponRules);
        this.stoneArmorPhysicsRules = List.copyOf(stoneArmorPhysicsRules);
        this.damageImmunities = List.copyOf(damageImmunities);
        this.armadilloBoots = armadilloBoots;
        this.heldEffects = List.copyOf(heldEffects);
    }

    public static DreamEquipmentSetEffectRules current() {
        return CURRENT;
    }

    public static void load() {
        try (var stream = DreamEquipmentSetEffectRules.class.getClassLoader().getResourceAsStream("data/dream_equipment/set_effects.json")) {
            if (stream == null) {
                CURRENT = defaults();
                return;
            }
            try (var reader = new InputStreamReader(stream, StandardCharsets.UTF_8)) {
                JsonObject root = GSON.fromJson(reader, JsonObject.class);
                CURRENT = parse(root);
            }
        } catch (Exception ex) {
            CURRENT = defaults();
            System.err.println("[Dream Equipment] Failed to load set_effects.json, using defaults: " + ex.getMessage());
        }
    }

    private static DreamEquipmentSetEffectRules parse(JsonObject root) {
        boolean enabled = bool(root, "enabled", true);
        List<PassiveEffectRule> passive = new ArrayList<>();
        JsonArray passiveArray = array(root, "passive_effects");
        for (JsonElement element : passiveArray) {
            JsonObject obj = element.getAsJsonObject();
            passive.add(new PassiveEffectRule(
                str(obj, "material", ""),
                str(obj, "effect", "minecraft:luck"),
                str(obj, "condition", "always"),
                integer(obj, "duration_ticks", 120),
                integer(obj, "amplifier", 0)
            ));
        }

        JsonObject cactusObj = object(root, "cactus_retaliation");
        CactusRule cactus = new CactusRule(
            bool(cactusObj, "enabled", true),
            flt(cactusObj, "damage_per_piece", 0.5f)
        );

        JsonObject slimeObj = object(root, "slime");
        SlimeRule slime = new SlimeRule(
            bool(slimeObj, "enabled", true),
            integer(slimeObj, "durability_damage_per_tick", 1),
            flt(slimeObj, "damage_cancel_chance", 0.10f),
            flt(slimeObj, "boots_safe_fall_distance", 12.0f),
            flt(slimeObj, "bounce_min_velocity", 0.45f),
            flt(slimeObj, "bounce_distance_divisor", 14.0f),
            flt(slimeObj, "fall_heal_ratio", 0.50f),
            intMap(object(slimeObj, "return_slime_balls"))
        );

        List<BrittleRule> brittle = new ArrayList<>();
        JsonArray brittleArray = array(root, "brittle_sets");
        for (JsonElement element : brittleArray) {
            JsonObject obj = element.getAsJsonObject();
            brittle.add(new BrittleRule(
                str(obj, "material", "glass"),
                flt(obj, "damage_threshold", 6.0f),
                flt(obj, "shatter_chance", 0.25f)
            ));
        }
        List<WetDurabilityRule> wetDurability = new ArrayList<>();
        JsonArray wetArray = array(root, "wet_durability");
        for (JsonElement element : wetArray) {
            JsonObject obj = element.getAsJsonObject();
            wetDurability.add(new WetDurabilityRule(
                str(obj, "material", "paper"),
                integer(obj, "interval_ticks", 100),
                integer(obj, "damage", 1)
            ));
        }
        JsonObject redstoneObj = object(root, "redstone_signal");
        RedstoneSignalRule redstone = new RedstoneSignalRule(
            bool(redstoneObj, "enabled", true),
            integer(redstoneObj, "boots_signal", 7),
            integer(redstoneObj, "full_set_signal", 15),
            integer(redstoneObj, "boots_pulse_ticks", 8),
            integer(redstoneObj, "full_set_pulse_ticks", 12)
        );
        List<WetRepairRule> wetRepair = new ArrayList<>();
        for (JsonElement element : array(root, "wet_repair")) {
            JsonObject obj = element.getAsJsonObject();
            wetRepair.add(new WetRepairRule(str(obj, "material", "mossy_cobblestone"), integer(obj, "interval_ticks", 60), integer(obj, "repair", 1)));
        }
        List<BrittleWeaponRule> brittleWeapons = new ArrayList<>();
        for (JsonElement element : array(root, "brittle_weapons")) {
            JsonObject obj = element.getAsJsonObject();
            brittleWeapons.add(new BrittleWeaponRule(str(obj, "material", "obsidian"), flt(obj, "break_chance", 0.05f)));
        }
        List<StoneArmorPhysicsRule> stonePhysics = new ArrayList<>();
        for (JsonElement element : array(root, "stone_armor_physics")) {
            JsonObject obj = element.getAsJsonObject();
            stonePhysics.add(new StoneArmorPhysicsRule(
                str(obj, "material", "stone"),
                flt(obj, "cancel_chance_per_piece", 0.0f),
                flt(obj, "shatter_damage_threshold", 999.0f),
                flt(obj, "slowness_per_piece", 0.0f)
            ));
        }
        List<DamageImmunityRule> damageImmunities = new ArrayList<>();
        for (JsonElement element : array(root, "damage_immunities")) {
            JsonObject obj = element.getAsJsonObject();
            damageImmunities.add(new DamageImmunityRule(str(obj, "material", "amethyst"), str(obj, "damage_type", "minecraft:sonic_boom")));
        }
        JsonObject armadilloObj = object(root, "armadillo_boots");
        List<String> armadilloBlocks = new ArrayList<>();
        for (JsonElement element : array(armadilloObj, "blocks")) armadilloBlocks.add(element.getAsString());
        ArmadilloBootsRule armadillo = new ArmadilloBootsRule(
            bool(armadilloObj, "enabled", true), armadilloBlocks,
            str(armadilloObj, "effect", "minecraft:speed"),
            integer(armadilloObj, "duration_ticks", 80),
            integer(armadilloObj, "amplifier", 2)
        );
        List<HeldEffectRule> heldEffects = new ArrayList<>();
        for (JsonElement element : array(root, "held_effects")) {
            JsonObject obj = element.getAsJsonObject();
            heldEffects.add(new HeldEffectRule(
                str(obj, "item", ""),
                str(obj, "condition", "always"),
                str(obj, "effect", "minecraft:haste"),
                integer(obj, "duration_ticks", 120),
                integer(obj, "amplifier", 0)
            ));
        }
        return new DreamEquipmentSetEffectRules(enabled, passive, cactus, slime, brittle, wetDurability, redstone, wetRepair, brittleWeapons, stonePhysics, damageImmunities, armadillo, heldEffects);
    }

    private static DreamEquipmentSetEffectRules defaults() {
        List<PassiveEffectRule> passive = List.of(
            new PassiveEffectRule("emerald", "minecraft:luck", "always", 220, 0),
            new PassiveEffectRule("emerald", "minecraft:hero_of_the_village", "always", 220, 0),
            new PassiveEffectRule("bone", "minecraft:night_vision", "always", 260, 0),
            new PassiveEffectRule("lapis", "minecraft:haste", "always", 220, 0),
            new PassiveEffectRule("redstone", "minecraft:speed", "always", 140, 0),
            new PassiveEffectRule("quartz", "minecraft:resistance", "always", 140, 0),
            new PassiveEffectRule("amethyst", "minecraft:regeneration", "always", 120, 0),
            new PassiveEffectRule("prismarine", "minecraft:water_breathing", "always", 260, 0),
            new PassiveEffectRule("prismarine", "minecraft:dolphins_grace", "in_water", 120, 0),
            new PassiveEffectRule("slime", "minecraft:jump_boost", "always", 140, 0),
            new PassiveEffectRule("slime", "minecraft:slow_falling", "always", 140, 0),
            new PassiveEffectRule("coal", "minecraft:fire_resistance", "always", 140, 0),
            new PassiveEffectRule("mossy_cobblestone", "minecraft:regeneration", "always", 120, 0),
            new PassiveEffectRule("cobbled_deepslate", "minecraft:resistance", "always", 140, 0),
            new PassiveEffectRule("cobbled_deepslate", "minecraft:slowness", "always", 120, 0),
            new PassiveEffectRule("blackstone", "minecraft:fire_resistance", "always", 140, 0),
            new PassiveEffectRule("blackstone", "minecraft:slowness", "always", 120, 0),
            new PassiveEffectRule("sandstone", "minecraft:speed", "always", 120, 0),
            new PassiveEffectRule("red_sandstone", "minecraft:speed", "always", 120, 0),
            new PassiveEffectRule("end_stone", "minecraft:slow_falling", "always", 140, 0),
            new PassiveEffectRule("tuff", "minecraft:haste", "always", 120, 0),
            new PassiveEffectRule("calcite", "minecraft:night_vision", "always", 160, 0),
            new PassiveEffectRule("paper", "minecraft:slow_falling", "dry", 120, 0),
            new PassiveEffectRule("paper", "minecraft:weakness", "wet", 120, 0),
            new PassiveEffectRule("paper", "minecraft:slowness", "wet", 120, 0),
            new PassiveEffectRule("obsidian", "minecraft:fire_resistance", "always", 220, 0),
            new PassiveEffectRule("obsidian", "minecraft:resistance", "always", 120, 0),
            new PassiveEffectRule("obsidian", "minecraft:slowness", "always", 120, 0)
        );
        Map<String, Integer> returns = new LinkedHashMap<>();
        returns.put("helmet", 2);
        returns.put("chestplate", 3);
        returns.put("leggings", 3);
        returns.put("boots", 2);
        List<BrittleRule> brittle = List.of(
            new BrittleRule("glass", 6.0f, 0.25f),
            new BrittleRule("calcite", 5.0f, 0.20f),
            new BrittleRule("quartz", 7.0f, 0.10f),
            new BrittleRule("amethyst", 8.0f, 0.08f)
        );
        return new DreamEquipmentSetEffectRules(true, passive, new CactusRule(true, 0.5f), new SlimeRule(true, 1, 0.10f, 12.0f, 0.45f, 14.0f, 0.50f, returns), brittle, List.of(new WetDurabilityRule("paper", 100, 1)), new RedstoneSignalRule(true, 7, 15, 8, 12), List.of(new WetRepairRule("mossy_cobblestone", 60, 1)), List.of(new BrittleWeaponRule("obsidian", 0.05f)), List.of(), List.of(new DamageImmunityRule("amethyst", "minecraft:sonic_boom")), new ArmadilloBootsRule(true, List.of("minecraft:sand", "minecraft:red_sand", "minecraft:gravel"), "minecraft:speed", 80, 2), List.of(new HeldEffectRule("dream_equipment:prismarine_pickaxe", "in_water", "minecraft:haste", 120, 1)));
    }

    private static JsonObject object(JsonObject root, String key) {
        return root != null && root.has(key) && root.get(key).isJsonObject() ? root.getAsJsonObject(key) : new JsonObject();
    }

    private static JsonArray array(JsonObject root, String key) {
        return root != null && root.has(key) && root.get(key).isJsonArray() ? root.getAsJsonArray(key) : new JsonArray();
    }

    private static boolean bool(JsonObject obj, String key, boolean fallback) {
        return obj != null && obj.has(key) ? obj.get(key).getAsBoolean() : fallback;
    }

    private static String str(JsonObject obj, String key, String fallback) {
        return obj != null && obj.has(key) ? obj.get(key).getAsString() : fallback;
    }

    private static int integer(JsonObject obj, String key, int fallback) {
        return obj != null && obj.has(key) ? obj.get(key).getAsInt() : fallback;
    }

    private static float flt(JsonObject obj, String key, float fallback) {
        return obj != null && obj.has(key) ? obj.get(key).getAsFloat() : fallback;
    }

    private static Map<String, Integer> intMap(JsonObject obj) {
        if (obj == null) return Collections.emptyMap();
        Map<String, Integer> out = new LinkedHashMap<>();
        for (var entry : obj.entrySet()) {
            out.put(entry.getKey(), entry.getValue().getAsInt());
        }
        return out;
    }

    public record PassiveEffectRule(String material, String effect, String condition, int durationTicks, int amplifier) {
        public Holder<MobEffect> effectHolder() {
            return BuiltInRegistries.MOB_EFFECT.get(Identifier.parse(effect)).orElse(null);
        }
    }

    public record CactusRule(boolean enabled, float damagePerPiece) {}
    public record SlimeRule(boolean enabled, int durabilityDamagePerTick, float damageCancelChance, float bootsSafeFallDistance,
                            float bounceMinVelocity, float bounceDistanceDivisor, float fallHealRatio, Map<String, Integer> returnSlimeBalls) {
        public int returnCount(String piece) {
            return returnSlimeBalls.getOrDefault(piece, 1);
        }
    }
    public record BrittleRule(String material, float damageThreshold, float shatterChance) {}
    public record WetDurabilityRule(String material, int intervalTicks, int damage) {}
    public record RedstoneSignalRule(boolean enabled, int bootsSignal, int fullSetSignal, int bootsPulseTicks, int fullSetPulseTicks) {}
    public record WetRepairRule(String material, int intervalTicks, int repair) {}
    public record BrittleWeaponRule(String material, float breakChance) {}
    public record StoneArmorPhysicsRule(String material, float cancelChancePerPiece, float shatterDamageThreshold, float slownessPerPiece) {}
    public record DamageImmunityRule(String material, String damageType) {
        public ResourceKey<DamageType> damageTypeKey() { return ResourceKey.create(Registries.DAMAGE_TYPE, Identifier.parse(damageType)); }
    }
    public record ArmadilloBootsRule(boolean enabled, List<String> blocks, String effect, int durationTicks, int amplifier) {
        public Holder<MobEffect> effectHolder() { return BuiltInRegistries.MOB_EFFECT.get(Identifier.parse(effect)).orElse(null); }
    }
    public record HeldEffectRule(String item, String condition, String effect, int durationTicks, int amplifier) {
        public Holder<MobEffect> effectHolder() { return BuiltInRegistries.MOB_EFFECT.get(Identifier.parse(effect)).orElse(null); }
    }
}
