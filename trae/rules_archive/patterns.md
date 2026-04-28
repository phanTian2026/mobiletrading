# Python 常用模式

> 本文件在 [common/patterns.md](../common/patterns.md) 基础上补充 Python 细则。

## Protocol（鸭子类型）

```python
from typing import Protocol

class Repository(Protocol):
    def find_by_id(self, id: str) -> dict | None: ...
    def save(self, entity: dict) -> dict: ...
```

## dataclass 作为数据传递对象

```python
from dataclasses import dataclass

@dataclass
class CreateUserRequest:
    name: str
    email: str
    age: int | None = None
```

## 上下文管理器与生成器

- 用上下文管理器（`with`）管理资源
- 用生成器做惰性求值与节省内存的遍历

## 参考

详见 skill：`python-patterns`
