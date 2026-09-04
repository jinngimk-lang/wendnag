# Agent Reach usage in `wendnag`

## Purpose

Use Agent Reach as the default project-level routing skill for **external evidence collection** when researching:

- Pre-A / Seed / early Series A pitch decks and financing materials;
- AI software, Agent, embodied intelligence, robotics and smart-hardware companies;
- company websites, founder interviews, product demos and funding announcements;
- GitHub repositories and technical evidence;
- public discussions on platforms supported by Agent Reach when those discussions materially improve the research.

The skill collects evidence; it does **not** replace the project's analysis, writing, verification or copyright rules.

## Research order for BP work

Prefer evidence in this order:

1. company/founder official material;
2. regulator / exchange / government / university / event organizer source;
3. investor or accelerator source;
4. original public PDF/PPT/DOC or founder-published deck;
5. reputable media reporting;
6. third-party pitch-deck archive only as a secondary source.

For every useful financing material, record:

- company;
- stage;
- year/date;
- material type;
- original URL;
- whether the source is official;
- whether the original file is directly visible;
- whether redistribution permission is explicit;
- what part of the story is transferable to Aegiston.

## Browser / authenticated platform rules

- Start with `agent-reach doctor --json` when Agent Reach runtime is available.
- Use read-only commands for research.
- Do not automatically log in to websites.
- Do not read or extract browser cookies without an explicit user-controlled flow allowed by the upstream tool.
- Never commit cookies, tokens, passwords, session storage, downloaded profile data or private-account content.
- Do not bypass CAPTCHA, paywalls, access controls, rate limits or platform restrictions.
- Do not use write operations (post/comment/like/follow/message) for BP research.

## Copyright rule remains authoritative

Agent Reach can make a document easier to discover; that does not create permission to redistribute it.

- If a complete BP/PDF/PPT is clearly licensed for redistribution, it may be stored with license evidence.
- If redistribution permission is unclear, save the original URL, metadata, page/module analysis and short quotations only.
- If the material states confidential / do not distribute / no reproduction, do not copy it into the repository.
- Do not create a full translated replacement of an unauthorised copyrighted deck.

These rules inherit from `00-project/REQUIREMENTS_BP_BENCHMARK.md`.

## wendnag-specific research pattern

For a new comparable company:

1. Search broadly for company + stage + deck/pitch/BP/融资计划书/商业计划书.
2. Locate the earliest original source possible.
3. Verify the financing round independently where needed.
4. Read the original material page-by-page when available.
5. Separate **what the source says** from **our inference**.
6. Extract the narrative flow, evidence placement, visual hierarchy and financing-to-milestone logic.
7. Map only transferable patterns into the Aegiston rewrite recommendations.
8. Update benchmark source index and project status.

## Current structural anchor

The HuaEngine / 华擎（武汉）通信科技 22-page Pre-A financing BP is a core structure reference for the current rewrite because its flow is direct and investment-oriented:

`项目总览 → 产品/应用 → 市场/痛点 → 技术能力 → 竞品/壁垒 → 团队/客户 → 融资 → 资金用途 → 经济结果 → 里程碑`.

See `05-benchmark/sources/11-huaengine-2019-prea.md`.
