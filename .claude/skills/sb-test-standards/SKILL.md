---
name: sb-test-standards
description: Use when writing or reviewing locator, page object, or test files in the seleniumbase-python project — authoritative reference for the three-layer POM conventions.
---

# SeleniumBase Python — Test Coding Standards

> Single source of truth for the three-layer coding conventions used in `seleniumbase-python`.
> Consumed by `sb-generator`, `sb-healer`, and `sb-planner` as the authoritative reference for
> what correct locator, page object, and test file code looks like.

---

## Section 1: Three-Layer Architecture

Every feature follows a strict three-layer Page Object Model. Each layer has a dedicated file and strict separation of concerns.

| Layer | Path | Class Pattern |
| --- | --- | --- |
| Locators | `src/pages/features/<feature>/locators.py` | `XxxLocators` |
| Page Object | `src/pages/features/<feature>/<feature>_page.py` | `XxxPage(BasePage)` |
| Test | `tests/the_internet/ui_test_suite/test_<feature>.py` for single-page features; `tests/the_internet/ui_test_suite/test_<feature>/test_<subpage>.py` for multi-page features — one file per sub-page (e.g., `test_frames/test_iframe.py`). All sub-pages share the same `@allure.sub_suite` value. | `TestXxx(UiBaseCase)` |

### What belongs in each layer

**Locators layer** (`locators.py`)

- Class attributes only — no methods, no `__init__`, no class inheritance
- Every selector string lives here and **only** here — never hardcoded in page objects or tests
- Attribute type: `Locator` dict

**Page Object layer** (`<feature>_page.py`)

- Standard element interactions (click, type, visibility checks, text retrieval) go through `BasePage` methods. For browser operations without a `BasePage` wrapper (hover, drag-and-drop, JS execution, alert handling, scrolling), call `self.driver.*` directly — see Section 4 for the full list. Never call `self.driver.find_element()` raw.
- No test assertions — assertions live in the test layer only
- No `self.logger.info(...)` calls — logging lives in the test layer only
- No hardcoded selector strings — all selectors come from the locators class

**Test layer** (`test_<feature>.py`)

- All assertions — only `self.assert_equal`, `self.assert_in`, `self.assert_true`, `self.assert_false`
- All `self.logger.info(...)` calls
- All test data constants (credentials, expected messages, expected text)
- No selector strings — never reference locators directly

---

## Section 2: The `Locator` Type

`Locator` is a type alias defined in `src/pages/base/base_page.py` (TYPE_CHECKING only):

```python
Locator = dict[str, str]
```

### Dict shape

```python
{"selector": "<value>", "by": By.<STRATEGY>}
```

### Consumption by unpacking

Locators are consumed by unpacking into BasePage's calls to SeleniumBase:

```python
self.driver.click(**locator)                               # in click_element
self.driver.type(text=text, **locator)                     # in send_keys_to_element
self.driver.wait_for_element_visible(**locator, timeout=t) # in wait_for_page_to_load
```

### `format_locator` pattern for dynamic selectors

When a selector contains a `{placeholder}` that must be filled at runtime, use `self.format_locator`:

```python
# In locators.py:
FILE_LINK: Locator = {"selector": "a[href='{file_name}']", "by": By.CSS_SELECTOR}

# In page object method:
formatted = self.format_locator(FeatureLocators.FILE_LINK, file_name=file_name)
self.click_element(formatted)
```

`format_locator` returns a new `Locator` dict with the selector formatted; the original is unchanged.

### `PAGE_LOADED_INDICATOR` convention

`PAGE_LOADED_INDICATOR` must always be:

- The **first** attribute in every `XxxLocators` class
- Passed to `self.wait_for_page_to_load(...)` in the page object's `__init__`

```python
# In locators.py:
class CheckboxesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "div.example h3", "by": By.CSS_SELECTOR}

# In page object __init__:
self.wait_for_page_to_load(CheckboxesPageLocators.PAGE_LOADED_INDICATOR)
```

### Locator strategy priority rules (non-negotiable)

1. **`By.ID`** — when the element has a stable `id` attribute. Strip the leading `#` when converting from CSS notation:

   ```python
   # Correct:
   USERNAME_TEXTBOX: Locator = {"selector": "username", "by": By.ID}
   FLASH_MSG: Locator = {"selector": "flash", "by": By.ID}
   # Incorrect:
   USERNAME_TEXTBOX: Locator = {"selector": "#username", "by": By.ID}
   ```

