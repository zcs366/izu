---
title: "aweskill: AI Agents 自有 Skills 集中管理器"
source: "微信公众号"
source_url: "https://mp.weixin.qq.com/s/wNMMwTHIGXFw8FIjcyVAKA"
author: "unknown"
date: 2026-05-19
ingested: 2026-05-19
sha256: b3549837f0eadbd1cf06ea362afebf70d56cdbf77839f66f01cccda40a1b9572
type: article
tags: [aweskill, skill-manager, multi-agent, npm-for-skills]
eval_level: 极大
---

# aweskill: AI Agents 自有 Skills 集中管理器

**GitHub**: https://github.com/mugpeng/aweskill
**官网**: https://aweskill.webioinfo.top
**npm**: aweskill (npm install -g)

## 核心理念
中央仓库（~/.aweskill/skills/）维护唯一副本 → symlink投影到各个Agent目录。
让 Skills 像 npm 包一样可管理。

## 核心特性
| # | 特性 | 说明 |
|---|------|------|
| 1 | 中央仓库 | 每个skill只存一份 |
| 2 | 多Agent投影 | 支持47个agent（Claude Code、Cursor、Codex、Gemini CLI等） |
| 3 | Bundle打包 | 按工作流分组，一键投影整组 |
| 4 | 来源追踪更新 | 记录skill出处，可拉取上游更新且保护本地改动 |
| 5 | 内置Agent管理技能 | Agent可通过自然语言管理skill |
| 6 | 本地维护 | 备份、恢复、查重、清理、同步、修复 |

## 独特优势
- 来源追踪更新 + 保护本地修改（同类工具大部分没有）
- 内置Agent可调用的管理技能（独有）
- 本地维护与恢复（backup/dedup/clean/recover）——独有

## 使用场景
1. 独立开发者中途切换Agent
2. 团队构建标准Skill集（bundle）
3. Skill作者发布更新
4. 科研类Skill多Agent共享
5. 灾难恢复

## 支持47个Agent
Claude Code、Cursor、Windsurf、Codex、GitHub Copilot、Gemini CLI、OpenCode、Goose、Amp、Roo Code、Kiro CLI、Kilo Code、Trae、Cline等
