---
type: Agent Rule
title: Ollama OKF Agent Rule
description: Ollama-specific rules for using compact OKF context packs.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/agents/ollama.md
tags: [okf, ollama, agent-rule]
applies_to: [ollama]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-24T15:54:09+01:00
---

# Purpose

Use small, explicit OKF context packs for local model workflows.

# Applies To

Ollama CLI or local OpenAI-compatible endpoint workflows.

# Required Behaviour

Build a context pack with only relevant OKF concepts, source snippets, task instructions, and output requirements.

# Prohibited Behaviour

Do not treat Ollama output as accepted project knowledge until reviewed.

# Pre-Task Checklist

- Generate or curate a compact context pack.
- Include verification status for relevant concepts.

# Post-Task Checklist

- Mark Ollama recommendations as unverified until reviewed.
- Convert useful output into OKF concepts before relying on it.

# Escalation Conditions

Escalate when a local model's limitations could affect correctness or safety.
