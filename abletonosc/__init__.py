import logging, traceback
logger = logging.getLogger("abletonosc")

logger.info("Reloading abletonosc...")

from .constants import OSC_LISTEN_PORT, OSC_RESPONSE_PORT

try:
    from .osc_server import OSCServer
except (ImportError, NameError) as e:
    traceback.print_exc()
    logger.error("Failed to import OSCServer")

try:
    from .application import ApplicationHandler
except (ImportError, NameError) as e:
    traceback.print_exc()
    logger.error("Failed to import ApplicationHandler")

try:
    from .browser import BrowserHandler
except (ImportError, NameError) as e:
    traceback.print_exc()
    logger.error("Failed to import BrowserHandler")

try:
    from .song import SongHandler
except (ImportError, NameError) as e:
    traceback.print_exc()
    logger.error("Failed to import SongHandler")

try:
    from .clip import ClipHandler
except (ImportError, NameError) as e:
    traceback.print_exc()
    logger.error("Failed to import ClipHandler")

try:
    from .clip_slot import ClipSlotHandler
except (ImportError, NameError) as e:
    traceback.print_exc()
    logger.error("Failed to import ClipSlotHandler")

try:
    from .track import TrackHandler
except (ImportError, NameError) as e:
    traceback.print_exc()
    logger.error("Failed to import TrackHandler")

try:
    from .device import DeviceHandler
except (ImportError, NameError) as e:
    traceback.print_exc()
    logger.error("Failed to import DeviceHandler")

try:
    from .view import ViewHandler
except (ImportError, NameError) as e:
    traceback.print_exc()
    logger.error("Failed to import ViewHandler")

from .constants import OSC_LISTEN_PORT, OSC_RESPONSE_PORT
