# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

try:
    from jupyter_server.extension.application import ExtensionApp
except ModuleNotFoundError:
    raise ModuleNotFoundError("Jupyter Server must be installed to use this extension.")

from traitlets import Float, Int, Type
from ypy_websocket.ystore import BaseYStore  # type: ignore

from .handlers import JupyterSQLiteYStore, YDocRoomIdHandler, YDocWebSocketHandler


class YDocExtension(ExtensionApp):

    name = "jupyter_server_ydoc"

    collaborative_file_poll_interval = Int(
        1,
        config=True,
        help="""The period in seconds to check for file changes on disk (relevant only
        in collaborative mode). Defaults to 1s, if 0 then file changes will only be checked when
        saving changes from the front-end.""",
    )

    collaborative_document_cleanup_delay = Int(
        60,
        allow_none=True,
        config=True,
        help="""The delay in seconds to keep a document in memory in the back-end after all clients
        disconnect (relevant only in collaborative mode). Defaults to 60s, if None then the
        document will be kept in memory forever.""",
    )

    collaborative_document_save_delay = Float(
        1,
        allow_none=True,
        config=True,
        help="""The delay in seconds to wait after a change is made to a document before saving it
        (relevant only in collaborative mode). Defaults to 1s, if None then the document will never be saved.""",
    )

    collaborative_ystore_class = Type(
        default_value=JupyterSQLiteYStore,
        klass=BaseYStore,
        config=True,
        help="""The YStore class to use for storing Y updates (relevant only in collaborative mode).
        Defaults to JupyterSQLiteYStore, which stores Y updates in a '.jupyter_ystore.db' SQLite
        database in the current directory.""",
    )

    def initialize_settings(self):
        self.settings.update(
            {
                "collaborative_file_poll_interval": self.collaborative_file_poll_interval,
                "collaborative_document_cleanup_delay": self.collaborative_document_cleanup_delay,
                "collaborative_document_save_delay": self.collaborative_document_save_delay,
                "collaborative_ystore_class": self.collaborative_ystore_class,
            }
        )

    def initialize_handlers(self):
        self.handlers.extend(
            [
                (r"/api/yjs/roomid/(.*)", YDocRoomIdHandler),
                (r"/api/yjs/(.*)", YDocWebSocketHandler),
            ]
        )
