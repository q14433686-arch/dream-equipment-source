package com.dreamequipment;

import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.minecraft.core.Holder;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.AxeItem;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.HoeItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ShovelItem;
import net.minecraft.world.level.block.entity.BannerPatternLayers;
import net.minecraft.world.item.component.BlocksAttacks;
import net.minecraft.world.item.ShieldItem;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.ToolMaterial;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;
import net.minecraft.world.item.equipment.EquipmentAssets;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Optional;
import java.util.Map;
import java.util.ArrayList;
import java.util.function.Function;

public final class DreamEquipmentItems {
    private static final Map<String, Item> ITEMS_MUTABLE = new LinkedHashMap<>();
    private static final List<Item> TOOL_ITEMS_MUTABLE = new ArrayList<>();
    private static boolean registered = false;

    public static Map<String, Item> ITEMS = Collections.emptyMap();
    public static List<Item> ALL_ITEMS = List.of();
    public static List<Item> TOOL_ITEMS = List.of();

    private DreamEquipmentItems() {}

    public static void register() {
        if (!registered) {
            for (DreamEquipmentFamilyRules.Family family : DreamEquipmentFamilyRules.current().families) {
                registerFamily(family);
            }
            ITEMS = Collections.unmodifiableMap(ITEMS_MUTABLE);
            ALL_ITEMS = List.copyOf(ITEMS_MUTABLE.values());
            TOOL_ITEMS = List.copyOf(TOOL_ITEMS_MUTABLE);
            registered = true;
        }
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.COMBAT).register(entries -> ALL_ITEMS.forEach(entries::accept));
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.TOOLS_AND_UTILITIES).register(entries -> TOOL_ITEMS.forEach(entries::accept));
    }

    public static Item item(String path) {
        return ITEMS.get(path);
    }

    private static void registerFamily(DreamEquipmentFamilyRules.Family family) {
        if (family.tools() != null) {
            registerTools(family.id(), family.tools());
        }
        if (family.armor() != null) {
            ArmorMaterial material = armorMaterial(family.id(), family.armor());
            for (String piece : family.armor().pieces()) {
                registerArmor(family.id() + "_" + piece, material, armorType(piece));
            }
        }
        if (family.shield() != null && family.shield().enabled()) {
            registerShield(family.id() + "_shield", family.id(), family.shield());
        }
    }

    private static void registerTools(String material, DreamEquipmentFamilyRules.Tools rules) {
        ToolMaterial toolMaterial = new ToolMaterial(
            blockTag(rules.incorrectBlocksForDrops()),
            rules.durability(),
            rules.speed(),
            rules.attackDamageBonus(),
            rules.enchantmentValue(),
            repairTag(material)
        );
        for (String type : rules.types()) {
            String name = material + "_" + type;
            switch (type) {
                case "sword" -> registerTool(name, new Item.Properties().sword(toolMaterial, 3.0f, -2.4f));
                case "pickaxe" -> registerTool(name, new Item.Properties().pickaxe(toolMaterial, 1.0f, -2.8f));
                case "axe" -> registerTool(name, settings -> new AxeItem(toolMaterial, 5.0f, -3.0f, settings));
                case "shovel" -> registerTool(name, settings -> new ShovelItem(toolMaterial, 1.5f, -3.0f, settings));
                case "hoe" -> registerTool(name, settings -> new HoeItem(toolMaterial, -3.0f, 0.0f, settings));
                case "spear" -> registerTool(name, new Item.Properties().spear(toolMaterial, 1.05f, 1.075f, 0.5f, 3.0f, 10.0f, 6.5f, 5.1f, 10.0f, 4.6f));
                default -> throw new IllegalArgumentException("Unknown tool type: " + type);
            }
        }
    }

    private static Item registerTool(String name, Item.Properties properties) {
        Item item = register(name, properties);
        TOOL_ITEMS_MUTABLE.add(item);
        return item;
    }

    private static Item registerTool(String name, Function<Item.Properties, Item> factory) {
        Identifier id = Identifier.fromNamespaceAndPath(DreamEquipment.MOD_ID, name);
        ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, id);
        Item item = factory.apply(new Item.Properties().setId(key));
        Registry.register(BuiltInRegistries.ITEM, key, item);
        ITEMS_MUTABLE.put(name, item);
        TOOL_ITEMS_MUTABLE.add(item);
        return item;
    }

    private static Item registerShield(String name, String material, DreamEquipmentFamilyRules.Shield rules) {
        Identifier id = Identifier.fromNamespaceAndPath(DreamEquipment.MOD_ID, name);
        ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, id);
        Item.Properties properties = new Item.Properties()
            .setId(key)
            .durability(rules.durability());
        if (material.equals("netherite")) {
            properties.fireResistant();
        }
        properties
            .component(DataComponents.BANNER_PATTERNS, BannerPatternLayers.EMPTY)
            .component(DreamEquipmentDataComponents.SHIELD_BASE_TEXTURE, Identifier.fromNamespaceAndPath("minecraft", "entity/shield/dream_equipment/" + name + "_base_nopattern"))
            .repairable(repairTag(material))
            .equippableUnswappable(EquipmentSlot.OFFHAND)
            .delayedComponent(DataComponents.BLOCKS_ATTACKS, DreamEquipmentItems::vanillaShieldBlocksAttacks)
            .component(DataComponents.BREAK_SOUND, SoundEvents.SHIELD_BREAK);
        Item item = new ShieldItem(properties);
        Registry.register(BuiltInRegistries.ITEM, key, item);
        ITEMS_MUTABLE.put(name, item);
        return item;
    }

    private static BlocksAttacks vanillaShieldBlocksAttacks(net.minecraft.core.HolderLookup.Provider registries) {
        return new BlocksAttacks(
            0.25f,
            1.0f,
            List.of(new BlocksAttacks.DamageReduction(90.0f, Optional.empty(), 0.0f, 1.0f)),
            new BlocksAttacks.ItemDamageFunction(3.0f, 1.0f, 1.0f),
            Optional.of(registries.getOrThrow(DamageTypeTags.BYPASSES_SHIELD)),
            Optional.of(SoundEvents.SHIELD_BLOCK),
            Optional.of(SoundEvents.SHIELD_BREAK)
        );
    }

    private static Item registerArmor(String name, ArmorMaterial material, ArmorType type) {
        return register(name, new Item.Properties().humanoidArmor(material, type));
    }

    private static Item register(String name, Item.Properties properties) {
        Identifier id = Identifier.fromNamespaceAndPath(DreamEquipment.MOD_ID, name);
        ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, id);
        Item item = new Item(properties.setId(key));
        Registry.register(BuiltInRegistries.ITEM, key, item);
        ITEMS_MUTABLE.put(name, item);
        return item;
    }

    private static ArmorMaterial armorMaterial(String material, DreamEquipmentFamilyRules.Armor rules) {
        ResourceKey<net.minecraft.world.item.equipment.EquipmentAsset> asset = ResourceKey.create(
            EquipmentAssets.ROOT_ID,
            Identifier.fromNamespaceAndPath(DreamEquipment.MOD_ID, material)
        );
        Map<ArmorType, Integer> defense = new LinkedHashMap<>();
        defense.put(ArmorType.HELMET, rules.helmetDefense());
        defense.put(ArmorType.CHESTPLATE, rules.chestplateDefense());
        defense.put(ArmorType.LEGGINGS, rules.leggingsDefense());
        defense.put(ArmorType.BOOTS, rules.bootsDefense());
        return new ArmorMaterial(rules.durabilityMultiplier(), defense, rules.enchantmentValue(), equipSound(rules.equipSound()), rules.toughness(), rules.knockbackResistance(), repairTag(material), asset);
    }

    private static ArmorType armorType(String piece) {
        return switch (piece) {
            case "helmet" -> ArmorType.HELMET;
            case "chestplate" -> ArmorType.CHESTPLATE;
            case "leggings" -> ArmorType.LEGGINGS;
            case "boots" -> ArmorType.BOOTS;
            default -> throw new IllegalArgumentException("Unknown armor piece: " + piece);
        };
    }

    private static Holder<SoundEvent> equipSound(String sound) {
        return switch (sound) {
            case "chain" -> SoundEvents.ARMOR_EQUIP_CHAIN;
            case "diamond" -> SoundEvents.ARMOR_EQUIP_DIAMOND;
            case "gold" -> SoundEvents.ARMOR_EQUIP_GOLD;
            case "leather" -> SoundEvents.ARMOR_EQUIP_LEATHER;
            case "netherite" -> SoundEvents.ARMOR_EQUIP_NETHERITE;
            case "wolf" -> SoundEvents.ARMOR_EQUIP_WOLF;
            case "turtle" -> SoundEvents.ARMOR_EQUIP_TURTLE;
            case "copper" -> SoundEvents.ARMOR_EQUIP_COPPER;
            default -> SoundEvents.ARMOR_EQUIP_IRON;
        };
    }

    private static TagKey<Item> repairTag(String material) {
        return itemTag("repairs_" + material + (material.equals("emerald") ? "_equipment" : "_armor"));
    }

    private static TagKey<Item> itemTag(String path) {
        return TagKey.create(Registries.ITEM, Identifier.fromNamespaceAndPath(DreamEquipment.MOD_ID, path));
    }

    private static TagKey<net.minecraft.world.level.block.Block> blockTag(String id) {
        return TagKey.create(Registries.BLOCK, Identifier.parse(id));
    }
}
