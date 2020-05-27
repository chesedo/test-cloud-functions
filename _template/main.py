import logging
from typing import Any


def _template(aData: Any, aContext: Any) -> None:
    """HTTP end-point for ...

    Arguments:
        aData {FileEvent} -- The file event that triggered this function
        aContext {Context} -- The context
    """
    logging.basicConfig(level=logging.DEBUG)
    logging.info(f"Processing {aData}")

    try:
        pass
    except Exception as lException:
        logging.critical(f"Processing failed: {lException}")
