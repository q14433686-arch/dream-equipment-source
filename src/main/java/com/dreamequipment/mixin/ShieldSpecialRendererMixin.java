package com.dreamequipment.mixin;

import com.dreamequipment.DreamEquipmentDataComponents;
import net.minecraft.client.renderer.Sheets;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.special.ShieldSpecialRenderer;
import net.minecraft.client.resources.model.sprite.SpriteId;
import net.minecraft.core.component.DataComponentMap;
import net.minecraft.resources.Identifier;
import com.mojang.blaze3d.vertex.PoseStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyVariable;

@Mixin(ShieldSpecialRenderer.class)
public abstract class ShieldSpecialRendererMixin {
    @ModifyVariable(
        method = "submit(Lnet/minecraft/core/component/DataComponentMap;Lcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/SubmitNodeCollector;IIZI)V",
        at = @At(value = "STORE"),
        ordinal = 0
    )
    private SpriteId dream_equipment$useCustomShieldBase(SpriteId original, DataComponentMap components, PoseStack poseStack, SubmitNodeCollector collector, int light, int overlay, boolean glint, int something) {
        Identifier texture = components == null ? null : components.get(DreamEquipmentDataComponents.SHIELD_BASE_TEXTURE);
        return texture == null ? original : new SpriteId(Sheets.SHIELD_SHEET, texture);
    }
}
