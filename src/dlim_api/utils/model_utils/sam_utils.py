from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry

logger = logging.getLogger(__name__)

WORK_DIR = Path().absolute()
IMAGE_DIR = WORK_DIR / "src/dlim_api/images"


mask_generator = None  # TODO hmm


def get_masks(anns):
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x["area"]), reverse=True)
    img = np.ones((sorted_anns[0]["segmentation"].shape[0], sorted_anns[0]["segmentation"].shape[1], 4))
    img[:, :, 3] = 0
    for ann in sorted_anns:
        m = ann["segmentation"]
        color_mask = np.concatenate([np.random.random(3), [0.35]])
        img[m] = color_mask
    return img


def load_sam():
    global mask_generator
    try:
        WORK_DIR = Path().absolute()  # Gets current working dir
        SAM_CHECKPOINT = WORK_DIR / "src/dlim_api/utils/model_checkpoints/sam_vit_h_4b8939.pth"
        model_type = "vit_h"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"{device} detected")
        sam = sam_model_registry[model_type](checkpoint=SAM_CHECKPOINT)
        sam.to(device=device)
        mask_generator = SamAutomaticMaskGenerator(model=sam, points_per_batch=32)
        return
    except Exception as e:
        logger.error(str(e))
        return str(e)


def segment_image(image_path):
    try:
        # Open image
        image = Image.open(image_path)
        image = np.asarray(image)

        # Generate Masks
        logger.info("Generating masks")
        masks = mask_generator.generate(image)
        logger.info("Masks Generated")

        # Paste masks over image
        image = Image.fromarray(image)
        image_masks = Image.fromarray(np.uint8(get_masks(masks) * 255))
        image.paste(image_masks, (0, 0), image_masks)
        image.save(image_path)

        # Return pasted image
        return image_path

    except torch.cuda.CudaOutOfMemory:
        # Handle out-of-memory error
        logger.error("Cuda out of memory")
        # Add below to the dict
        # result = {"status": "failed", "message": "CUDA out of memory error"}

    except Exception as e:
        # Handle other exceptions if needed
        logger.error(str(e))
        # Add below to the dict
        # result = {"status": "failed", "message": f"Error: {str(e)}"}


def run_segment_image(image_path, task_id):
    global task_data
    task_data[task_id] = {}
    current_task = task_data[task_id]
    current_task["status"] = "running"

    try:
        logger.info("Starting segmentation")
        image_path = segment_image(image_path)
        logger.info("Finished segmentation")

        current_task["status"] = "completed"
        current_task["path_to_image"] = image_path
    except Exception as e:
        logger.error(str(e))
