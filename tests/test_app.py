# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import annotations

from jupyter_collaboration.stores import SQLiteYStore, TempFileYStore


def test_default_settings(jp_serverapp):
    settings = jp_serverapp.web_app.settings["jupyter_collaboration_config"]

    assert settings["disable_rtc"] is False
    assert settings["file_poll_interval"] == 1
    assert settings["document_cleanup_delay"] == 60
    assert settings["document_save_delay"] == 1
    assert settings["ystore_class"] == SQLiteYStore


def test_settings_should_disable_rtc(jp_configurable_serverapp):
    argv = ["--YDocExtension.disable_rtc=True"]

    app = jp_configurable_serverapp(argv=argv)
    settings = app.web_app.settings["jupyter_collaboration_config"]

    assert settings["disable_rtc"] is True


def test_settings_should_change_file_poll(jp_configurable_serverapp):
    argv = ["--YDocExtension.file_poll_interval=2"]

    app = jp_configurable_serverapp(argv=argv)
    settings = app.web_app.settings["jupyter_collaboration_config"]

    assert settings["file_poll_interval"] == 2


def test_settings_should_change_document_cleanup(jp_configurable_serverapp):
    argv = ["--YDocExtension.document_cleanup_delay=10"]

    app = jp_configurable_serverapp(argv=argv)
    settings = app.web_app.settings["jupyter_collaboration_config"]

    assert settings["document_cleanup_delay"] == 10


def test_settings_should_change_save_delay(jp_configurable_serverapp):
    argv = ["--YDocExtension.document_save_delay=10"]

    app = jp_configurable_serverapp(argv=argv)
    settings = app.web_app.settings["jupyter_collaboration_config"]

    assert settings["document_save_delay"] == 10


def test_settings_should_change_ystore_class(jp_configurable_serverapp):
    argv = ["--YDocExtension.ystore_class=jupyter_collaboration.stores.TempFileYStore"]

    app = jp_configurable_serverapp(argv=argv)
    settings = app.web_app.settings["jupyter_collaboration_config"]

    assert settings["ystore_class"] == TempFileYStore


async def test_get_document_file(rtc_create_file, jp_serverapp):
    path, content = await rtc_create_file("test.txt", "test", store=True)
    collaboration = jp_serverapp.web_app.settings["jupyter_collaboration"]
    document = await collaboration.get_document(path=path, content_type="file", file_format="text")
    assert document.get() == content == "test"
    await collaboration.stop_extension()


async def test_get_document_file_is_a_fork(rtc_create_file, jp_serverapp, rtc_fetch_session):
    path, content = await rtc_create_file("test.txt", "test", store=True)
    collaboration = jp_serverapp.web_app.settings["jupyter_collaboration"]
    document = await collaboration.get_document(path=path, content_type="file", file_format="text")
    document.set("other")
    fresh_copy = await collaboration.get_document(
        path=path, content_type="file", file_format="text"
    )
    assert fresh_copy.get() == "test"
    await collaboration.stop_extension()
