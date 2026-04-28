---
globs: ["因子库/**", "因子库(600+因子)/**", "截面因子库/**"]
---

# 因子库使用规则

## 两个因子库的区别

- `因子库/` — **官方因子库**，可被系统 FactorHub 通过 `importlib.import_module("因子库.{name}")` 自动索引和加载
- `因子库(600+因子)/` — **扩展因子库**，包含 606 个因子，**不可被系统直接索引**

## 使用扩展因子的步骤

当需要使用 `因子库(600+因子)/` 中的因子时，**必须先将该因子文件复制到 `因子库/` 目录**，然后才能在 config 中引用。

```bash
cp "因子库(600+因子)/Macd.py" "因子库/Macd.py"
```

## 因子加载机制

1. FactorHub (`core/utils/factor_hub.py`) 通过 `importlib.import_module` 动态加载因子
2. 每个因子文件必须包含 `add_factor(df, param, **kwargs)` 函数
3. 因子通过 config 中的 `factor_list` 和 `filter_list` 引用（按文件名，不含 .py）
4. 可选属性：`fin_cols`（财务列）、`extra_data`（额外数据）、`is_cross`（截面因子）

## 因子引用格式

```python
# factor_list: (因子名, 是否升序, 参数, 权重)
("ROE", False, "单季", 0.9)

# filter_list: (因子名, 参数, 条件)
("成交额Mean", 5, "val:>=2000_0000")
```

## 注意事项

- 两个库有 44 个同名因子，复制时注意不要覆盖已有的官方版本（除非确认要替换）
- 扩展因子库中有 `AAA_606因子查询表.md` 作为因子速查参考
- 官方库有 162 个因子，其中 118 个是官方库独有的

## 因子预选与目录查询

项目共有 **966 个因子**（基础因子库 173 + 扩展因子库 793）。使用 `tools/factor_catalog.py` 进行因子预选，详见 `docs/因子目录工具使用指南.md`。

### 因子预选工作流（策略优化时必读）

```
Step 1: 维度缺口分析 → python tools/factor_catalog.py --strategy config_xxx
Step 2: 浏览候选因子 → python tools/factor_catalog.py --category 资金流
Step 3: 查看因子详情 → python tools/factor_catalog.py --detail DDX
Step 4: 搜索特定因子 → python tools/factor_catalog.py --search 流通市值
Step 5: 选择候选 → 从每个缺失维度选 2-3 个代表性因子加入 config
Step 6: 批量计算 → 运行一次增强版回测（计算新因子）
Step 7: 快速迭代 → 后续调权重/组合只需 选股+回测.py
```

因子目录数据（`tools/因子目录.json`）包含：分类（27维度）、使用列、运算类型、数据维度、参数用途、选股/过滤案例等。
新增因子后刷新：`python tools/factor_catalog.py --refresh`

因子所依赖的底层数据表、字段含义、编码等，请参考 [`data-structure-spec.md`](./data-structure-spec.md)。
