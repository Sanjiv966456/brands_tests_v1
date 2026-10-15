# Brands UI tests

The live /brands/ page returned HTTP 200 and exposed 15 linked brand logos. Search, filtering, sorting, pagination, load-more, and infinite-scroll controls were not present, so their test modules intentionally contain no tests.

## Install

From the brands_tests directory, run:

    python -m pip install -r requirements.txt
    python -m playwright install

The accessibility test loads axe-core from cdnjs while it runs.
The Allure Python plugin writes results; install the standalone Allure command-line tool separately to run the Allure serve command.

## PyCharm

1. Open brands_tests as a project, or add it as a content root in the existing project.
2. Set the project interpreter to Python 3.11 or newer and install requirements.txt.
3. Under Settings → Tools → Python Integrated Tools, set the default test runner to pytest.
4. Create a Python tests → pytest run configuration. Set the target to tests and the working directory to brands_tests.
5. Add --headed --browser chromium to additional arguments for a visible browser.

Run these commands from brands_tests:

    pytest -m smoke --headed --browser chromium
    pytest -n 4 --alluredir=allure-results
    allure serve allure-results

The pytest-playwright --browser option accepts chromium, firefox, and webkit. Install the matching engines with python -m playwright install.

## Failure artifacts

Each test records a trace and video. On failure, the screenshot, trace, and video are attached to Allure results. The responsive suite is parameterized for 1920×1080, 1366×768, 768×1024, and 390×844.

## Observed issue

The live listing has no meta[name=description] and no link[rel=canonical]. The SEO test asserts these required elements and will fail until the site supplies them.
