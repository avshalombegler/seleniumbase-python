# Sortable Data Tables Test Plan

<!--
  SPEC FORMAT v1.0 — SeleniumBase Python Project
  Generator: sb-generator
  Do not edit manually — update the spec and re-run the generator.
-->

---

## Feature Metadata

| Field | Value |
| --- | --- |
| **Feature name** | `Sortable Data Tables` |
| **URL** | `/tables` |
| **Full URL** | `https://the-internet.herokuapp.com/tables` |
| **Feature directory** | `sortable_data_tables` |
| **Page object class** | `SortableDataTablesPage` |
| **Locators class** | `SortableDataTablesLocators` |
| **Test class** | `TestSortableDataTables` |
| **Test file** | `tests/the_internet/ui_test_suite/test_sortable_data_tables.py` |
| **Page object file** | `src/pages/features/sortable_data_tables/sortable_data_tables_page.py` |
| **Locators file** | `src/pages/features/sortable_data_tables/locators.py` |
| **MainPage nav method** | `click_sortable_data_tables_link` |
| **Allure sub_suite** | `Sortable Data Tables` |

---

## Page Elements

| Locator name | Strategy | Selector | Notes |
| --- | --- | --- | --- |
| `PAGE_LOADED_INDICATOR` | `By.CSS_SELECTOR` | `"div.example h3"` | Confirmed present in raw HTML: `<div class="example"><h3>Data Tables</h3>` |
| `TABLE1` | `By.ID` | `"table1"` | First table — no class/id attributes on cells; `id="table1"` confirmed in raw HTML |
| `TABLE2` | `By.ID` | `"table2"` | Second table — cells have class attributes; `id="table2"` confirmed in raw HTML |
| `TABLE1_HEADERS` | `By.CSS_SELECTOR` | `"#table1 thead th"` | All column header cells in table1 |
| `TABLE2_HEADERS` | `By.CSS_SELECTOR` | `"#table2 thead th"` | All column header cells in table2 |
| `TABLE1_ROWS` | `By.CSS_SELECTOR` | `"#table1 tbody tr"` | All data rows in table1 |
| `TABLE2_ROWS` | `By.CSS_SELECTOR` | `"#table2 tbody tr"` | All data rows in table2 |
| `TABLE1_HEADER_LAST_NAME` | `By.CSS_SELECTOR` | `"#table1 thead th:nth-child(1)"` | Last Name header in table1; no class on th elements — structural selector required |
| `TABLE1_HEADER_DUE` | `By.CSS_SELECTOR` | `"#table1 thead th:nth-child(4)"` | Due header in table1; used for sort verification |
| `TABLE2_HEADER_LAST_NAME` | `By.CSS_SELECTOR` | `"#table2 thead th:nth-child(1)"` | Last Name header in table2 |
| `TABLE2_HEADER_DUE` | `By.CSS_SELECTOR` | `"#table2 thead th:nth-child(4)"` | Due header in table2 |
| `TABLE1_FIRST_ROW_LAST_NAME` | `By.CSS_SELECTOR` | `"#table1 tbody tr:first-child td:first-child"` | First row, Last Name cell in table1; no class attributes on table1 td elements |
| `TABLE2_FIRST_ROW_LAST_NAME` | `By.CSS_SELECTOR` | `"#table2 tbody tr:first-child td.last-name"` | First row, Last Name cell in table2; `class='last-name'` confirmed in raw HTML |
| `TABLE2_FIRST_ROW_DUE` | `By.CSS_SELECTOR` | `"#table2 tbody tr:first-child td.dues"` | First row, Due cell in table2; `class='dues'` confirmed in raw HTML |
| `TABLE1_SORT_INDICATOR_LAST_NAME` | `By.CSS_SELECTOR` | `"#table1 thead th:nth-child(1).tablesorter-headerAsc, #table1 thead th:nth-child(1).tablesorter-headerDesc"` | Sort direction indicator classes applied by tablesorter plugin after header click |
| `TABLE2_SORT_INDICATOR_DUE` | `By.CSS_SELECTOR` | `"#table2 thead th:nth-child(4).tablesorter-headerAsc, #table2 thead th:nth-child(4).tablesorter-headerDesc"` | Sort direction indicator class after Due header click in table2 |

---

## Page Object Methods

