package com.dreamequipment;

import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;


public final class DreamEquipmentSetEffects {
    private static boolean thornGuard = false;

    private DreamEquipmentSetEffects() {}

    public static void register() {
        ServerTickEvents.END_SERVER_TICK.register(server -> {
            for (ServerPlayer player : server.getPlayerList().getPlayers()) {
                tickPlayer(player);
            }
        });
        ServerLivingEntityEvents.ALLOW_DAMAGE.register(DreamEquipmentSetEffects::allowDamage);
        ServerLivingEntityEvents.AFTER_DAMAGE.register(DreamEquipmentSetEffects::afterDamage);
    }

    private static void tickPlayer(ServerPlayer player) {
        DreamEquipmentSetEffectRules rules = DreamEquipmentSetEffectRules.current();
        if (!rules.enabled || player.isCreative() || player.isSpectator()) return;

        for (DreamEquipmentSetEffectRules.PassiveEffectRule rule : rules.passiveEffects) {
            if (fullSet(player, rule.material()) && conditionMatches(player, rule.condition())) {
                Holder<MobEffect> effect = rule.effectHolder();
                if (effect != null) add(player, effect, rule.durationTicks(), rule.amplifier());
            }
        }

        if (rules.slime.enabled() && fullSet(player, "slime")) {
            damageSlimeArmor(player, rules.slime);
        }
        for (DreamEquipmentSetEffectRules.WetDurabilityRule rule : rules.wetDurabilityRules) {
            if (fullSet(player, rule.material()) && player.isInWaterOrRain() && rule.intervalTicks() > 0 && player.tickCount % rule.intervalTicks() == 0) {
                damageOneEquipped(player, rule.material(), rule.damage());
            }
        }
        for (DreamEquipmentSetEffectRules.WetRepairRule rule : rules.wetRepairRules) {
            if (fullSet(player, rule.material()) && player.isInWaterOrRain() && rule.intervalTicks() > 0 && player.tickCount % rule.intervalTicks() == 0) {
                repairEquipped(player, rule.material(), rule.repair());
            }
        }
        applyArmadilloBoots(player, rules.armadilloBoots);
        applyHeldEffects(player, rules);
        for (DreamEquipmentSetEffectRules.StoneArmorPhysicsRule rule : rules.stoneArmorPhysicsRules) {
            int pieces = armorPieceCount(player, rule.material());
            if (pieces > 0 && rule.slownessPerPiece() > 0.0f) {
                int amplifier = Math.max(0, (int)Math.ceil(pieces * rule.slownessPerPiece()) - 1);
                add(player, net.minecraft.world.effect.MobEffects.SLOWNESS, 80, amplifier);
            }
        }
    }


    private static void applyArmadilloBoots(ServerPlayer player, DreamEquipmentSetEffectRules.ArmadilloBootsRule rule) {
        if (!rule.enabled() || !wearing(player, EquipmentSlot.FEET, "armadillo_shell_boots")) return;
        if (!isStandingOnAny(player, rule.blocks())) return;
        Holder<MobEffect> effect = rule.effectHolder();
        if (effect != null) add(player, effect, rule.durationTicks(), rule.amplifier());
    }

    private static void applyHeldEffects(ServerPlayer player, DreamEquipmentSetEffectRules rules) {
        for (DreamEquipmentSetEffectRules.HeldEffectRule rule : rules.heldEffects) {
            if (!conditionMatches(player, rule.condition())) continue;
            if (!held(player, rule.item())) continue;
            Holder<MobEffect> effect = rule.effectHolder();
            if (effect != null) add(player, effect, rule.durationTicks(), rule.amplifier());
        }
    }

    private static boolean held(ServerPlayer player, String itemId) {
        Identifier id = Identifier.parse(itemId);
        return BuiltInRegistries.ITEM.getKey(player.getMainHandItem().getItem()).equals(id)
            || BuiltInRegistries.ITEM.getKey(player.getOffhandItem().getItem()).equals(id);
    }

