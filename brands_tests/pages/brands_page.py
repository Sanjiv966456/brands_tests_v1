"""Page object for the observed Brands listing."""
import allure
from playwright.sync_api import Locator, Page, Response, expect

from .base_page import BasePage


class BrandsPage(BasePage):
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.heading = page.get_by_role("heading", name="Brands", exact=True)
        # Verified in the live DOM: each brand logo is inside an anchor with class brands-div.
        self.cards = page.locator("a.brands-div")

    @allure.step("Open Brands listing")
    def open_listing(self) -> Response | None:
        return self.open()

    @allure.step("Expect {count} brand links")
    def expect_brand_count(self, count: int) -> None:
        expect(self.cards).to_have_count(count)

    def card(self, brand_name: str) -> Locator:
        return self.cards.filter(has=self.page.get_by_role("img", name=brand_name, exact=True))

    @allure.step("Open brand detail: {brand_name}")
    def open_brand(self, brand_name: str) -> None:
        card = self.card(brand_name)
        expect(card).to_have_count(1)
        card.click()
