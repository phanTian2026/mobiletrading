---
name: xbx-factors-modify
description: 邢不行量化因子设计规范（COIN｜币圈）- 用于在 position-mgmt_v2.1.0 等币圈框架下创建和修改因子文件。
---

# 邢不行量化因子设计规范（COIN｜币圈）

本 skill 用于指导在 COIN 工作区的币圈框架下进行因子设计与修改，确保因子文件能被框架正确调用，并尽量避免未来函数。

生活类比：因子就是给每根 K 线贴标签的机器。标签贴错时间（用到下一根 K 线的信息）就等于偷看答案，回测会虚高，实盘一定翻车。

## 1. 因子放哪里

- `position-mgmt_v2.1.0/factors/`
- 模板文件：`.trae/skills/xbx-factors-modify/factor_template.py`

## 2. 因子文件必须提供什么

### 2.1 signal（必须）

```python
def signal(*args):
    df = args[0]
    param = args[1]
    factor_name = args[2]
    n = int(param) if param else 24
    df[factor_name] = df["close"].pct_change(n)
    return df
```

约定解释：

- `df` 是单币对的 K 线数据表
- `factor_name` 是输出列名（框架传入），直接写入 `df[factor_name]`
- `param` 通常是窗口 n（例如 24 根 1H K 线）

### 2.2 signal_multi_params（强烈建议）

当一个因子需要计算多个参数（例如 12/24/48），建议实现聚合计算以提速：

```python
def signal_multi_params(df, param_list) -> dict:
    ret = {}
    for param in param_list:
        n = int(param)
        ret[str(param)] = df["close"].pct_change(n)
    return ret
```

## 3. 外部数据（需要时才用）

如果因子需要外部字段（例如 coin-cap 的 circulating_supply），在因子文件里声明：

```python
extra_data_dict = {
    "coin-cap": ["circulating_supply"],
}
```

规则：

- key 必须与 `position-mgmt_v2.1.0/config.py -> data_source_dict` 的 key 一致
- 合并外部数据必须严格做时间对齐，避免引入未来数据

## 4. 数据列约定（币圈K线）

常见可用列（以实际预处理数据为准）：

- 时间：`candle_begin_time`
- 价格：`open/high/low/close`
- 成交：`volume`（可能还有 `quote_volume`）
- 模拟成交价：可能存在 `avg_price_1m` 等列（由框架/预处理提供）

## 5. 绝对底线（防踩坑）

- 禁止未来函数：用于交易决策的数据时间必须 ≤ 交易执行时间；不确定就保守 `shift(1)`
- 除法安全：任何 `A / B` 一律写成 `A / (B + 1e-8)`
- 先冒烟回测：短区间/少币对跑通全链路，再全量回测

## 6. 使用方式（把因子接进策略）

1. 把新因子文件放入 `position-mgmt_v2.1.0/factors/`
2. 在 `position-mgmt_v2.1.0/config.py` 的 `factor_list`（或多空的 `long_factor_list/short_factor_list`）里引用：

```python
('MyFactor', False, 24, 0.3)
```

