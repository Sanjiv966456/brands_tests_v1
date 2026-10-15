"""Browser fixtures with per-test failure artifacts."""
from __future__ import annotations

import re
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from utils.helpers import TEST_DATA


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config) -> str:
    configured = pytestconfig.getoption("--base-url", default=None)
    return (configured or TEST_DATA["base_url"]).rstrip("/") + "/"


@pytest.fixture
def viewport() -> dict[str, int]:
    """Default desktop viewport; responsive tests explicitly parametrize their sizes."""
    return {"width": 1366, "height": 768}


@pytest.fixture
def context(
    browser: Browser, viewport: dict[str, int], tmp_path: Path, request: pytest.FixtureRequest
) -> BrowserContext:
    context = browser.new_context(viewport=viewport, record_video_dir=str(tmp_path / "video"))
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    failed = bool(getattr(request.node, "rep_call", None) and request.node.rep_call.failed)
    trace_path = tmp_path / "trace.zip"
    context.tracing.stop(path=str(trace_path))
    context.close()
    if failed and trace_path.exists():
        allure.attach.file(str(trace_path), name="playwright-trace", attachment_type=allure.attachment_type.ZIP)
        for video in (tmp_path / "video").glob("*.webm"):
            allure.attach.file(str(video), name="failure-video", attachment_type="video/webm")


@pytest.fixture
def page(context: BrowserContext, request: pytest.FixtureRequest, tmp_path: Path) -> Page:
    page = context.new_page()
    page.set_default_timeout(10_000)
    yield page
    if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
        image_path = tmp_path / "failure.png"
        page.screenshot(path=str(image_path), full_page=True)
        allure.attach.file(
            str(image_path), name="failure-screenshot", attachment_type=allure.attachment_type.PNG
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "smoke: critical page and listing checks")
    config.addinivalue_line("markers", "regression: broader behavior checks")
    config.addinivalue_line("markers", "a11y: accessibility checks")
    config.addinivalue_line("markers", "responsive: responsive layout checks")
    config.addinivalue_line("markers", "negative: URL and invalid input checks")
