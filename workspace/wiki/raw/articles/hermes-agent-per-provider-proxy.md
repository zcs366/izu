---
source_url: https://mp.weixin.qq.com/s/rWccNOTTdcvWtChYzFThWA
ingested: 2026-05-10
sha256: b4cdecbe08e21b902d36b7f302b8a87dcdab86521089e93a1dc0b645190258b2
title: Hermes Agent 重磅更新：按 Provider 独立配置代理
author: 码爪炼金社
description: Hermes Agent 新增 model_providers 配置，按 Provider 独立设置代理，OpenAI 走代理+国内 API 直连互不干扰
---

技术解读 · 配置教程 · 源码解析
痛点：一个代理走天下？太粗暴了
不同 AI Provider 的网络情况完全不同：

        
          
            
            
          Provider网络需求OpenAI (openai-codex)🇨🇳 国内被墙必须走代理OpenRouter🇨🇳 可能被墙必须走代理MiniMax (minimax-cn)🇨🇳 国内直连走代理反而慢
        
      
传统方案：全局 HTTPS_PROXY，所有流量都走代理——国内 API 平白无故绕一圈。

现在：Hermes Agent 支持按 Provider 独立配置代理，每个 Provider 单独设置，互不影响。

架构：4 个文件，职责清晰

    
    
    
  ~/.hermes/config.yaml
        ↓ 用户配置
hermes_cli/config.py      ← 新增 model_providers: {} 配置节点
        ↓ 读取配置
run_agent.py               ← _create_openai_client() 中注入 proxy
        ↓
httpx.Client              ← 带着 proxy 参数创建，发请求时自动走代理

改动量：极小。核心逻辑只有 15 行新增代码。
核心逻辑（run_agent.py）

    
    
    
  # 获取当前 Provider 名称
_provider = getattr(self, "provider", None) or ""

# 读取用户的 model_providers 配置
_cfg = load_config()
_model_providers = _cfg.get("model_providers") or {}
_proxy_url = _model_providers.get(_provider)

# 找到代理配置 → 创建带 proxy 的 httpx.Client
# 未找到 → 创建普通 httpx.Client（直连）
if _proxy_url:
    client_kwargs["http_client"] = httpx.Client(
        transport=_transport,
        proxy=_proxy_url,
    )
else:
    client_kwargs["http_client"] = httpx.Client(
        transport=_transport,
    )

配置：3 步搞定
Step 1：打开 ~/.hermes/config.yaml，添加节点：

    
    
    
  model_providers:
  openai-codex: http://127.0.0.1:7897   # OpenAI 走代理
  openrouter: http://127.0.0.1:7897     # OpenRouter 走代理
Step 2：保存文件

Step 3：直接用，无需重启

    
    
    
  # OpenAI 请求自动走代理
hermes chat -m gpt-5.4 --provider openai-codex

# MiniMax 请求直连（不配置代理的 Provider 不受影响）
hermes chat -m default --provider minimax-cn支持的代理协议• http://host:port — HTTP 代理（Clash HTTP 端口）• https://host:port — HTTPS 代理• socks5://host:port — SOCKS5 代理（Clash SOCKS 端口）
Clash Verge Rev 默认端口：HTTP = 7897，SOCKS = 7891（注意不是 7890）
使用场景对比

    
    
    
  ┌─────────────────────────────────────────────────────┐
│  配置前：全局代理，所有 Provider 都走代理            │
│  ✗ 国内 API（MiniMax） 平白绕路，延迟增加           │
├─────────────────────────────────────────────────────┤
│  配置后：按 Provider 独立路由                       │
│  ✓ openai-codex  → 走代理 (127.0.0.1:7897)         │
│  ✓ openrouter    → 走代理 (127.0.0.1:7897)         │
│  ✓ minimax-cn    → 直连，不走代理                  │
└─────────────────────────────────────────────────────┘

源码改动一览
        
          
            
            
          文件改动hermes_cli/config.pyDEFAULT_CONFIG 新增 model_providers: {}run_agent.py_create_openai_client() 新增 15 行 proxy 注入逻辑cli-config.yaml.example新增配置说明文档~/.hermes/config.yaml用户实际配置位置（需用户自行添加）
        
      总结• ✅ 按 Provider 独立配置代理，互不干扰• ✅ 配置简单，用户只需修改 config.yaml• ✅ 国内 API 直连，海外 API 走代理，速度最优• ✅ 支持 HTTP / HTTPS / SOCKS5 三种代理协议• ✅ 源码改动极小（核心 15 行），风险低相关文件• 用户配置：~/.hermes/config.yaml• 核心逻辑：~/.hermes/hermes-agent/run_agent.py• 配置定义：~/.hermes/hermes-agent/hermes_cli/config.py• 配置示例：~/.hermes/hermes-agent/cli-config.yaml.example
技术文档完整版:码爪炼金社

