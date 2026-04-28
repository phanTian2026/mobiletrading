# Python 测试

> 本文件在 [common/testing.md](../common/testing.md) 基础上补充 Python 细则。

## 测试框架

使用 **pytest**。

## 覆盖率

```bash
pytest --cov=src --cov-report=term-missing
```

## 测试组织

用 `pytest.mark` 做分类：

```python
import pytest

@pytest.mark.unit
def test_calculate_total():
    ...

@pytest.mark.integration
def test_database_connection():
    ...
```

## 参考

详见 skill：`python-testing`
