"""Page quality checks applicable to the observed Brands page."""
import allure
import pytest

from utils.helpers import is_http_url


@pytest.mark.regression
@allure.feature("Brands")
@allure.story("Links")
@allure.title("HTTP links on the page do not return 4xx or 5xx")
def test_http_links_are_not_broken(page, base_url):
    """Given HTTP anchors on Brands, when each unique URL is requested, then none responds with an error."""
    page.goto(base_url, wait_until="domcontentloaded")
    urls = page.locator("a[href]").evaluate_all(
        "(els) => [...new Set(els.map(a => a.href).filter(h => h.startsWith('http://') || h.startsWith('https://')))]"
    )
    errors = []
    for url in urls:
        response = page.request.get(url, timeout=20_000)
        if response.status >= 400:
            errors.append(f"{response.status} {url}")
    assert not errors, "Broken HTTP links: " + "; ".join(errors)


@pytest.mark.regression
@allure.feature("Brands")
@allure.story("Browser health")
@allure.title("Brands page has no console errors or failed requests")
def test_no_console_errors_or_failed_requests(page, base_url):
    """Given the Brands listing, when it loads, then the browser reports no console errors or failed requests."""
    console_errors = []
    failed_requests = []
    page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
    page.on("requestfailed", lambda request: failed_requests.append(f"{request.url}: {request.failure}"))
    page.goto(base_url, wait_until="domcontentloaded")
    page.evaluate("() => document.fonts.ready")
    assert not console_errors, console_errors
    assert not failed_requests, failed_requests


@pytest.mark.regression
@allure.feature("Brands")
@allure.story("Performance")
@allure.title("Brands document load and LCP timings are measurable")
def test_load_performance_timings_present(page, base_url):
    """Given the Brands page, when navigation performance is read, then document load and LCP metrics are non-zero."""
    page.goto(base_url, wait_until="load")
    page.evaluate("() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
    metrics = page.evaluate("""() => {
      const nav = performance.getEntriesByType('navigation')[0];
      const lcp = performance.getEntriesByType('largest-contentful-paint').at(-1);
      return {load: nav ? nav.loadEventEnd : 0, lcp: lcp ? lcp.startTime : 0};
    }""")
    assert metrics["load"] > 0, metrics
    assert metrics["lcp"] > 0, metrics
