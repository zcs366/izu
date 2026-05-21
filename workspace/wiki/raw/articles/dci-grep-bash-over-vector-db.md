---
source_url: PLACEHOLDER
ingested: 2026-05-14
sha256: 6fd0675466ae0525
note: 与匠石原则高度共鸣：embedding不如grep，最好的retriever就是没有retriever
title: 向量数据库白建了？grep + bash 碾压 embedding 检索，准确率暴涨 11 个点，成本反降 30%
author: 井底之硅
source: 微信公众号
---

一篇刚发布的论文提出了 Direct Corpus Interaction（DCI）——把 embedding model、向量索引、top-k 检索全部砍掉，让 agent 直接用 grep 和 bash 搜索原始语料。

在 BrowseComp-Plus 上，同样用 Claude Sonnet 4.6 做 backbone，准确率从 69.0% 涨到 80.0%，成本从 $1,440 降到 $1,016。

## 核心宣言

"Introducing Direct Corpus Interaction (DCI)! The best retriever for agentic search is no retriever."

「最好的 retriever 就是不需要 retriever。」

"We replaced the entire agentic search pipeline — embedding model, vector index, top-k retrieval — with only `grep` and `bash`."

「把整个 agentic search 流水线全部替换成了 grep 和 bash。」

## 为什么有效

把 embedding 砍掉后，Agent 直接面对原始语料。DCI 给 LLM 的不是"最相似的 5 个 chunk"，而是让 LLM 自己决定怎么搜——grep 关键词、find 文件、读相邻段落、写小脚本抽取模式。这比被动接受 top-k 结果更灵活。

coding agent 的实践早已证明：程序员理解代码库从来是先 rg 函数名、再 find 文件结构、读相邻代码、写脚本抽取模式，逐步缩小范围。没人只靠一个 semantic search top-k。DCI 把这个范式搬到了通用语料搜索上。

## 与匠石原则的共鸣

本 wiki 的 [[aihot-code-over-model-principle|匠石原则]]（能用代码就别用模型）与 DCI 共享同一底层逻辑：模型只做语义理解，代码做检索和匹配。DCI 把这条原则推到了极致——连 embedding model 本身都是多余的。

## 适用边界

- 需要足够强的 agent backbone
- 大规模语料上有成本和准确率压力
- 依赖文件系统结构
- 不适合需要真正"语义相似"而非"关键词匹配"的场景
