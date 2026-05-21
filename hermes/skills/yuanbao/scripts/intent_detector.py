#!/usr/bin/env python3
"""
元宝派小白助手 - 意图检测器（代码优先，零LLM）
匠石原则：能用代码就别用模型。
"""
import re

# === 意图模式表 ===
# 顺序匹配，命中即停。按使用频率排序。
PATTERNS = [
    # 文案写作
    ("写文案", [
        r'(写|帮我写|写个|写一篇|帮我写个|帮我写一篇).*(文案|宣传|推广|广告|介绍|推荐)',
        r'(写|帮我写|写个|帮写).*(朋友圈|小红书|抖音|微博|公众号|视频脚本|口播)',
        r'(写|帮我写).*(标题|slogan|口号|广告语)',
    ]),
    # 内容创作
    ("写文章", [
        r'(写|帮我写|写一篇).*(文章|方案|计划|报告|总结|通知|邀请函|演讲稿)',
        r'(写|帮我写).*(故事|笑话|诗歌|对联|祝福语|贺词)',
        r'(写|帮我写).*(教案|课程|课件|教材)',
    ]),
    # 资料查询
    ("查资料", [
        r'(查|搜|找|查一下|搜一下|找一下).*(资料|信息|数据|新闻|最新)',
        r'(什么是|什么叫|什么是叫|解释一下).+',
        r'(.+)是什么意思',
        r'(介绍|科普).*(一下|下)?(.+)',
    ]),
    # 方案策划
    ("做方案", [
        r'(策划|规划|设计).*(方案|活动|项目|流程)',
        r'(帮我|帮我做|做个).*(方案|计划|策划)',
    ]),
    # 文字润色
    ("润色", [
        r'(润色|改写|改一下|优化|润饰).*(文字|文章|这段话|文案)',
        r'(帮我改|帮我改一下|帮我优化).*(文字|文章|这段话)',
        r'(这段话|这段文字).*(改|优化|润色)',
    ]),
    # 翻译
    ("翻译", [
        r'(翻译|译|翻).*(成|为|到).*(英文|中文|日文|韩文|法文|德文)',
        r'(translate|翻一下|翻译一下)',
    ]),
    # 总结提炼
    ("总结", [
        r'(总结|概括|归纳|提炼).*(一下|下)?(.+)',
        r'(.+)(的)?(要点|重点|核心)',
        r'(帮我|给我).*(总结|概括|归纳)',
    ]),
    # 解释概念
    ("解释", [
        r'(解释|说明|讲讲|说说).*(什么是|什么叫|.+)',
        r'(.+)(是什么|怎么回事|什么意思)',
    ]),
    # 数据整理
    ("整理数据", [
        r'(整理|归类|分类|排序|筛选).*(数据|信息|名单|列表)',
        r'(帮我).*(整理|归类).+',
    ]),
    # 计算/换算
    ("计算", [
        r'(计算|算|换算).*(一下|下)?(.+)',
        r'(.+)(等于|相当于|换算).+',
    ]),
    # 问答
    ("问答", [
        r'(.+)(吗|呢|吧|好不好|行不行|可不可以)',
        r'(怎么|如何|怎样).+',
        r'为什么.+',
    ]),
]

# === 场景参数提取 ===
def extract_params(text):
    """从用户输入提取关键参数"""
    params = {}
    
    # 平台/渠道
    platform_match = re.search(r'(小红书|抖音|微信|朋友圈|公众号|微博|B站|知乎|快手)', text)
    if platform_match:
        params['platform'] = platform_match.group(1)
    
    # 字数/长度
    length_match = re.search(r'(\d+)\s*(字|词|个?字)', text)
    if length_match:
        params['length'] = int(length_match.group(1))
    
    # 语气/风格
    style_match = re.search(r'(正式|幽默|亲切|专业|通俗|文艺|口语|书面)', text)
    if style_match:
        params['style'] = style_match.group(1)
    
    # 目标受众
    audience_match = re.search(r'(给|针对|面向)(小孩|孩子|小学生|中学生|家长|客户|老人|员工|领导)', text)
    if audience_match:
        params['audience'] = audience_match.group(2)
    
    return params


def detect(text):
    """
    检测意图，返回 (intent_name, params)
    未命中返回 (None, {})
    """
    text = text.strip()
    
    for intent_name, pattern_list in PATTERNS:
        for pattern in pattern_list:
            if re.search(pattern, text):
                params = extract_params(text)
                return (intent_name, params)
    
    return (None, {})


def get_prompt(intent_name, params, user_text):
    """根据意图生成对应的系统提示前缀"""
    base = "你是元宝派里的AI助手「小祝」。用自然的口语回复，像朋友聊天一样。输出要直接可用，不要解释过程。"
    
    prompts = {
        "写文案": f"{base}\n用户要写{params.get('platform', '社交媒体')}文案。直接给成品文案，带上emoji和话题标签。如果用户没指定字数，默认150-300字。",
        "写文章": f"{base}\n用户要写文章。先给标题建议（3个选项），再写正文。格式清晰，分段合理。{('面向' + params['audience'] + '，语言要适合他们理解') if params.get('audience') else ''}",
        "查资料": f"{base}\n用户要查资料。先给核心答案（3句话内），再补充关键细节。标注信息来源。",
        "做方案": f"{base}\n用户要做方案。给出结构化方案：目标→步骤→时间→注意事项。每步可执行。",
        "润色": f"{base}\n用户要润色文字。给出润色后的版本，附带简要说明改了什么（1句话）。",
        "翻译": f"{base}\n用户要翻译。给出翻译结果，必要时附注关键术语的选择理由。",
        "总结": f"{base}\n用户要总结。先给一段话总结，再列3-5个要点。",
        "解释": f"{base}\n用户要解释概念。用通俗的话解释，给一个生活中的类比。如果概念复杂，分层次说明。",
        "整理数据": f"{base}\n用户要整理数据。输出清晰的表格或列表。",
        "计算": f"{base}\n用户要计算。给答案+简要计算过程。",
        "问答": f"{base}\n用户在问问题。给直接明确的答案，如有不同观点也简要提及。",
    }
    
    return prompts.get(intent_name, base)


# CLI 测试
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = sys.stdin.read().strip()
    
    intent, params = detect(text)
    print(f"INTENT: {intent}")
    print(f"PARAMS: {params}")
    print(f"PROMPT: {get_prompt(intent, params, text)}")
