import logging
import logging.config

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARN)
logging.getLogger('sqlalchemy.dialects').setLevel(logging.WARN)
logging.getLogger('sqlalchemy.pool').setLevel(logging.WARN)
logging.getLogger('sqlalchemy.orm').setLevel(logging.WARN)
logger = logging.getLogger(__name__)
