"""Negative and edge checks that do not rely on absent Brands controls."""
import allure
import pytest
from playwright.sync_api import expect

from pages.brands_page import BrandsPage
from utils.helpers import TEST_DATA


@pytest.mark.negative
@allure.feature("Brands")
@allure.story("URL edge cases")
@allure.title("Unknown query strings do not execute as page markup")
@pytest.mark.parametrize(
    "query",
    [
        "?unexpected=invalid",
        "?term=%3Cscript%3Ealert(1)%3C%2Fscript%3E",
        "?term=%27%20OR%201%3D1--",
        "?term=" + ("x" * 1000),
    ],
    ids=["unknown-param", "encoded-xss", "sql-like", "long-value"],
)
def test_unknown_query_is_inert(page, base_url, query):
    """Given an unrecognized URL query, when Brands loads, then the listing remains and query content is not injected."""
    response = page.goto(base_url + query, wait_until="domcontentloaded")
    assert response is not None and response.status == 200
    expect(page.get_by_role("heading", name="Brands", exact=True)).to_be_visible()
    expect(page.locator("script:visible")).to_have_count(0)


@pytest.mark.negative
@allure.feature("Brands")
@allure.story("URL normalization")
@allure.title("Brands listing works with and without a trailing slash")
@pytest.mark.parametrize("suffix", ["", "/"])
def test_brands_trailing_slash(page, base_url, suffix):
    """Given either observed listing URL form, when it is opened, then the brand cards remain available."""
    response = page.goto(base_url.rstrip("/") + suffix, wait_until="domcontentloaded")
    assert response is not None and response.status == 200
    BrandsPage(page, base_url).expect_brand_count(TEST_DATA["brand_count"])
