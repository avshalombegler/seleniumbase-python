# Shifting Content Test Plan

<!--
  SPEC FORMAT v1.0 — SeleniumBase Python Project
  Generator: sb-generator
  Do not edit manually — update the spec and re-run the generator.
-->

---

## Feature Metadata

| Field | Value |
| --- | --- |
| **Feature name** | Shifting Content |
| **URL** | `/shifting_content` |
| **Full URL** | `https://the-internet.herokuapp.com/shifting_content` |
| **Feature directory** | `shifting_content` |
| **Page object class** | `ShiftingContentPage` |
| **Locators class** | `ShiftingContentLocators` |
| **Test class** | `TestShiftingContent` |
| **Test file** | `tests/the_internet/ui_test_suite/test_shifting_content.py` |
| **Page object file** | `src/pages/features/shifting_content/shifting_content_page.py` |
| **Locators file** | `src/pages/features/shifting_content/locators.py` |
| **MainPage nav method** | `click_shifting_content_link` |
| **Allure sub_suite** | `Shifting Content` |

---

## Page Elements

| Locator name | Strategy | Selector | Notes |
| --- | --- | --- | --- |
| `PAGE_LOADED_INDICATOR` | `By.CSS_SELECTOR` | `".example h3"` | Confirms index page is loaded; h3 heading reads "Shifting Content" — see Generator Notes for verification requirement |
| `EXAMPLE_1_LINK` | `By.CSS_SELECTOR` | `"a[href='/shifting_content/menu']"` | "Example 1: Menu Element" link on the index page |
| `EXAMPLE_2_LINK` | `By.CSS_SELECTOR` | `"a[href='/shifting_content/image']"` | "Example 2: An Image" link on the index page |
| `EXAMPLE_3_LINK` | `By.CSS_SELECTOR` | `"a[href='/shifting_content/list']"` | "Example 3: A List" link on the index page |
| `MENU_CONTAINER` | `By.CSS_SELECTOR` | `"#menu"` | Nav menu container on the `/shifting_content/menu` sub-page — see Generator Notes for id verification |
| `IMAGE_ELEMENT` | `By.CSS_SELECTOR` | `".example img"` | Image element on the `/shifting_content/image` sub-page |
| `LIST_CONTAINER` | `By.CSS_SELECTOR` | `".example ul"` | Unordered list on the `/shifting_content/list` sub-page |

---

## Page Object Methods

The feature has one index page (`ShiftingContentPage`) that links to three sub-pages. Each sub-page is navigated via direct link click from the index page. Given the sub-pages are minimal (no interactive actions beyond navigation), all sub-page interactions are handled by returning to the same page object class after navigation, with dedicated check methods.

| Method | Signature | Returns | Notes |
| --- | --- | --- | --- |
| `__init__` | `(self, driver: BaseCase)` | `None` | `super().__init__(driver)` then `wait_for_page_to_load(PAGE_LOADED_INDICATOR)` |
| `get_heading_text` | `(self)` | `str` | Returns text of `PAGE_LOADED_INDICATOR` via `get_dynamic_element_text` |
| `click_menu_example_link` | `(self)` | `None` | Clicks `EXAMPLE_1_LINK` via `click_element`; navigates to `/shifting_content/menu`; caller asserts the URL |
| `click_image_example_link` | `(self)` | `None` | Clicks `EXAMPLE_2_LINK` via `click_element`; navigates to `/shifting_content/image`; caller asserts the URL |
| `click_list_example_link` | `(self)` | `None` | Clicks `EXAMPLE_3_LINK` via `click_element`; navigates to `/shifting_content/list`; caller asserts the URL |
| `is_menu_container_visible` | `(self)` | `bool` | Returns `is_element_visible(MENU_CONTAINER)` — used after navigating to the menu sub-page |
| `is_image_visible` | `(self)` | `bool` | Returns `is_element_visible(IMAGE_ELEMENT)` — used after navigating to the image sub-page |
| `is_list_visible` | `(self)` | `bool` | Returns `is_element_visible(LIST_CONTAINER)` — used after navigating to the list sub-page |

---

## Test Scenarios

Each scenario maps to exactly one test method in `TestShiftingContent`.

---

### Scenario 1: Shifting Content index page loads with correct heading

**Method:** `test_shifting_content_index_page_loads`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `CRITICAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/shifting_content` via `MainPage.click_shifting_content_link()`
   - `expect:` Page loads — verified by `PAGE_LOADED_INDICATOR`

2. Retrieve heading text via `page.get_heading_text()`
   - `locator:` `PAGE_LOADED_INDICATOR`
   - `expect:` Heading text equals "Shifting Content"

**Assertions:**

```python
heading = page.get_heading_text()
self.assert_equal(heading, EXPECTED_HEADING, f"Expected heading '{EXPECTED_HEADING}', got '{heading}'")
```

---

### Scenario 2: Clicking Example 1 navigates to the menu sub-page

**Method:** `test_menu_example_link_navigates_correctly`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/shifting_content` via `MainPage.click_shifting_content_link()`
   - `expect:` Index page loads — verified by `PAGE_LOADED_INDICATOR`

2. Click the menu example link via `page.click_menu_example_link()`
   - `locator:` `EXAMPLE_1_LINK`
   - `expect:` Browser navigates to `/shifting_content/menu` and the menu container is present in the DOM

**Assertions:**

```python
self.assert_true(
    self.get_current_url().endswith("/shifting_content/menu"),
    "Expected URL to end with /shifting_content/menu"
)
self.assert_true(
    page.is_menu_container_visible(),
    "Expected the menu container to be visible on the menu sub-page"
)
```

---

### Scenario 3: Clicking Example 2 navigates to the image sub-page

**Method:** `test_image_example_link_navigates_correctly`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/shifting_content` via `MainPage.click_shifting_content_link()`
   - `expect:` Index page loads — verified by `PAGE_LOADED_INDICATOR`

