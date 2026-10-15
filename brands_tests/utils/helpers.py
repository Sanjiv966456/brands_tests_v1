"""Shared data and response helpers for the Brands suite."""
import json
from pathlib import Path
from urllib.parse import urljoin


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "test_data.json"
with DATA_PATH.open(encoding="utf-8") as data_file:
    TEST_DATA = json.load(data_file)


def absolute_url(base_url: str, href: str) -> str:
    """Resolve a page link against the site base URL."""
    return urljoin(base_url, href)


def is_http_url(url: str) -> bool:
    return url.startswith(("http://", "https://"))
