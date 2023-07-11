import logging
from rich.logging import RichHandler
import inspect

FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.DEBUG, format=FORMAT, datefmt="[%X]", handlers=[RichHandler(markup=True)])

logger = logging.getLogger("rich")