    private static boolean isStandingOnAny(ServerPlayer player, java.util.List<String> blocks) {
        net.minecraft.world.level.block.state.BlockState state = player.level().getBlockState(player.blockPosition().below());
        for (String block : blocks) {
            net.minecraft.world.level.block.Block value = BuiltInRegistries.BLOCK.getValue(Identifier.parse(block));
            if (value != null && state.is(value)) return true;
        }
        return false;
    }

    private static boolean allowDamage(LivingEntity entity, DamageSource source, float amount) {
        DreamEquipmentSetEffectRules rules = DreamEquipmentSetEffectRules.current();
        if (!rules.enabled || amount <= 0.0f || !(entity instanceof ServerPlayer player)) return true;
        if (player.isCreative() || player.isSpectator()) return true;
        for (DreamEquipmentSetEffectRules.DamageImmunityRule rule : rules.damageImmunities) {
            if (fullSet(player, rule.material()) && source.is(rule.damageTypeKey())) return false;
        }
        if (rules.slime.enabled() && wearing(player, EquipmentSlot.FEET, "slime_boots") && source.is(DamageTypeTags.IS_FALL) && player.fallDistance <= rules.slime.bootsSafeFallDistance()) {
            bounceLikeSlime(player, rules.slime);
            return false;
        }
        if (rules.slime.enabled() && fullSet(player, "slime") && player.getRandom().nextFloat() < rules.slime.damageCancelChance()) {
            return false;
        }
        for (DreamEquipmentSetEffectRules.StoneArmorPhysicsRule rule : rules.stoneArmorPhysicsRules) {
            int pieces = armorPieceCount(player, rule.material());
            if (pieces > 0 && player.getRandom().nextFloat() < Math.min(0.50f, pieces * rule.cancelChancePerPiece())) {
                return false;
            }
        }
        return true;
    }

    private static void afterDamage(LivingEntity entity, DamageSource source, float baseDamageTaken, float damageTaken, boolean blocked) {
        DreamEquipmentSetEffectRules rules = DreamEquipmentSetEffectRules.current();
        if (!rules.enabled || blocked || damageTaken <= 0.0f || !(entity instanceof ServerPlayer player)) return;
        if (player.isCreative() || player.isSpectator()) return;

        int cactusPieces = armorPieceCount(player, "cactus");
        if (rules.cactus.enabled() && cactusPieces > 0) cactusRetaliate(player, source, cactusPieces * rules.cactus.damagePerPiece());

        if (wearing(player, EquipmentSlot.FEET, "armadillo_shell_boots") && source.is(DamageTypeTags.IS_FALL)) {
            player.heal(Math.max(0.0f, damageTaken * 0.35f));
        }
        for (DreamEquipmentSetEffectRules.BrittleRule rule : rules.brittleRules) {
            if (hasStonePhysicsRule(rules, rule.material())) continue;
            if (fullSet(player, rule.material()) && damageTaken >= rule.damageThreshold() && player.getRandom().nextFloat() < rule.shatterChance()) {
                shatterOneArmorPiece(player, rule.material(), true);
            }
        }
        for (DreamEquipmentSetEffectRules.StoneArmorPhysicsRule rule : rules.stoneArmorPhysicsRules) {
            if (armorPieceCount(player, rule.material()) > 0 && damageTaken >= rule.shatterDamageThreshold()) {
                shatterOneArmorPiece(player, rule.material(), true);
            }
        }
        maybeBreakBrittleWeapon(source, rules);
        if (rules.slime.enabled() && fullSet(player, "slime") && source.is(DamageTypeTags.IS_FALL)) {
            player.heal(Math.max(0.0f, damageTaken * rules.slime.fallHealRatio()));
        }
    }

    private static boolean hasStonePhysicsRule(DreamEquipmentSetEffectRules rules, String material) {
        for (DreamEquipmentSetEffectRules.StoneArmorPhysicsRule rule : rules.stoneArmorPhysicsRules) {
            if (rule.material().equals(material)) return true;
        }
        return false;
    }