2. **`By.CSS_SELECTOR`** — preferred for all other cases. Forms used in this project:

   ```python
   LOGIN_BTN: Locator = {"selector": "button[type=submit]", "by": By.CSS_SELECTOR}
   LOGOUT_BTN: Locator = {"selector": "a[href='/logout']", "by": By.CSS_SELECTOR}
   PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h3", "by": By.CSS_SELECTOR}
   CHECKBOXES: Locator = {"selector": "form#checkboxes input[type=checkbox]", "by": By.CSS_SELECTOR}
   START_BTN: Locator = {"selector": "div#start > button", "by": By.CSS_SELECTOR}
   ```

3. **`By.XPATH`** — only when CSS cannot express the query. Acceptable cases: text-based matching, ancestor traversal. Always a last resort:

   ```python
   REMOVE_BTN: Locator = {"selector": "//button[text()='Remove']", "by": By.XPATH}
   ADD_BTN: Locator = {"selector": "//button[text()='Add']", "by": By.XPATH}
   ```

4. **`By.LINK_TEXT`** — used **exclusively** in `MainPageLocators` for homepage navigation links:

   ```python
   CHECKBOXES_LINK: Locator = {"selector": "Checkboxes", "by": By.LINK_TEXT}
   ```

5. **Forbidden**: `By.CLASS_NAME` alone, `By.TAG_NAME` alone — too brittle or too broad.

---

## Section 3: Locators File Standards

A correct `locators.py` file follows this exact structure:

```python
"""
Module containing locators for Checkboxes page object.
"""

from selenium.webdriver.common.by import By

from src.pages.base.base_page import Locator


class CheckboxesPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": "div.example h3", "by": By.CSS_SELECTOR}
    CHECKBOXES: Locator = {"selector": "form#checkboxes input[type=checkbox]", "by": By.CSS_SELECTOR}
```

*(Source: `src/pages/features/checkboxes/locators.py`)*

### Rules

- **Module docstring**: `"""Module containing locators for <Feature Name> page object."""` — triple-quoted, exact format shown above
- **Import block**: exactly two imports, in this order:
  1. `from selenium.webdriver.common.by import By`
  2. `from src.pages.base.base_page import Locator`
- **Class definition**: no inheritance (`class XxxLocators:` not `class XxxLocators(object):`), no `__init__`, no methods
- **`PAGE_LOADED_INDICATOR`**: always the first attribute
- **Attribute naming**: `SCREAMING_SNAKE_CASE`
- **No blank lines** between locator definitions — they run consecutively
- **Type annotation on every locator**: `NAME: Locator = {...}`

When a feature has multiple pages, define a separate class per page in the same `locators.py` file:

```python
class FormAuthenticationPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h2", "by": By.CSS_SELECTOR}
    USERNAME_TEXTBOX: Locator = {"selector": "username", "by": By.ID}
    PASSWORD_TEXTBOX: Locator = {"selector": "password", "by": By.ID}
    LOGIN_BTN: Locator = {"selector": "button[type=submit]", "by": By.CSS_SELECTOR}
    FLASH_MSG: Locator = {"selector": "flash", "by": By.ID}


class SecureAreaPageLocators:
    PAGE_LOADED_INDICATOR: Locator = {"selector": ".example h2", "by": By.CSS_SELECTOR}
    LOGOUT_BTN: Locator = {"selector": "a[href='/logout']", "by": By.CSS_SELECTOR}
    FLASH_MSG: Locator = {"selector": "flash", "by": By.ID}
```

*(Source: `src/pages/features/form_authentication/locators.py`)*

---

## Section 4: Page Object File Standards

A correct page object file follows this exact structure:

