---
title: "匠石工程评估：OpenHands → izu 移植可行性"
date: 2026-05-14
evaluator: 匠石（engineer-agent）
source: github.com/All-Hands-AI/OpenHands
---

# 匠石工程评估：OpenHands → izu 移植可行性

## 一、核心结论

**三句话：**

1. **Docker沙箱可轻量化移植——甚至不用Docker。** OpenHands自己有ProcessSandboxService，直接用子进程替代Docker容器。这是我们要找的轻量方案。
2. **多Agent是营销术语。** 本质是同一个Agent引擎的不同提示词模板（Plan Agent → Code Agent两级切换），没有多进程通信。
3. **MVP只需约200行Python。** 不引入任何openhands-*包，不依赖Docker。

## 二、架构核心发现

### OpenHands沙箱设计精髓

```
SandboxService (抽象基类)
├── DockerSandboxService    ← 生产环境，需要Docker守护进程
├── ProcessSandboxService   ← 🎯 我们要的！subprocess + psutil，无Docker依赖
├── RemoteSandboxService    ← K8s Pod，多租户
└── PresetSandboxService    ← 预置环境
```

**四个实现通过统一接口互换**——这就是OpenHands最值得学的地方。

### OpenHands的"多Agent"真相

```
AgentType.PLAN  ──生成 PLAN.md──→ AgentType.DEFAULT (CodeActAgent)
 (只能创建计划)                      (执行代码，使用所有工具)
```

**不是多进程/多Agent通信，是同一个引擎换提示词模板+工具过滤。** 营销包装成了"多智能体协作"。

## 三、技术选型决策矩阵

| 决策点 | 推荐方案 | 理由 |
|--------|---------|------|
| 沙箱方案 | **ProcessSandbox（子进程）** | 无Docker依赖，WSL友好，启动<1秒 |
| agent server | **izu自建精简版** | 避免75+间接依赖（browsergym/playwright/jupyter） |
| 安全隔离 | **临时目录 + 超时强制终止** | izu本地单用户场景，不需要Docker级隔离 |
| 任务分解 | **借用提示词模板** | Plan/Code切换本质是提示词工程 |
| 浏览器 | **暂不加** | WSL下Playwright配置复杂，MVP不需要 |
| 进程管理 | `subprocess` + `psutil` | psutil提供进程状态查询 |

## 四、MVP定义（200行核心代码）

**必须有的：**
- 子进程执行：临时目录中启动Python子进程
- 文件读写：主进程读写沙箱内文件
- 自动清理：沙箱结束后删除临时目录
- 超时保护：子进程超时强制终止
- AIHOT集成：在"写"阶段将代码写入沙箱执行验证

**可以没有的：**
- ❌ Docker方案、多用户隔离、浏览器执行、网络隔离、快照/恢复、完整安全分析器、任何openhands-*包

### 核心代码模式

```python
class Sandbox:
    def __init__(self):
        self.workdir = tempfile.mkdtemp(prefix='izu_sandbox_')
    
    def exec(self, cmd: str, timeout: int = 30) -> dict:
        result = subprocess.run(cmd, shell=True, cwd=self.workdir,
            capture_output=True, text=True, timeout=timeout)
        return {'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
    
    def write_file(self, path, content): ...
    def read_file(self, path): ...
    def cleanup(self): shutil.rmtree(self.workdir, ignore_errors=True)
```

## 五、实现路径

| 里程碑 | 内容 | 工期 |
|--------|------|------|
| M1：沙箱核心 | SandboxManager类 + 文件代理 + 健康检查 | 3天 |
| M2：AIHOT集成 | 流水线注入 + Plan→Code两级代理 | 2天 |
| M3：安全健壮 | 超时限制 + 资源限制 + 僵尸清理 | 2天 |

**总工期：乐观5天 / 最可能7天 / 悲观14天**

## 六、SDK依赖黑洞警告

⚠️ OpenHands的核心在四个PyPI包，合计依赖数百个包：
- `openhands-agent-server` → browsergym, playwright, jupyter...
- `openhands-sdk` → docker SDK, psutil...
- `openhands-aci` → Agent-Computer Interface
- Python版本限制：`>=3.12,<3.14`

**结论：不要引入任何openhands-*包。只借鉴设计模式，代码自己写。**