2. Click the image example link via `page.click_image_example_link()`
   - `locator:` `EXAMPLE_2_LINK`
   - `expect:` Browser navigates to `/shifting_content/image` and an image element is visible

**Assertions:**

```python
self.assert_true(
    self.get_current_url().endswith("/shifting_content/image"),
    "Expected URL to end with /shifting_content/image"
)
self.assert_true(
    page.is_image_visible(),
    "Expected an image element to be visible on the image sub-page"
)
```

---

### Scenario 4: Clicking Example 3 navigates to the list sub-page

**Method:** `test_list_example_link_navigates_correctly`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/shifting_content` via `MainPage.click_shifting_content_link()`
   - `expect:` Index page loads — verified by `PAGE_LOADED_INDICATOR`

2. Click the list example link via `page.click_list_example_link()`
   - `locator:` `EXAMPLE_3_LINK`
   - `expect:` Browser navigates to `/shifting_content/list` and a list element is visible

**Assertions:**

```python
self.assert_true(
    self.get_current_url().endswith("/shifting_content/list"),
    "Expected URL to end with /shifting_content/list"
)
self.assert_true(
    page.is_list_visible(),
    "Expected the list container to be visible on the list sub-page"
)
```

---

## Out of Scope

| Excluded scenario | Reason |
| --- | --- |
| Asserting the exact number of menu items on the menu sub-page | The menu randomly includes or excludes a "Home" link; the item count is non-deterministic and cannot be asserted reliably |
| Asserting the horizontal position of the image on the image sub-page | The image position shifts randomly on each page load; positional assertions are inherently flaky against this page |
| Asserting the exact number of list items on the list sub-page | The list content changes randomly; item count is non-deterministic |
| Asserting text content of individual list items | List item text is server-randomized; exact text assertions cannot be made |
| Asserting the presence or absence of the "Home" menu item | The "Home" link appears randomly; any assertion on its presence would be non-deterministic |
| Performance / layout shift measurement (CLS metrics) | Performance and visual regression testing is out of scope |
| Accessibility auditing of shifting elements | Accessibility auditing is out of scope |
| Network-level inspection of random server-side selection | Network-level assertions are out of scope |

---

## Test Data

```python
EXPECTED_HEADING = "Shifting Content"
```

These constants should be defined at module level in the test file (not in the page object or
locators file) so they are visible alongside the assertions that use them.

---

## Generator Notes

- **PAGE_LOADED_INDICATOR verification required:** The selector `".example h3"` is the standard the-internet container pattern but was not confirmed via a live Playwright snapshot during planning (browser tools were unavailable). The generator MUST verify this selector against the live page source before implementing. If the heading is instead an `h2` or uses a different container class, update accordingly. Alternative candidate: `"h3"` (bare tag as last resort only).

- **EXAMPLE_1_LINK, EXAMPLE_2_LINK, EXAMPLE_3_LINK href values:** The href attribute values `/shifting_content/menu`, `/shifting_content/image`, and `/shifting_content/list` were not verified verbatim from live HTML. The generator MUST confirm these href values from the raw page source before implementing the CSS attribute selectors. If the href values differ (e.g., no leading slash, query params), update accordingly.

- **MENU_CONTAINER id verification:** The selector `"#menu"` for the menu container on the `/shifting_content/menu` sub-page was not confirmed from live HTML. The generator must fetch the sub-page source and confirm the `id="menu"` attribute exists on the nav container. If no id exists, fall back to `By.CSS_SELECTOR` with `.example nav` or `.example ul` and update the locator strategy and selector.

- **Sub-page page object pattern:** All three sub-pages (`/menu`, `/image`, `/list`) are handled by the same `ShiftingContentPage` class rather than separate page objects. This is appropriate because the sub-pages have no interactive elements beyond their structural content — there are no forms, buttons, or inputs. The page object methods `click_*_example_link` navigate away from the index page; the same `page` instance is reused to call `is_*_visible()` after navigation. The `wait_for_page_to_load(PAGE_LOADED_INDICATOR)` in `__init__` only runs when instantiated at the index page — after sub-page navigation, the `page` object does not re-instantiate, so no wait is re-executed. The generator should NOT create a new page object instance after calling `click_*_example_link()`.

- **`is_element_visible` timeout:** Use `timeout=0` in all three `is_*_visible()` methods for fast non-waiting checks — the sub-pages load the elements immediately on page load. If elements take time to appear, increase to `settings.SHORT_TIMEOUT`.

- **MainPage registration:** Add `SHIFTING_CONTENT_LINK: Locator = {"selector": "Shifting Content", "by": By.LINK_TEXT}` to `MainPageLocators` in alphabetical order. "Shifting Content" falls after `SHADOW_DOM_LINK` ("Shadow DOM") alphabetically. Confirm the exact homepage link text from the live page — it is expected to be "Shifting Content".

- **No `@parameterized.expand`:** The three sub-page navigation scenarios (Scenarios 2, 3, 4) have different locators, URL segments, and visibility check methods — they cannot be collapsed into a single parameterized test without losing the per-locator specificity. Keep them as separate test methods.

- **`EXPECTED_HEADING` value:** The value `"Shifting Content"` was inferred from the URL path and feature name. The generator must confirm the exact text of the h3 element on the live page before finalizing this constant. If the heading differs (e.g., "Shifting Content Examples"), update `EXPECTED_HEADING` accordingly.
