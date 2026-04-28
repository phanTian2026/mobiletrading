# Python 钩子规则

> 本文件在 [common/hooks.md](../common/hooks.md) 基础上补充 Python 细则。

## 工具执行后自动动作（PostToolUse）

在 `settings.json` 配置：

- **black/ruff**：编辑后自动格式化 `.py`
- **mypy/pyright**：编辑后自动做类型检查

## 警告

- 若编辑文件出现 `print()`，提醒改用 `logging`
