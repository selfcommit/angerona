from sqlalchemy.exc import (
    OperationalError,
    DBAPIError
    )
from angerona.models import (
    DBSession,
    Secret,
    )
import datetime
from AppLogging import logger

def CleanupDatabase(request):
    if request.matched_route is None:
        return
    routename = request.matched_route.name
    if (routename == "save") or (routename == "retr"):
        logger.debug("Route matched for cleanup: %s" % routename)
        try:
            session = DBSession()
            result = session.query(Secret).\
                filter((Secret.ExpiryTime < datetime.datetime.now()) | (Secret.LifetimeReads == 0)).\
                delete()
            session.flush()
            session.close()
        except (OperationalError, DBAPIError), exc:
            logger.error("CleanupDatabase(): DBAPIError %s" % exc)
            pass
