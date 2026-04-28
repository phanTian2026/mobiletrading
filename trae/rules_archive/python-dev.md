---
globs: ["**/*.py"]
---

# Python 开发规范

## 编码风格
- **PEP 8** + **black**（line-length=120）+ **ruff**
- 函数签名必须有**类型注解**
- 优先使用不可变数据结构（`frozen dataclass`、`NamedTuple`）
- 使用上下文管理器（`with`）管理资源，用生成器做惰性求值

## 测试
- 框架：**pytest**
- 覆盖率：`pytest --cov=因子库 --cov-report=term-missing`
- 用 `pytest.mark.unit` / `pytest.mark.integration` 分类

## 安全
- 敏感信息通过 `env.py` 管理，绝不硬编码
- 用 `ruff check .` 做静态分析

## 性能
- `n_jobs`：默认 `cpu_count()-3`，内存不足时降低
- `factor_col_limit`：默认8（16G内存），32G可提到12~16
- 避免因子函数中创建大型中间 DataFrame，及时 `del` + `gc.collect()`
- 上下文窗口较大任务应在前 80% 内完成

## 详细参考
- Skill: `coding-standards` — 项目编码标准
- Skill: `python-patterns` — Python 惯用法
- Skill: `python-testing` — 测试策略
- Skill: `security-review` — 安全审查
