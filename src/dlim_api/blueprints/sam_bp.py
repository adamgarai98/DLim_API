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

from dlim_api.utils.model_utils import sam_utils

logger = logging.getLogger(__name__)


sam_blueprint = Blueprint("sam", __name__)

WORK_DIR = Path().absolute()
IMAGE_DIR = WORK_DIR / "src/dlim_api/images"


@sam_blueprint.route("/blueprint-hc", methods=["GET"])
def bp_hc():
    return "BP OK"


@sam_blueprint.route("/racoon-in-a-suit", methods=["GET"])
def send_racoon():
    # Gets current working dir
    PATH_TO_RACOON = WORK_DIR / "src/dlim_api/images/racoon_in_suit.jpg"
    return send_file(PATH_TO_RACOON, mimetype="image/jpeg")


@sam_blueprint.route("/sam/load", methods=["PUT"])
def load_sam():
    try:
        sam_utils.load_sam()
        return "Successfuly loaded SAM"
    except Exception as e:
        return str(e)


@sam_blueprint.route("/sam/segment", methods=["POST"])
def segment_image():
    # img.save(PATH_TO_IMG)
    image = request.files["image"]
    try:
        return send_file(sam_utils.segment_image(image))
    except Exception as e:
        return str(e)
