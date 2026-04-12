# Shadow DOM Test Plan

<!--
  SPEC FORMAT v1.0 — SeleniumBase Python Project
  Generator: sb-generator
  Do not edit manually — update the spec and re-run the generator.
-->

---

## Feature Metadata

| Field | Value |
| --- | --- |
| **Feature name** | Shadow DOM |
| **URL** | `/shadowdom` |
| **Full URL** | `https://the-internet.herokuapp.com/shadowdom` |
| **Feature directory** | `shadow_dom` |
| **Page object class** | `ShadowDomPage` |
| **Locators class** | `ShadowDomLocators` |
| **Test class** | `TestShadowDom` |
| **Test file** | `tests/the_internet/ui_test_suite/test_shadow_dom.py` |
| **Page object file** | `src/pages/features/shadow_dom/shadow_dom_page.py` |
| **Locators file** | `src/pages/features/shadow_dom/locators.py` |
| **MainPage nav method** | `click_shadow_dom_link` |
| **Allure sub_suite** | `Shadow DOM` |

---

## Page Elements

| Locator name | Strategy | Selector | Notes |
| --- | --- | --- | --- |
| `PAGE_LOADED_INDICATOR` | `By.CSS_SELECTOR` | `".example h3"` | Confirms page is loaded; h3 text reads "Shadow DOM" |
| `SHADOW_HOST` | `By.CSS_SELECTOR` | `"my-paragraph"` | The custom Web Component element that hosts the Shadow DOM; standard CSS selectors cannot reach inside its shadow root |

---

## Page Object Methods

| Method | Signature | Returns | Notes |
| --- | --- | --- | --- |
| `__init__` | `(self, driver: BaseCase)` | `None` | `super().__init__(driver)` then `wait_for_page_to_load(PAGE_LOADED_INDICATOR)` |
| `get_heading_text` | `(self)` | `str` | Returns the text of `PAGE_LOADED_INDICATOR` via `get_dynamic_element_text` |
| `get_shadow_slot_text` | `(self)` | `str` | Uses `self.driver.execute_script` with JS to pierce the shadow root of `my-paragraph` and return the text of the slotted `<p>` element; see Generator Notes for the JS snippet |
| `get_shadow_default_text` | `(self)` | `str` | Uses `self.driver.execute_script` with JS to pierce the shadow root and return the inner text of the default (non-slotted) paragraph content; see Generator Notes for implementation guidance |

---

## Test Scenarios

Each scenario maps to exactly one test method in `TestShadowDom`.

---

### Scenario 1: Shadow DOM page loads with correct heading

**Method:** `test_shadow_dom_page_loads`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `CRITICAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/shadowdom` via `MainPage.click_shadow_dom_link()`
   - `expect:` Page loads — verified by `PAGE_LOADED_INDICATOR`

2. Retrieve heading text via `page.get_heading_text()`
   - `locator:` `PAGE_LOADED_INDICATOR`
   - `expect:` Heading text equals "Shadow DOM"

**Assertions:**

```python
heading = page.get_heading_text()
self.assert_equal(heading, EXPECTED_HEADING, f"Expected heading '{EXPECTED_HEADING}', got '{heading}'")
```

---

### Scenario 2: Shadow DOM slotted content is accessible via JavaScript

**Method:** `test_shadow_dom_slot_text`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/shadowdom` via `MainPage.click_shadow_dom_link()`
   - `expect:` Page loads — verified by `PAGE_LOADED_INDICATOR`

2. Retrieve slotted paragraph text via `page.get_shadow_slot_text()`
   - `locator:` `SHADOW_HOST` (accessed via JavaScript inside the page object method)
   - `expect:` The slotted text content is non-empty and matches the expected value

**Assertions:**

```python
slot_text = page.get_shadow_slot_text()
self.assert_equal(slot_text, EXPECTED_SLOT_TEXT, f"Expected slot text '{EXPECTED_SLOT_TEXT}', got '{slot_text}'")
```

---

### Scenario 3: Shadow DOM host element is present in the regular DOM

**Method:** `test_shadow_dom_host_element_visible`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `MINOR`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/shadowdom` via `MainPage.click_shadow_dom_link()`
   - `expect:` Page loads — verified by `PAGE_LOADED_INDICATOR`

