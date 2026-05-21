# DCI（Direct Corpus Interaction）

> 概念 | 用 grep + bash 替代 embedding + 向量检索

## 定义

DCI（直接语料交互）：砍掉 embedding model、向量索引、top-k 检索，让 Agent 用 grep 和 bash 直接搜索原始语料。核心理念——**最好的 retriever 就是没有 retriever**。

论文实验：BrowseComp-Plus 上，Claude Sonnet 4.6 + DCI，准确率 69%→80%，成本 $1,440→$1,016。

## 为什么有效

Embedding 检索的本质是**压缩**——把文档压成一个向量，检索时只看最相似的 k 个 chunk。这个过程不可逆地丢失了信息。DCI 让 LLM 直接面对原始语料，自己决定搜什么、怎么组合结果。

## 与匠石原则的关系

[[aihot-code-over-model-principle|匠石原则]]说"能用代码就别用模型"。DCI 是这条原则在检索层的极致实践：**连 embedding model 都是多余的**。grep（代码）做检索，LLM（模型）只做最后的语义理解和综合。

## 对 wiki 系统的启示

当前 wiki 依赖全文搜索和索引导航。DCI 的思路提示：也许不需要给每个文档建向量，让 Agent 直接 grep + read_file 组合搜索原始 markdown，效果更好且零成本。这与 wiki 的 raw/ 层设计哲学一致——保留原始语料，不做过度预处理。

## 适用条件

- Agent backbone 足够强（能做多步工具调用和结果综合）
- 语料有结构化的文件系统（而非无结构的文本流）
- 任务需要精确匹配（函数名、术语、日期）而非模糊语义联想
