import os
import sys

_STUBS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "stubs")
sys.path.insert(0, _STUBS)

import logging

from server import serve

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

serve()
