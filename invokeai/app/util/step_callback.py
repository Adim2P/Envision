from math import floor
from typing import Callable, Optional, TypeAlias

import torch
from PIL import Image

from invokeai.app.services.session_processor.session_processor_common import CanceledException
from invokeai.backend.model_manager.config import BaseModelType
from invokeai.backend.stable_diffusion.diffusers_pipeline import PipelineIntermediateState

# fast latents preview matrix for sdxl
# generated by @StAlKeR7779
SDXL_LATENT_RGB_FACTORS = [
    #   R        G        B
    [0.3816, 0.4930, 0.5320],
    [-0.3753, 0.1631, 0.1739],
    [0.1770, 0.3588, -0.2048],
    [-0.4350, -0.2644, -0.4289],
]
SDXL_SMOOTH_MATRIX = [
    [0.0358, 0.0964, 0.0358],
    [0.0964, 0.4711, 0.0964],
    [0.0358, 0.0964, 0.0358],
]

# origingally adapted from code by @erucipe and @keturn here:
# https://discuss.huggingface.co/t/decoding-latents-to-rgb-without-upscaling/23204/7
# these updated numbers for v1.5 are from @torridgristle
SD1_5_LATENT_RGB_FACTORS = [
    #    R        G        B
    [0.3444, 0.1385, 0.0670],  # L1
    [0.1247, 0.4027, 0.1494],  # L2
    [-0.3192, 0.2513, 0.2103],  # L3
    [-0.1307, -0.1874, -0.7445],  # L4
]

FLUX_LATENT_RGB_FACTORS = [
    [-0.0412, 0.0149, 0.0521],
    [0.0056, 0.0291, 0.0768],
    [0.0342, -0.0681, -0.0427],
    [-0.0258, 0.0092, 0.0463],
    [0.0863, 0.0784, 0.0547],
    [-0.0017, 0.0402, 0.0158],
    [0.0501, 0.1058, 0.1152],
    [-0.0209, -0.0218, -0.0329],
    [-0.0314, 0.0083, 0.0896],
    [0.0851, 0.0665, -0.0472],
    [-0.0534, 0.0238, -0.0024],
    [0.0452, -0.0026, 0.0048],
    [0.0892, 0.0831, 0.0881],
    [-0.1117, -0.0304, -0.0789],
    [0.0027, -0.0479, -0.0043],
    [-0.1146, -0.0827, -0.0598],
]


def sample_to_lowres_estimated_image(
    samples: torch.Tensor, latent_rgb_factors: torch.Tensor, smooth_matrix: Optional[torch.Tensor] = None
):
    latent_image = samples[0].permute(1, 2, 0) @ latent_rgb_factors

    if smooth_matrix is not None:
        latent_image = latent_image.unsqueeze(0).permute(3, 0, 1, 2)
        latent_image = torch.nn.functional.conv2d(latent_image, smooth_matrix.reshape((1, 1, 3, 3)), padding=1)
        latent_image = latent_image.permute(1, 2, 3, 0).squeeze(0)

    latents_ubyte = (
        ((latent_image + 1) / 2).clamp(0, 1).mul(0xFF).byte()  # change scale from -1..1 to 0..1  # to 0..255
    ).cpu()

    return Image.fromarray(latents_ubyte.numpy())


def calc_percentage(intermediate_state: PipelineIntermediateState) -> float:
    """Calculate the percentage of completion of denoising."""

    step = intermediate_state.step
    total_steps = intermediate_state.total_steps
    order = intermediate_state.order

    if total_steps == 0:
        return 0.0
    if order == 2:
        return floor(step / 2) / floor(total_steps / 2)
    # order == 1
    return step / total_steps


SignalProgressFunc: TypeAlias = Callable[[str, float | None, Image.Image | None, tuple[int, int] | None], None]


def stable_diffusion_step_callback(
    signal_progress: SignalProgressFunc,
    intermediate_state: PipelineIntermediateState,
    base_model: BaseModelType,
    is_canceled: Callable[[], bool],
) -> None:
    if is_canceled():
        raise CanceledException

    # Some schedulers report not only the noisy latents at the current timestep,
    # but also their estimate so far of what the de-noised latents will be. Use
    # that estimate if it is available.
    if intermediate_state.predicted_original is not None:
        sample = intermediate_state.predicted_original
    else:
        sample = intermediate_state.latents

    if base_model in [BaseModelType.StableDiffusionXL, BaseModelType.StableDiffusionXLRefiner]:
        sdxl_latent_rgb_factors = torch.tensor(SDXL_LATENT_RGB_FACTORS, dtype=sample.dtype, device=sample.device)
        sdxl_smooth_matrix = torch.tensor(SDXL_SMOOTH_MATRIX, dtype=sample.dtype, device=sample.device)
        image = sample_to_lowres_estimated_image(sample, sdxl_latent_rgb_factors, sdxl_smooth_matrix)
    else:
        v1_5_latent_rgb_factors = torch.tensor(SD1_5_LATENT_RGB_FACTORS, dtype=sample.dtype, device=sample.device)
        image = sample_to_lowres_estimated_image(sample, v1_5_latent_rgb_factors)

    width = image.width * 8
    height = image.height * 8
    percentage = calc_percentage(intermediate_state)

    signal_progress("Denoising", percentage, image, (width, height))


def flux_step_callback(
    signal_progress: SignalProgressFunc,
    intermediate_state: PipelineIntermediateState,
    is_canceled: Callable[[], bool],
) -> None:
    if is_canceled():
        raise CanceledException
    sample = intermediate_state.latents
    latent_rgb_factors = torch.tensor(FLUX_LATENT_RGB_FACTORS, dtype=sample.dtype, device=sample.device)
    latent_image_perm = sample.permute(1, 2, 0).to(dtype=sample.dtype, device=sample.device)
    latent_image = latent_image_perm @ latent_rgb_factors
    latents_ubyte = (
        ((latent_image + 1) / 2).clamp(0, 1).mul(0xFF)  # change scale from -1..1 to 0..1  # to 0..255
    ).to(device="cpu", dtype=torch.uint8)
    image = Image.fromarray(latents_ubyte.cpu().numpy())

    width = image.width * 8
    height = image.height * 8
    percentage = calc_percentage(intermediate_state)

    signal_progress("Denoising", percentage, image, (width, height))