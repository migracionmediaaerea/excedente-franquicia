import json
import logging
from datetime import datetime

logger = logging.getLogger('file_logger')

def log(obj: dict):
    obj["time"] = datetime.utcnow().isoformat()
    logger.error(json.dumps(obj))