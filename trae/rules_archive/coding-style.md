# Python 编码风格

> 本文件在 [common/coding-style.md](../common/coding-style.md) 基础上补充 Python 细则。

## 基本规范

- 遵循 **PEP 8**
- 所有函数签名必须有**类型注解**

## 不可变优先

优先使用不可变数据结构：

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    name: str
    email: str

from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
```

## 格式化与检查

- 代码格式化：**black**
- import 排序：**isort**
- 静态检查：**ruff**

## 参考

详见 skill：`python-patterns`
