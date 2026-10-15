from pathlib import Path

import pytest
from playwright.sync_api import expect


URL = "https://melbournetadev.wpenginepowered.com/"
VIEWPORTS = [
    pytest.param("mobile", 375, 667, id="mobile"),
    pytest.param("tablet", 768, 1024, id="tablet"),
    pytest.param("desktop", 1440, 900, id="desktop"),
]


def load_page(page, width, height):
    page.set_viewport_size({"width": width, "height": height})
    page.goto(URL, wait_until="load")


@pytest.mark.parametrize(("name", "width", "height"), VIEWPORTS)
def test_no_horizontal_scroll(page, name, width, height):
    load_page(page, width, height)

    assert page.evaluate(
        "document.documentElement.scrollWidth <= window.innerWidth"
    )
    screenshot_dir = Path(__file__).parent / "screenshots"
    screenshot_dir.mkdir(exist_ok=True)
    page.screenshot(path=str(screenshot_dir / f"{name}.png"), full_page=True)


@pytest.mark.parametrize(("name", "width", "height"), VIEWPORTS)
def test_header_and_logo_visible(page, name, width, height):
    load_page(page, width, height)

    header = page.get_by_role("banner")
    logo = header.locator('img[alt="Melbournetableandchairhire"]')
    expect(header).to_be_visible()
    expect(logo).to_be_visible()
    for element in (header, logo):
        box = element.bounding_box()
        assert box is not None
        assert box["x"] >= 0
        assert box["x"] + box["width"] <= width


@pytest.mark.parametrize(("name", "width", "height"), VIEWPORTS)
def test_navigation_behavior(page, name, width, height):
    load_page(page, width, height)

    header = page.get_by_role("banner")
    nav = header.get_by_role("navigation")
    hamburger = header.locator("a.togglebtn")
    if width < 1024:
        expect(hamburger).to_be_visible()
        expect(nav).to_be_hidden()
        hamburger.click()
        expect(nav).to_be_visible()
    else:
        expect(hamburger).to_be_hidden()
        for link_name in (
            "Home",
            "Browse Hire",
            "Browse Events",
            "Party Package",
            "About Us",
            "Gallery",
            "Blog",
            "Contact Us",
        ):
            expect(nav.get_by_role("link", name=link_name)).to_be_visible()


@pytest.mark.parametrize(("name", "width", "height"), VIEWPORTS)
def test_hero_and_main_content_visible(page, name, width, height):
    load_page(page, width, height)

    hero = page.locator("section.sec-hmbanner")
    heading = page.get_by_role("heading", level=1)
    expect(hero).to_be_visible()
    expect(heading).to_be_visible()
    box = hero.bounding_box()
    assert box is not None
    assert box["x"] >= 0
    assert box["x"] + box["width"] <= width


@pytest.mark.parametrize(("name", "width", "height"), VIEWPORTS)
def test_images_and_footer_fit(page, name, width, height):
    load_page(page, width, height)

    footer = page.get_by_role("contentinfo")
    page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
    expect(footer).to_be_visible()
    oversized_images = page.locator("img").evaluate_all(
        """images => images.filter(image =>
            image.checkVisibility() &&
            image.getBoundingClientRect().width > window.innerWidth
        ).map(image => image.currentSrc || image.src)"""
    )
    assert not oversized_images
