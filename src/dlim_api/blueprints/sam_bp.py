from __future__ import annotations

import logging
import multiprocessing
import os
import uuid
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
from flask import Blueprint, abort, current_app, jsonify, request, send_file
from PIL import Image
from segment_anything import SamAutomaticMaskGenerator, SamPredictor, sam_model_registry

logger = logging.getLogger(__name__)


sam_blueprint = Blueprint("sam", __name__)

WORK_DIR = Path().absolute()
IMAGE_DIR = WORK_DIR / "src/dlim_api/images"

mask_generator = None  # TODO CHANGE to object etc dict wahtever


def get_masks(anns):  # TODO MOVE
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


@sam_blueprint.route("/blueprint-hc", methods=["GET"])
def bp_hc():
    return "BP OK"


@sam_blueprint.route("/racoon-in-a-suit", methods=["GET"])
def send_racoon():
    # Gets current working dir
    PATH_TO_RACOON = WORK_DIR / "src/dlim_api/images/racoon_in_suit.jpg"
    return send_file(PATH_TO_RACOON, mimetype="image/jpeg")


@sam_blueprint.route("/sam", methods=["PUT"])
def load_sam():
    try:
        WORK_DIR = Path().absolute()  # Gets current working dir
        SAM_CHECKPOINT = WORK_DIR / "src/dlim_api/utils/model_checkpoints/sam_vit_h_4b8939.pth"
        model_type = "vit_h"
        device = "cuda"
        sam = sam_model_registry[model_type](checkpoint=SAM_CHECKPOINT)
        sam.to(device=device)
        global mask_generator
        mask_generator = SamAutomaticMaskGenerator(model=sam, points_per_batch=32)

        return "Successfuly loaded SAM"
    except Exception as e:
        return str(e)


@sam_blueprint.route("/sam", methods=["POST"])
def segment_image():
    image = request.files["image"]
    image_name = image.filename
    PATH_TO_IMG = IMAGE_DIR / image_name
    image = Image.open(image.stream)

    image = np.asarray(image)
    masks = mask_generator.generate(image)
    image = Image.fromarray(image)
    image_masks = Image.fromarray(np.uint8(get_masks(masks) * 255))
    image.paste(image_masks, (0, 0), image_masks)
    image.save(PATH_TO_IMG)

    # img.save(PATH_TO_IMG)

    return send_file(PATH_TO_IMG)