| Method | Signature | Returns | Notes |
| --- | --- | --- | --- |
| `__init__` | `(self, driver: BaseCase)` | `None` | `super().__init__(driver)` then `wait_for_page_to_load(PAGE_LOADED_INDICATOR)` |
| `get_heading_text` | `(self)` | `str` | Returns text of `PAGE_LOADED_INDICATOR` via `get_dynamic_element_text(SortableDataTablesLocators.PAGE_LOADED_INDICATOR)` |
| `get_table1_row_count` | `(self)` | `int` | Returns `get_number_of_elements(SortableDataTablesLocators.TABLE1_ROWS)` |
| `get_table2_row_count` | `(self)` | `int` | Returns `get_number_of_elements(SortableDataTablesLocators.TABLE2_ROWS)` |
| `get_table1_header_count` | `(self)` | `int` | Returns `get_number_of_elements(SortableDataTablesLocators.TABLE1_HEADERS)` |
| `get_table2_header_count` | `(self)` | `int` | Returns `get_number_of_elements(SortableDataTablesLocators.TABLE2_HEADERS)` |
| `get_table1_first_row_last_name` | `(self)` | `str` | Returns `get_dynamic_element_text(SortableDataTablesLocators.TABLE1_FIRST_ROW_LAST_NAME)` |
| `get_table2_first_row_last_name` | `(self)` | `str` | Returns `get_dynamic_element_text(SortableDataTablesLocators.TABLE2_FIRST_ROW_LAST_NAME)` |
| `get_table2_first_row_due` | `(self)` | `str` | Returns `get_dynamic_element_text(SortableDataTablesLocators.TABLE2_FIRST_ROW_DUE)` |
| `click_table1_last_name_header` | `(self)` | `None` | `click_element(SortableDataTablesLocators.TABLE1_HEADER_LAST_NAME)` — triggers tablesorter sort |
| `click_table1_due_header` | `(self)` | `None` | `click_element(SortableDataTablesLocators.TABLE1_HEADER_DUE)` — triggers sort on Due column |
| `click_table2_last_name_header` | `(self)` | `None` | `click_element(SortableDataTablesLocators.TABLE2_HEADER_LAST_NAME)` — triggers tablesorter sort |
| `click_table2_due_header` | `(self)` | `None` | `click_element(SortableDataTablesLocators.TABLE2_HEADER_DUE)` — triggers sort on Due column |
| `is_table1_last_name_header_sorted` | `(self)` | `bool` | Returns `is_element_visible(SortableDataTablesLocators.TABLE1_SORT_INDICATOR_LAST_NAME, timeout=0)` — checks whether tablesorter applied asc or desc class |
| `is_table2_due_header_sorted` | `(self)` | `bool` | Returns `is_element_visible(SortableDataTablesLocators.TABLE2_SORT_INDICATOR_DUE, timeout=0)` — checks whether tablesorter applied asc or desc class |
| `get_all_table1_last_name_values` | `(self)` | `list[str]` | Returns list of `.text` values from `get_all_elements(SortableDataTablesLocators.TABLE1_ROWS)` — generator note below |
| `get_all_table2_due_values` | `(self)` | `list[str]` | Returns list of `.text` values from cells in table2 dues column — generator note below |

---

## Test Scenarios

Each scenario maps to exactly one test method in `TestSortableDataTables`.

---

### Scenario 1: Page loads with both data tables visible

**Method:** `test_page_loads_with_both_tables`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `CRITICAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/tables` via `MainPage.click_sortable_data_tables_link()`
   - `expect:` Page loads with heading "Data Tables" — verified by `PAGE_LOADED_INDICATOR`

2. Get heading text via `page.get_heading_text()`
   - `locator:` `PAGE_LOADED_INDICATOR`
   - `expect:` Heading text equals "Data Tables"

3. Get table1 row count via `page.get_table1_row_count()`
   - `locator:` `TABLE1_ROWS`
   - `expect:` Table1 has 4 data rows

4. Get table2 row count via `page.get_table2_row_count()`
   - `locator:` `TABLE2_ROWS`
   - `expect:` Table2 has 4 data rows

5. Get table1 header count via `page.get_table1_header_count()`
   - `locator:` `TABLE1_HEADERS`
   - `expect:` Table1 has 6 column headers

6. Get table2 header count via `page.get_table2_header_count()`
   - `locator:` `TABLE2_HEADERS`
   - `expect:` Table2 has 6 column headers

**Assertions:**

```python
self.assert_equal(heading, EXPECTED_HEADING, f"Expected heading '{EXPECTED_HEADING}', got '{heading}'")
self.assert_equal(table1_rows, EXPECTED_ROW_COUNT, f"Expected {EXPECTED_ROW_COUNT} rows in table1, got {table1_rows}")
self.assert_equal(table2_rows, EXPECTED_ROW_COUNT, f"Expected {EXPECTED_ROW_COUNT} rows in table2, got {table2_rows}")
self.assert_equal(table1_headers, EXPECTED_HEADER_COUNT, f"Expected {EXPECTED_HEADER_COUNT} headers in table1, got {table1_headers}")
self.assert_equal(table2_headers, EXPECTED_HEADER_COUNT, f"Expected {EXPECTED_HEADER_COUNT} headers in table2, got {table2_headers}")
```

