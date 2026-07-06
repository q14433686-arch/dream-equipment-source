package com.dreamequipment.mixin;

import com.dreamequipment.DreamEquipmentRedstonePower;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.SignalGetter;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(SignalGetter.class)
public interface SignalGetterMixin {
    @Inject(method = "getSignal", at = @At("RETURN"), cancellable = true)
    private void dream_equipment$getSignal(BlockPos pos, Direction direction, CallbackInfoReturnable<Integer> cir) {
        int signal = DreamEquipmentRedstonePower.signalAt(this, pos);
        if (signal > cir.getReturnValue()) cir.setReturnValue(signal);
    }

    @Inject(method = "getDirectSignal", at = @At("RETURN"), cancellable = true)
    private void dream_equipment$getDirectSignal(BlockPos pos, Direction direction, CallbackInfoReturnable<Integer> cir) {
        int signal = DreamEquipmentRedstonePower.signalAt(this, pos);
        if (signal > cir.getReturnValue()) cir.setReturnValue(signal);
    }

    @Inject(method = "getBestNeighborSignal", at = @At("RETURN"), cancellable = true)
    private void dream_equipment$getBestNeighborSignal(BlockPos pos, CallbackInfoReturnable<Integer> cir) {
        int signal = DreamEquipmentRedstonePower.bestNeighborSignalAt(this, pos);
        if (signal > cir.getReturnValue()) cir.setReturnValue(signal);
    }

    @Inject(method = "hasNeighborSignal", at = @At("RETURN"), cancellable = true)
    private void dream_equipment$hasNeighborSignal(BlockPos pos, CallbackInfoReturnable<Boolean> cir) {
        if (!cir.getReturnValue() && DreamEquipmentRedstonePower.bestNeighborSignalAt(this, pos) > 0) cir.setReturnValue(true);
    }

}