```python
from __future__ import annotations

from typing import TYPE_CHECKING

import allure

from src.pages.base.base_page import BaseCase, BasePage
from src.pages.features.form_authentication.locators import FormAuthenticationPageLocators
from src.pages.features.form_authentication.secure_area_page import SecureAreaPage

if TYPE_CHECKING:
    pass


class FormAuthenticationPage(BasePage):
    """Page object for the Form Auth page containing methods to interact with and validate page functionality"""

    def __init__(self, driver: BaseCase) -> None:
        super().__init__(driver)
        self.wait_for_page_to_load(FormAuthenticationPageLocators.PAGE_LOADED_INDICATOR)

    @allure.step("Enter username '{username}'")
    def enter_username(self, username: str) -> None:
        self.send_keys_to_element(FormAuthenticationPageLocators.USERNAME_TEXTBOX, username)

    @allure.step("Click login - correct")
    def click_login_correct(self) -> SecureAreaPage:
        self.click_element(FormAuthenticationPageLocators.LOGIN_BTN)
        return SecureAreaPage(self.driver)

    @allure.step("Get flash message")
    def get_flash_message(self) -> str:
        return self.get_dynamic_element_text(FormAuthenticationPageLocators.FLASH_MSG)
```

*(Source: `src/pages/features/form_authentication/form_authentication_page.py`)*

### Rules

- **First line**: always `from __future__ import annotations`
- **Import ordering**:
  1. `from typing import TYPE_CHECKING`
  2. stdlib (if any)
  3. third-party: `import allure`
  4. local: `from src.pages.base.base_page import BaseCase, BasePage`, then feature locators
- **`if TYPE_CHECKING: pass` block**: always present even when empty — it is the project convention
- **Class inherits from `BasePage`**: `class XxxPage(BasePage):`
- **`__init__` signature**: `(self, driver: BaseCase) -> None`
- **`__init__` body**: `super().__init__(driver)` first, then `self.wait_for_page_to_load(<Locators>.PAGE_LOADED_INDICATOR)`
- **Every public method**: decorated with `@allure.step("...")`
- **Method bodies**: use `self.<base_page_method>(<Locators>.<LOCATOR_NAME>)` — never hardcoded selector strings
- **Return types**: always explicit on every method
- **No `self.logger.info(...)` in page object methods** — logging lives in test files only
- **Multi-page features**: a method that transitions to a different page returns the new page object:

  ```python
  @allure.step("Click login - correct")
  def click_login_correct(self) -> SecureAreaPage:
      self.click_element(FormAuthenticationPageLocators.LOGIN_BTN)
      return SecureAreaPage(self.driver)
  ```

- **When `BasePage` has no wrapper**: call `self.driver.*` directly for browser operations not covered by `BasePage`. This is the correct pattern, not a violation:

  ```python
  self.driver.hover(**locator)                      # mouse hover
  self.driver.drag_and_drop(...)                    # drag-and-drop
  self.driver.accept_alert()                        # alert accept
  self.driver.wait_for_and_switch_to_alert()        # switch to alert
  self.driver.execute_script("return ...")          # JavaScript execution
  self.driver.scroll_down(pixels)                   # scrolling
  self.driver.execute_cdp_cmd("...", {...})          # Chrome DevTools Protocol
  self.driver.switch_to_default_content()           # exit iframe context

  button = self.wait_for_visibility(locator)
  button.click()                                    # direct WebElement click
  ```

  The last pattern — calling `.click()` on the `WebElement` returned by `wait_for_visibility` — avoids a second DOM lookup and is preferred when the click triggers an alert (calling `click_element` after the alert fires causes a stale-element exception). Never call `self.driver.find_element()` raw — always go through a `BasePage` method to obtain the element first.

---

## Section 5: `BasePage` Method Reference

Actual method signatures from `src/pages/base/base_page.py`.

### Wait Methods

```python
def wait_for_page_to_load(
    self, indicator_locator: Locator | None, timeout: int | float | None = None, use_ready_state: bool = True
) -> None:
```

Combines a `document.readyState` check with `wait_for_element_visible` on the indicator. Defaults to `long_wait`. Used in every page object `__init__`.

```python
def wait_for_visibility(self, locator: Locator, timeout: int | float | None = None) -> Any:
```

Waits for element to be visible. Defaults to `short_wait`. Returns the WebElement.

```python
def wait_for_invisibility(self, locator: Locator, timeout: int | float | None = None) -> bool:
```

Waits for element to disappear. Defaults to `short_wait`. Returns `True` when invisible.

```python
def wait_for_loader(self, locator: Locator, timeout: int | float | None = None) -> bool:
```

