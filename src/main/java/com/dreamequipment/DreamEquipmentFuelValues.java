package com.dreamequipment;

import net.fabricmc.fabric.api.item.v1.DefaultItemComponentEvents;
import net.minecraft.core.component.DataComponents;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.component.CookingFuel;
import net.minecraft.world.level.storage.loot.providers.number.floats.ContextFloatProviders;
import net.minecraft.world.level.storage.loot.providers.number.floats.ResolvableFloat;
import net.minecraft.world.level.storage.loot.providers.number.ints.ResolvableInt;

public final class DreamEquipmentFuelValues {
    private DreamEquipmentFuelValues() {}

    public static void register() {
        DefaultItemComponentEvents.MODIFY.register(context -> {
            for (DreamEquipmentFamilyRules.Family family : DreamEquipmentFamilyRules.current().families) {
                int perMaterial = family.fuelBurnTimePerMaterial();
                if (perMaterial <= 0 || family.armor() == null) {
                    continue;
                }
                for (String piece : family.armor().pieces()) {
                    Item item = DreamEquipmentItems.item(family.id() + "_" + piece);
                    if (item != null) {
                        registerCookingFuel(context, item, perMaterial * armorMaterialCount(piece));
                    }
                }
                if (family.shield() != null && family.shield().enabled()) {
                    Item shield = DreamEquipmentItems.item(family.id() + "_shield");
                    if (shield != null) {
                        registerCookingFuel(context, shield, perMaterial * 6);
                    }
                }
            }
        });
    }

    private static void registerCookingFuel(DefaultItemComponentEvents.ModifyContext context, Item item, int burnTime) {
        if (burnTime <= 0) return;
        CookingFuel fuel = new CookingFuel(
                new ResolvableInt.Constant(burnTime),
                ResolvableFloat.fromKey(ContextFloatProviders.COOKING_DEFAULT_SPEED_MULTIPLIER)
        );
        context.modify(item, builder -> builder.set(DataComponents.COOKING_FUEL, fuel));
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
