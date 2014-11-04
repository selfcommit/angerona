from sqlalchemy.exc import (
    DBAPIError
    )
from angerona.models import (
    DBSession,
    Secret,
    )
import datetime
from AppLogging import logger

def CleanupDatabase(self):
    logger.debug("Enter CleanupDatabase")
    try:
        session = DBSession()
        result = session.query(Secret).\
            filter((Secret.ExpiryTime < datetime.datetime.now()) | (Secret.LifetimeReads == 0)).\
            delete()
        session.flush()
    except DBAPIError, exc:
        logger.error("CleanupDatabase(): DBAPIError %s" % exc)
    logger.debug("Leaving CleanupDatabase")