Waits for a loading indicator to appear then disappear. Returns `True` if loader completed, `False` on timeout.

```python
def wait_for_file_to_download(self, filename: str, timeout: int | float | None = None) -> bool:
```

Polls for `filename` in the per-worker download directory. Returns `True` when the file appears, `False` on timeout. Defaults to `short_wait`. Always call this after `download_file()` to confirm completion before asserting on the downloaded file.

### Navigation Methods

```python
def navigate_to(self, url: str) -> None:
```

Navigates to the given URL. Decorated with `@allure.step`. Not used in `@pytest.mark.ui` tests — `setUp` handles navigation.

```python
def refresh_page(self) -> None:
```

Refreshes the current page.

```python
def navigate_back(self) -> None:
```

Navigates back in browser history.

### Frame/Window Methods

```python
def switch_to_frame(self, locator: Locator) -> None:
```

Switches the driver context into the iframe identified by `locator`. After switching, all element interactions target the frame's DOM. To exit the frame, call `self.driver.switch_to_default_content()` directly (no `BasePage` wrapper for this).

### Interaction Methods

```python
def click_element(self, locator: Locator) -> None:
```

Clicks an element. Raises on failure.

```python
def send_keys_to_element(self, locator: Locator, text: str) -> None:
```

Types `text` into the element. Calls `driver.type(text=text, **locator)`.

```python
def perform_right_click(self, locator: Locator) -> None:
```

Right-clicks an element using ActionChains.

```python
def download_file(self, locator: Locator, file_name: str, timeout: int | float | None = None) -> None:
```

Clicks a download link. The `locator` must have a `{file_name}` placeholder — `format_locator` is called internally.

### State Methods

```python
def is_element_visible(self, locator: Locator, timeout: int | float | None = None) -> bool:
```

Returns `True` if the element is visible within `timeout`. Use `timeout=0` for a fast, non-waiting check. Defaults to `short_wait`.

```python
def is_element_selected(self, locator: Locator, timeout: int | float | None = None) -> bool:
```

Returns `True` if the element (checkbox, radio) is selected. Use `timeout=0` for fast check.

```python
def is_element_enabled(self, locator: Locator, timeout: int | float | None = None) -> bool:
```

Returns `True` if the element is enabled. Use `timeout=0` for fast check.

### Query Methods

```python
def get_dynamic_element_text(self, locator: Locator, timeout: int | float | None = None) -> str:
```

Waits for the element then returns its text content. Defaults to `long_wait`.

```python
def get_all_elements(self, locator: Locator) -> list:
```

Returns all elements matching the locator. Returns empty list if none found.

```python
def get_number_of_elements(self, locator: Locator) -> int:
```

Returns the count of elements matching the locator.

```python
def get_element_attr(self, locator: Locator, attribute: str) -> Any | None:
```

Returns the value of the named attribute. Returns `None` on failure.

```python
def get_base_url(self) -> str | AnyUrl:
```

Returns `settings.BASE_URL` from the project configuration. Use this in page object methods that must construct absolute URLs (e.g., credential-embedded auth URLs in `get_<feature>_page` methods). In `main_page.py`, the instance attribute `self.base_url` provides the same value.

### Utility

```python
def format_locator(self, locator: Locator, **kwargs: Any) -> Locator:
```

Returns a new Locator dict with `{placeholder}` values in the selector formatted using `**kwargs`. The original locator is not modified.

---

## Section 6: Test File Standards

A correct test file follows this exact structure:

```python
import allure
import pytest

from src.pages.base.ui_base_case import UiBaseCase
from src.pages.common.main_page.main_page import MainPage


@allure.parent_suite("the-internet")
@allure.suite("UI Test Suite")
@allure.sub_suite("A/B Testing")
class TestABTesting(UiBaseCase):
    """Tests for verifying title and paragraph content of page"""

    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_ab_testing_content(self) -> None:
        self.logger.info("Tests for verifying title and paragraph content of page")
        main_page = MainPage(self)
        page = main_page.click_ab_testing_link()

        title = page.get_title_text()
        self.logger.info(f"Retrieved title: {title}.")
        expected_titles = ["A/B Test Control", "A/B Test Variation 1"]
        self.assert_in(title, expected_titles, f"Expected title in {expected_titles}, got '{title}'")
```

