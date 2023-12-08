from __future__ import annotations

import logging
from flask import Flask

from utils.args_utils import parse_flask_server_args
from utils.logging_utils import setup_logger


app = Flask(__name__)

@app.route("/healthcheck")
def healthcheck():
    return "OK"

logger = logging.getLogger(__name__)


def main(host: str = "0.0.0.0", port: int = 5000, debug: bool = False) -> None:
    logger.info("Starting server...")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    args = parse_flask_server_args()
    setup_logger(args.log_level, args.console_log)
    debug = True
    # if args.log_level == logging.DEBUG:
    #     debug = True
    main(args.host, args.port, debug)

