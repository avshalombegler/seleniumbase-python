# Notification Messages Test Plan

<!--
  SPEC FORMAT v1.0 — SeleniumBase Python Project
  Generator: sb-generator
  Do not edit manually — update the spec and re-run the generator.
-->

---

## Feature Metadata

| Field | Value |
| --- | --- |
| **Feature name** | Notification Messages |
| **URL** | `/notification_message` |
| **Full URL** | `https://the-internet.herokuapp.com/notification_message` |
| **Feature directory** | `notification_messages` |
| **Page object class** | `NotificationMessagesPage` |
| **Locators class** | `NotificationMessagesLocators` |
| **Test class** | `TestNotificationMessages` |
| **Test file** | `tests/the_internet/ui_test_suite/test_notification_messages.py` |
| **Page object file** | `src/pages/features/notification_messages/notification_messages_page.py` |
| **Locators file** | `src/pages/features/notification_messages/locators.py` |
| **MainPage nav method** | `click_notification_messages_link` |
| **Allure sub_suite** | `Notification Messages` |

---

## Page Elements

| Locator name | Strategy | Selector | Notes |
| --- | --- | --- | --- |
| `PAGE_LOADED_INDICATOR` | `By.CSS_SELECTOR` | `".example h3"` | Confirms page is loaded; both `/notification_message` and `/notification_message_rendered` share the same h3 heading |
| `CLICK_HERE_LINK` | `By.CSS_SELECTOR` | `"a[href='/notification_message_rendered']"` | "Click here" link that triggers navigation to the rendered URL and produces a random flash message |
| `FLASH_MESSAGE` | `By.ID` | `"flash"` | Flash notification container; only present on `/notification_message_rendered`; contains a random message from the known set |
| `FLASH_CLOSE_BUTTON` | `By.CSS_SELECTOR` | `"#flash a.close"` | The `×` dismiss button inside the flash message |

---

## Page Object Methods

The feature uses two pages: `NotificationMessagesPage` (landing at `/notification_message`) and
`NotificationMessageRenderedPage` (at `/notification_message_rendered`). Both are defined in
`notification_messages_page.py`. The locators file defines a single `NotificationMessagesLocators`
class shared by both page objects.

| Method | Signature | Returns | Notes |
| --- | --- | --- | --- |
| `__init__` | `(self, driver: BaseCase)` | `None` | `super().__init__(driver)` then `wait_for_page_to_load(PAGE_LOADED_INDICATOR)` |
| `click_here` | `(self)` | `NotificationMessageRenderedPage` | Clicks `CLICK_HERE_LINK`; returns `NotificationMessageRenderedPage(self.driver)` |

**`NotificationMessageRenderedPage` methods:**

| Method | Signature | Returns | Notes |
| --- | --- | --- | --- |
| `__init__` | `(self, driver: BaseCase)` | `None` | `super().__init__(driver)` then `wait_for_page_to_load(PAGE_LOADED_INDICATOR)` |
| `get_flash_message` | `(self)` | `str` | Returns text of `FLASH_MESSAGE` via `get_dynamic_element_text`; the text includes an embedded `×` from the close button — strip it or assert with `assert_in` on a substring |
| `is_flash_message_visible` | `(self)` | `bool` | Returns `is_element_visible(FLASH_MESSAGE)` |
| `dismiss_flash_message` | `(self)` | `None` | Clicks `FLASH_CLOSE_BUTTON` |
| `click_here` | `(self)` | `NotificationMessageRenderedPage` | Clicks `CLICK_HERE_LINK`; navigates to a new rendered page with a new random message; returns `NotificationMessageRenderedPage(self.driver)` |

---

## Test Scenarios

Each scenario maps to exactly one test method in `TestNotificationMessages`.

---

### Scenario 1: Flash message is rendered after clicking "Click here"

**Method:** `test_flash_message_rendered_on_click`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `CRITICAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/notification_message` via `MainPage.click_notification_messages_link()`
   - `expect:` Landing page loads — verified by `PAGE_LOADED_INDICATOR`

2. Click "Click here" via `page.click_here()`
   - `locator:` `CLICK_HERE_LINK`
   - `expect:` Browser navigates to `/notification_message_rendered` and a flash message becomes visible

3. Retrieve the flash message text via `rendered_page.get_flash_message()`
   - `locator:` `FLASH_MESSAGE`
   - `expect:` Flash message text is one of the three known notification strings

**Assertions:**

```python
self.assert_true(
    self.get_current_url().endswith("/notification_message_rendered"),
    "Expected URL to end with /notification_message_rendered"
)
self.assert_true(
    rendered_page.is_flash_message_visible(),
    "Expected flash message to be visible after clicking 'Click here'"
)
flash_text = rendered_page.get_flash_message()
self.assert_true(
    any(msg in flash_text for msg in EXPECTED_FLASH_MESSAGES),
    f"Expected flash message to be one of {EXPECTED_FLASH_MESSAGES}, got: '{flash_text}'"
)
```

---

### Scenario 2: Flash message can be dismissed

**Method:** `test_flash_message_can_be_dismissed`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/notification_message` via `MainPage.click_notification_messages_link()`
   - `expect:` Landing page loads — verified by `PAGE_LOADED_INDICATOR`

2. Click "Click here" via `page.click_here()`
   - `locator:` `CLICK_HERE_LINK`
   - `expect:` Rendered page loads with a visible flash message

3. Dismiss the flash message via `rendered_page.dismiss_flash_message()`
   - `locator:` `FLASH_CLOSE_BUTTON`
   - `expect:` Flash message disappears from the page

**Assertions:**

```python
self.assert_false(
    rendered_page.is_flash_message_visible(),
    "Expected flash message to be hidden after dismissal"
)
```

---

### Scenario 3: Repeated clicks produce valid flash messages each time

**Method:** `test_repeated_clicks_produce_valid_flash_messages`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `MINOR`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/notification_message` via `MainPage.click_notification_messages_link()`
   - `expect:` Landing page loads — verified by `PAGE_LOADED_INDICATOR`

