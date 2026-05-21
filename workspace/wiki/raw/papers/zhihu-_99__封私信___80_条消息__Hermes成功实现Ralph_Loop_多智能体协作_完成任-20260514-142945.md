# (99+ 封私信 / 80 条消息) Hermes成功实现Ralph Loop+多智能体协作 完成任务质量大大提高！！！

> 来源: https://zhuanlan.zhihu.com/p/2033380482713392938
> 抓取: 2026-05-14 14:29:45
> 工具: 透心 v4

Ralph Loop 工作流详解
一句话概括
Ralph Loop 是一个Bash 驱动的多 Agent 任务循环控制器，它从文件队列中按优先级取出任务，在 tmux 中启动 Hermes Agent 执行，通过状态机跟踪进度，并自动验证结果。复杂任务会用 Python 编排器拆分为 4 阶段（Research → Plan → Execute → Verify），简单任务直接 spawn 一个 Worker 完成。
整体架构图
┌─────────────────────────────────────────────────────────────────────────┐
│                         Ralph Loop 核心组件                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────────────────┐   │
│  │ task-queue  │────▶│ state-machine│────▶│    ralph-loop.sh      │   │
│  │  (YAML队列)  │     │  (状态转换)  │     │    (主循环控制器)      │   │
│  └─────────────┘     └─────────────┘     └─────────────────────────┘   │
│         ▲                                        │                      │
│         │                                        ▼                      │
│  ┌──────┴──────┐     ┌──────────────────────────────────────────┐     │
│  │  queue.md   │◄────│              执行决策                      │     │
│  │ (任务清单)   │     │  ┌────────────────────────────────────┐  │     │
│  └─────────────┘     │  │ 复杂度=complex?                      │  │     │
│                      │  │  ├── Yes → ralph-orchestrator.py    │  │     │
│  ┌─────────────┐     │  │  │          (4阶段编排)              │  │     │
│  │ CONTEXT.md  │◄────│  │  └── No  → spawn-hermes.sh         │  │     │
│  │ (共享上下文) │     │  │            (单Worker)               │  │     │
│  └─────────────┘     │  └────────────────────────────────────┘  │     │
│                      └──────────────────────────────────────────┘     │
│                                                                         │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────────────────┐   │
│  │ PROGRESS.md │     │ spawn-hermes│────▶│    tmux session         │   │
│  │ (进度记录)   │     │  (启动Agent) │     │  hermes chat -q task   │   │
│  └─────────────┘     └─────────────┘     └─────────────────────────┘   │
│                                                    │                    │
│                                                    ▼                    │
│                              ┌──────────────────────────────────┐     │
│                              │  wait_for_agent() 检测工作进程完成 │     │
│                              │  (之前修复的 tmux 进程检测逻辑)     │     │
│                              └──────────────────────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
各组件详解
1. ralph-config.sh — 配置中心
RALPH_ROOT="/Volumes/A/RalphLoop"     # 工作目录
HERMES_MODEL="MiniMax-M2.7-highspeed" # 模型
MAX_ITERATIONS=100                     # 最大循环次数
MAX_IDLE_SECONDS=3600                  # 单个任务最长等待时间
LINEAR_MODE=true                       # 线性模式（一次一个任务）
MAX_CONCURRENT_AGENTS=3                # 并发数（非线性模式）
2. task-queue.sh — 任务队列管理

存储格式：tasks/queue.md（YAML 格式）

tasks:
  - id: task-20260430_150101-6716
    title: "检查飞书状态"
    description: "排查飞书消息无回应问题"
    status: pending          # pending | in_progress | completed | failed
    priority: P1             # P0 > P1 > P2 > P3
    agent: worker            # worker | orchestrator
    verify_cmd: "grep 'message' /tmp/feishu.log"
    verify_timeout: 30
    retry_count: 0
    max_retries: 3

子命令：

./task-queue.sh add "标题" "描述" P1 worker        # 添加任务
./task-queue.sh list                              # 列出所有任务
./task-queue.sh next                              # 获取下一个最高优先级 pending 任务
./task-queue.sh complete <task_id>               # 标记完成
./task-queue.sh fail <task_id> "原因"            # 标记失败
3. state-machine.sh — 状态机引擎

7 个状态 + 7 个事件：

