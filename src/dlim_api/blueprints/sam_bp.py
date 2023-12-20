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
from flask import (
    Blueprint,
    abort,
    current_app,
    jsonify,
    make_response,
    request,
    send_file,
)
from PIL import Image
from segment_anything import SamAutomaticMaskGenerator, SamPredictor, sam_model_registry

from dlim_api.utils.model_utils import sam_utils

logger = logging.getLogger(__name__)


sam_blueprint = Blueprint("sam", __name__)

WORK_DIR = Path().absolute()
IMAGE_DIR = WORK_DIR / "src/dlim_api/images"


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
        logger.error(str(e))
        return str(e)


@sam_blueprint.route("/sam/segment/image-only", methods=["POST"])
def segment_image():
    # img.save(PATH_TO_IMG)
    if "image" not in request.files:
        logger.info("No image provided")
        return jsonify({"error": "No image provided"}), 400

    image = request.files["image"]

    try:
        image_path = sam_utils.segment_image(image)
        image_response = make_response(send_file(image_path))
        os.remove(image_path)
        logger.info(os.path.isfile(image_path))  # Seems to be deleting
        additional_data = {"status": "completed", "message": "Image served successfully"}
        # response.headers["Content-Type"] = "application/json"
        # response.set_data(jsonify(additional_data).data)
        final_response = make_response(image_response.get_data())
        final_response.headers.extend(image_response.headers)
        final_response.set_data(jsonify(additional_data).get_data())
        return final_response
    except Exception as e:
        logger.error(str(e))
        return str(e)
