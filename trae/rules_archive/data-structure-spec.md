---
description: COIN（币圈）数据结构规范。定义K线数据、外部数据（如 coin-cap）、以及合并对齐的时间规则。
globs: ["**/*.py", "**/config.py", "**/factors/*.py"]
---

# 币圈量化底层数据结构规范（COIN｜TRAE）

目标：让“因子/信号/回测”都在同一套字段和时间对齐规则下工作，避免因为字段含义不一致或时间戳对齐错误导致的结果失真。

生活类比：数据表就是仓库里的“箱子标签”。标签贴错（字段含义错、时间错）就会把快递送错人（回测结论错）。

## 1. 核心对齐键

在 COIN 工作区里，大多数计算以以下两列对齐：

- `symbol`：交易对/合约标的（示例：`BTC-USDT`）
- `candle_begin_time`：K 线开始时间（建议为 UTC 或与数据源一致的时区，但必须全项目统一）

约定：

- `candle_begin_time` 表示这根 K 线覆盖的时间区间起点；该 K 线的 OHLCV 是在区间结束后才“完全确定”的。
- 若策略在“下一根 K 线开盘”成交，则所有用于决策的因子/信号都应整体 `shift(1)`。

## 2. K 线 DataFrame（df）字段规范

### 2.1 必备字段（最小集合）

以下字段为最常用最小集合，因子实现默认可依赖：

- `candle_begin_time`：datetime
- `symbol`：str
- `open` / `high` / `low` / `close`：float
- `volume`：float（基础成交量，单位以数据源为准）

### 2.2 常用增强字段（建议存在）

不同框架/预处理可能提供更多列，常见包括：

- `quote_volume`：计价成交量（例如 USDT 计价）
- `avg_price_1m` / `avg_price_5m`：用于更贴近成交的均价列（实盘/回测一致性关键）
- `funding_rate`：资金费率（通常为外部数据或合并字段）
- `open_interest`：未平仓量（通常为外部数据或合并字段）
- `is_trade`：是否可交易标记（新币、停牌式异常、数据缺失等过滤用）

## 3. 外部数据（extra_data_dict）字段规范

在 `position-mgmt_v2.1.0/factors/*.py` 中，如果因子需要额外字段（不在 K 线 df 内），用：

```python
extra_data_dict = {
    "数据源标签": ["字段1", "字段2"]
}
```

数据源标签需要与 `config.py -> data_source_dict` 的 key 一致。

### 3.1 coin-cap（市值/供给相关）

用于市值、流通市值、供给变化等因子。常见字段（以实际数据为准）：

- `circulating_supply`：流通供给
- `total_supply`：总供给（若有）
- `max_supply`：最大供给（若有）

典型用法（示例逻辑）：`circulating_mcap = circulating_supply * close`

参考因子：`position-mgmt_v2.1.0/factors/CirculatingMcap.py`

### 3.2 coin-btc（对照序列/基准）

用于构造相对 BTC 的收益/相关性等。常见字段（以实际数据为准）：

- `btc_close` 或类似字段（用于计算对照收益）

## 4. 时间对齐与合并规则（最重要）

合并外部数据时必须满足“过去→现在”的对齐，避免把未来一条数据合并进来。

最小规则：

- 任何外部数据的时间戳必须能明确映射到 `candle_begin_time`
- 当外部数据频率低于 K 线频率（例如日频 vs 1H），必须明确“当天数据何时可得”
  - 如果无法确定可得时间，默认只能从次日开始使用（更保守但更安全）

## 5. 交易成本相关字段（用于回测一致性）

策略结果是否“可交易”，很大程度取决于成本假设是否一致。常见成本相关配置（由框架配置，不一定在 df 内）：

- 手续费（现货/合约）
- 滑点假设（有时被并入手续费）
- 最小下单额限制
- 杠杆/维持保证金率（爆仓风险）

建议在分析策略时同时检查：`position-mgmt_v2.1.0/config.py -> simulator_config`

