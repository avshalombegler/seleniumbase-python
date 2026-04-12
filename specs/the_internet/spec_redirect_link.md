# Redirector Test Plan

<!--
  SPEC FORMAT v1.0 — SeleniumBase Python Project
  Generator: sb-generator
  Do not edit manually — update the spec and re-run the generator.
-->

---

## Feature Metadata

| Field | Value |
| --- | --- |
| **Feature name** | Redirector |
| **URL** | `/redirector` |
| **Full URL** | `https://the-internet.herokuapp.com/redirector` |
| **Feature directory** | `redirect_link` |
| **Page object class** | `RedirectLinkPage` |
| **Locators class** | `RedirectLinkLocators` |
| **Test class** | `TestRedirectLink` |
| **Test file** | `tests/the_internet/ui_test_suite/test_redirect_link.py` |
| **Page object file** | `src/pages/features/redirect_link/redirect_link_page.py` |
| **Locators file** | `src/pages/features/redirect_link/locators.py` |
| **MainPage nav method** | `click_redirect_link_link` |
| **Allure sub_suite** | `Redirector` |

---

## Page Elements

| Locator name | Strategy | Selector | Notes |
| --- | --- | --- | --- |
| `PAGE_LOADED_INDICATOR` | `By.CSS_SELECTOR` | `".example h3"` | Confirms page is loaded; h3 heading reads "Redirection" |
| `REDIRECT_HERE_LINK` | `By.CSS_SELECTOR` | `"a[href='/redirect']"` | "here" anchor link; clicking it triggers a server-side redirect to `/status_codes` |

---

## Page Object Methods

| Method | Signature | Returns | Notes |
| --- | --- | --- | --- |
| `__init__` | `(self, driver: BaseCase)` | `None` | `super().__init__(driver)` then `wait_for_page_to_load(PAGE_LOADED_INDICATOR)` |
| `get_heading_text` | `(self)` | `str` | Returns text of `PAGE_LOADED_INDICATOR` via `get_dynamic_element_text` |
| `click_redirect_here` | `(self)` | `None` | Clicks `REDIRECT_HERE_LINK` via `click_element`; the server issues a redirect chain `/redirect` → `/status_codes`; caller asserts the final URL |

---

## Test Scenarios

Each scenario maps to exactly one test method in `TestRedirectLink`.

---

### Scenario 1: Clicking "here" link redirects to the status codes page

**Method:** `test_redirect_link_navigates_to_status_codes`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `CRITICAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/redirector` via `MainPage.click_redirect_link_link()`
   - `expect:` Page loads — verified by `PAGE_LOADED_INDICATOR`

2. Click the "here" redirect link via `page.click_redirect_here()`
   - `locator:` `REDIRECT_HERE_LINK`
   - `expect:` Browser follows the redirect chain and the current URL ends with `/status_codes`

**Assertions:**

```python
self.assert_true(
    self.get_current_url().endswith("/status_codes"),
    "Expected URL to end with /status_codes after clicking the redirect link"
)
```

---

### Scenario 2: Redirector page loads with correct heading

**Method:** `test_redirector_page_heading`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/redirector` via `MainPage.click_redirect_link_link()`
   - `expect:` Page loads — verified by `PAGE_LOADED_INDICATOR`

2. Retrieve heading text via `page.get_heading_text()`
   - `locator:` `PAGE_LOADED_INDICATOR`
   - `expect:` Heading text equals the expected value "Redirection"

**Assertions:**

```python
heading = page.get_heading_text()
self.assert_equal(heading, EXPECTED_HEADING, f"Expected heading '{EXPECTED_HEADING}', got '{heading}'")
```

---

## Out of Scope

| Excluded scenario | Reason |
| --- | --- |
| Asserting the intermediate `/redirect` URL during the redirect chain | The server-side 301 redirect resolves before the browser can assert an intermediate URL; there is no observable intermediate state in Selenium |
| Asserting HTTP status codes (301, 200) | Network-level assertions are out of scope |
| Asserting content of the `/status_codes` landing page | The status codes page is a separate feature; its content is not the responsibility of this test |
| Performance of the redirect chain (latency) | Performance testing is out of scope |
| Back-navigation from `/status_codes` to `/redirector` | No documented expected behavior for this navigation; no observable assertion target beyond URL |
| Visual regression of the "here" link styling | Visual regression testing is out of scope |

---

## Test Data

```python
EXPECTED_HEADING = "Redirection"
```

These constants should be defined at module level in the test file (not in the page object or
locators file) so they are visible alongside the assertions that use them.

---

## Generator Notes

- **Nav method name:** The `feature_dir` was explicitly set to `redirect_link` by the user. Applying the formula `click_<feature_dir>_link` produces `click_redirect_link_link` (double "link"). This is intentional per the user's override — implement the method with this exact name.

- **MainPage registration:** Add `REDIRECT_LINK_LINK: Locator = {"selector": "Redirector", "by": By.LINK_TEXT}` to `MainPageLocators` (alphabetical order — "Redirector" falls between `NOTIFICATION_MESSAGES_LINK` and the next entry alphabetically). The exact homepage link text is "Redirector".

- **Locator for `REDIRECT_HERE_LINK`:** The `By.CSS_SELECTOR` selector `a[href='/redirect']` is used because raw HTML source was not fetched during planning. If the anchor carries `id="redirect"`, the generator may upgrade to `By.ID` with selector `"redirect"` after verifying the id attribute in the raw HTML. Until confirmed, use `By.CSS_SELECTOR`.

- **`click_redirect_here` return type:** The method returns `None` because after the click the page transitions to `/status_codes` — a different feature's page. There is no `StatusCodesPage` object in scope for this feature, so the URL assertion is performed inline in the test body using `self.get_current_url()`.

- **Single interactive element:** This page has exactly one interactive element (the "here" link). There are no forms, inputs, error states, or dynamic content to test beyond the redirect behavior and page heading.

- **`allure_sub_suite` note:** The `allure_sub_suite` is set to `"Redirector"` (the human-readable page heading), not `"redirect_link"`. The `redirect_link` identifier applies only to code artifacts (class names, file names, directory, nav method) per the user's override.