*(Source: `tests/the_internet/ui_test_suite/test_ab_testing.py`)*

### Class Level

- **Three Allure decorators** in this order:
  1. `@allure.parent_suite("the-internet")`
  2. `@allure.suite("UI Test Suite")`
  3. `@allure.sub_suite("<Feature Name>")`
- **Inherits from `UiBaseCase`**: `class TestXxx(UiBaseCase):`
- **Class docstring**: `"""Tests <Feature Name> functionality"""`
- **Test data constants**: two accepted locations — choose based on scope:
  - **Class-level** (inside class, above all methods): for constants used only by this test class — most common:
    ```python
    class TestHovers(UiBaseCase):
        USER: str = "user"
        FIRST_USER: int = 1
        NUM_OF_USERS: int = 3
    ```
  - **Module-level** (above the class): for constants shared across multiple classes in the same file, or for large parameterized data tables referenced by `@parameterized.expand`
  - **Never**: inside test method bodies — constants must not be local variables

### Method Level

- **Decorator order** (exactly this order):
  1. `@pytest.mark.regression`
  2. `@pytest.mark.ui`
  3. `@allure.severity(allure.severity_level.<LEVEL>)`
  4. `@pytest.mark.smoke` — only when explicitly designated, never by default
- **Return type**: always `-> None`
- **First statement**: always `self.logger.info("...")`
- **Navigation pattern**:

  ```python
  main_page = MainPage(self)
  page = main_page.click_<feature>_link()
  ```

- **Never call** `self.navigate_to()` or `self.open()` directly in `@pytest.mark.ui` tests — `setUp` navigates to `BASE_URL` automatically

### `self.driver` in tests vs. page objects

| Context | `self.driver` refers to | Raw WebDriver access |
|---|---|---|
| Page object (`BasePage` subclass) | `BaseCase` instance | `self.driver.driver` |
| Test (`UiBaseCase` subclass) | Selenium `WebDriver` directly | `self.driver` — no extra `.driver` |

**Never use `self.driver.driver` in a test file.** The extra `.driver` attribute does not exist in the test context and will raise `AttributeError` at runtime. When a test needs direct WebDriver access (e.g. `current_window_handle`, `window_handles`), use `self.driver.<attribute>` directly.

### Assertion Rules

- Use only: `self.assert_equal`, `self.assert_in`, `self.assert_true`, `self.assert_false`
- **Never** bare Python `assert`
- Every assertion includes a descriptive message as the last argument:

  ```python
  self.assert_true(page.is_checkbox_checked(0), "Expected checkbox 0 to be checked")
  self.assert_in("You logged into", flash_message, f"Expected '{flash_message}' to contain login text")
  self.assert_equal(result_text, expected_result, f"Expected '{result_text}', but got '{expected_result}'")
  ```

- URL assertions always use `self.get_current_url().endswith("/segment")` pattern:

  ```python
  self.assert_true(self.get_current_url().endswith("/secure"), "Expected URL to end with /secure")
  ```

### `@pytest.mark.ui` and `setUp` behavior

`UiBaseCase.setUp` automatically opens `settings.BASE_URL` when the test is marked `@pytest.mark.ui`. Tests must not duplicate this navigation. Tests without `@pytest.mark.ui` must call `navigate_to` explicitly (rare — only for non-UI tests).

---

## Section 7: `MainPage` Registration Standards

Every feature must be registered in `MainPage` via a locator in `MainPageLocators` and a navigation method in `main_page.py`.

### `MainPageLocators` entry

```python
# src/pages/common/main_page/locators.py
CHECKBOXES_LINK: Locator = {"selector": "Checkboxes", "by": By.LINK_TEXT}
FORM_AUTH_LINK: Locator = {"selector": "Form Authentication", "by": By.LINK_TEXT}
```

*(Source: `src/pages/common/main_page/locators.py`)*

Rules:

- Always use `By.LINK_TEXT` with the **exact** `<a>` link text from the homepage
- Entries are in **alphabetical order** by link text within the class

### Navigation method — standard (`click_<feature>_link`)

Use this pattern when the feature has a direct link on the homepage:

