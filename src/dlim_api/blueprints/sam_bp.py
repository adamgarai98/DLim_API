from __future__ import annotations

import base64
import concurrent.futures
import logging
import multiprocessing
import os
import threading
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
from werkzeug.utils import secure_filename

from dlim_api.utils.model_utils import sam_utils

logger = logging.getLogger(__name__)


sam_blueprint = Blueprint("sam", __name__)

WORK_DIR = Path().absolute()
IMAGE_DIR = WORK_DIR / "src/dlim_api/images"

executor = concurrent.futures.ThreadPoolExecutor()

task_data = {}


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


def run_segment_image(image_path, task_id):
    global task_data
    # task_id = str(uuid.uuid4())
    task_data[task_id] = {}
    current_task = task_data[task_id]
    current_task["status"] = "running"

    try:
        logger.info("Starting segmentation")
        image_path = sam_utils.segment_image(image_path)
        logger.info("Finished segmentation")

        current_task["status"] = "completed"
        current_task["path_to_image"] = image_path
    except Exception as e:
        logger.error(str(e))


@sam_blueprint.route("/sam/segment/", methods=["POST"])
def segment_image():
    # Declare as global since modifying
    global task_data

    # Check if there is an image
    if "image" not in request.files:
        logger.info("No image provided")
        return jsonify({"error": "No image provided"}), 400

    image = request.files["image"]
    task_id = str(uuid.uuid4())

    # Save file first
    image_name = secure_filename(image.filename)
    logger.info(str(image_name))
    logger.info(str(image.mimetype))
    PATH_TO_IMG = IMAGE_DIR / image_name
    image.save(PATH_TO_IMG)

    # image_name = image.filename
    # PATH_TO_IMG = IMAGE_DIR / image_name
    # image.save(PATH_TO_IMG)

    # Submit task
    future = executor.submit(run_segment_image, PATH_TO_IMG, task_id)
    return jsonify({"message": "Request in progress", "task_id": task_id})


@sam_blueprint.route("/sam/segment/status/<task_id>", methods=["GET"])
def get_segementation_status(task_id):
    # Check the status of the task
    # task_id = int(task_id)
    task = task_data.get(task_id, {"status": "not_found", "message": "Task not found"})

    if task["status"] == "completed":
        # If task is completed return result
        logger.info("Sending image back")
        return send_file(task["path_to_image"])

    return jsonify(task)


@sam_blueprint.route("/sam/segment/image-only", methods=["POST"])
def segment_image_only():
    # Check if there is an image
    if "image" not in request.files:
        logger.info("No image provided")
        return jsonify({"error": "No image provided"}), 400

    image = request.files["image"]

    try:
        image_path = sam_utils.segment_image(image)
        image_response = send_file(image_path)
        os.remove(image_path)
        logger.info(os.path.isfile(image_path))  # Seems to be deleting
        return image_response
    except Exception as e:
        logger.error(str(e))
        return str(e)
