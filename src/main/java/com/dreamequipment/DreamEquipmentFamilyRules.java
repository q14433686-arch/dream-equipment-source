package com.dreamequipment;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonElement;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public final class DreamEquipmentFamilyRules {
    private static final Gson GSON = new Gson();
    private static DreamEquipmentFamilyRules CURRENT = new DreamEquipmentFamilyRules(List.of());

    public final List<Family> families;

    private DreamEquipmentFamilyRules(List<Family> families) {
        this.families = List.copyOf(families);
    }

    public static DreamEquipmentFamilyRules current() {
        return CURRENT;
    }

    public static void load() {
        try (var stream = DreamEquipmentFamilyRules.class.getClassLoader().getResourceAsStream("data/dream_equipment/equipment_families.json")) {
            if (stream == null) {
                CURRENT = new DreamEquipmentFamilyRules(List.of());
                return;
            }
            try (var reader = new InputStreamReader(stream, StandardCharsets.UTF_8)) {
                CURRENT = parse(GSON.fromJson(reader, JsonObject.class));
            }
        } catch (Exception ex) {
            CURRENT = new DreamEquipmentFamilyRules(List.of());
            System.err.println("[Dream Equipment] Failed to load equipment_families.json: " + ex.getMessage());
        }
    }

    private static DreamEquipmentFamilyRules parse(JsonObject root) {
        List<Family> families = new ArrayList<>();
        JsonArray array = root.getAsJsonArray("families");
        for (JsonElement element : array) {
            JsonObject obj = element.getAsJsonObject();
            Armor armor = obj.has("armor") ? parseArmor(obj.getAsJsonObject("armor")) : null;
            Tools tools = obj.has("tools") ? parseTools(obj.getAsJsonObject("tools")) : null;
            Shield shield = obj.has("shield") ? parseShield(obj.getAsJsonObject("shield")) : null;
            families.add(new Family(
                str(obj, "id", ""),
                str(obj, "ingredient", "minecraft:air"),
                str(obj, "zh_name", ""),
                str(obj, "en_name", ""),
                armor,
                tools,
                shield,
                integer(obj, "fuel_burn_time_per_material", 0)
            ));
        }
        return new DreamEquipmentFamilyRules(families);
    }

    private static Armor parseArmor(JsonObject obj) {
        List<String> pieces = new ArrayList<>();
        for (JsonElement e : obj.getAsJsonArray("pieces")) pieces.add(e.getAsString());
        JsonObject defense = obj.getAsJsonObject("defense");
        return new Armor(
            pieces,
            integer(obj, "durability_multiplier", 7),
            integer(obj, "enchantment_value", 10),
            str(obj, "equip_sound", "iron"),
            flt(obj, "toughness", 0.0f),
            flt(obj, "knockback_resistance", 0.0f),
            integer(defense, "helmet", 0),
            integer(defense, "chestplate", 0),
            integer(defense, "leggings", 0),
            integer(defense, "boots", 0)
        );
    }

    private static Shield parseShield(JsonObject obj) {
        return new Shield(
            bool(obj, "enabled", true),
            integer(obj, "durability", 336)
        );
    }

    private static Tools parseTools(JsonObject obj) {
        List<String> types = new ArrayList<>();
        for (JsonElement e : obj.getAsJsonArray("types")) types.add(e.getAsString());
        return new Tools(
            types,
            str(obj, "incorrect_blocks_for_drops", "minecraft:incorrect_for_wooden_tool"),
            integer(obj, "durability", 59),
            flt(obj, "speed", 2.0f),
            flt(obj, "attack_damage_bonus", 0.0f),
            integer(obj, "enchantment_value", 10)
        );
    }

    private static String str(JsonObject obj, String key, String fallback) { return obj != null && obj.has(key) ? obj.get(key).getAsString() : fallback; }
    private static int integer(JsonObject obj, String key, int fallback) { return obj != null && obj.has(key) ? obj.get(key).getAsInt() : fallback; }
    private static float flt(JsonObject obj, String key, float fallback) { return obj != null && obj.has(key) ? obj.get(key).getAsFloat() : fallback; }
    private static boolean bool(JsonObject obj, String key, boolean fallback) { return obj != null && obj.has(key) ? obj.get(key).getAsBoolean() : fallback; }

    public record Family(String id, String ingredient, String zhName, String enName, Armor armor, Tools tools, Shield shield, int fuelBurnTimePerMaterial) {}
    public record Armor(List<String> pieces, int durabilityMultiplier, int enchantmentValue, String equipSound, float toughness, float knockbackResistance,
                        int helmetDefense, int chestplateDefense, int leggingsDefense, int bootsDefense) {}
    public record Tools(List<String> types, String incorrectBlocksForDrops, int durability, float speed, float attackDamageBonus, int enchantmentValue) {}
    public record Shield(boolean enabled, int durability) {}
}
