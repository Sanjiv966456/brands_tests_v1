import re
from pathlib import Path

from playwright.sync_api import Page


URL = "https://acsdebtcolldev.wpenginepowered.com/"
TEXT_PATTERN = re.compile(r"(?<![\d.])4\.8(?![\d])")


def _accept_consent_if_present(page: Page) -> None:
    for role in ("button", "link"):
        accept_controls = page.get_by_role(role, name=re.compile(r"\baccept\b", re.I))
        for index in range(accept_controls.count()):
            control = accept_controls.nth(index)
            if control.is_visible():
                control.click()
                return


def _scroll_page_to_load_content(page: Page) -> None:
    # Scroll in viewport-sized steps and repeat if lazy-loaded content extends the page.
    page.evaluate(
        """async () => {
            const frame = () => new Promise(resolve => requestAnimationFrame(resolve));
            const pageHeight = () =>
                Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
            let stablePasses = 0;

            while (stablePasses < 2) {
                const previousHeight = pageHeight();
                const step = Math.max(window.innerHeight, 1);
                for (let y = 0; y < previousHeight; y += step) {
                    window.scrollTo(0, y);
                    await frame();
                }
                window.scrollTo(0, pageHeight());
                await frame();
                stablePasses = pageHeight() === previousHeight ? stablePasses + 1 : 0;
            }

            window.scrollTo(0, 0);
            await frame();
        }"""
    )


def test_4_8_is_present_on_page(page: Page) -> None:
    page.goto(URL, wait_until="networkidle")
    _accept_consent_if_present(page)
    _scroll_page_to_load_content(page)

    matches = page.get_by_text(TEXT_PATTERN)
    match_count = matches.count()
    print(f"Found {match_count} text match(es) for '4.8'.")

    visible_text = page.locator("body").inner_text()
    visible_text_has_match = TEXT_PATTERN.search(visible_text) is not None
    html_has_match = TEXT_PATTERN.search(page.content()) is not None
    if html_has_match and not visible_text_has_match:
        print("'4.8' exists in the raw HTML but not in visible page text.")

    visible_match_count = 0
    for index in range(match_count):
        match = matches.nth(index)
        text = match.inner_text()
        is_visible = match.is_visible()
        parent_text = match.evaluate(
            "(element) => element.parentElement?.innerText ?? ''"
        )
        print(
            f"Match {index + 1}: visible={is_visible}; "
            f"text={text!r}; parent={parent_text!r}"
        )
        if is_visible:
            visible_match_count += 1
        match.evaluate(
            "(element) => { element.style.outline = '3px solid red'; "
            "element.style.outlineOffset = '2px'; }"
        )

    screenshot_path = Path(__file__).resolve().parent / "screenshots" / "4_8_check.png"
    screenshot_path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(screenshot_path), full_page=True)

    assert visible_match_count > 0, "Text '4.8' not found on the page"