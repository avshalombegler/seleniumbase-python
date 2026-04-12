# Large and Deep DOM Test Plan

<!--
  SPEC FORMAT v1.0 — SeleniumBase Python Project
  Generator: sb-generator
  Do not edit manually — update the spec and re-run the generator.
-->

---

## Feature Metadata

| Field | Value |
| --- | --- |
| **Feature name** | Large and Deep DOM |
| **URL** | `/large` |
| **Full URL** | `https://the-internet.herokuapp.com/large` |
| **Feature directory** | `large_and_deep_dom` |
| **Page object class** | `LargeAndDeepDomPage` |
| **Locators class** | `LargeAndDeepDomLocators` |
| **Test class** | `TestLargeAndDeepDom` |
| **Test file** | `tests/the_internet/ui_test_suite/test_large_and_deep_dom.py` |
| **Page object file** | `src/pages/features/large_and_deep_dom/large_and_deep_dom_page.py` |
| **Locators file** | `src/pages/features/large_and_deep_dom/locators.py` |
| **MainPage nav method** | `click_large_and_deep_dom_link` |
| **Allure sub_suite** | `Large and Deep DOM` |

---

## Page Elements

| Locator name | Strategy | Selector | Notes |
| --- | --- | --- | --- |
| `PAGE_LOADED_INDICATOR` | `By.ID` | `"large-table"` | Confirms 50×50 DOM table is present and page is loaded |
| `TABLE` | `By.ID` | `"large-table"` | The large 50×50 table element |
| `FIRST_ROW` | `By.ID` | `"row-1"` | First `<tr>` — id pattern is `row-N` |
| `LAST_ROW` | `By.ID` | `"row-50"` | Last `<tr>` — confirms all 50 rows rendered |
| `FIRST_CELL` | `By.ID` | `"c1-1"` | Cell at row 1, column 1 — contains a sibling link |
| `LAST_CELL` | `By.ID` | `"c50-50"` | Cell at row 50, column 50 — confirms full depth of DOM |
| `SIBLING_LINK` | `By.CSS_SELECTOR` | `"#c1-1 a"` | The only anchor element in the table, found in cell c1-1 |

---

## Page Object Methods

| Method | Signature | Returns | Notes |
| --- | --- | --- | --- |
| `__init__` | `(self, driver: BaseCase)` | `None` | `super().__init__(driver)` then `wait_for_page_to_load(PAGE_LOADED_INDICATOR)` |
| `get_table_row_count` | `(self)` | `int` | Returns `get_number_of_elements({"selector": "table#large-table tr", "by": By.CSS_SELECTOR})` |
| `get_table_col_count` | `(self)` | `int` | Returns `get_number_of_elements({"selector": "table#large-table tr:first-child td", "by": By.CSS_SELECTOR})` |
| `get_cell_text` | `(self, row: int, col: int)` | `str` | Uses `format_locator` with `By.ID` and selector `f"c{row}-{col}"`, then `get_dynamic_element_text` |
| `is_last_cell_present` | `(self)` | `bool` | Returns `is_element_visible(LAST_CELL)` |
| `click_sibling_link` | `(self)` | `None` | `click_element(SIBLING_LINK)` — clicks the anchor in cell c1-1 |
| `get_sibling_link_text` | `(self)` | `str` | Returns `get_dynamic_element_text(SIBLING_LINK)` |

---

## Test Scenarios

Each scenario maps to exactly one test method in `TestLargeAndDeepDom`.

---

### Scenario 1: Page Loads with Large DOM Table Present

**Method:** `test_large_dom_table_is_present`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `CRITICAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/large` via `MainPage.click_large_and_deep_dom_link()`
   - `expect:` Page loads and the table with id `large-table` is visible

**Assertions:**

```python
self.assert_true(self.get_current_url().endswith("/large"), "URL should end with /large")
self.assert_element_visible("#large-table")
```

---

### Scenario 2: Table Has 50 Rows

**Method:** `test_table_has_50_rows`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/large` via `MainPage.click_large_and_deep_dom_link()`
   - `expect:` Page loads with `large-table` present

2. Count table rows via `page.get_table_row_count()`
   - `locator:` `TABLE`
   - `expect:` Exactly 50 rows are present

**Assertions:**

```python
self.assert_equal(page.get_table_row_count(), EXPECTED_ROW_COUNT, "Table should have 50 rows")
```

---

### Scenario 3: Table Has 50 Columns

**Method:** `test_table_has_50_columns`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/large` via `MainPage.click_large_and_deep_dom_link()`
   - `expect:` Page loads with `large-table` present

