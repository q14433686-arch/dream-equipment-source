package com.dreamequipment;

import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Blocks;

import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

public final class DreamEquipmentRedstonePower {
    private static final Map<ServerLevel, Map<BlockPos, Pulse>> ACTIVE_PULSES = new HashMap<>();
    private static final Map<UUID, SourceState> LAST_PLAYER_SOURCE = new HashMap<>();
    private static long tickCounter = 0L;

    private DreamEquipmentRedstonePower() {}

    public static void register() {
        ServerTickEvents.END_SERVER_TICK.register(DreamEquipmentRedstonePower::tickPulses);
    }

    public static int signalAt(Object levelLike, BlockPos poweredBlockPos) {
        if (!(levelLike instanceof ServerLevel level)) return 0;
        Pulse pulse = ACTIVE_PULSES.getOrDefault(level, Map.of()).get(poweredBlockPos);
        return pulse != null && pulse.expiresAt() >= tickCounter ? pulse.signal() : 0;
    }

    public static int bestNeighborSignalAt(Object levelLike, BlockPos pos) {
        if (!(levelLike instanceof ServerLevel level)) return 0;
        Map<BlockPos, Pulse> pulses = ACTIVE_PULSES.getOrDefault(level, Map.of());
        int best = 0;
        for (Direction direction : Direction.values()) {
            Pulse pulse = pulses.get(pos.relative(direction));
            if (pulse != null && pulse.expiresAt() >= tickCounter && pulse.signal() > best) best = pulse.signal();
            if (best >= 15) return 15;
        }
        return best;
    }

    public static int redstoneSignalFor(ServerPlayer player, DreamEquipmentSetEffectRules.RedstoneSignalRule rule) {
        if (!rule.enabled() || player.isSpectator()) return 0;
        if (fullRedstoneSet(player)) return rule.fullSetSignal();
        if (path(player.getItemBySlot(EquipmentSlot.FEET).getItem()).equals("redstone_boots")) return rule.bootsSignal();
        return 0;
    }

    private static void tickPulses(MinecraftServer server) {
        tickCounter++;
        expireOldPulses();

        DreamEquipmentSetEffectRules.RedstoneSignalRule rule = DreamEquipmentSetEffectRules.current().redstoneSignal;
        Set<UUID> seenPlayers = new HashSet<>();
        if (rule.enabled()) {
            for (ServerPlayer player : server.getPlayerList().getPlayers()) {
                UUID uuid = player.getUUID();
                seenPlayers.add(uuid);
                int signal = redstoneSignalFor(player, rule);
                SourceState previous = LAST_PLAYER_SOURCE.get(uuid);
                if (signal <= 0) {
                    LAST_PLAYER_SOURCE.remove(uuid);
                    continue;
                }
                ServerLevel level = (ServerLevel) player.level();
                BlockPos pos = sourcePos(player);
                SourceState current = new SourceState(level, pos, signal);
                if (!current.equals(previous)) {
                    addPulse(level, pos, signal, pulseTicksFor(signal, rule));
                    LAST_PLAYER_SOURCE.put(uuid, current);
                }
            }
        }
        LAST_PLAYER_SOURCE.keySet().removeIf(uuid -> !seenPlayers.contains(uuid));
    }

    private static int pulseTicksFor(int signal, DreamEquipmentSetEffectRules.RedstoneSignalRule rule) {
        return signal >= rule.fullSetSignal() ? rule.fullSetPulseTicks() : rule.bootsPulseTicks();
    }

    public static void emitPulse(ServerLevel level, BlockPos pos, int signal, int durationTicks) {
        addPulse(level, pos, signal, durationTicks);
    }

    private static void addPulse(ServerLevel level, BlockPos pos, int signal, int durationTicks) {
        if (signal <= 0 || durationTicks <= 0) return;
        long expiresAt = tickCounter + durationTicks;
        Map<BlockPos, Pulse> pulses = ACTIVE_PULSES.computeIfAbsent(level, ignored -> new LinkedHashMap<>());
        Pulse old = pulses.get(pos);
        Pulse next = old == null
            ? new Pulse(signal, expiresAt)
            : new Pulse(Math.max(signal, old.signal()), Math.max(expiresAt, old.expiresAt()));
        pulses.put(pos, next);
        if (old == null || old.signal() != next.signal()) {
            notifyRedstoneAround(level, pos);
        }
    }

    private static void expireOldPulses() {
        ACTIVE_PULSES.entrySet().removeIf(levelEntry -> {
            ServerLevel level = levelEntry.getKey();
            Map<BlockPos, Pulse> pulses = levelEntry.getValue();
            pulses.entrySet().removeIf(pulseEntry -> {
                boolean expired = pulseEntry.getValue().expiresAt() < tickCounter;
                if (expired) notifyRedstoneAround(level, pulseEntry.getKey());
                return expired;
            });
            return pulses.isEmpty();
        });
    }

    private static BlockPos sourcePos(ServerPlayer player) {
        // A short-lived virtual redstone pulse occupies the player's feet-space.
        return player.blockPosition();
    }

    private static void notifyRedstoneAround(ServerLevel level, BlockPos source) {
        for (int dx = -2; dx <= 2; dx++) {
            for (int dy = -1; dy <= 1; dy++) {
                for (int dz = -2; dz <= 2; dz++) {
                    level.updateNeighborsAt(source.offset(dx, dy, dz), Blocks.REDSTONE_BLOCK);
                }
            }
        }
    }

    private static boolean fullRedstoneSet(ServerPlayer player) {
        return path(player.getItemBySlot(EquipmentSlot.HEAD).getItem()).equals("redstone_helmet")
            && path(player.getItemBySlot(EquipmentSlot.CHEST).getItem()).equals("redstone_chestplate")
            && path(player.getItemBySlot(EquipmentSlot.LEGS).getItem()).equals("redstone_leggings")
            && path(player.getItemBySlot(EquipmentSlot.FEET).getItem()).equals("redstone_boots");
    }

    private static String path(Item item) {
        net.minecraft.resources.Identifier id = net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(item);
        return id == null ? "" : id.getPath();
    }

    private record Pulse(int signal, long expiresAt) {}
    private record SourceState(ServerLevel level, BlockPos pos, int signal) {}
}
