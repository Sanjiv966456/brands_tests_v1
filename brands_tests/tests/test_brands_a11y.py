"""Accessibility checks for the observed brand listing."""
import allure
import pytest
from playwright.sync_api import expect

from pages.brands_page import BrandsPage


@pytest.mark.a11y
@pytest.mark.regression
@allure.feature("Brands")
@allure.story("Accessibility")
@allure.title("Brands page has no serious axe-core violations")
def test_brands_axe_scan(page, base_url):
    """Given the Brands page, when axe-core scans it, then there are no serious or critical violations."""
    BrandsPage(page, base_url).open_listing()
    page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js")
    result = page.evaluate(
        "async () => { const r = await axe.run(document); "
        "return r.violations.filter(v => ['critical', 'serious'].includes(v.impact)) "
        ".map(v => ({id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.length})); }"
    )
    assert result == [], f"axe-core violations: {result}"


@pytest.mark.a11y
@allure.feature("Brands")
@allure.story("Keyboard access")
@allure.title("A brand link can receive keyboard focus")
def test_brand_link_keyboard_focus(page, base_url):
    """Given the listing, when keyboard navigation reaches the Audi card, then it is focused and visible."""
    BrandsPage(page, base_url).open_listing()
    audi_link = page.locator("a.brands-div").filter(has=page.get_by_role("img", name="Audi", exact=True))
    audi_href = audi_link.get_attribute("href")
    found = False
    for _ in range(80):
        page.keyboard.press("Tab")
        if page.locator(":focus").evaluate("(el) => el.getAttribute('href')") == audi_href:
            found = True
            break
    assert found, "Keyboard tab order did not reach Audi brand link"
    expect(audi_link).to_be_visible()
    assert page.locator(":focus").evaluate("(el) => el.matches(':focus-visible')")
