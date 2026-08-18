# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.
# SPDX-License-Identifier: GPL-3.0-or-later

"""File log for DAV, usable from any thread.

DAV runs inside FreeCAD: ``print`` goes to the Report View, which is lost when
the window closes and is gone entirely when the process dies hard. A native
crash in a worker thread (Vosk aborting the process, a Qt widget touched off
the GUI thread) leaves no Python traceback anywhere, so the last lines written
here are the only evidence of what DAV was doing.

Every record is flushed on write. Buffering would drop exactly the lines that
matter -- the ones just before the crash.

Example::

    from core.dav_log import get_logger

    log = get_logger(__name__)
    log.info("mic abierto: idioma=%s", language)
    log.exception("fallo al aplicar la gramatica")   # incluye traceback
"""

from __future__ import annotations

import logging
import logging.handlers
import os
import sys
from pathlib import Path

_LOGGER_NAME = "dav"
_MAX_BYTES = 1_000_000
_BACKUP_COUNT = 1

_configured = False


def log_file_path() -> Path:
    """Return the log file location, next to settings.json."""
    from core.settings import CONFIG_DIR

    return CONFIG_DIR / "dav.log"


def _build_handler(path: Path) -> logging.Handler:
    """Rotating file handler, or a stderr handler if the file is unusable."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        handler: logging.Handler = logging.handlers.RotatingFileHandler(
            path,
            maxBytes=_MAX_BYTES,
            backupCount=_BACKUP_COUNT,
            encoding="utf-8",
            delay=False,
        )
    except OSError:
        # Sin permisos o disco lleno: mejor loguear a stderr que romper el
        # arranque de FreeCAD por no poder abrir un archivo de log.
        handler = logging.StreamHandler(sys.stderr)

    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)-7s [%(threadName)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    return handler


def _configure() -> None:
    """Attach the file handler once per process."""
    global _configured
    if _configured:
        return

    logger = logging.getLogger(_LOGGER_NAME)
    logger.setLevel(logging.DEBUG if os.environ.get("DAV_DEBUG") else logging.INFO)
    # DAV escribe su propio archivo: que no suba al root, que en FreeCAD
    # termina duplicando todo en el Report View.
    logger.propagate = False

    if not logger.handlers:
        logger.addHandler(_build_handler(log_file_path()))

    _configured = True


def get_logger(name: str | None = None) -> logging.Logger:
    """Return the DAV logger, configuring the file handler on first use.

    Args:
        name: Usually ``__name__``. Becomes a child logger so each record
            shows which module wrote it.

    Returns:
        A logger that writes to ``config/dav.log``, flushed on every record.
    """
    _configure()
    if not name or name == _LOGGER_NAME:
        return logging.getLogger(_LOGGER_NAME)
    return logging.getLogger(f"{_LOGGER_NAME}.{name}")


def log_unhandled_thread_exceptions() -> None:
    """Route uncaught worker-thread exceptions into the log.

    ``threading.excepthook`` fires when a thread dies from an exception that
    nobody caught. Without this the thread disappears silently and the UI keeps
    showing the mic as active. This does NOT catch native crashes (a C++ abort
    inside Vosk takes the process down without unwinding Python).
    """
    import threading

    log = get_logger("thread")
    previous = threading.excepthook

    def _hook(args) -> None:
        log.error(
            "Hilo '%s' murio por una excepcion sin atrapar",
            getattr(args.thread, "name", "?"),
            exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
        )
        previous(args)

    threading.excepthook = _hook
