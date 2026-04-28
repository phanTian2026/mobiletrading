Trae 在量化研究中的高阶用法（整理版）

核心思路

不要把 Trae 当成“代码补全工具”。

要把它当：

- AI 量化研究员
- 编程搭档
- 研究审稿人
- 架构顾问

目标不是写更多代码，而是提高研究速度和研究质量。

---

一、Alpha Researcher（因子研究员）

不是问：

«帮我写个策略»

而是问：

给我20个基于微观结构的 alpha 假设，
要求低相关、可日频实现。

或者：

Challenge this factor:
它可能只是哪些风险暴露伪装出来的？

让它做：

- 生成新假设
- 扩展已有想法
- 从反方角度挑战因子

---

工作流

Obsidian记录 idea
→ Trae 扩展假设
→ 选择若干进入回测

作用：

提升 alpha throughput（因子研究产出速度）。

---

二、Quant Reviewer（量化审稿人）

把回测结果给 Trae：

Sharpe:1.7
Turnover:380%
Capacity: low

让它审稿：

像一个 skeptical PM 一样审查这个策略。

或者：

指出过拟合风险
给 robustness tests checklist

让它像投委会挑刺。

---

重点检查：

- 过拟合风险
- 稳健性问题
- 容量问题
- 风险暴露伪装
- 样本外崩塌风险

用途：

让模型扮演“反对派”。

---

三、Pair Quant Programmer（配对研究编程）

不是让它写整套系统。

让它协助：

- 重构因子代码
- 优化向量化
- 检查 lookahead bias
- 检查 leakage
- 补测试

示例：

检查这段回测代码有没有未来函数。

---

高价值用途：因子变体生成

给这个动量因子生成10个变体
并说明适用 regime

一个因子变多个实验。

---

四、Research Agent（迷你研究代理）

给 Trae 固定研究模板：

收到新alpha后执行：

1 提出理论依据
2 给3个改进版
3 设计回测实验
4 列风险点
5 给上线前 checklist

这样它变成可复用研究流程。

相当于一个初级研究员。

---

五、Repo Copilot（仓库架构顾问）

针对已有成熟框架：

让 Trae 理解整个 repo。

问：

这个 execution 模块和 signal 模块耦合在哪里？

帮我找架构瓶颈

如果我要加 portfolio optimizer
插在哪层最干净？

它是在做架构咨询。

不是自动补全。

---

六、时间分配建议

20%

写代码

40%

研究对话

（最高价值）

30%

结果审稿

10%

架构咨询

大多数人刚好反过来。

---

七、建议建立 Prompt 库（放进 Obsidian）

Prompt 1 — Alpha Generator

Generate orthogonal alpha ideas based on ...

---

Prompt 2 — PM Critic

Destroy this strategy thesis.

---

Prompt 3 — Robustness Auditor

List all robustness tests this strategy needs.

---

Prompt 4 — Code Auditor

Check this backtest for leakage,
lookahead, survivorship bias.

---

Prompt 5 — Regime Researcher

In what regimes should this alpha fail?

这五个提示已经很强。

---

八、把 Trae 接入研究闭环

Idea
↓
Trae挑战假设

Backtest
↓
Trae审稿

优化
↓
Trae生成变体

上线前
↓
Trae做风险review

贯穿整个 alpha 生命周期。

---

一句话总结

普通人把 Trae 当 Copilot。

你应该把 Trae 当：

AI quant researcher
（AI量化研究员）

这是本质区别。