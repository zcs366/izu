---
type: evaluation
date: 2026-05-14
source_article: raw/articles/digitalplat-free-domain.md
author: 素语PlainTalking / 科技素语
content_type: 福利文
verdict: ⚠️ 真实可用但不适合做主域名
audience: 想零成本学习 DNS/Cloudflare 的开发者
---

# 评估：DigitalPlat 免费域名

## 核心主张

DigitalPlat 提供免费子域名（`*.dpdns.org` / `*.qzz.io`），KYC 通过 GitHub OAuth，可托管 Cloudflare，新账号2-3个免费名额，到期前90天可免费续。

## 核实

| 文章声称 | 核实结果 | 证据 |
|---------|---------|------|
| 非营利组织 | ✅ 属实 | Hack Foundation 501c3 (EIN 81-2908499)，GitHub/Cloudflare/Twilio/1Password 赞助 |
| 免费+可续期 | ✅ 属实 | 官方文档确认，GitHub FAQ 明确 |
| GitHub KYC | ✅ 属实 | OAuth EdwardLab，无需上传证件 |
| Cloudflare 托管 | ✅ 属实 | bring-your-own-DNS 设计 |
| 新账号3个名额 | ⚠️ 默认2个 | 邀请码+1，Star+1，实际可变 |
| US.KG 曾崩溃 | ✅ 文章自己承认 | 社区有记录 |

## 定论：⚠️ 练手可以，上场不行

**本质：** 免费二级域名（子域名），非注册局域名。类比 eu.org / freedns.afraid.org。

**适合：** Cloudflare/DNS 学习、自用面板、临时项目、内网穿透——零成本练手。

**不适合：** 对外正式网站、任何依赖域名稳定性的业务。所有权不在你手里。

## 对张成市的价值

如果你需要一个域名来玩 Cloudflare Workers/Zero Trust/Tunnel，这东西够用。但如果将来 aizu 或洁琼的事业需要对外站点，**老老实实买个付费域名**——.com 一年几十块钱的事，省这个不值得。

## 建议

- 想要：注册 dpdns.org 或 qzz.io（避开 qd.je，Cloudflare 兼容性问题）
- 注册完立刻托管到 Cloudflare，别用 DigitalPlat 自带的 DNS
- 自己设日历提醒续期，官方不提醒
