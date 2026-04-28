# 项目规则（TRAE）

## 项目目标

币圈量化回测/选币/轮动/仓位管理：编写因子/策略/信号/配置，运行回测与（可选）实盘产出结果。

## 强制约束（必须遵守）

1. 禁止未来函数（前视偏差）
   - 核心：任何用于交易决策的数据时间必须 ≤ 交易执行时间（像“考试时偷看答案”一样，回测会虚高）。
   - 速查：日内定时换仓时，择时因子时间点必须 ≤ `rebalance_time` 的买入时间。
   - 细则： [future-function-prevention.md](../rules_archive/future-function-prevention.md)
2. 禁止修改框架主干（除非用户明确确认）
   - 核心：你当前在用的币圈框架目录（例如 `position-mgmt_v2.1.0/`、`select-coin-pro_v2.0.0/`）下的 `core/` 与主流程脚本视为“上游仓库”，默认只在扩展点新增/改动（`factors/`、`signals/`、策略配置 `config.py` 等）。
   - 细则： [framework-protection.md](../rules_archive/framework-protection.md)
3. 长任务先冒烟测试（预计 >10 分钟必须先跑 1–3 分钟验证）
   - 核心：先用短日期/少组合跑通全链路，确认能出结果，再跑全量（像先点“试运行”再点“正式运行”）。
   - 细则： [smoke-test.md](../rules_archive/smoke-test.md) / [long-running-commands.md](../rules_archive/long-running-commands.md)
4. 除法安全（防止除零异常）
   - 核心：所有 `A / B` 一律写成 `A / (B + 1e-8)`（像给分母加“防滑垫”，避免 0 或极小值摔跤）。
   - 细则： [safe-math.md](../rules_archive/safe-math.md)

## 规则索引（先查目录，再看细则）

使用方法（像翻目录一样）：

1. 先在下表里按“你正在做的事”找到对应规则文件
2. 只打开那 1–2 个规则文件读细则
3. 若涉及修改代码：先满足“强制约束”，再做实现

### 自动按需加载（关键词路由）

目标：让你不用手动点“书柜”，我会根据你说的话自动去 `rules_archive` 把对应细则“取出来放桌上”，再开始回答。

规则：当用户的描述命中下列任一触发词/意图时，助手在给方案前，必须先读取对应细则文件（通常 1–2 个，最多不超过 3 个）。

- 新建/修改因子（如："新建一个大市值因子"、"写个动量因子"）→ `factor-library.md` +（需要时）`python-dev.md` / `safe-math.md`
- 回测不对/怀疑穿越（如："结果太好不真实"、"可能有未来函数"、"是不是用到了未来K线"）→ `future-function-prevention.md`
- 回测很慢/参数遍历很慢（如："怎么加速"、"批量搜索参数"）→ `backtest-optimization.md` +（需要时）`param-search-optimization.md` / `long-running-commands.md` / `smoke-test.md`
- 想改 `core/` / 主流程脚本（如："改回测引擎"）→ `framework-protection.md`
- 涉及密钥/账号（如："填API Key"、"读取env"）→ `security.md`

### 按场景查规则

| 你正在做的事 | 先看这个（入口） | 需要时再看（细则） |
|---|---|---|
| 写新因子 / 改因子 | [factor-library.md](../rules_archive/factor-library.md) | [python-dev.md](../rules_archive/python-dev.md)、[safe-math.md](../rules_archive/safe-math.md)、[future-function-prevention.md](../rules_archive/future-function-prevention.md) |
| 回测结果不对 / 怀疑有穿越 | [future-function-prevention.md](../rules_archive/future-function-prevention.md) | [strategy-evaluation.md](../rules_archive/strategy-evaluation.md)、[smoke-test.md](../rules_archive/smoke-test.md) |
| 回测太慢 / 参数搜索太慢 | [backtest-optimization.md](../rules_archive/backtest-optimization.md) | [param-search-optimization.md](../rules_archive/param-search-optimization.md)、[long-running-commands.md](../rules_archive/long-running-commands.md) |
| 需要改框架底层（core/ 等） | [framework-protection.md](../rules_archive/framework-protection.md) | [framework-technical-spec.md](../rules_archive/framework-technical-spec.md)、[data-structure-spec.md](../rules_archive/data-structure-spec.md) |
| 需要写测试 / 保证不改坏 | [testing.md](../rules_archive/testing.md) | [smoke-test.md](../rules_archive/smoke-test.md) |
| 涉及账号/密钥/安全 | [security.md](../rules_archive/security.md) | [git-workflow.md](../rules_archive/git-workflow.md) |

## 质量基线（默认执行）

- Python：PEP 8 + 类型标注；black/ruff 统一风格： [python-dev.md](../rules_archive/python-dev.md) / [coding-style.md](../rules_archive/coding-style.md)
- 测试：pytest： [testing.md](../rules_archive/testing.md)
- 密钥：仅环境变量： [security.md](../rules_archive/security.md)

## 命令白名单与限制

- 默认只使用以下几类命令，除非用户明确要求且经过风险说明：
  - Python 运行相关：`python *.py`、`python -m *`
  - 代码格式与静态检查：`black`、`ruff check`、`ruff format`
  - Git 操作：`git status/diff/log/add/commit/push/pull/branch/checkout`
  - 包管理：`pip install`（仅安装项目需要的依赖）、`pip list`
  - 文件查看与统计：`cat`、`ls`、`find`、`head`、`tail`、`wc`、`grep`
  - 目录/文件管理：`mkdir [-p]`、`cp [-r]`、`mv`
- 禁止执行具有破坏性或高风险的命令，例如：
  - `rm -rf`、`sudo`、系统级服务管理、磁盘/网络配置等
  - 任意不在上述白名单中的命令（除非用户明确同意）


## 任务模板（按需引用）

- plan： [plan.md](../commands/plan.md)
- quant-debug： [quant-debug.md](../commands/quant-debug.md)
- factor-research： [factor-research.md](../commands/factor-research.md)
- strategy-analyze / strategy-optimize： [strategy-analyze.md](../commands/strategy-analyze.md) / [strategy-optimize.md](../commands/strategy-optimize.md)

## 币圈框架参考（按需）

- 币圈回测配置示例：[`position-mgmt_v2.1.0/config.py`](../../position-mgmt_v2.1.0/config.py)
- 因子实现示例：[`position-mgmt_v2.1.0/factors/PctChange.py`](../../position-mgmt_v2.1.0/factors/PctChange.py)
