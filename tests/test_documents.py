# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import sys

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

import pytest
from anyio import sleep
from pycrdt_websocket import WebsocketProvider

jupyter_ydocs = {ep.name: ep.load() for ep in entry_points(group="jupyter_ydoc")}


@pytest.fixture
def rtc_document_save_delay():
    return 0.5


async def test_dirty(
    rtc_create_file,
    rtc_connect_doc_client,
    rtc_document_save_delay,
):
    file_format = "text"
    file_type = "file"
    file_path = "dummy.txt"
    await rtc_create_file(file_path)
    jupyter_ydoc = jupyter_ydocs[file_type]()

    async with await rtc_connect_doc_client(file_format, file_type, file_path) as ws:
        async with WebsocketProvider(jupyter_ydoc.ydoc, ws):
            for _ in range(2):
                jupyter_ydoc.dirty = True
                await sleep(rtc_document_save_delay * 1.5)
                assert not jupyter_ydoc.dirty
