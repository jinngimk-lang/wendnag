# Agent Reach upstream integration

This project vendors the **skill layer** of Agent Reach for research routing.

- Upstream repository: https://github.com/Panniantong/Agent-Reach
- Upstream pinned commit inspected for this integration: `da5044d26fc6adddb6554d5679c94ac22e76e428`
- License: MIT (`LICENSE` in this directory)
- Upstream install guide: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md

## Why only the skill layer is vendored

`wendnag` is a BP/research repository, not a Python application. Agent Reach itself is designed to keep runtime files and upstream tools outside the user's project workspace under `~/.agent-reach/` and temporary output under `/tmp/`. Vendoring the complete Python runtime here would pollute the BP repository and create avoidable dependency drift.

Therefore this repository keeps:

- `SKILL.md` — upstream routing rules;
- `references/` — project-relevant routing notes;
- `LICENSE` — upstream MIT license;
- `PROJECT_USAGE.md` — wendnag-specific research and safety rules.

The actual runtime should be installed separately when needed, following the upstream guide. Start with the read-only health check:

```bash
agent-reach install --env=auto
agent-reach doctor --json
```

Do not use `--system`, import browser credentials, or configure authenticated channels unless the user has explicitly approved those system/account changes for the environment being used.

## Update policy

Before a major external-research sprint:

1. Check the upstream repository for a newer release/commit.
2. Review license and security changes.
3. Diff the upstream `agent_reach/skill/` directory against this vendored copy.
4. Import only useful, compatible changes.
5. Preserve local rules in `PROJECT_USAGE.md`.
6. Record the new upstream commit here.
