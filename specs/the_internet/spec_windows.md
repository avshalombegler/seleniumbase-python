# Multiple Windows Test Plan

<!--
  SPEC FORMAT v1.0 — SeleniumBase Python Project
  Generator: sb-generator
  Do not edit manually — update the spec and re-run the generator.
-->

---

## Feature Metadata

| Field | Value |
| --- | --- |
| **Feature name** | Multiple Windows |
| **URL** | `/windows` |
| **Full URL** | `https://the-internet.herokuapp.com/windows` |
| **Feature directory** | `windows` |
| **Page object class** | `MultipleWindowsPage` |
| **Locators class** | `MultipleWindowsLocators` |
| **Test class** | `TestMultipleWindows` |
| **Test file** | `tests/the_internet/ui_test_suite/test_windows.py` |
| **Page object file** | `src/pages/features/windows/windows_page.py` |
| **Locators file** | `src/pages/features/windows/locators.py` |
| **MainPage nav method** | `click_windows_link` |
| **Allure sub_suite** | `Multiple Windows` |

---

## Page Elements

| Locator name | Strategy | Selector | Notes |
| --- | --- | --- | --- |
| `PAGE_LOADED_INDICATOR` | `By.CSS_SELECTOR` | `"a[href='/windows/new']"` | Confirms /windows page is loaded |
| `OPEN_NEW_WINDOW_LINK` | `By.CSS_SELECTOR` | `"a[href='/windows/new']"` | "Click Here" link; opens /windows/new in a new tab (target="_blank") |
| `PAGE_HEADING` | `By.CSS_SELECTOR` | `".example h3"` | H3 heading on the current page; works on both /windows and /windows/new |

---

## Page Object Methods

| Method | Signature | Returns | Notes |
| --- | --- | --- | --- |
| `__init__` | `(self, driver: BaseCase)` | `None` | `super().__init__(driver)` then `wait_for_page_to_load(PAGE_LOADED_INDICATOR)` |
| `click_open_new_window` | `(self)` | `None` | `click_element(OPEN_NEW_WINDOW_LINK)` — triggers new tab/window via target="_blank" |
| `get_window_handles` | `(self)` | `list[str]` | Returns `self.driver.driver.window_handles` — list of all open window handles |
| `switch_to_window` | `(self, handle: str)` | `None` | Calls `self.driver.driver.switch_to.window(handle)` to focus the given handle |
| `get_page_heading` | `(self)` | `str` | `get_dynamic_element_text(PAGE_HEADING)` — returns H3 text of the currently active window |

---

## Test Scenarios

Each scenario maps to exactly one test method in `TestMultipleWindows`.

---

### Scenario 1: New window opens and contains expected content

**Method:** `test_new_window_opens_with_expected_content`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `CRITICAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/windows` via `MainPage.click_windows_link()`
   - `expect:` Page loads — verified by `PAGE_LOADED_INDICATOR`

2. Record the current (original) window handle and click the "Click Here" link via `page.click_open_new_window()`
   - `locator:` `OPEN_NEW_WINDOW_LINK`
   - `expect:` A new browser window or tab opens, resulting in two open window handles

3. Switch to the new window handle via `page.switch_to_window(new_handle)`
   - `expect:` Browser focus moves to the new window at URL `/windows/new`

4. Read the heading of the new window via `page.get_page_heading()`
   - `locator:` `PAGE_HEADING`
   - `expect:` The heading reads "New Window"

**Assertions:**

```python
handles = page.get_window_handles()
self.assert_equal(len(handles), 2, "Exactly two window handles should be open after clicking the link")
new_handle = [h for h in handles if h != original_handle][0]
page.switch_to_window(new_handle)
self.assert_true(self.get_current_url().endswith("/windows/new"), "New window URL should end with /windows/new")
self.assert_equal(page.get_page_heading(), NEW_WINDOW_HEADING, "New window heading should read 'New Window'")
```

---

### Scenario 2: Original window remains intact after new window opens