┌──────────┐   dequeue    ┌────────────┐
│ pending  │ ───────────▶ │in_progress │
└──────────┘              └─────┬──────┘
                                │
                   ┌────────────┼────────────┐
                   ▼            ▼            ▼
              ┌────────┐  ┌────────┐  ┌──────────┐
              │completed│  │ failed │  │(timeout) │
              └────┬───┘  └────────┘  └──────────┘
                   │ task_completed
                   ▼
              ┌──────────┐
              │verifying │
              └────┬─────┘
         ┌─────────┴──────────┐
         ▼                    ▼
      passed               verify_retry
         │                    │
         │ verify_success     │ verify_failure (还有重试次数)
         ▼                    ▼
      ┌──────────┐      ┌────────────┐
      │completed │◄─────│verify_retry│
      └──────────┘      └─────┬──────┘
                              │ max_retries_exceeded
                              ▼
                         ┌────────────┐
                         │verify_failed│
                         └────────────┘
4. ralph-loop.sh — 主循环控制器（948 行）

主循环逻辑：

main_loop() {
    while check_stop:                    # 检查是否收到停止信号
        iteration++                      # 迭代计数
        
        task = task-queue.sh next        # 获取下一个任务
        if 没有任务:
            if CONTINUOUS_MODE:          # 连续模式
                generate-knowledge-task.py  # 自动生成新任务
            else:
                break                     # 停止循环
        
        # 决策：简单任务 or 复杂任务？
        if 任务标记 complexity=complex 或 orchestrator=true:
            ralph-orchestrator.py --task-file task.md   # 多阶段编排
        else:
            spawn-hermes.sh session_name task.md        # 直接 spawn worker
        
        wait_for_agent session_name        # 等待完成（检测工作进程）
        
        if 成功:
            执行 verify_cmd（如有）        # 验证任务结果
            更新状态机 → completed
        else:
            更新状态机 → failed
        
        update_context_start/end()         # 更新 CONTEXT.md
        update_progress()                   # 更新 PROGRESS.md
        capture_logs()                      # 捕获日志
}
5. ralph-orchestrator.py — 复杂任务编排器（4 阶段）

这是 Ralph Loop 的大脑，负责复杂任务的多 Agent 协作：

# Phase 1: Research（研究）
#   - 启动 researcher agent 探索代码库/文档
#   - 收集上下文信息

# Phase 2: Plan（规划）
#   - 启动 master/planner agent 制定执行计划
#   - 生成子任务列表

# Phase 3: Execute（执行）
#   - 启动 worker agent 执行具体任务
#   - 或并行启动多个 worker

# Phase 4: Verify（验证）
#   - 启动 qa agent 验证结果
#   - Feynman 验证（用简单语言解释）
#   - 如果验证失败且有 gaps，生成 refinement 任务重新执行

简单任务 vs 复杂任务：

类型	判断条件	执行方式
简单任务	无 complexity: complex 标记	execute_simple_task() → 直接 spawn 一个 worker
复杂任务	有 complexity: complex 或 orchestrator: true	execute_complex_task() → 4 阶段编排
6. ralph-decompose.py — 任务分解器
读取用户输入（URL、文件、文本）
将大任务分解为多个子任务
每个子任务生成一个独立的 .md 文件放入队列
7. spawn-hermes.sh — Agent 启动器

核心逻辑：

# 1. 读取任务文件内容
TASK_CONTENT="$(cat "$TASK_FILE")"

# 2. 构建完整提示词（模板 + 任务内容）
TASK_PROMPT="$WORKER_PROMPT\n---\nCURRENT TASK:\n$TASK_CONTENT"

# 3. 写入临时文件
printf '%s' "$TASK_PROMPT" > "$PROMPT_FILE"

# 4. 生成 wrapper 脚本
cat > "$WRAPPER_SCRIPT" << EOF
#!/bin/bash
cd "/Volumes/A/RalphLoop"
PROMPT_CONTENT=\$(cat "$PROMPT_FILE")
hermes chat -q "\$PROMPT_CONTENT" 2>&1
EOF

# 5. 创建 tmux session
tmux new-session -d -s "$SESSION_NAME"
tmux send-keys -t "$SESSION_NAME" "bash $WRAPPER_SCRIPT" Enter

关键点：