2. Count first-row columns via `page.get_table_col_count()`
   - `locator:` `TABLE`
   - `expect:` Exactly 50 columns are present in the first row

**Assertions:**

```python
self.assert_equal(page.get_table_col_count(), EXPECTED_COL_COUNT, "Table should have 50 columns")
```

---

### Scenario 4: Last Cell Is Present (Deep DOM Renders Fully)

**Method:** `test_last_cell_is_present`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/large` via `MainPage.click_large_and_deep_dom_link()`
   - `expect:` Page loads with `large-table` present

2. Check last cell presence via `page.is_last_cell_present()`
   - `locator:` `LAST_CELL`
   - `expect:` Cell with id `c50-50` exists in the DOM and is visible

**Assertions:**

```python
self.assert_true(page.is_last_cell_present(), "Cell c50-50 should be present — deep DOM rendered fully")
```

---

### Scenario 5: Sibling Link in Cell c1-1 Is Present

**Method:** `test_sibling_link_is_present`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/large` via `MainPage.click_large_and_deep_dom_link()`
   - `expect:` Page loads with `large-table` present

2. Retrieve sibling link text via `page.get_sibling_link_text()`
   - `locator:` `SIBLING_LINK`
   - `expect:` An anchor element with text "Sibling" is present in cell c1-1

**Assertions:**

```python
self.assert_in(SIBLING_LINK_TEXT, page.get_sibling_link_text(), "Cell c1-1 should contain a sibling link with expected text")
```

---

### Scenario 6: First Row and First Cell Are Accessible by ID

**Method:** `test_first_row_and_cell_accessible_by_id`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `MINOR`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/large` via `MainPage.click_large_and_deep_dom_link()`
   - `expect:` Page loads

2. Check first row visibility inline via `self.assert_element_visible`
   - `locator:` `FIRST_ROW`
   - `expect:` Element with id `row-1` is visible

3. Check first cell visibility inline via `self.assert_element_visible`
   - `locator:` `FIRST_CELL`
   - `expect:` Element with id `c1-1` is visible

**Assertions:**

```python
self.assert_element_visible("#row-1")
self.assert_element_visible("#c1-1")
```

---

## Out of Scope

| Excluded scenario | Reason |
| --- | --- |
| Page load performance timing (milliseconds) | Performance measurement is outside the framework's assertion scope — requires dedicated tooling |
| Visual regression of table layout | Visual regression testing is out of scope for this framework |
| All 2,500 individual cell values | Combinatorially impractical and not meaningful for functional verification |
| Browser memory/CPU metrics during render | Requires browser internals access beyond SeleniumBase API |
| Scrolling behaviour and lazy loading | No lazy loading observed on this page; scroll-triggered behavior is not testable without explicit `time.sleep()` |
| Accessibility audit of 2,500 cells | Accessibility auditing is out of scope for this framework |
| Cell content for c2-1 through c50-50 | Cells contain numeric auto-generated values with no documented expected values |

---

## Test Data

```python
EXPECTED_ROW_COUNT = 50
EXPECTED_COL_COUNT = 50
SIBLING_LINK_TEXT = "Sibling"
```

These constants should be defined at module level in the test file (not in the page object or
locators file) so they are visible alongside the assertions that use them.

---

## Generator Notes

- The homepage link text for this page is "Large & Deep DOM" (with ampersand). The `MainPage` nav method should use `click_large_and_deep_dom_link` and the link locator should match the exact anchor text "Large & Deep DOM".
- `FIRST_ROW` and `FIRST_CELL` interactions in Scenario 6 happen inline in the test body (not via a page object method) using `self.assert_element_visible`.
- `get_table_row_count` uses `get_number_of_elements` from BasePage with selector `"table#large-table tr"` (CSS).
- `get_table_col_count` uses `get_number_of_elements` with selector `"table#large-table tr:first-child td"` (CSS).
- `get_cell_text` uses `format_locator` with a dynamic `By.ID` selector built as `f"c{row}-{col}"` and then calls `get_dynamic_element_text`. If `format_locator` does not support dynamic ID building, use `get_dynamic_element_text({"selector": f"#c{row}-{col}", "by": By.CSS_SELECTOR})` directly.
- The sibling link `href` is `"#"` — clicking it does not navigate away. Scenario 5 only verifies the link's presence and text, not click behaviour.
- The table renders fully on page load — no JavaScript-driven lazy loading was observed.
- `assert_equal` is used for integer comparisons in Scenarios 2 and 3. If not available on `UiBaseCase`/`BaseCase`, use `self.assert_true(actual == expected, message)` instead.
