"""Check whether Volvo appears in the homepage's observed navigation dropdown."""
from urllib.parse import urljoin

import allure
import pytest
from playwright.sync_api import expect


@pytest.mark.regression
@allure.feature("Homepage navigation")
@allure.story("Our Services dropdown")
@allure.title("Report whether Volvo is visible in the Our Services dropdown")
def test_volvo_visibility_in_dropdown(page, base_url):
    """Given the homepage, when the Our Services menu is opened, then report whether it contains a visible Volvo link."""
    home_url = urljoin(base_url, "/")
    response = page.goto(home_url, wait_until="domcontentloaded")
    assert response is not None and response.status == 200

    services_menu = page.locator("nav .service_menu")
    expect(services_menu).to_be_visible()
    dropdown = services_menu.locator(".megamenu")
    services_menu.locator("a").first.click()
    expect(dropdown).to_be_visible()

    volvo_link = dropdown.get_by_role("link", name="Volvo", exact=True)
    is_visible = volvo_link.count() > 0 and volvo_link.is_visible()
    print(f"Volvo visible in the Our Services dropdown: {is_visible}")

    # The live menu inspected during discovery has no Volvo entry.
    assert is_visible is False, "Volvo unexpectedly appeared in the Our Services dropdown."
    page.screenshot(path="volvo_dropdown_visibility.png", full_page=True)
