# /checkpoint（进度点）

在关键节点做“存档/对比”，避免改坏后找不到回退点。

## 用法

`/checkpoint create <名称>`  
`/checkpoint verify <名称>`  
`/checkpoint list`  

## create（创建）

1. 确认当前能跑（至少不报错）
2. 用 git 做一次临时保存（stash/commit 二选一）
3. 记录到 `.trae/checkpoints.log`

```bash
echo "$(date +%Y-%m-%d-%H:%M) | $CHECKPOINT_NAME | $(git rev-parse --short HEAD)" >> .trae/checkpoints.log
```

## verify（对比）

对比当前状态 vs 某个存档点，输出：
- 变更文件数
- 测试通过/失败情况
- 覆盖率变化（如有）
- 是否能构建/运行

## list（列出）

列出所有存档点：名称、时间、git 短哈希
