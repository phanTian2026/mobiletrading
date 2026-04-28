# Git 工作流

## 提交信息格式

```
<类型>: <说明>

<可选正文>
```

类型：feat、fix、refactor、docs、test、chore、perf、ci

备注：已在 `settings.json` 全局关闭 attribution。

## PR 流程

创建 PR 时：
1. 分析完整提交历史（不只看最后一次提交）
2. 用 `git diff [base-branch]...HEAD` 查看全部改动
3. 写清楚 PR 总结（覆盖所有改动点）
4. 写测试计划（含 TODO）
5. 新分支推送时加 `-u`

## 功能开发流程

1. **先做计划**
   - 用 planner 角色输出实施计划
   - 标出依赖与风险
   - 分阶段拆解

2. **TDD**
   - 用 tdd-guide 角色
   - 先写失败测试（RED）
   - 写最小实现让测试通过（GREEN）
   - 重构（IMPROVE）
   - 覆盖率 ≥ 80%

3. **代码审查**
   - 写完立刻用 code-reviewer 角色审查
   - 必须修复 CRITICAL/HIGH
   - 尽量修复 MEDIUM

4. **提交与推送**
   - 提交信息写清楚
   - 遵循约定式提交规范
