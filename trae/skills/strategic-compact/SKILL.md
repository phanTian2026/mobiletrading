---
name: strategic-compact
description: 在合适的阶段边界建议手动压缩上下文，避免自动压缩打断任务。
---

# 分阶段压缩上下文（Strategic Compact）

在合适的节点建议手动 `/compact`，不要依赖随机触发的自动压缩。

## 为什么要分阶段压缩

自动压缩可能在随机时刻触发：
- 容易在任务中途压缩，丢上下文
- 不理解“阶段边界”
- 可能打断多步骤任务

建议在阶段边界压缩：
- 探索结束 → 开始实现之前
- 一个里程碑完成之后
- 任务主题切换之前

## 工作方式

`suggest-compact.sh` 在 PreToolUse（Edit/Write）阶段运行：

1. 统计工具调用次数
2. 达到阈值后提示（默认 50 次）
3. 超过阈值后每 25 次提醒一次

## Hook Setup

加入 `settings.json`：

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "tool == \"Edit\" || tool == \"Write\"",
      "hooks": [{
        "type": "command",
        "command": "skills/strategic-compact/suggest-compact.sh"
      }]
    }]
  }
}
```

## Configuration

环境变量：
- `COMPACT_THRESHOLD`：首次提示前的工具调用次数（默认 50）

## Best Practices

1. 计划确定后再压缩，进入实现阶段
2. debug 完成后压缩，开启下一阶段
3. 不要在实现中途压缩，避免丢关联上下文
4. 有提示不等于必须压缩，按阶段边界决定

## Related

- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - Token optimization section
- Memory persistence hooks - For state that survives compaction
