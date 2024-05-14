---
description: >-
  When defining action and condition methods, parameter names should avoid these
  keywords (drvier, store, xpath, css need to be explicitly defined to take
  effect)
---

# Keyword

| keywords     | introduction                                                                                                                                                                                                                               |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| method       | Indicate the name of the action method                                                                                                                                                                                                     |
| condition    | Indicate the name of the condition method                                                                                                                                                                                                  |
| next         | Next Action Script                                                                                                                                                                                                                         |
| if           | 'judge' keyword must appear simultaneously with method                                                                                                                                                                                     |
| check        | 'judge' keyword, 'check' priority higher than 'if'                                                                                                                                                                                         |
| loop         | 'loop' keyword, 'loop' priority is higher than 'check'                                                                                                                                                                                     |
| while        | Keyword within 'loop'                                                                                                                                                                                                                      |
| return\_flag | Return value tag keywords                                                                                                                                                                                                                  |
| store        | Memory keywords will be automatically passed in after explicit definition                                                                                                                                                                  |
| driver       | <p>The added action and condition methods must include a driver. The driver type needs to be as follows:</p><pre class="language-python"><code class="lang-python">from selenium.webdriver.remote.webdriver import WebDriver
</code></pre> |
| xpath        | Explicitly defined will automatically perform implicit waiting before execution                                                                                                                                                            |
| css          | Explicitly defined will automatically perform implicit waiting before execution                                                                                                                                                            |
| fail\_script | Execute the script when the condition result is False                                                                                                                                                                                      |