---

### Scenario 2: Table 1 displays correct initial row data

**Method:** `test_table1_displays_correct_data`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/tables` via `MainPage.click_sortable_data_tables_link()`
   - `expect:` Page loads — verified by `PAGE_LOADED_INDICATOR`

2. Get first row last name in table1 via `page.get_table1_first_row_last_name()`
   - `locator:` `TABLE1_FIRST_ROW_LAST_NAME`
   - `expect:` First row Last Name cell contains "Smith" (default sort order from raw HTML)

**Assertions:**

```python
self.assert_equal(first_row_last_name, TABLE1_FIRST_ROW_LAST_NAME_DEFAULT, f"Expected table1 first row last name to be '{TABLE1_FIRST_ROW_LAST_NAME_DEFAULT}', got '{first_row_last_name}'")
```

---

### Scenario 3: Table 2 displays correct initial row data using class-based selectors

**Method:** `test_table2_displays_correct_data`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/tables` via `MainPage.click_sortable_data_tables_link()`
   - `expect:` Page loads — verified by `PAGE_LOADED_INDICATOR`

2. Get first row last name in table2 via `page.get_table2_first_row_last_name()`
   - `locator:` `TABLE2_FIRST_ROW_LAST_NAME`
   - `expect:` First row Last Name cell contains "Smith" (class attribute `last-name` confirmed in raw HTML)

3. Get first row due amount in table2 via `page.get_table2_first_row_due()`
   - `locator:` `TABLE2_FIRST_ROW_DUE`
   - `expect:` First row Due cell contains "$50.00" (class attribute `dues` confirmed in raw HTML)

**Assertions:**

```python
self.assert_equal(first_row_last_name, TABLE2_FIRST_ROW_LAST_NAME_DEFAULT, f"Expected table2 first row last name '{TABLE2_FIRST_ROW_LAST_NAME_DEFAULT}', got '{first_row_last_name}'")
self.assert_equal(first_row_due, TABLE2_FIRST_ROW_DUE_DEFAULT, f"Expected table2 first row due '{TABLE2_FIRST_ROW_DUE_DEFAULT}', got '{first_row_due}'")
```

---

### Scenario 4: Table 1 Last Name column is sortable

**Method:** `test_table1_last_name_column_is_sortable`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/tables` via `MainPage.click_sortable_data_tables_link()`
   - `expect:` Page loads — verified by `PAGE_LOADED_INDICATOR`

2. Click the Last Name column header in table1 via `page.click_table1_last_name_header()`
   - `locator:` `TABLE1_HEADER_LAST_NAME`
   - `expect:` tablesorter plugin applies `.tablesorter-headerAsc` or `.tablesorter-headerDesc` CSS class to the header cell, indicating sort is active

3. Check sort indicator via `page.is_table1_last_name_header_sorted()`
   - `locator:` `TABLE1_SORT_INDICATOR_LAST_NAME`
   - `expect:` Sort indicator is visible — at least one sort direction class is applied

**Assertions:**

```python
self.assert_true(is_sorted, "Expected table1 Last Name header to have a sort direction class after clicking")
```

---

### Scenario 5: Table 2 Due column is sortable using class-based selector

**Method:** `test_table2_due_column_is_sortable`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/tables` via `MainPage.click_sortable_data_tables_link()`
   - `expect:` Page loads — verified by `PAGE_LOADED_INDICATOR`

2. Click the Due column header in table2 via `page.click_table2_due_header()`
   - `locator:` `TABLE2_HEADER_DUE`
   - `expect:` tablesorter plugin applies a sort direction class to the Due header in table2

3. Check sort indicator via `page.is_table2_due_header_sorted()`
   - `locator:` `TABLE2_SORT_INDICATOR_DUE`
   - `expect:` Sort indicator is visible

**Assertions:**

```python
self.assert_true(is_sorted, "Expected table2 Due header to have a sort direction class after clicking")
```

---

### Scenario 6: Both tables have correct URL after navigation

