package com.dreamequipment.mixin;

import com.dreamequipment.DreamEquipmentEnchantingSupport;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.EnchantmentMenu;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(EnchantmentMenu.class)
public abstract class EnchantmentMenuMixin {
    @Inject(method = "clickMenuButton", at = @At("RETURN"))
    private void dream_equipment$refundLapis(Player player, int buttonId, CallbackInfoReturnable<Boolean> cir) {
        if (!cir.getReturnValue() || !(player instanceof ServerPlayer serverPlayer)) return;
        if (buttonId < 0 || buttonId > 2 || player.hasInfiniteMaterials()) return;
        int vanillaCost = buttonId + 1;
        ItemStack lapisSlot = ((EnchantmentMenuAccessor) this).dream_equipment$enchantSlots().getItem(1);
        // If vanilla consumed lapis successfully, refund nearly all of the lapis cost through lapis armor durability.
        // This is intentionally post-transaction so the vanilla enchanting flow remains stable.
        if (lapisSlot.isEmpty() || lapisSlot.is(Items.LAPIS_LAZULI)) {
            DreamEquipmentEnchantingSupport.refundLapisAndDamageArmor(serverPlayer, vanillaCost);
        }
    }
}
