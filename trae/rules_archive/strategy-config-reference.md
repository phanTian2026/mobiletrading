---
globs: ["position-mgmt_v2.1.0/config.py", "position-mgmt_v2.1.0/factors/**", "**/config.py"]
---

# 策略配置参考（COIN｜币圈）

本文件描述 COIN 工作区里常见的“币圈轮动/多空策略”配置方式，重点以 `position-mgmt_v2.1.0/config.py` 的结构为参考。

生活类比：配置就像写“分拣规则”。你告诉系统用什么标签（因子）给每个币打分，然后按分数挑前几名去买/卖。

## 1. 核心入口

- 策略配置参考：`position-mgmt_v2.1.0/config.py`
- 因子实现目录：`position-mgmt_v2.1.0/factors/`

## 2. strategy_config（多策略轮动总配置）

常见字段（以实际代码为准）：

- `hold_period`：基础 K 线周期（例如 `1H`）
- `rotation_period`：轮动周期（例如 `6H`，每 6 小时换一次）
- `offset_list`：轮动错峰组（例如 `[0, 6]`）
- `select_num`：选币数量（例如 `1`）
- `factor_list`：综合排序因子列表（见第 4 节）
- `rotation_group`：多组资金配比（例如 多头组/空头组）

## 3. strategy_pool（子策略池：多空配对/多池子）

常见字段（以实际代码为准）：

- `market`：交易市场（例如 `mix_swap`）
- `hold_period`：持仓周期（例如 `6H`）
- `offset_list`：分散调仓偏移（例如 `list(range(0, 24, 1))`）
- `long_factor_list` / `short_factor_list`：多头/空头各自排序因子列表（见第 4 节）
- `filter_list`：交易池过滤（见第 5 节）

## 4. 排序因子配置（factor_list / long_factor_list / short_factor_list）

在币圈框架里，常用的因子元组格式为 4 元素：

```python
(factor_name, is_sort_asc, param, weight)
```

- `factor_name`：对应 `position-mgmt_v2.1.0/factors/{factor_name}.py`
- `is_sort_asc`：`False` 表示值越大排名越靠前，`True` 相反
- `param`：因子参数（最常见是窗口 n，例如 24 根 1H K 线）
- `weight`：权重（多因子加权排序时使用）

示例：

```python
('MomentumStrength', False, 24, 0.5)
('ZfMeanQ', False, 24, 0.3)
('Bias', False, 120, 0.2)
```

## 5. 过滤条件（filter_list）

过滤用于“先把明显不该交易的币排掉”，再做排序。

常见元组格式（以框架支持为准）：

```python
(factor_name, param, filter_rule, is_sort_asc)
```

- `filter_rule` 格式：`"<how>:<op><val>"`
  - `pct:` 按百分位过滤（更常用）
  - `rank:` 按名次过滤
  - `val:` 按数值过滤
- 比较符：`>= <= == != > <`
- 过滤规则的含义是“保留满足条件的”

示例（来自本工作区配置风格）：

```python
('PctChangeMax', 24, 'pct:<0.3', False)
```

## 6. 外部数据（data_source_dict / extra_data_dict）

当因子依赖外部字段（例如 coin-cap 的 circulating_supply）：

- `config.py -> data_source_dict` 声明数据源标签与加载器/路径
- 因子文件通过 `extra_data_dict` 声明所需字段

关键约束：外部数据必须与 K 线时间戳严格对齐，避免未来函数。
