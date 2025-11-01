from loguru import logger
import sys


def setup_logging() -> None:
	logger.remove()
	logger.add(
		sys.stdout,
		format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
		level="INFO",
		backtrace=False,
		enqueue=True,
	)
