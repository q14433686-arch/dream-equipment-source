package com.dreamequipment;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

public final class DreamEquipmentEnchantingSupport {
    private DreamEquipmentEnchantingSupport() {}

    public static void refundLapisAndDamageArmor(ServerPlayer player, int consumedLapis) {
        if (consumedLapis <= 0 || !hasLapisArmor(player)) return;
        ItemStack refund = new ItemStack(Items.LAPIS_LAZULI, consumedLapis);
        if (!player.addItem(refund)) player.drop(refund, false);
        damageLapisArmor(player, consumedLapis * 12);
    }

    private static boolean hasLapisArmor(ServerPlayer player) {
        for (EquipmentSlot slot : armorSlots()) {
            if (isLapisArmor(player.getItemBySlot(slot))) return true;
        }
        return false;
    }

    private static void damageLapisArmor(ServerPlayer player, int totalDamage) {
        if (!(player.level() instanceof ServerLevel level)) return;
        int remaining = totalDamage;
        for (EquipmentSlot slot : armorSlots()) {
            ItemStack stack = player.getItemBySlot(slot);
            if (!isLapisArmor(stack)) continue;
            int damage = Math.max(1, remaining / Math.max(1, lapisPieceCount(player)));
            stack.hurtAndBreak(damage, level, player, item -> player.onEquippedItemBroken(item, slot));
            remaining -= damage;
            if (remaining <= 0) return;
        }
    }

    private static int lapisPieceCount(ServerPlayer player) {
        int count = 0;
        for (EquipmentSlot slot : armorSlots()) if (isLapisArmor(player.getItemBySlot(slot))) count++;
        return count;
    }

    private static boolean isLapisArmor(ItemStack stack) {
        if (stack.isEmpty()) return false;
        net.minecraft.resources.Identifier id = net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(stack.getItem());
        return id != null && DreamEquipment.MOD_ID.equals(id.getNamespace()) && id.getPath().startsWith("lapis_")
            && (id.getPath().endsWith("_helmet") || id.getPath().endsWith("_chestplate") || id.getPath().endsWith("_leggings") || id.getPath().endsWith("_boots"));
    }

    private static EquipmentSlot[] armorSlots() {
        return new EquipmentSlot[]{EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET};
    }
}
