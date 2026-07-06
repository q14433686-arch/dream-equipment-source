package com.dreamequipment;

import net.fabricmc.fabric.api.registry.FuelValueEvents;
import net.minecraft.world.item.Item;

public final class DreamEquipmentFuelValues {
    private DreamEquipmentFuelValues() {}

    public static void register() {
        FuelValueEvents.BUILD.register((builder, context) -> {
            for (DreamEquipmentFamilyRules.Family family : DreamEquipmentFamilyRules.current().families) {
                int perMaterial = family.fuelBurnTimePerMaterial();
                if (perMaterial <= 0 || family.armor() == null) {
                    continue;
                }
                for (String piece : family.armor().pieces()) {
                    Item item = DreamEquipmentItems.item(family.id() + "_" + piece);
                    if (item != null) {
                        builder.add(item, perMaterial * armorMaterialCount(piece));
                    }
                }
                if (family.shield() != null && family.shield().enabled()) {
                    Item shield = DreamEquipmentItems.item(family.id() + "_shield");
                    if (shield != null) {
                        builder.add(shield, perMaterial * 6);
                    }
                }
            }
        });
    }

    private static int armorMaterialCount(String piece) {
        return switch (piece) {
            case "helmet" -> 5;
            case "chestplate" -> 8;
            case "leggings" -> 7;
            case "boots" -> 4;
            default -> 0;
        };
    }
}