2. Click "Click here" via `page.click_here()` — first click
   - `locator:` `CLICK_HERE_LINK`
   - `expect:` Rendered page loads with a visible flash message

3. Click "Click here" again via `rendered_page.click_here()` — second click from the rendered page
   - `locator:` `CLICK_HERE_LINK`
   - `expect:` A new rendered page loads with a fresh flash message; message may differ from the first

**Assertions:**

```python
flash_text = rendered_page_2.get_flash_message()
self.assert_true(
    any(msg in flash_text for msg in EXPECTED_FLASH_MESSAGES),
    f"Expected second flash message to be one of {EXPECTED_FLASH_MESSAGES}, got: '{flash_text}'"
)
self.assert_true(
    rendered_page_2.is_flash_message_visible(),
    "Expected flash message to be visible after second click"
)
```

---

### Scenario 4: No flash message on initial landing page load

**Method:** `test_no_flash_message_on_landing_page`
**Markers:** `@pytest.mark.regression`, `@pytest.mark.ui`
**Allure severity:** `NORMAL`
**setUp:** Navigates to `BASE_URL` automatically via `@pytest.mark.ui` — no explicit navigate call needed.

**Steps:**

1. Navigate to `/notification_message` via `MainPage.click_notification_messages_link()`
   - `expect:` Landing page loads — verified by `PAGE_LOADED_INDICATOR`
   - `expect:` No flash message is visible on the initial page load

**Assertions:**

```python
self.assert_false(
    page.is_flash_message_visible(),
    "Expected no flash message to be visible on the initial /notification_message page"
)
```

---

## Out of Scope

| Excluded scenario | Reason |
| --- | --- |
| Asserting a specific exact flash message text | The message is chosen randomly server-side; the test cannot control which of the three messages is returned. Asserting exact text would make the test non-deterministic |
| Asserting the distribution of flash messages across many clicks | Statistical/property-based testing is outside the framework scope |
| Flash message CSS color / styling | Visual regression testing is out of scope |
| Accessibility of the close button (aria labels) | Accessibility auditing is out of scope |
| Network-level assertion that the server randomises the message | Network-level assertions are out of scope |
| Browser back-navigation after dismissal | Not an observable core behavior of the feature; no documented expected outcome |

---

## Test Data

```python
# Expected flash message substrings (server randomly selects one per request)
EXPECTED_FLASH_MESSAGES = [
    "Action successful",
    "Action unsuccessful, please try again",
    "Action unsuccesful, please try again",
]
```

These constants should be defined at module level in the test file (not in the page object or
locators file) so they are visible alongside the assertions that use them.

---

## Generator Notes

- **Two-page feature:** The landing page (`/notification_message`) and the rendered page
  (`/notification_message_rendered`) are two distinct pages. Define two page object classes
  in the single `notification_messages_page.py` file:
  `NotificationMessagesPage` and `NotificationMessageRenderedPage`.
  Both classes share `NotificationMessagesLocators` from `locators.py`.

- **Flash message text contains embedded close button text:** `get_dynamic_element_text` on
  `FLASH_MESSAGE` returns the full text content including the `×` character from the nested
  close button anchor. Use `assert_in` with substring matching (e.g., `"Action successful" in
  flash_text`) rather than exact equality. The `EXPECTED_FLASH_MESSAGES` list contains the
  substrings to check against.

- **Typo in one message variant:** The server is known to emit "Action unsuccesful" (one `s`
  missing in "unsuccessful") as a third variant. Include both the correctly-spelled and the
  typo variant in `EXPECTED_FLASH_MESSAGES` to avoid a false negative.

- **`is_flash_message_visible` in `NotificationMessagesPage`:** The landing page
  (`/notification_message`) never renders `#flash`, so `is_element_visible` with
  `timeout=0` (fast, non-waiting check) should be used in both page objects to avoid
  slowing down the test. Pass `timeout=0` when calling `is_element_visible(FLASH_MESSAGE)`.

- **`dismiss_flash_message` animation:** The flash close button uses a CSS fade-out animation.
  After clicking `FLASH_CLOSE_BUTTON`, call `wait_for_invisibility(FLASH_MESSAGE)` before
  returning from the method so the caller receives control only after the element is gone.

- **`click_here` on `NotificationMessageRenderedPage`:** Re-using `CLICK_HERE_LINK` locator is
  valid — the same `<a href='/notification_message_rendered'>` anchor is present on both pages.
  The method returns a new `NotificationMessageRenderedPage(self.driver)` instance.

- **MainPage registration:** Add `NOTIFICATION_MESSAGES_LINK: Locator = {"selector":
  "Notification Messages", "by": By.LINK_TEXT}` to `MainPageLocators` (alphabetical order
  between `MULTIPLE_WINDOWS_LINK` and the next entry). The homepage link text is
  "Notification Messages".

- **`is_flash_message_visible` in Scenario 4 (`test_no_flash_message_on_landing_page`):** This
  method is called on a `NotificationMessagesPage` instance (not `NotificationMessageRenderedPage`).
  Both page objects must expose `is_flash_message_visible`. Either define it on a shared base or
  duplicate the method in both classes. Duplication is acceptable given the method is a one-liner.
