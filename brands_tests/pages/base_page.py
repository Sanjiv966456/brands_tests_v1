"""Common navigation and metadata helpers."""
import allure
from playwright.sync_api import Page, Response


class BasePage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/") + "/"

    @allure.step("Open page: {path}")
    def open(self, path: str = "") -> Response | None:
        return self.page.goto(f"{self.base_url}{path.lstrip('/')}", wait_until="domcontentloaded")

    def title(self) -> str:
        return self.page.title()
