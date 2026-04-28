# Python 安全

> 本文件在 [common/security.md](../common/security.md) 基础上补充 Python 细则。

## 密钥管理

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["OPENAI_API_KEY"]  # 如果缺失会抛 KeyError
```

## 安全扫描

- 使用 **bandit** 做静态安全检查：
  ```bash
  bandit -r src/
  ```

## 参考

如项目使用 Django，参考 skill：`django-security`