2. Check that the shadow host element is visible via `page.is_element_visible(ShadowDomLocators.SHADOW_HOST)`
   - `locator:` `SHADOW_HOST`
   - `expect:` The `<my-paragraph>` custom element is present and visible in the outer DOM

**Assertions:**

```python
self.assert_true(
    page.is_element_visible(ShadowDomLocators.SHADOW_HOST),
    "Expected <my-paragraph> shadow host to be visible in the DOM"
)
```

---

## Out of Scope

| Excluded scenario | Reason |
| --- | --- |
| Asserting shadow DOM content via standard CSS selectors | Shadow DOM content is encapsulated and not reachable by `document.querySelector` from the outer document; no `By.CSS_SELECTOR` locator can pierce the shadow root in SeleniumBase without JavaScript |
| Testing custom element slot assignment behavior | Slot mechanics are a browser-internal concern; no observable test target exists beyond reading the rendered text |
| Testing with `shadowRoot.mode = "closed"` | The-internet's `<my-paragraph>` uses open mode; closed mode is not present on this page |
| Visual regression of shadow DOM styling | Visual regression testing is outside framework scope |
| Performance or rendering timing of custom elements | Performance testing is out of scope |
| Cross-browser shadow DOM compatibility | Browser compatibility testing is out of scope for this framework |
| Asserting the number of `<my-paragraph>` elements on the page | The page contains exactly one; counting elements adds no meaningful coverage for this feature |

---

## Test Data

```python
EXPECTED_HEADING = "Shadow DOM"
EXPECTED_SLOT_TEXT = "Let's have some different text!"
```

These constants should be defined at module level in the test file (not in the page object or
locators file) so they are visible alongside the assertions that use them.

---

## Generator Notes

- **Live page inspection:** The Playwright MCP browser tools were not available in this planning session. Page structure is derived from training knowledge of the stable `the-internet.herokuapp.com/shadowdom` page (unchanged since initial publication). The generator must verify selector accuracy before committing. Specifically: confirm that `".example h3"` matches the heading element and that `"my-paragraph"` is the correct custom element tag name by fetching the raw HTML source via `get_page_source("https://the-internet.herokuapp.com/shadowdom")`.

- **Homepage link text:** The exact `<a>` link text on the homepage for this feature is `"Shadow DOM"`. Add `SHADOW_DOM_LINK: Locator = {"selector": "Shadow DOM", "by": By.LINK_TEXT}` to `MainPageLocators` in alphabetical order (after `REDIRECT_LINK_LINK`, before any entry starting with "T").

- **`get_shadow_slot_text` implementation:** Use `self.driver.execute_script` to pierce the shadow root. A candidate JS snippet:
  ```javascript
  return document.querySelector('my-paragraph').shadowRoot.querySelector('slot').assignedNodes()[0].textContent.trim();
  ```
  If `assignedNodes()` returns empty (no slot assignment found), fall back to the `<p>` inside the light DOM: `document.querySelector('my-paragraph > p').textContent.trim()`. The generator must verify which approach returns the correct text by executing the JS against the live page.

- **`get_shadow_default_text` method:** This method is listed in the Page Object Methods table but is not exercised in a dedicated test scenario, because the exact JS path to the default text node inside the shadow root requires live verification. The generator may omit this method if live inspection confirms the slotted text covers all observable page content. If a second text value is discoverable, add a Scenario 4 using `EXPECTED_DEFAULT_TEXT` (value to be determined at generation time).

- **Scenario 3 locator import in test file:** `page.is_element_visible(ShadowDomLocators.SHADOW_HOST)` requires the test file to import `ShadowDomLocators` from `src.pages.features.shadow_dom.locators`. Add this import to the test file imports section.

- **`EXPECTED_SLOT_TEXT` value:** The value `"Let's have some different text!"` is derived from training knowledge. The generator must confirm this exact string against the live page and update the constant if the text differs.

- **No interactive elements:** This page has no buttons, forms, inputs, or dynamic state changes. All three test scenarios are read-only assertions. No error state, boundary value, or negative flow scenarios are applicable to this page.

- **`feature_dir` note:** The feature directory is `shadow_dom` (spaces-to-underscore convention applied to "Shadow DOM"), which differs from the URL path `/shadowdom` (no underscore). The URL is used only in the spec metadata and `navigate_to` calls — all file/class/method names use `shadow_dom`.