**Method:** `test_original_window_remains_after_new_window_opens`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/windows` via `MainPage.click_windows_link()`
   - `expect:` Page loads — verified by `PAGE_LOADED_INDICATOR`

2. Record the original window handle and heading, then click the link via `page.click_open_new_window()`
   - `locator:` `OPEN_NEW_WINDOW_LINK`
   - `expect:` New window opens alongside the original

3. Switch back to the original window handle via `page.switch_to_window(original_handle)`
   - `expect:` Browser focus returns to the original /windows tab

4. Read the heading of the original window via `page.get_page_heading()`
   - `locator:` `PAGE_HEADING`
   - `expect:` The heading still reads "Opening a new window"

**Assertions:**

```python
handles = page.get_window_handles()
self.assert_equal(len(handles), 2, "Two window handles should be open")
page.switch_to_window(original_handle)
self.assert_true(self.get_current_url().endswith("/windows"), "Original window URL should still end with /windows")
self.assert_equal(page.get_page_heading(), ORIGINAL_WINDOW_HEADING, "Original window heading should still read 'Opening a new window'")
```

---

### Scenario 3: Two-window context — switching back and forth

**Method:** `test_switch_between_windows`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/windows` via `MainPage.click_windows_link()`
   - `expect:` Page loads — verified by `PAGE_LOADED_INDICATOR`

2. Click the link via `page.click_open_new_window()`, then switch to the new window via `page.switch_to_window(new_handle)`
   - `locator:` `OPEN_NEW_WINDOW_LINK`
   - `expect:` New window is active; heading reads "New Window"

3. Switch back to the original window via `page.switch_to_window(original_handle)`
   - `expect:` Original window is re-focused; heading reads "Opening a new window"

**Assertions:**

```python
# In new window
page.switch_to_window(new_handle)
self.assert_equal(page.get_page_heading(), NEW_WINDOW_HEADING, "New window heading should be 'New Window'")
# Back in original window
page.switch_to_window(original_handle)
self.assert_equal(page.get_page_heading(), ORIGINAL_WINDOW_HEADING, "Original window heading should be 'Opening a new window'")
```

---

## Out of Scope

| Excluded scenario | Reason |
| --- | --- |
| Opening more than one additional window | The page only provides one "Click Here" link; multi-window stacking beyond 2 handles is not observable without scripted interaction |
| Verifying new window is a separate browser process | Cross-process isolation is a browser-level concern outside SeleniumBase assertion scope |
| Testing window close behavior | Closing one window and asserting driver state after `driver.close()` is not observable on this page's UI and risks orphaning the WebDriver session |
| Keyboard shortcut to open link in new tab | Keyboard navigation testing is outside the defined UI interaction scope for this project |
| Performance/load time of the new window | Performance testing is out of scope per project boundaries |

---

## Test Data

```python
NEW_WINDOW_HEADING = "New Window"
ORIGINAL_WINDOW_HEADING = "Opening a new window"
NEW_WINDOW_URL_SEGMENT = "/windows/new"
WINDOWS_URL_SEGMENT = "/windows"
```

These constants should be defined at module level in the test file (not in the page object or
locators file) so they are visible alongside the assertions that use them.

---

## Generator Notes

- `get_window_handles` uses `self.driver.driver.window_handles` because `self.driver` is the `BaseCase` instance and `.driver` on it returns the underlying Selenium WebDriver. The generator should verify this access pattern against `BasePage` / `UiBaseCase` to confirm the correct attribute chain.
- `switch_to_window` uses `self.driver.driver.switch_to.window(handle)` for the same reason — raw Selenium API call wrapped in the page object method.
- The test body must capture `original_handle = self.driver.driver.current_window_handle` (or equivalent) BEFORE clicking the link, then derive `new_handle` as the handle not in the original set. This inline handle capture should happen in the test body, not in a page object method, since it is state-tracking logic. Generator Note: "original_handle and new_handle derivation happens inline in the test body."
- After switching to a new window, `page.get_page_heading()` calls `get_dynamic_element_text(PAGE_HEADING)` — this will look up `.example h3` in the now-active window context, which is correct for `/windows/new`.
- No `LOCATOR_UNRESOLVED` items. All locators were confirmed from raw HTML source.
- `PAGE_HEADING` selector `".example h3"` resolves correctly on both `/windows` (heading: "Opening a new window") and `/windows/new` (heading: "New Window") — the same locator is reused in both window contexts.
- Homepage link text confirmed as "Multiple Windows" from the-internet homepage anchor text.
- The `feature_dir` is `windows` (not `multiple_windows`) because the URL path is `/windows`. The `allure_sub_suite`, `feature name`, page class names, and test class name all use "Multiple Windows" (from the H3 heading). The nav method is `click_windows_link` (derived from feature_dir = windows).