```python
@allure.step("Navigate to {page_name} page")
def click_checkboxes_link(self, page_name: str = "Checkboxes") -> CheckboxesPage:
    self.logger.info(f"Navigating to {page_name} page.")
    self.click_element(MainPageLocators.CHECKBOXES_LINK)

    return CheckboxesPage(self.driver)
```

*(Source: `src/pages/common/main_page/main_page.py`)*

Rules:

- **Decorator**: `@allure.step("Navigate to {page_name} page")`
- **Signature**: `def click_<feature>_link(self, page_name: str = "<Feature Name>") -> <FeaturePage>:`
- **Body line 1**: `self.logger.info(f"Navigating to {page_name} page.")`
- **Body line 2**: `self.click_element(MainPageLocators.<FEATURE>_LINK)`
- **Blank line** between `click_element` and `return` — part of the style
- **Return**: `return <FeaturePage>(self.driver)`
- Import for the new page object is added in **alphabetical order** in the import block of `main_page.py`
- **Required:** After inserting the import, re-read the import block with the Read tool to confirm the line is present before proceeding to add the navigation method. A missing import will silently break every test for this feature at runtime.

### Navigation method — URL-based (`get_<feature>_page`)

Use this pattern when the feature requires URL construction (credentials embedded in the URL, direct URL navigation without a homepage click, or no homepage link exists):

```python
@allure.step("Navigate to {page_name} page")
def get_digest_auth_page(
    self, username: str, password: str, page_name: str = "Digest Authentication"
) -> DigestAuthPage:
    self.logger.info(f"Navigating to {page_name} page.")
    if not username or not password:
        raise ValueError(f"Invalid credentials: username='{username}', password='{password or ''}'")
    base_path = urljoin(str(self.base_url), "digest_auth")
    url = base_path.replace("https://", f"https://{username}:{password}@")
    self.navigate_to(url)

    return DigestAuthPage(self.driver)
```

*(Source: `src/pages/common/main_page/main_page.py`)*

Rules:

- **Method name**: `get_<feature>_page(self, ...)` — never `click_*` when there is no click
- **Decorator**: same `@allure.step("Navigate to {page_name} page")` convention
- Use `"Returning object of {page_name} page"` as the step text when no navigation occurs at all (e.g., `get_basic_auth_page` — the page is already loaded by test setup)
- **URL construction**: use `urljoin(str(self.base_url), "<path>")` to build paths relative to `BASE_URL`; ensure `from urllib.parse import urljoin` is at the top of `main_page.py`
- **No `MainPageLocators` entry** required — URL-based features skip the link-click entirely
- **Return**: `return <FeaturePage>(self.driver)` — same as standard pattern

---

## Section 8: Pytest Markers

All markers registered in `pyproject.toml`. `--strict-markers` is enforced — using an unregistered marker causes a collection error.

**Registered markers** (must only use these — `--strict-markers` is enforced):

| Marker | Purpose |
| --- | --- |
| `@pytest.mark.ui` | Triggers `setUp` auto-navigation to `BASE_URL`; required on all the-internet UI tests |
| `@pytest.mark.regression` | Full regression suite; required on all generated tests |
| `@pytest.mark.smoke` | Critical path only; added explicitly, never by default |
| `@pytest.mark.api` | API tests only |
| `@pytest.mark.fix` | Marks tests needing human review; added by healer, never by generator |

**Standard pytest markers** (always available, no registration required):

| Marker | When to use |
| --- | --- |
| `@pytest.mark.skip(reason="...")` | Applied at **class** level when an entire feature is not yet implemented |
| `@pytest.mark.skipif(condition, reason="...")` | Applied at **method** level for runtime conditions (e.g., `os.getenv("BROWSER") == "firefox"`) |
| `@pytest.mark.xfail(reason="...")` | Applied at **method** level for tests expected to fail intermittently (e.g., flaky external dependencies); the test still runs — a pass becomes `XPASS` |
| `pytest.skip("reason")` | Called **inside** a test method body for conditional skips based on runtime state (e.g., page source check); not a decorator |

---

## Section 9: Allure Severity Mapping

| Allure Level | Scenario Type |
| --- | --- |
| `CRITICAL` | Core happy path — the site fundamentally breaks without this test passing |
| `NORMAL` | Important negative / error flows — wrong credentials, invalid input |
| `MINOR` | Edge cases, secondary feature behavior |
| `TRIVIAL` | Cosmetic, rarely-hit paths |

