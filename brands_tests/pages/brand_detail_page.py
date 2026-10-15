"""Page object for a brand detail route."""
import allure
import re
from playwright.sync_api import Page, expect

from .base_page import BasePage


class BrandDetailPage(BasePage):
    @allure.step("Verify brand detail route for {slug}")
    def expect_brand_route(self, slug: str) -> None:
        expect(self.page).to_have_url(f"{self.base_url}{slug}/")
        expect(self.page).to_have_title(re.compile(r".+ - Alexandria Automotive Services"))
