# 角色编排 — 量化策略研究体系

## 可用角色（斜杠命令）

| 命令 | 角色 | 触发场景 | 模型 |
|------|-----------|----------|------|
| `/factor-research` | 因子研究员 | 开发因子、分析因子有效性、因子组合 | opus |
| `/strategy-analyze` | 策略分析师 | 诊断策略表现、找问题、归因分析 | opus |
| `/strategy-optimize` | 策略优化师 | 参数调优、因子替换、生成优化配置 | sonnet |
| `/signal-design` | 择时信号设计师 | 设计新择时信号、信号集成、信号评估 | opus |
| `/portfolio-review` | 组合评审官 | 多策略组合分析、配权优化、策略淘汰 | opus |
| `/quant-debug` | 量化诊断专家 | 回测异常、报错、未来函数检测、问题排查 | sonnet |
| `/market-regime` | 市场研判员 | 分析市场状态、策略适配、BTC主导/波动/拥挤度 | opus |

## 保留的通用角色

| 命令 | 用途 |
|------|------|
| `/plan` | 复杂任务的实施规划 |
| `/python-review` | Python 代码质量审查 |
| `/learn` | 从会话中提取可复用模式 |
| `/checkpoint` | 保存当前进度 |
| `/tdd` | 测试驱动开发 |
| `/update-docs` | 更新文档 |

## 角色使用原则

### 策略研究类任务的角色选择

```
用户说「写个新因子」      → /factor-research
用户说「分析这个策略」    → /strategy-analyze
用户说「优化参数」        → /strategy-optimize
用户说「设计择时信号」    → /signal-design
用户说「评审组合配置」    → /portfolio-review
用户说「回测结果不对」    → /quant-debug
用户说「现在该用什么策略」→ /market-regime
```

### 多角色协作场景

**场景 1：完整策略开发**
1. `/factor-research` — 开发/筛选因子
2. `/strategy-analyze` — 设计策略逻辑
3. `/strategy-optimize` — 参数优化
4. `/quant-debug` — 验证无未来函数

**场景 2：策略体检**
1. `/strategy-analyze` — 诊断问题
2. `/portfolio-review` — 评估组合影响
3. `/market-regime` — 判断当前适配性

**场景 3：择时升级**
1. `/signal-design` — 设计新信号
2. `/quant-debug` — 验证信号正确性
3. `/strategy-optimize` — 调整参数

## 并行执行

对独立的分析任务，始终使用并行任务执行：
```
# 好：并行分析多个策略
同时启动 3 个 /strategy-analyze 分析不同策略

# 好：并行因子筛选
同时启动 /factor-research 分析 5 个候选因子
```