**Method:** `test_tables_page_url`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `MINOR`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/tables` via `MainPage.click_sortable_data_tables_link()`
   - `expect:` URL ends with `/tables`

**Assertions:**

```python
self.assert_true(self.get_current_url().endswith(EXPECTED_URL_SUFFIX), f"Expected URL to end with '{EXPECTED_URL_SUFFIX}'")
```

---

## Out of Scope

| Excluded scenario | Reason |
| --- | --- |
| Verify sort order of all rows after ascending/descending sort | Sort interaction outcome (row reordering) was not directly observed via Playwright click+snapshot in this session — including precise row-order assertions would be based on inference, not live observation |
| Edit/delete link functionality | `<a href='#edit'>` and `<a href='#delete'>` are fragment anchors only — no navigation or state change occurs; nothing observable to assert beyond link presence |
| Verify edit and delete links are present in every row | Requires iterating all rows and cells; complex multi-element iteration beyond simple count/text assertions — better suited for a dedicated accessibility or content audit test |
| Persistent sort state across page refresh | No state persistence mechanism was observed in the HTML; tablesorter is purely client-side with no server-side state |
| Sort on remaining columns (First Name, Email, Web Site, Action) | The sortable column feature is demonstrated adequately by Last Name and Due columns; testing all 6 columns in both tables produces 12 scenarios with no additional coverage value |
| Cross-browser sort consistency | Framework scope — browser compatibility testing is outside this project's test suite |
| Table rendering without JavaScript | The tablesorter plugin requires JavaScript; testing JS-disabled behavior is outside framework scope |

---

## Test Data

```python
EXPECTED_HEADING = "Data Tables"
EXPECTED_URL_SUFFIX = "/tables"
EXPECTED_ROW_COUNT = 4
EXPECTED_HEADER_COUNT = 6
TABLE1_FIRST_ROW_LAST_NAME_DEFAULT = "Smith"
TABLE2_FIRST_ROW_LAST_NAME_DEFAULT = "Smith"
TABLE2_FIRST_ROW_DUE_DEFAULT = "$50.00"
```

These constants should be defined at module level in the test file (not in the page object or
locators file) so they are visible alongside the assertions that use them.

---

## Generator Notes

- **Sorting observation gap**: The tablesorter sort interaction was NOT directly observed with Playwright click+snapshot in this session (page content was retrieved via a fetch script). Sort scenarios (Scenarios 4 and 5) are designed based on the tablesorter CSS class pattern (`.tablesorter-headerAsc`, `.tablesorter-headerDesc`) visible in the raw HTML `<style>` block. The generator should implement these scenarios but the healer may need to verify the selector syntax for the sort indicator CSS class check if it does not work as written.
- **`TABLE1_SORT_INDICATOR_LAST_NAME` locator**: The CSS selector uses a comma-separated compound selector (`a, b`) which is valid CSS but may behave differently depending on how `wait_for_element_visible` resolves it. The generator should implement `is_table1_last_name_header_sorted` using `is_element_visible(..., timeout=0)` with the compound selector. If it fails, an alternative is to check `get_element_attr(TABLE1_HEADER_LAST_NAME, "class")` and assert that `"tablesorter-headerAsc"` or `"tablesorter-headerDesc"` is in the result — flag in Generator Notes.
- **`get_all_table1_last_name_values` / `get_all_table2_due_values`**: These methods require iterating `get_all_elements` results and extracting `.text` from each element. The generator should implement them by calling `get_all_elements` on `TABLE1_ROWS` / `TABLE2_ROWS` and then using a structural CSS selector with `format_locator` or by building per-cell locators. These methods are defined in the spec for completeness but are not used in any of the planned scenarios — omit them if the generator prefers minimal methods.
- **table1 `<td>` elements**: Raw HTML confirms no `id` or `class` attributes on `<td>` elements in table1. CSS structural selectors (`:first-child`, `:nth-child`) are the only option for targeting specific cells. `By.ID` cannot be used for any table1 cell locator.
- **table2 `<td>` elements**: Raw HTML confirms `class` attributes on all table2 `<td>` elements. Values are: `last-name`, `first-name`, `email`, `dues`, `web-site`, `action`. Use `By.CSS_SELECTOR` with class selectors — never use `By.CLASS_NAME` alone.
- **`dues` vs `due`**: The column header says "Due" but the class attribute on table2 `<td>` cells is `dues` (plural). Use `td.dues` in selectors — not `td.due`.
- **Homepage link text**: Raw HTML of homepage contains `<a href='/tables'>Sortable Data Tables</a>`. The `MainPageLocators` entry must use `By.LINK_TEXT` with `"Sortable Data Tables"`. The `nav_method` default `page_name` parameter should be `"Sortable Data Tables"`.
- **`EXPECTED_HEADING` = "Data Tables"**: Taken verbatim from `<h3>Data Tables</h3>`. This is different from the homepage link text "Sortable Data Tables" — do not conflate the two.
- **Test data placement**: All constants listed in Test Data above should be placed at module level (above the class) since `EXPECTED_ROW_COUNT` and `EXPECTED_HEADER_COUNT` are integers, not strings — module-level placement is appropriate per SKILL.md Section 6.
- **No inline interactions**: All interactions in test scenarios are delegated to page object methods — no inline locator usage in the test body.
