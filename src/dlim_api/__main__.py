from __future__ import annotations

import logging

from utils.args_utils import parse_args
from utils.logging_utils import setup_logger

logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Hello World!")
    return None


if __name__ == "__main__":
    args = parse_args()
    setup_logger(args.log_level, args.console_log)
    main()
