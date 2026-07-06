package com.dreamequipment;

import net.fabricmc.api.ModInitializer;

public final class DreamEquipment implements ModInitializer {
    public static final String MOD_ID = "dream_equipment";

    @Override
    public void onInitialize() {
        DreamEquipmentDataComponents.register();
        DreamEquipmentFamilyRules.load();
        DreamEquipmentSetEffectRules.load();
        DreamEquipmentShieldEffectRules.load();
        DreamEquipmentItems.register();
        DreamEquipmentFuelValues.register();
        DreamEquipmentRedstonePower.register();
        DreamEquipmentSetEffects.register();
        DreamEquipmentShieldEffects.register();
    }
}
