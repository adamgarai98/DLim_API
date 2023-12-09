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


@sam_blueprint.route("/blueprint-hc", methods=["GET"])
def bp_hc():
    return str(torch.cuda.is_available())


@sam_blueprint.route("/racoon-in-a-suit", methods=["GET"])
def send_racoon():
    WORK_DIR = Path().absolute()  # Gets current working dir
    PATH_TO_RACOON = WORK_DIR / "src/dlim_api/images/racoon_in_suit.jpg"
    return send_file(PATH_TO_RACOON, mimetype="image/jpeg")
    # TODO CHECK if this works with docker, works locally right now


@sam_blueprint.route("/sam", methods=["PUT"])
def send_racoon():
    WORK_DIR = Path().absolute()  # Gets current working dir
    PATH_TO_RACOON = WORK_DIR / "src/dlim_api/images/racoon_in_suit.jpg"
    return send_file(PATH_TO_RACOON, mimetype="image/jpeg")
    # TODO CHECK if this works with docker, works locally right now
