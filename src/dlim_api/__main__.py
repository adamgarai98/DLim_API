from __future__ import annotations

import logging
import os

from flask import Flask

from dlim_api.blueprints import blueprints
from dlim_api.utils.args_utils import parse_flask_server_args
from dlim_api.utils.logging_utils import setup_logger

logger = logging.getLogger(__name__)

app = Flask(__name__)

for blueprint in blueprints:
    app.register_blueprint(blueprint)


@app.route("/healthcheck")
def healthcheck():
    app.logger.info("Healthcheck")  # TODO both these actually work lol
    logger.info("Base logger")
    return "OK"


def run_server(host: str = "0.0.0.0", port: int = 5000, debug: bool = False) -> None:
    # app.logger.info("Starting server...")
    app.run(host=host, port=port, debug=debug)


def main():
    args = parse_flask_server_args()
    setup_logger(args.log_level, args.console_log)
    run_server(args.host, args.port, False if args.log_level == logging.DEBUG else True)


# Turns out this never actually runs if building the package
if __name__ == "__main__":
    main()
