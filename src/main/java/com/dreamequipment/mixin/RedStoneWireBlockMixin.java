package com.dreamequipment.mixin;

import com.dreamequipment.DreamEquipmentRedstonePower;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.RedStoneWireBlock;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(RedStoneWireBlock.class)
public abstract class RedStoneWireBlockMixin {
    @Inject(method = "getBlockSignal", at = @At("RETURN"), cancellable = true)
    private void dream_equipment$getBlockSignal(Level level, BlockPos pos, CallbackInfoReturnable<Integer> cir) {
        int signal = DreamEquipmentRedstonePower.bestNeighborSignalAt(level, pos);
        if (signal > cir.getReturnValue()) cir.setReturnValue(signal);
    }
}
