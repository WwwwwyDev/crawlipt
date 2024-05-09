---
description: action和condition方法定义时，参数名应避开这些关键词（drvier、store、xpath、css需要显式定义才能生效）
---

# 关键词

| 关键词          | 说明                                                                                                                                                                                  |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| method       | 指明action方法名称                                                                                                                                                                        |
| condition    | 指明condition方法名称                                                                                                                                                                     |
| next         | 下一步操作脚本                                                                                                                                                                             |
| if           | judge关键词                                                                                                                                                                            |
| check        | judge关键词                                                                                                                                                                            |
| loop         | loop关键词                                                                                                                                                                             |
| while        | loop关键词                                                                                                                                                                             |
| return\_flag | 返回值标记关键词                                                                                                                                                                            |
| store        | 存储器关键词，显式定义后会自动传入                                                                                                                                                                   |
| driver       | <p>添加的action以及condition方法必须包含driver。driver类型需要如下:</p><pre class="language-python"><code class="lang-python">from selenium.webdriver.remote.webdriver import WebDriver
</code></pre> |
| xpath        | 显式定义后会自动在执行前进行隐式等待                                                                                                                                                                  |
| css          | 显式定义后会自动在执行前进行隐式等待                                                                                                                                                                  |

