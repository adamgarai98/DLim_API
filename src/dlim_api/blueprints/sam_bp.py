from __future__ import annotations

import concurrent.futures
import logging
import os
import threading
import uuid
from pathlib import Path

from flask import Blueprint, jsonify, request, send_file
from werkzeug.utils import secure_filename

from dlim_api.utils.model_utils import sam_utils

logger = logging.getLogger(__name__)


sam_blueprint = Blueprint("sam", __name__)

WORK_DIR = Path().absolute()
IMAGE_DIR = WORK_DIR / "src/dlim_api/images"

executor = concurrent.futures.ThreadPoolExecutor()


@sam_blueprint.route("/sam/load", methods=["PUT"])
def load_sam():
    try:
        sam_utils.load_sam()
        return "Successfuly loaded SAM", 201
    except Exception as e:
        logger.error(str(e))
        return str(e)


@sam_blueprint.route("/sam/segment/", methods=["POST"])
def segment_image():
    # Check if there is an image
    if "image" not in request.files:
        logger.info("No image provided")
        return jsonify({"error": "No image provided"}), 400

    image = request.files["image"]
    task_id = str(uuid.uuid4())

    # Save file first
    image_name = secure_filename(image.filename)
    logger.debug(str(image_name))
    logger.debug(str(image.mimetype))
    PATH_TO_IMG = IMAGE_DIR / image_name
    image.save(PATH_TO_IMG)

    # Submit task
    future = executor.submit(sam_utils.run_segment_image, PATH_TO_IMG, task_id)
    return jsonify({"message": "Request in progress", "task_id": task_id})


@sam_blueprint.route("/sam/segment/status/<task_id>", methods=["GET"])
def get_segementation_status(task_id):
    # Check the status of the task
    task = sam_utils.task_data.get(task_id, {"status": "not_found", "message": "Task not found"})

    # If task is completed return image
    if task["status"] == "completed":
        logger.info("Sending image")
        return send_file(task["path_to_image"])

    return jsonify(task)


# TODO change below for a flag maybe

# @sam_blueprint.route("/sam/segment/image-only", methods=["POST"])
# def segment_image_only():
#     # Check if there is an image
#     if "image" not in request.files:
#         logger.info("No image provided")
#         return jsonify({"error": "No image provided"}), 400

#     image = request.files["image"]
#     try:
#         image_path = sam_utils.segment_image(image)
#         image_response = send_file(image_path)
#         os.remove(image_path)
#         logger.info(os.path.isfile(image_path))  # Seems to be deleting
#         return image_response
#     except Exception as e:
#         logger.error(str(e))
#         return str(e)
