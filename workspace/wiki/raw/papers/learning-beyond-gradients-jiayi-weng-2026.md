---
title: Learning Beyond Gradients — 启发式学习论文原文
author: Jiayi Weng (翁家翌), OpenAI
url: https://trinkle23897.github.io/learning-beyond-gradients/
retrieved: 2026-05-18
type: raw
tags: [AI/ML, training, architecture, paper]
---

# Learning Beyond Gradients

**Author:** Jiayi Weng (翁家翌), OpenAI

## Core Definition – Heuristic System (HS)

> "An HS contains at least a programmatic policy, state representation, feedback channels, experiment records, replays or tests, memory, and an update mechanism executed by a coding agent."

## HL vs Deep RL

| Axis | Deep RL | HL |
|---|---|---|
| Policy | Neural network parameters | Code: rules, state machines, MPC, macro-actions |
| State | Usually explicit observations | Explicit variables, detectors, caches |
| Action | NN forward pass | Executing code logic |
| Feedback | Mainly fixed reward | Environment reward + tests, logs, replays, human feedback |
| Update | Gradient-based | Direct code edits by agent |
| Memory | On-policy: none; off-policy: replay buffer | Explicit trials, summaries, diffs, failures |

## Five Key Properties of HL

1. **Explainability** – code can be translated to plain language
2. **Sample efficiency** – one effective code edit can jump to new policy
3. **Regression-testability** – old capabilities become tests/replays
4. **Constrained overfitting** – simplification, multi-seed checks
5. **Mitigate catastrophic forgetting** – rules/tests externalise knowledge

## Why HL Didn't Take Off Earlier

Hand-maintained heuristics become unmanageable: "Add one rule today to fix case A. Tomorrow, case B breaks. Add another if-statement the day after. The day after that, nobody dares delete anything."

Coding agents automate maintenance — feedback loop closes automatically in bounded systems.

## Continual Learning in HL

Forgetting becomes an **engineering problem** (not structural):
- Absorb feedback – write new failures/logs/rewards into system
- Compress history – fold local patches into simpler, maintainable representations

## Coupling Complexity

= how many interdependent states, rules, tests, and historical constraints an update must account for.

**Working hypotheses:**
- Clearer feedback → higher maintainable complexity
- Stronger models handle higher coupling
- Modularity, tests, replays shift complexity into environment
- Compression prevents decay into "big ball of mud"

## The Next Paradigm – System 1 / System 2

- **Specialised shallow NNs (S1):** perception, classification, state estimation
- **HL (S1):** fresh data handling, rules, tests, safety, local recovery
- **LLM agent (S2):** gives feedback to HL, improves data, periodically updates itself

## Key Experimental Results

### Breakout (Atari)
387 → 507 → 839 → **864** (theoretical max). No NN training. Image-only version reached 864 in 14,504 env steps.

### Ant (MuJoCo)
CPG + PD → yaw feedback → harmonics → residual MPC → **6146** (DRL range). ~106k cumulative env steps.

### HalfCheetah (MuJoCo)
Staged-tree MPC + CPG → **mean 11837** (5-episode evaluation). DRL mainstream territory.

### Atari57 Full Suite
342 search trajectories. Medium HNS at 100M env steps **significantly exceeds PPO** and other DRL baselines.

### VizDoom
D1 Basic (medikit): pure CV (OpenCV + NumPy) → mean 0.94
D3 Battle (FPS): screen CV + public game variables → competitive with DRL

## Core Philosophical Claim

> "Anything that can be continuously iterated becomes solvable – this could be the next paradigm after pretraining, RLHF, and large-scale RL/RLVR."

The thing being updated was no longer just a policy function. It was a software system with memory, feedback channels, and regression mechanisms.
