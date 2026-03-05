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
| Test | `tests/the_internet/ui_test_suite/test_<feature>.py` | `TestXxx(UiBaseCase)` |

### What belongs in each layer

**Locators layer** (`locators.py`)

- Class attributes only — no methods, no `__init__`, no class inheritance
- Every selector string lives here and **only** here — never hardcoded in page objects or tests
- Attribute type: `Locator` dict

**Page Object layer** (`<feature>_page.py`)

- All element interaction goes through `BasePage` methods — never `self.driver.find_element()` directly
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
- **Test data constants**: defined at **module level** (above the class), never inside the class or methods

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

### Navigation method

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

---

## Section 8: Pytest Markers

All markers registered in `pyproject.toml`. `--strict-markers` is enforced — using an unregistered marker causes a collection error.

| Marker | Purpose |
| --- | --- |
| `@pytest.mark.ui` | Triggers `setUp` auto-navigation to `BASE_URL`; required on all the-internet UI tests |
| `@pytest.mark.regression` | Full regression suite; required on all generated tests |
| `@pytest.mark.smoke` | Critical path only; added explicitly, never by default |
| `@pytest.mark.api` | API tests only |
| `@pytest.mark.fix` | Marks tests needing human review; added by healer, never by generator |

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
