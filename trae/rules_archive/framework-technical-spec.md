---
description: COIN（币圈）量化回测/选币/轮动框架技术规范（面向 position-mgmt_v2.1.0 等目录结构）。
globs: ["**/config.py", "**/factors/*.py", "**/signals/*.py"]
---

# 币圈量化框架技术规范（COIN｜TRAE）

目标：用尽量少的“约定”，把回测链路跑稳：数据→因子→选币→模拟交易→结果。

生活类比：框架像一条流水线。你可以换“贴纸机”（因子）、换“分拣规则”（选币），但不要随便改“传送带电机”（core 主干），否则整条线都可能停。

## 1. 框架范围与保护约束

COIN 工作区常见回测/轮动框架目录：

- `position-mgmt_v2.1.0/`（仓位管理/多空轮动）

默认约束：

- `core/` 与主流程脚本视为上游主干，除非用户明确确认，否则只改扩展点：
  - `factors/`
  - `signals/`（若存在）
  - `config.py`（策略配置与参数）

## 2. 关键入口与扩展点

### 2.1 配置入口（config.py）

以 `position-mgmt_v2.1.0/config.py` 为例，常见关键区块：

- 回测区间：`start_date` / `end_date`
- 数据路径：`pre_data_path`
- 策略配置：`strategy_config`、`strategy_pool`
- 交易模拟：`simulator_config`（手续费/滑点/最小下单额/杠杆与维持保证金率）
- 外部数据接入：`data_source_dict`

### 2.2 因子（factors/*.py）

币圈因子实现通常遵循以下接口：

- `signal(*args)`：在 df 上新增一列因子值
  - `args[0]`：df（K线数据）
  - `args[1]`：param（通常是窗口 n）
  - `args[2]`：factor_name（因子列名）
- `signal_multi_params(df, param_list) -> dict`（可选）：同因子多参数聚合提速
- `extra_data_dict`（可选）：声明因子所需外部数据字段（见 2.4）

参考：`position-mgmt_v2.1.0/factors/PctChange.py`、`position-mgmt_v2.1.0/factors/CirculatingMcap.py`

### 2.3 选币与轮动（策略配置层）

典型模式：

- `factor_list`：综合排序（多因子加权）
- `long_factor_list` / `short_factor_list`：多空分别排序
- `filter_list`：交易池过滤（例如单周期极端涨跌幅过滤、上市时间过滤等）
- `rotation_period` / `hold_period` / `offset_list`：轮动节奏与分散调仓

### 2.4 外部数据接入（data_source_dict / extra_data_dict）

用法：`config.py -> data_source_dict` 声明数据源标签与加载器/路径；因子文件通过 `extra_data_dict` 声明需要哪些字段。

示例（思路）：

- `coin-cap`：供给/市值类数据（如 `circulating_supply`）
- `coin-btc`：BTC 对照序列

关键要求：

- 外部数据必须与 K 线时间戳对齐，且不得引入未来数据（见 `future-function-prevention.md`）

## 3. 性能与缓存（避免“跑一次等一天”）

常见性能开关（以 `position-mgmt_v2.1.0/config.py` 为例）：

- `job_num`：并行任务数量
- `factor_col_limit`：一次计算多少列因子（越大越快但越吃内存）
- `cross_section_chunk_size`：截面分片大小，降低峰值内存
- `reserved_cache`：缓存保留策略

强烈建议：

- 新增/修改因子后先做冒烟回测（短区间/少币对）跑通，再全量回测
- 优先给因子实现 `signal_multi_params`，减少重复 rolling 计算

## 4. 回测一致性与风险假设

币圈回测最容易“纸面好看、实盘翻车”的原因通常不是因子本身，而是：

- 手续费/滑点低估
- 资金费率忽略（合约）
- 流动性不足导致的容量问题（下单额越大，越容易滑点/插针）
- 极端行情跳跃风险（插针、单边 squeeze）

因此分析与优化时，必须把 `simulator_config` 当成策略的一部分一起审查。

