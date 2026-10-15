"""Core page and observed brand listing behaviors."""
import allure
import pytest
from playwright.sync_api import expect

from pages.brand_detail_page import BrandDetailPage
from pages.brands_page import BrandsPage
from utils.helpers import TEST_DATA


@pytest.mark.smoke
@allure.feature("Brands")
@allure.story("Listing")
@allure.title("Brands page loads and displays its brand listing")
def test_brands_page_loads(page, base_url):
    """Given the Brands route, when it loads, then it responds successfully and exposes the title and listing."""
    brands = BrandsPage(page, base_url)
    response = brands.open_listing()
    assert response is not None and response.status == 200
    expect(page).to_have_title("Brands - Alexandria Automotive Services")
    expect(brands.heading).to_be_visible()
    brands.expect_brand_count(TEST_DATA["brand_count"])


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Brands")
@allure.story("Brand cards")
@allure.title("Every brand card has a named logo and a same-site detail link")
def test_every_brand_card_has_logo_name_and_valid_link(page, base_url):
    """Given the listing, when each observed card is inspected, then its logo has a name and its link uses the brand route."""
    brands = BrandsPage(page, base_url)
    brands.open_listing()
    brands.expect_brand_count(TEST_DATA["brand_count"])
    for brand in TEST_DATA["brands"]:
        card = brands.card(brand["name"])
        expect(card).to_have_count(1)
        expect(card.get_by_role("img", name=brand["name"], exact=True)).to_be_visible()
        expect(card).to_have_attribute("href", f"{base_url}{brand['slug']}/")


@pytest.mark.smoke
@allure.feature("Brands")
@allure.story("Brand detail navigation")
@allure.title("Opening a brand and using browser Back restores the listing")
def test_brand_detail_and_back_restore_listing(page, base_url):
    """Given the brand listing, when Audi is opened and browser Back is used, then its route is correct and all cards return."""
    brands = BrandsPage(page, base_url)
    brands.open_listing()
    brands.open_brand("Audi")
    detail = BrandDetailPage(page, base_url)
    detail.expect_brand_route("audi-service")
    page.go_back(wait_until="domcontentloaded")
    expect(page).to_have_url(base_url)
    brands.expect_brand_count(TEST_DATA["brand_count"])


@pytest.mark.regression
@allure.feature("Brands")
@allure.story("Page metadata")
@allure.title("Brands page has one H1, meta description, and canonical URL")
def test_brands_seo_metadata(page, base_url):
    """Given the Brands page, when metadata is read, then one H1, a description, and a canonical link are present."""
    page.goto(base_url, wait_until="domcontentloaded")
    expect(page.locator("h1")).to_have_count(1)
    expect(page.locator("meta[name='description']")).to_have_count(1)
    expect(page.locator("link[rel='canonical']")).to_have_attribute("href", base_url)


@pytest.mark.regression
@allure.feature("Brands")
@allure.story("Open Graph")
@allure.title("Brands page exposes its observed Open Graph title and URL")
def test_brands_open_graph_metadata(page, base_url):
    """Given the Brands page, when Open Graph metadata is read, then the observed title and listing URL are present."""
    page.goto(base_url, wait_until="domcontentloaded")
    expect(page.locator("meta[property='og:title']")).to_have_attribute(
        "content", "Brands - Alexandria Automotive Services"
    )
    expect(page.locator("meta[property='og:url']")).to_have_attribute("content", base_url)


@pytest.mark.regression
@allure.feature("Brands")
@allure.story("Images and accessibility text")
@allure.title("Brand logos load and provide alternative text")
def test_brand_logo_images_are_loaded_and_named(page, base_url):
    """Given the brand cards, when their images finish loading, then no card logo is broken or unnamed."""
    brands = BrandsPage(page, base_url)
    brands.open_listing()
    for brand in TEST_DATA["brands"]:
        logo = brands.card(brand["name"]).get_by_role("img", name=brand["name"], exact=True)
        logo.scroll_into_view_if_needed()
        expect(logo).to_be_visible()
        expect(logo).to_have_attribute("alt", brand["name"])
        logo.evaluate("(img) => img.decode()")
        assert logo.evaluate("(img) => img.complete && img.naturalWidth > 0")


@pytest.mark.regression
@pytest.mark.brand_links          # <-- new, unique to this test
@allure.feature("Brands")
@allure.story("Links")
@allure.title("Brand card links resolve without a client or server error")
def test_brand_links_return_success(page, base_url):
    """Given all brand cards, when their destinations are requested, then every detail route returns below HTTP 400."""
    brands = BrandsPage(page, base_url)
    brands.open_listing()
    for brand in TEST_DATA["brands"]:
        url = f"{base_url}{brand['slug']}/"
        response = page.request.get(url)
        assert response.status < 400, f"{url} returned {response.status}"
        page.screenshot(path=f"brands_tests/screenshots/{brand['slug']}.png", full_page=True)
