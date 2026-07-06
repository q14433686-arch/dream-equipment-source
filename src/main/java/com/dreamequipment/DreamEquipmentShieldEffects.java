package com.dreamequipment;

import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageTypes;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.Vec3;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public final class DreamEquipmentShieldEffects {
    private static final Map<UUID, Integer> LAST_CACTUS_RETALIATE_TICK = new HashMap<>();

    private DreamEquipmentShieldEffects() {}

    public static void register() {
        ServerLivingEntityEvents.ALLOW_DAMAGE.register(DreamEquipmentShieldEffects::allowDamage);
        ServerLivingEntityEvents.AFTER_DAMAGE.register(DreamEquipmentShieldEffects::afterDamage);
        ServerTickEvents.END_SERVER_TICK.register(server -> {
            for (ServerPlayer player : server.getPlayerList().getPlayers()) {
                tickPlayer(player);
            }
        });
    }

    private static boolean allowDamage(LivingEntity entity, DamageSource source, float amount) {
        if (!(entity instanceof ServerPlayer player) || player.isCreative() || player.isSpectator()) return true;
        ItemStack shield = blockingShield(player);
        if (!"amethyst".equals(shieldMaterial(shield))) return true;
        DreamEquipmentShieldEffectRules.AmethystShield rule = DreamEquipmentShieldEffectRules.current().amethyst;
        if (!rule.enabled() || !source.is(DamageTypes.SONIC_BOOM)) return true;
        damageShield(player, shield, rule.sonicBoomDamageCost());
        player.playSound(SoundEvents.AMETHYST_BLOCK_CHIME, 0.8f, 1.2f);
        return false;
    }

    private static void afterDamage(LivingEntity entity, DamageSource source, float baseDamageTaken, float damageTaken, boolean blocked) {
        if (!blocked || !(entity instanceof ServerPlayer player) || player.isCreative() || player.isSpectator()) return;
        ItemStack shield = blockingShield(player);
        String material = shieldMaterial(shield);
        if (material.isEmpty()) return;

        DreamEquipmentShieldEffectRules rules = DreamEquipmentShieldEffectRules.current();
        switch (material) {
            case "cactus" -> cactusRetaliate(player, source, rules.cactus);
            case "glass" -> maybeShatterShield(player, shield, rules.glass, baseDamageTaken);
            case "redstone" -> redstonePulse(player, rules.redstone);
            case "slime" -> slimeBounce(player, source, rules.slime);
            case "obsidian" -> obsidianStability(player, source, shield, rules.obsidian);
            case "prismarine" -> prismarineWaterRepair(player, shield, rules.prismarine);
            case "bone" -> boneUndeadRepair(source, shield, rules.bone);
            case "coal" -> coalFireRepair(source, shield, rules.coal);
            case "quartz" -> quartzProjectileRepair(source, shield, rules.quartz);
            default -> {}
        }
    }

    private static void tickPlayer(ServerPlayer player) {
        if (player.isCreative() || player.isSpectator()) return;
        DreamEquipmentShieldEffectRules rules = DreamEquipmentShieldEffectRules.current();
        DreamEquipmentShieldEffectRules.PaperShield paper = rules.paper;
        if (paper.enabled() && paper.wetDamageInterval() > 0 && player.tickCount % paper.wetDamageInterval() == 0 && player.isInWaterOrRain() && player.isBlocking()) {
            ItemStack shield = blockingShield(player);
            if ("paper".equals(shieldMaterial(shield))) damageShield(player, shield, paper.wetDamage());
        }
        DreamEquipmentShieldEffectRules.ObsidianShield obsidian = rules.obsidian;
        if (obsidian.enabled() && player.isBlocking() && "obsidian".equals(shieldMaterial(blockingShield(player)))) {
            player.addEffect(new MobEffectInstance(MobEffects.SLOWNESS, obsidian.slownessDurationTicks(), obsidian.slownessAmplifier(), false, false, true));
        }
    }

    private static void cactusRetaliate(ServerPlayer player, DamageSource source, DreamEquipmentShieldEffectRules.CactusShield rule) {
        if (!rule.enabled() || rule.retaliateDamage() <= 0.0f) return;
        int lastTick = LAST_CACTUS_RETALIATE_TICK.getOrDefault(player.getUUID(), -1000000);
        if (player.tickCount - lastTick < Math.max(0, rule.cooldownTicks())) return;
        Entity attacker = source.getEntity();
        if (!(attacker instanceof LivingEntity living) || attacker == player || !attacker.level().equals(player.level())) return;
        LAST_CACTUS_RETALIATE_TICK.put(player.getUUID(), player.tickCount);
        living.hurtServer((ServerLevel) player.level(), player.damageSources().thorns(player), rule.retaliateDamage());
    }

    private static void maybeShatterShield(ServerPlayer player, ItemStack shield, DreamEquipmentShieldEffectRules.GlassShield rule, float blockedDamage) {
        if (!rule.enabled() || blockedDamage < rule.shatterThreshold()) return;
        if (player.getRandom().nextFloat() >= rule.shatterChance()) return;
        breakBlockingShield(player);
        player.playSound(SoundEvents.GLASS_BREAK, 0.9f, 1.15f);
    }

    private static void redstonePulse(ServerPlayer player, DreamEquipmentShieldEffectRules.RedstoneShield rule) {
        if (!rule.enabled()) return;
        DreamEquipmentRedstonePower.emitPulse((ServerLevel) player.level(), player.blockPosition(), rule.pulseSignal(), rule.pulseTicks());
    }

    private static void slimeBounce(ServerPlayer player, DamageSource source, DreamEquipmentShieldEffectRules.SlimeShield rule) {
        if (!rule.enabled() || rule.knockbackStrength() <= 0.0f) return;
        Entity attacker = source.getEntity();
        if (!(attacker instanceof LivingEntity living) || attacker == player || !attacker.level().equals(player.level())) return;
        Vec3 direction = living.position().subtract(player.position());
        if (direction.lengthSqr() < 0.0001) direction = player.getLookAngle();
        direction = direction.normalize().scale(rule.knockbackStrength());
        living.push(direction.x, rule.verticalBoost(), direction.z);
        living.hurtMarked = true;
    }

    private static void obsidianStability(ServerPlayer player, DamageSource source, ItemStack shield, DreamEquipmentShieldEffectRules.ObsidianShield rule) {
        if (!rule.enabled()) return;
        if (source.is(DamageTypeTags.IS_FIRE) || source.is(DamageTypeTags.IS_EXPLOSION)) repairShield(shield, rule.refundDamage());
    }

    private static void prismarineWaterRepair(ServerPlayer player, ItemStack shield, DreamEquipmentShieldEffectRules.PrismarineShield rule) {
        if (rule.enabled() && player.isInWater()) repairShield(shield, rule.waterRefundDamage());
    }

    private static void boneUndeadRepair(DamageSource source, ItemStack shield, DreamEquipmentShieldEffectRules.BoneShield rule) {
        if (!rule.enabled() || !(source.getEntity() instanceof LivingEntity living) || !isUndeadLike(living)) return;
        repairShield(shield, rule.undeadRefundDamage());
    }

    private static void coalFireRepair(DamageSource source, ItemStack shield, DreamEquipmentShieldEffectRules.CoalShield rule) {
        if (rule.enabled() && source.is(DamageTypeTags.IS_FIRE)) repairShield(shield, rule.fireRefundDamage());
    }

    private static void quartzProjectileRepair(DamageSource source, ItemStack shield, DreamEquipmentShieldEffectRules.QuartzShield rule) {
        if (rule.enabled() && source.is(DamageTypeTags.IS_PROJECTILE)) repairShield(shield, rule.projectileRefundDamage());
    }

    private static boolean isUndeadLike(LivingEntity entity) {
        String path = BuiltInRegistries.ENTITY_TYPE.getKey(entity.getType()).getPath();
        return path.contains("zombie") || path.contains("skeleton") || path.equals("drowned") || path.equals("husk") || path.equals("stray") || path.equals("bogged") || path.equals("parched") || path.contains("wither");
    }

    private static ItemStack blockingShield(ServerPlayer player) {
        if (player.isBlocking()) return player.getUseItem();
        return ItemStack.EMPTY;
    }

    private static void damageShield(ServerPlayer player, ItemStack shield, int amount) {
        if (amount <= 0 || shield.isEmpty()) return;
        shield.hurtAndBreak(amount, player, player.getUsedItemHand());
    }

    private static void repairShield(ItemStack shield, int amount) {
        if (amount <= 0 || shield.isEmpty() || !shield.isDamaged()) return;
        shield.setDamageValue(Math.max(0, shield.getDamageValue() - amount));
    }

    private static void breakBlockingShield(ServerPlayer player) {
        InteractionHand hand = player.getUsedItemHand();
        player.setItemInHand(hand, ItemStack.EMPTY);
    }

    private static String shieldMaterial(ItemStack stack) {
        if (stack.isEmpty()) return "";
        String path = path(stack.getItem());
        if (!path.endsWith("_shield")) return "";
        return path.substring(0, path.length() - "_shield".length());
    }

    private static String path(Item item) {
        Identifier id = BuiltInRegistries.ITEM.getKey(item);
        if (id == null || !DreamEquipment.MOD_ID.equals(id.getNamespace())) return "";
        return id.getPath();
    }
}