    private static boolean conditionMatches(ServerPlayer player, String condition) {
        return switch (condition) {
            case "always" -> true;
            case "in_water" -> player.isInWater();
            case "wet" -> player.isInWaterOrRain();
            case "dry" -> !player.isInWaterOrRain();
            default -> true;
        };
    }

    private static void cactusRetaliate(ServerPlayer wearer, DamageSource source, float amount) {
        if (thornGuard || amount <= 0.0f) return;
        Entity attacker = source.getEntity();
        if (!(attacker instanceof LivingEntity living) || attacker == wearer || !attacker.level().equals(wearer.level())) return;
        thornGuard = true;
        try {
            living.hurtServer((ServerLevel) wearer.level(), wearer.damageSources().thorns(wearer), amount);
        } finally {
            thornGuard = false;
        }
    }

    private static void shatterOneArmorPiece(ServerPlayer player, String material, boolean returnIngredient) {
        EquipmentSlot[] slots = {EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET};
        EquipmentSlot slot = slots[player.getRandom().nextInt(slots.length)];
        ItemStack stack = player.getItemBySlot(slot);
        if (!stack.isEmpty() && path(stack.getItem()).startsWith(material + "_")) {
            player.setItemSlot(slot, ItemStack.EMPTY);
            if (returnIngredient) returnIngredient(player, material);
            player.playSound(SoundEvents.GLASS_BREAK, 1.0f, 1.1f);
        }
    }


    private static void maybeBreakBrittleWeapon(DamageSource source, DreamEquipmentSetEffectRules rules) {
        if (!(source.getEntity() instanceof ServerPlayer attacker)) return;
        for (DreamEquipmentSetEffectRules.BrittleWeaponRule rule : rules.brittleWeaponRules) {
            if (attacker.getRandom().nextFloat() >= rule.breakChance()) continue;
            if (breakHeldIfMaterial(attacker, EquipmentSlot.MAINHAND, rule.material())) return;
            if (breakHeldIfMaterial(attacker, EquipmentSlot.OFFHAND, rule.material())) return;
        }
    }

    private static boolean breakHeldIfMaterial(ServerPlayer player, EquipmentSlot slot, String material) {
        ItemStack stack = player.getItemBySlot(slot);
        if (!stack.isEmpty() && path(stack.getItem()).startsWith(material + "_")) {
            player.setItemSlot(slot, ItemStack.EMPTY);
            player.playSound(SoundEvents.GLASS_BREAK, 0.8f, 0.9f);
            return true;
        }
        return false;
    }

    private static void returnIngredient(ServerPlayer player, String material) {
        for (DreamEquipmentFamilyRules.Family family : DreamEquipmentFamilyRules.current().families) {
            if (!family.id().equals(material) || family.ingredient().startsWith("#")) continue;
            Item item = BuiltInRegistries.ITEM.getValue(Identifier.parse(family.ingredient()));
            if (item == null || item == Items.AIR) return;
            ItemStack returned = new ItemStack(item, 1 + player.getRandom().nextInt(2));
            if (!player.addItem(returned)) player.drop(returned, false);
            return;
        }
    }

    private static void repairEquipped(ServerPlayer player, String material, int amount) {
        if (amount <= 0) return;
        for (EquipmentSlot slot : new EquipmentSlot[]{EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET}) {
            ItemStack stack = player.getItemBySlot(slot);
            if (!stack.isEmpty() && path(stack.getItem()).startsWith(material + "_") && stack.isDamaged()) {
                stack.setDamageValue(Math.max(0, stack.getDamageValue() - amount));
            }
        }
    }

    private static void bounceLikeSlime(ServerPlayer player, DreamEquipmentSetEffectRules.SlimeRule slime) {
        double bounce = Math.min(1.0, Math.max(slime.bounceMinVelocity(), player.fallDistance / Math.max(1.0f, slime.bounceDistanceDivisor())));
        player.setDeltaMovement(player.getDeltaMovement().x, bounce, player.getDeltaMovement().z);
        player.hurtMarked = true;
        player.resetFallDistance();
    }

