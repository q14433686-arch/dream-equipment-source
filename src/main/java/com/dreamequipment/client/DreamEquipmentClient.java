package com.dreamequipment.client;

import com.dreamequipment.DreamEquipmentFamilyRules;
import com.dreamequipment.DreamEquipmentSetEffectRules;
import net.fabricmc.api.ClientModInitializer;

public final class DreamEquipmentClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        // Ensure client-only tooltips can read the same startup JSON tables.
        DreamEquipmentFamilyRules.load();
        DreamEquipmentSetEffectRules.load();
        DreamEquipmentTooltips.register();
    }
}
