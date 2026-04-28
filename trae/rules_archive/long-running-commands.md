---
globs: ["寻找最优参数*.py", "回测主程序*.py", "批量回测主程序*.py", "选股+回测.py", "docs/策略研究/**/*.py", "param_search.py"]
---

# 长时间命令执行规则

## 核心原则：绝不无限等待

长时间运行的命令（回测、参数遍历、数据处理等）可能因各种原因挂起或进程消失。
必须设置明确的退出策略，避免陷入无限 read_bash 循环。

## 执行策略

### 1. 启动前：预估时间，设定上限

- 启动命令前，根据任务复杂度预估最大合理耗时
- 单次回测：5-10 分钟
- 参数遍历（<50组）：10-20 分钟
- 参数遍历（50-200组）：20-40 分钟
- 参数遍历（>200组）：考虑分批执行

### 2. 等待中：递进式检查，最多 3 轮

每轮 read_bash 之间，**必须检查进程是否存活**：

```
第1轮：read_bash delay=60-120s → 检查是否有新输出
第2轮：read_bash delay=120-180s → 如果无新输出，用 list_bash 检查会话是否存活
第3轮：read_bash delay=180s → 如果仍无新输出，强制退出等待
```

**关键规则：连续 2 次 read_bash 无任何新输出时，必须立即：**
1. 调用 `list_bash` 检查会话是否还在活跃列表中
2. 如果会话已不存在 → 进程已死，立即停止等待，转入结果检查
3. 如果会话存在但无输出 → 再给最后一次机会，之后强制终止

### 3. 超时后：止损并汇报

超时或进程消失后，立即执行：
1. 检查是否产生了部分结果（ls 输出目录）
2. 检查日志文件（logs/ 目录）
3. 向用户汇报：已完成多少、还差什么、建议下一步

**绝不要**：
- 在第 3 轮之后继续追加 read_bash
- 在 read_bash 的 delay 参数上无限翻倍（最大不超过 300s）
- 假设"再等一下就好了"

### 4. 替代方案：后台执行 + 轮询

对于预计超过 10 分钟的命令，优先使用后台模式：

```bash
# 使用 nohup + 日志文件，而非阻塞式等待
nohup python 寻找最优参数.py > logs/param_search.log 2>&1 &
echo $!  # 记录 PID
```

然后通过检查日志和进程状态来追踪进度：
```bash
# 检查进程是否存活
ps -p <PID> > /dev/null && echo "running" || echo "finished"
# 查看最新日志
tail -20 logs/param_search.log
# 检查结果文件
ls data/遍历结果/<name>/
```

### nohup 后台执行完整示例

#### 示例 1：参数搜索过夜任务

```bash
#!/bin/bash
# 创建过夜任务脚本

# 1. 确保日志目录存在
mkdir -p logs

# 2. 记录任务开始时间
echo "任务开始时间: $(date)" > logs/overnight_task.log

# 3. 后台执行参数搜索
nohup python 寻找最优参数.py \
    --config config_策略名.py \
    --start_date 2016-01-01 \
    --end_date 2024-12-31 \
    >> logs/overnight_task.log 2>&1 &

# 4. 记录 PID
TASK_PID=$!
echo $TASK_PID > logs/overnight_task.pid
echo "任务 PID: $TASK_PID"
echo "日志文件: logs/overnight_task.log"

# 5. 可选：设置邮件或通知命令（执行完成后触发）
# python send_notification.py --pid $TASK_PID --email "your@email.com"
```

#### 示例 2：多策略批量回测

```bash
#!/bin/bash
# 批量回测脚本

STRATEGIES=("小市值" "中市值" "大市值" "北交所")
LOG_DIR="logs/batch_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$LOG_DIR"

# 记录所有任务的 PID
PIDS=()

for strategy in "${STRATEGIES[@]}"; do
    echo "启动策略: $strategy"
    LOG_FILE="$LOG_DIR/${strategy}.log"

    nohup python 回测主程序_增强版.py \
        -name "config_${strategy}.py" \
        >> "$LOG_FILE" 2>&1 &

    PIDS+=($!)
    echo "PID: ${PIDS[-1]} | 日志: $LOG_FILE"
done

# 保存 PID 列表
printf "%s\n" "${PIDS[@]}" > "$LOG_DIR/pids.txt"
echo "所有任务已启动，PID 列表保存至: $LOG_DIR/pids.txt"

# 监控函数（可选）
monitor_tasks() {
    echo "监控任务进度..."
    while true; do
        local running=0
        for pid in "${PIDS[@]}"; do
            if ps -p "$pid" > /dev/null 2>&1; then
                ((running++))
            fi
        done
        echo "$(date) - 运行中: $running / ${#PIDS[@]}"

        if [ $running -eq 0 ]; then
            echo "所有任务已完成"
            break
        fi
        sleep 60
    done
}

# 后台启动监控（可选）
monitor_tasks &
```

#### 示例 3：带进度检查的后台任务

```bash
#!/bin/bash
# 带进度检查的参数搜索

LOG_FILE="logs/param_search_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs

# 启动任务
nohup python 寻找最优参数.py \
    --config config_xxx.py \
    --batch_size 100 \
    > "$LOG_FILE" 2>&1 &

PID=$!
echo "任务已启动，PID: $PID"
echo "日志文件: $LOG_FILE"

# 进度检查函数
check_progress() {
    echo "=== 进度检查 ==="
    echo "当前时间: $(date)"
    echo "最后 10 行日志:"
    tail -10 "$LOG_FILE"
    echo "=================="
}

# 定时检查（用户可手动调用）
while true; do
    sleep 300  # 每5分钟检查一次
    if ps -p $PID > /dev/null 2>&1; then
        check_progress
    else
        echo "任务已完成 (PID: $PID)"
        echo "最终结果:"
        tail -20 "$LOG_FILE"
        break
    fi
done
```

#### 常用 nohup 管理命令

```bash
# 查看所有 nohup 后台任务
ps aux | grep "nohup.*python"

# 终止指定 PID 的任务
kill <PID>

# 终止所有 nohup python 任务
pkill -f "nohup.*python"

# 查看任务日志
tail -f logs/任务名称.log

# 统计日志中的进度信息
grep "完成" logs/任务名称.log | wc -l
```

## 总结

| 情况 | 动作 |
|------|------|
| 连续2次无新输出 | list_bash 检查存活 |
| 会话已消失 | 停止等待，检查结果 |
| 3轮后仍无结果 | 强制停止，汇报用户 |
| 预计>10分钟 | 用 nohup 后台执行 |
| delay 参数 | 单次最大 300s，不无限翻倍 |
