---
description: "Python 代码审查：PEP 8、类型注解、安全与惯用写法；调用 python-reviewer 角色。"
---

# Python 代码审查

对 Python 代码进行全面审查。

## 工作流程

1. **识别变更文件**：通过 `git diff` 找到修改的 `.py` 文件
2. **运行静态分析**：执行 `ruff check` 和 `black --check`
3. **代码审查**：检查类型注解、错误处理、Pythonic 写法
4. **生成报告**：按严重程度分类

## 自动检查

```bash
# 静态检查与格式化
ruff check .
black --check --line-length=120 .
```

## 审查分类

### CRITICAL（必须修复）
- 未来函数（择时因子时间 > rebalance_time）
- 静默吞掉异常（bare except + pass）
- 硬编码敏感信息
- `[pd.DataFrame()] * N` 共享引用

### HIGH（应该修复）
- 公共函数缺少类型注解
- 可变默认参数 `def f(items=[])`
- 未使用 context manager 管理资源
- 除零未保护（缺少 `+ 1e-8`）

### MEDIUM（建议改进）
- PEP 8 格式问题
- 公共函数缺少 docstring
- 使用 print 而非 logging
- 魔法数字未命名为常量

## 审批标准

| 状态 | 条件 |
|------|------|
| ✅ 通过 | 无 CRITICAL 或 HIGH 问题 |
| ⚠️ 警告 | 仅有 MEDIUM 问题 |
| ❌ 不通过 | 有 CRITICAL 或 HIGH 问题 |

## 量化项目特殊检查

- **未来函数检测**：检查 shift() 方向、择时时间点
- **框架保护**：是否修改了 core/ 目录
- **AI 标记**：新文件是否有 `[AI-GENERATED]` 标记
- **因子规范**：add_factor 是否返回单列 DataFrame，是否使用 col_name