    private static void damageSlimeArmor(ServerPlayer player, DreamEquipmentSetEffectRules.SlimeRule slime) {
        damageSlimeSlot(player, EquipmentSlot.HEAD, slime.durabilityDamagePerTick(), slime.returnCount("helmet"));
        damageSlimeSlot(player, EquipmentSlot.CHEST, slime.durabilityDamagePerTick(), slime.returnCount("chestplate"));
        damageSlimeSlot(player, EquipmentSlot.LEGS, slime.durabilityDamagePerTick(), slime.returnCount("leggings"));
        damageSlimeSlot(player, EquipmentSlot.FEET, slime.durabilityDamagePerTick(), slime.returnCount("boots"));
    }

    private static void damageSlimeSlot(ServerPlayer player, EquipmentSlot slot, int damage, int returnedSlimeBalls) {
        ItemStack stack = player.getItemBySlot(slot);
        if (damage <= 0 || stack.isEmpty() || !path(stack.getItem()).startsWith("slime_")) return;
        if (stack.nextDamageWillBreak() || stack.getDamageValue() + damage >= stack.getMaxDamage()) {
            player.setItemSlot(slot, ItemStack.EMPTY);
            ItemStack returned = new ItemStack(Items.SLIME_BALL, returnedSlimeBalls);
            if (!player.addItem(returned)) player.drop(returned, false);
        } else {
            stack.setDamageValue(stack.getDamageValue() + damage);
        }
    }

    private static void damageOneEquipped(ServerPlayer player, String material, int amount) {
        EquipmentSlot[] slots = {EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET};
        EquipmentSlot slot = slots[player.getRandom().nextInt(slots.length)];
        ItemStack stack = player.getItemBySlot(slot);
        if (!stack.isEmpty() && path(stack.getItem()).startsWith(material + "_")) {
            stack.hurtAndBreak(amount, player, slot);
        }
    }

    private static boolean fullSet(ServerPlayer player, String material) {
        if (material.equals("turtle_shell")) {
            return wearing(player, EquipmentSlot.HEAD, "turtle_helmet")
                && wearing(player, EquipmentSlot.CHEST, "turtle_shell_chestplate")
                && wearing(player, EquipmentSlot.LEGS, "turtle_shell_leggings")
                && wearing(player, EquipmentSlot.FEET, "turtle_shell_boots");
        }
        return wearing(player, EquipmentSlot.HEAD, material + "_helmet")
            && wearing(player, EquipmentSlot.CHEST, material + "_chestplate")
            && wearing(player, EquipmentSlot.LEGS, material + "_leggings")
            && wearing(player, EquipmentSlot.FEET, material + "_boots");
    }

    private static int armorPieceCount(ServerPlayer player, String material) {
        int count = 0;
        if (material.equals("turtle_shell")) {
            if (wearing(player, EquipmentSlot.HEAD, "turtle_helmet")) count++;
            if (wearing(player, EquipmentSlot.CHEST, "turtle_shell_chestplate")) count++;
            if (wearing(player, EquipmentSlot.LEGS, "turtle_shell_leggings")) count++;
            if (wearing(player, EquipmentSlot.FEET, "turtle_shell_boots")) count++;
            return count;
        }
        if (wearing(player, EquipmentSlot.HEAD, material + "_helmet")) count++;
        if (wearing(player, EquipmentSlot.CHEST, material + "_chestplate")) count++;
        if (wearing(player, EquipmentSlot.LEGS, material + "_leggings")) count++;
        if (wearing(player, EquipmentSlot.FEET, material + "_boots")) count++;
        return count;
    }

    private static boolean wearing(ServerPlayer player, EquipmentSlot slot, String itemPath) {
        return path(player.getItemBySlot(slot).getItem()).equals(itemPath);
    }

    private static String path(Item item) {
        Identifier id = BuiltInRegistries.ITEM.getKey(item);
        return id == null ? "" : id.getPath();
    }

    private static void add(ServerPlayer player, Holder<MobEffect> effect, int duration, int amplifier) {
        player.addEffect(new MobEffectInstance(effect, duration, amplifier, true, false, true));
    }
}