使用 hermes chat -q（非交互模式，执行完退出）
在 tmux 中运行（可以后台运行、查看日志）
不删除 wrapper 脚本（下一次 spawn 会覆盖）
8. feynman-inner-loop.sh — 费曼验证（已简化）

当前版本是轻量级日志记录，真正的费曼验证由 feynman_verifier.py 通过 delegate_task 的 reviewer 实现。

9. 状态持久化文件
文件	作用
CONTEXT.md	共享上下文，记录当前活跃任务和已完成任务
PROGRESS.md	进度日志，每行记录一个任务的执行结果
queue.md	任务队列，YAML 格式存储所有任务
ralph-loop.log	主循环的运行日志
logs/*.log	每个 session 的详细日志
完整执行流程（一条任务的生命周期）
1. 用户创建任务
   ./task-queue.sh add "修复bug" "排查xxx" P1 worker
   
   ↓
   
2. 任务进入 queue.md，状态=pending
   
   ↓
   
3. ralph-loop.sh 主循环启动
   while 循环:
     task-queue.sh next → 返回最高优先级 pending 任务
     
     ↓
     
4. 状态机触发: fire_event "dequeue"
   pending → in_progress
   
   ↓
     
5. 决策: 简单任务 or 复杂任务?
   
   ├─ 简单任务 ──▶ spawn-hermes.sh → 启动 tmux session
   │               hermes chat -q "任务提示词"
   │               wait_for_agent() 等待完成
   │
   └─ 复杂任务 ──▶ ralph-orchestrator.py
                   Phase 1: Research → spawn researcher
                   Phase 2: Plan → spawn master/planner  
                   Phase 3: Execute → spawn worker(s)
                   Phase 4: Verify → spawn qa
                   （每个 phase 都可能 spawn 多个 agent）
   
   ↓
   
6. 任务完成（或超时）
   
   ├─ 成功 ──▶ fire_event "task_success"
   │            in_progress → completed
   │            如有 verify_cmd → 执行验证
   │            verify 通过 → 最终 completed
   │            verify 失败 → 重试或标记 verify_failed
   │
   └─ 失败 ──▶ fire_event "task_failure"
                in_progress → failed
   
   ↓
   
7. 更新所有状态文件
   - queue.md: 更新任务状态
   - CONTEXT.md: 移除 in_progress，添加到 completed/failed
   - PROGRESS.md: 追加执行记录
   
   ↓
   
8. 进入下一次迭代
你的使用场景映射
你想做的事	Ralph Loop 中的对应
让 sage-agent 回答一个问题	创建任务 → task-queue.sh add "问题" "描述" P1 worker
让多个 agent 并行工作	设置 LINEAR_MODE=false + orchestrator: true
复杂任务（代码重构）	标记 complexity: complex → 走 orchestrator 4 阶段
自动循环执行	CONTINUOUS_MODE=true + generate-knowledge-task.py
验证任务结果	在任务中设置 verify_cmd: "pytest tests/"
查看执行进度	cat PROGRESS.md 或 ./ralph-loop.sh --status
一句话总结
Ralph Loop = 任务队列 (task-queue.sh) + 状态机 (state-machine.sh) + Agent 启动器 (spawn-hermes.sh) + 编排器 (ralph-orchestrator.py)。它按优先级从队列取任务，在 tmux 中启动 Hermes Agent 执行，通过文件持久化状态，支持简单任务直接执行和复杂任务 4 阶段编排。

最近看到哔哩哔哩博主费曼冬瓜学徒的“Ralph+多智能体协作”，我认为很赞，这个方案很严谨，能解决非常多的现实问题，于是就花了两天时间在Hermes中引入，具体效果如何？

尝试了让Hermes自己添加自己改（minimax2.7speed），一天过去了，除了消耗六千多次的api调用次数以外还创造了一堆屎山文件，好在我的kimi 2.6第二天额度刷新了，大概改进了四十分钟左右，在Hermes上复刻了
费曼冬瓜学徒的“Ralph+多智能体协作”。
以下直接上图参考，
总结
反馈
过程

我执行的是一次性真实复杂任务，实际完成的质量非常好，而不是真正的ralph loop（无限循环）,但实际上现有配置已经可以进行无限循环了 ～。～

衷心感谢 B站博主“费曼学徒冬瓜”！！！