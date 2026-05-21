# Hermes 全系统评估侦察模板

> 适用场景：接管系统后的全面摸底、定期系统健康审查、用户要求"评估一下整体状态"。

## 执行流程（7步并行→聚合报告）

### Step 1: 系统状态快照

```bash
hermes status --all
```

提取项：
- 模型/Provider 当前配置
- 所有API key连通状态（✓/✗）
- 已配置的消息平台列表
- Gateway运行状态和PID
- 活跃会话数和定时任务数

### Step 2: 深度诊断

```bash
hermes doctor
```

提取项：
- 安全公告（是否有CVE）
- Python环境和依赖完整性
- 配置文件版本和一致性
- Auth Provider登录状态
- API连通性检查（并行检测所有provider）
- 工具可用性矩阵（哪些可用/缺依赖/缺key）
- Skills Hub状态
- 记忆Provider状态

### Step 3: 工作记忆读取

```bash
cat ~/.hermes/memories/WORKING.md
```

提取项：
- 当前高优先级任务
- 最近完成事项
- 下一步待办

这是项目上下文的入口——告诉评估者"此刻在做什么"。

### Step 4: 定时任务盘点

```bash
hermes cron list
```

提取项：
- 任务总数和分类（个人日报/群日报/研究/维护/备份）
- 每个任务的enabled/disabled状态
- last_status是否ok
- last_delivery_error是否有投递失败
- 脚本型(no_agent) vs Agent型任务分布

### Step 5: 配置概览

```bash
hermes config
```

提取项：
- 当前模型配置
- 平台配置完整性
- 压缩设置
- 辅助模型配置

### Step 6: 会话和资源统计

```bash
hermes sessions stats
hermes skills list | wc -l
ps aux | grep hermes | grep -v grep
df -h ~/.hermes && free -h && uptime
```

提取项：
- 会话总数、消息总数、数据库大小
- 技能总数
- 进程列表（识别所有运行中的Hermes组件）
- 磁盘/内存/CPU使用率

### Step 7: 日志健康检查

```bash
tail -20 ~/.hermes/logs/gateway.log
```

提取项：
- 最近的WARNING/ERROR
- SSL连接问题
- 投递失败
- 内存监控告警
- 中断递归深度警告

## 报告结构模板

```markdown
# Hermes 全系统评估报告

> 评估时间：YYYY-MM-DD HH:MM CST

## 一、系统健康总览（表格：项目/状态/详情）
## 二、API连通性（表格：Provider/状态/备注）
## 三、平台连接（表格：平台/状态/主频道）
## 四、定时任务盘点（分类统计+异常标注）
## 五、项目全景（从WORKING.md+workspace推导）
## 六、技能生态（分类统计）
## 七、发现的问题（⚠️清单+修复建议）
## 八、推进建议（按优先级排列）
```

## 关键 Pitfall

1. **不要只看status不看doctor** — status是概览，doctor有连通性实测和依赖检查
2. **WORKING.md是项目上下文入口** — 没有它你不知道"此刻在忙什么"
3. **日志要查WARNING不只是ERROR** — SSL间歇性故障、投递失败都在WARNING级别
4. **进程列表能揭示隐藏组件** — dashboard、web-ui、LSP server、TUI组件都可能在跑
5. **cron的last_delivery_error容易被忽略** — 任务看似正常运行但投递可能持续失败

## 与包拯审计的区别

| 维度 | 系统评估侦察 | 包拯项目审计 |
|------|-------------|-------------|
| 范围 | 整个Hermes系统 | 单个项目 |
| 深度 | 宏观健康 | L1-L5逐项核实 |
| 关注 | 基础设施+连通性+资源 | 交付物真实性 |
| 频率 | 接管时/定期 | 里程碑后 |
