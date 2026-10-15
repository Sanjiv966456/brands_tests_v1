"""Responsive checks for the observed Brands page."""
import allure
import pytest

from pages.brands_page import BrandsPage
from utils.helpers import TEST_DATA


@pytest.mark.responsive
@pytest.mark.regression
@allure.feature("Brands")
@allure.story("Responsive layout")
@allure.title("Brands listing fits viewport: {size[name]}")
@pytest.mark.parametrize("size", TEST_DATA["viewports"], ids=[v["name"] for v in TEST_DATA["viewports"]])
def test_brands_page_has_no_horizontal_overflow(page, base_url, size):
    """Given a supported viewport, when the listing is opened, then its document does not overflow horizontally."""
    page.set_viewport_size({"width": size["width"], "height": size["height"]})
    BrandsPage(page, base_url).open_listing()
    dimensions = page.evaluate(
        "() => ({width: document.documentElement.clientWidth, scrollWidth: document.documentElement.scrollWidth})"
    )
    assert dimensions["scrollWidth"] <= dimensions["width"], dimensions
