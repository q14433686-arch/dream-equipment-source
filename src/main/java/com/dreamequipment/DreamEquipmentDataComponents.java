package com.dreamequipment;

import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;

public final class DreamEquipmentDataComponents {
    public static final DataComponentType<Identifier> SHIELD_BASE_TEXTURE = Registry.register(
        BuiltInRegistries.DATA_COMPONENT_TYPE,
        Identifier.fromNamespaceAndPath(DreamEquipment.MOD_ID, "shield_base_texture"),
        DataComponentType.<Identifier>builder()
            .persistent(Identifier.CODEC)
            .networkSynchronized(Identifier.STREAM_CODEC)
            .build()
    );

    private DreamEquipmentDataComponents() {}

    public static void register() {
        // Class loading registers static component types.
    }
}
