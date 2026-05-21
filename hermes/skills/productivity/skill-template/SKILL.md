---
# ── 基础字段 ──
name: skill-name-here           # (必填) 技能名称，小写连字符
description: >                  # (必填) 一句话描述技能功能
  一段话描述这个技能做什么、在什么场景下使用。
version: 1.0.0                  # (必填) 语义化版本
author: 军师祭酒                  # (必填) 作者名
license: MIT                    # (可选) 开源协议
platforms:                      # (可选) 支持平台
  - linux
  - macos

# ── 触发条件（Agent类型skill必填）──
trigger: "关键词1|关键词2|短语|..."  # 触发该skill的文本模式

# ── 标签与分类 ──
tags:                           # (可选) 搜索/发现用标签
  - tag1
  - tag2
metadata:
  hermes:
    category: productivity       # (必填) skill类别
    tags: [tag1, tag2]          # (可选) 与上方tags对应
    related_skills: []          # (可选) 相关skill列表

# ═══════════════════════════════════════════════
# ★ MMSkills 增强字段（可选，视觉Agent/多模态skill用）
# ═══════════════════════════════════════════════
multimodal: false               # 是否是多模态skill（涉及视觉状态判断）
states: []                      # (可选) 定义关键运行时状态
  # 每个状态的结构：
  # - id: "state_1"            # 状态ID
  #   name: "搜索框就绪"       # 状态名称
  #   stage: "entry_state"     # 状态阶段: entry_state / operation_state / verification_state
  #   when_to_use: "..."       # 何时使用该状态检查
  #   when_not_to_use: "..."   # 何时不该使用
  #   visible_cues: ["..."]    # 需要检查的视觉线索
  #   verification_cue: "..."  # 如何验证操作成功/进度/失败
  #   visual_risk: "仅用作状态证据参考，不要直接复用坐标"
visual_references: []           # (可选) 视觉参考文件路径
  # - images/state1_full.png
  # - images/state1_focus.png
  # (图片放在 skill_dir/Images/ 目录下)
---