---

## Section 10: What Belongs Where — Quick Reference

| Concern | Location |
| --- | --- |
| Selector strings | `locators.py` only — nowhere else |
| Test data constants (credentials, expected messages) | Module level in test file |
| Element wait logic | Page object methods via `BasePage` |
| Assertions | Test methods only |
| `self.logger.info(...)` | Test methods only |
| `@allure.step(...)` | Page object methods only |
| `@pytest.mark.*` | Test methods only |
| Page-to-page navigation (returns new page object) | Page object method |
| `MainPage` navigation (click homepage link) | `main_page.py` nav method |

---

## Section 11: Advanced Page Object Patterns

These patterns apply to specific feature types. Use them only when the standard pattern is insufficient.

### Returning a dataclass instead of a page object

When a method returns multiple values from a single interaction, define a `@dataclass` in the same page object file and return it:

```python
from dataclasses import dataclass

@dataclass
class ClickResult:
    alert_present: bool
    alert_text: str = ""


class ContextMenuPage(BasePage):
    @allure.step("Perform right click outside hot spot area")
    def right_click_outside_hot_spot(self) -> ClickResult:
        self.perform_right_click(ContextMenuPageLocators.PAGE_LOADED_INDICATOR)
        return ClickResult(alert_present=False)
```

*(Source: `src/pages/features/context_menu/context_menu_page.py`)*

Rules:
- Dataclass defined **in the same file** as the page object, not in a separate file
- Dataclass placed **above** the page object class definition
- Add `from dataclasses import dataclass` to the page object file imports

### Local imports inside page object methods (circular import workaround)

When two page objects reference each other, use a local import inside the method that returns the other page:

```python
@allure.step("Click login - correct")
def click_login_correct(self) -> "SecureAreaPage":
    self.click_element(FormAuthenticationPageLocators.LOGIN_BTN)
    from src.pages.features.form_authentication.secure_area_page import SecureAreaPage
    return SecureAreaPage(self.driver)
```

Only use this when a top-level import would create a circular dependency. Prefer top-level imports wherever possible.

### Parameterized tests with `@parameterized.expand`

**Always use `@parameterized.expand` — never `@pytest.mark.parametrize`.**

`@pytest.mark.parametrize` does not work with `unittest.TestCase`-based classes. SeleniumBase's `BaseCase` extends `unittest.TestCase`, so `@pytest.mark.parametrize` silently skips or errors on these tests. `@parameterized.expand` generates real test methods at class-definition time and is fully compatible.

Use `@parameterized.expand` for data-driven tests where the same scenario must run against multiple inputs:

```python
from parameterized import parameterized

# Data table at module level (above the class):
OPTIONS = [["Option 1"], ["Option 2"]]

@allure.parent_suite("the-internet")
@allure.suite("UI Test Suite")
@allure.sub_suite("Dropdown List")
class TestDropdownList(UiBaseCase):
    @parameterized.expand(OPTIONS)
    @pytest.mark.regression
    @pytest.mark.ui
    @allure.severity(allure.severity_level.NORMAL)
    def test_dropdown_list_functionality(self, option: str) -> None:
        self.logger.info("Tests Dropdown List functionality.")
        ...
```

*(Source: `tests/the_internet/ui_test_suite/test_dropdown_list.py`)*

Rules:
- `@parameterized.expand` is the **outermost** decorator — above all `@pytest.mark.*` and `@allure.*` decorators
- The data table is defined at **module level** (above the class), not inline in the decorator
- Test parameters are declared as explicit typed arguments after `self`
- Include `@pytest.mark.ui` when the test navigates via `MainPage` (standard `click_*` link pattern)
- Omit `@pytest.mark.ui` when the test uses credential-URL navigation via `get_<feature>_page()` (e.g., digest auth tests), since `setUp` auto-navigation is not needed

### Multi-level navigation chaining

When a feature page links to a sub-page, chain navigation calls instead of navigating via URL directly:

```python
main_page = MainPage(self)
frames_page = main_page.click_frames_link()
iframe_page = frames_page.click_iframe_link()
```

Each chained call returns the next page object. The test then operates on the final page object in the chain.
