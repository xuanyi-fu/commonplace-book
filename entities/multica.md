---
type: entity
status: draft
created: 2026-04-28
updated: 2026-04-28
---

# Multica

`Multica` 是一个面向 human + agent teams 的 task collaboration / managed agents platform：官方首页把它定位成把 coding agents 变成可分配任务、汇报进展、沉淀 skills 的 teammate；官方 docs 则更具体地说，它让 humans 和 AI agents 在同一个 `workspace` 里协作，人可以像给同事派活一样把 `issue` assign 给 agent。[[sources/multica-shared-project-state-2026-04/summary|multica-shared-project-state-2026-04]] [Multica homepage](https://multica.ai/) [Multica docs](https://multica.ai/docs)

更准确地说，Multica 不是一个单次 prompt-response coding agent，而是一个把 `workspace`、`issue`、`comment`、`agent`、`skill`、task queue、session/workdir pointer 和 daemon/runtime execution 接在一起的 `[[concepts/agent-harness|agent-harness]]` / workflow-object platform。已有代码阅读结论是：它把厚状态放在平台对象和恢复指针里，再由本地 daemon 在每次执行时重建 agent workdir 和 runtime config。[[sources/multica-shared-project-state-2026-04/summary|multica-shared-project-state-2026-04]] [[syntheses/multica-shared-project-state-vs-ai-scientist|multica-shared-project-state-vs-ai-scientist]]

## Snapshot

- Product layer: project-management-like surface for assigning issues to humans or agents, tracking lifecycle, comments, blockers, task history, runtime status, and reusable skills. [Multica homepage](https://multica.ai/) [Multica docs](https://multica.ai/docs)
- Runtime layer: current official docs say agent tasks do not execute on Multica's servers in the default model; users run `multica daemon` locally, and the daemon drives local AI coding tools such as Claude Code, Codex, Cursor, Copilot, Gemini, Hermes, Kimi, OpenCode, OpenClaw, and Pi. [Multica docs](https://multica.ai/docs)
- Open-source repo: `multica-ai/multica` is a public TypeScript repo whose GitHub API description is "The open-source managed agents platform. Turn coding agents into real teammates - assign tasks, track progress, compound skills." It was created on 2026-01-13, and on the 2026-04-28 check it had about 22.1k stars, 2.7k forks, and latest release `v0.2.18` published on 2026-04-27. [GitHub repo API](https://api.github.com/repos/multica-ai/multica) [latest release API](https://api.github.com/repos/multica-ai/multica/releases/latest)
- Open-source boundary: the repo license is not plain Apache-2.0. It says Multica uses a modified Apache-2.0-style license: internal commercial use is allowed, but using the source to provide Multica as a hosted service, managed service, or embedded commercial offering to third parties requires a commercial license; frontend logo/copyright removal is also restricted. [Multica license](https://github.com/multica-ai/multica/blob/main/LICENSE)

## Why It Matters

Multica is interesting because it pushes coding-agent usage out of the individual chat/session UI and into a durable task platform. The important move is not just "agent can code"; it is that `issue`, `comment`, `agent`, `skill`, task queue, runtime status, `session_id`, and `work_dir` become first-class coordination objects. That makes it close to the same problem space as OpenAI Symphony-style issue-tracker control planes, while Multica's public implementation stores the shared state in its own platform objects and projects that state into local daemon runs. [[sources/multica-shared-project-state-2026-04/summary|multica-shared-project-state-2026-04]] [[syntheses/multica-shared-project-state-vs-ai-scientist|multica-shared-project-state-vs-ai-scientist]] [[notes/openai-codex-symphony-2026-04-reading-note|openai-codex-symphony-2026-04-reading-note]]

## People And Contributor Signal

GitHub's public contributors API shows that contributions are concentrated in a small set of accounts, but not only two people: on the 2026-04-28 check, the top returned contributors were `NevilleQingNY` with 773 contributions, `forrestchang` with 747, `Bohan-J` with 584, and `ldnvnbl` with 403, followed by a sharp drop to `devv-eve` with 35. This supports "small core team" as a repo signal, while also warning against collapsing the project to only the two named profiles. [contributors API](https://api.github.com/repos/multica-ai/multica/contributors?per_page=10)

### Jiayuan Zhang / forrestchang

`forrestchang` is the GitHub account whose public profile name is `Jiayuan Zhang`; the GitHub API profile lists company as `@multica-ai`, bio as "Building @multica-ai", and Twitter username `jiayuan_jy`. [forrestchang GitHub](https://github.com/forrestchang) [forrestchang GitHub API](https://api.github.com/users/forrestchang)

The strongest public background thread ties him to Devv.AI before Multica. Product Hunt's Devv.AI launch has a maker comment by Jiayuan introducing Devv as an AI-powered developer search engine with a vertical development-domain index and GitHub repo contextual search. [Devv.AI Product Hunt](https://www.producthunt.com/products/devv-ai?launch=devv-ai)

Secondary press coverage from EEWorld / Leiphone identifies Jiayuan Zhang as Devv AI's founder, says he worked at TikTok for nearly two years, left in October 2022, and later founded Devv AI. Treat this as useful background evidence, but weaker than first-party profile or product pages because it is a republished media article. [EEWorld / Leiphone profile](https://en.eeworld.com.cn/mp/leiphone/a376263.jspx)

### Bohan Jiang / Bohan-J

`Bohan-J` is the GitHub account whose public profile name is `Bohan Jiang`; the GitHub API profile lists company as `@multica-ai`, blog as `multica.ai`, and bio as "coFounder of @multica-ai". [Bohan-J GitHub](https://github.com/Bohan-J) [Bohan-J GitHub API](https://api.github.com/users/Bohan-J)

Bohan Jiang's public LinkedIn page says "coFounder at Devv.AI, building Multica.ai right now", lists Shanghai, links GitHub `Bohan-J`, Devv, and Multica, and lists University of Toronto education from 2017 to 2021 with CS-relevant coursework and honors. [Bohan Jiang LinkedIn](https://cn.linkedin.com/in/bohan-jiang-2941a41a3)

There are secondary due-diligence-style claims about former ByteDance experience and ReadPilot in a Medium article, but those claims were not independently confirmed in this pass. They should stay in the "secondary lead" bucket rather than the main verified biography. [Medium due diligence article](https://medium.com/%40ossinvestor.2026/i-traced-an-anonymous-github-team-to-its-founders-d83c2be22ec6)

## Funding Background

The cleanest conclusion from this pass is negative but narrow: I did not find a verifiable public Multica-specific financing announcement, investor list, round size, or lead investor. That is not proof that Multica has no financing; it only means the public evidence checked here does not support a concrete Multica funding claim.

There are company/commercial signals. The public license ends with "© 2025 Multica, Inc.", the homepage offers hosted/cloud usage plus self-hosting, and the license reserves a commercial-license requirement for hosted/managed/embedded third-party offerings. These facts support "company-backed open-source product" as a framing, but not a specific financing round. [Multica license](https://github.com/multica-ai/multica/blob/main/LICENSE) [Multica homepage](https://multica.ai/)

The related Devv.AI financing picture is mixed. EEWorld / Leiphone says Devv.AI received angel financing from a leading US-dollar fund, and Bohan Jiang's LinkedIn public activity includes a Devv.AI hiring post saying a new financing round was closing and another hiring post saying Devv.AI had investment support from a leading US-dollar fund. [EEWorld / Leiphone profile](https://en.eeworld.com.cn/mp/leiphone/a376263.jspx) [Bohan Jiang LinkedIn](https://cn.linkedin.com/in/bohan-jiang-2941a41a3)

At the same time, Latka lists Devv.AI as having `$330K` 2025 revenue, a 3-person team, and `$0` funding, while an IPAddress metadata mirror says Devv was "backed by millions in funding" in its meta description. Those contradictions make Devv.AI financing a low-confidence clue unless a primary funding announcement appears. [Latka Devv.AI profile](https://getlatka.com/companies/devv.ai) [Devv.ai metadata mirror](https://www.ipaddress.com/website/devv.ai/)

## Evidence Boundaries

- Product-positioning claims are strongest when sourced from Multica's own homepage/docs and the local code-reading source collection. [Multica homepage](https://multica.ai/) [Multica docs](https://multica.ai/docs) [[sources/multica-shared-project-state-2026-04/summary|multica-shared-project-state-2026-04]]
- Repo maturity and contributor distribution should be treated as point-in-time GitHub API observations from 2026-04-28, not stable historical facts. [GitHub repo API](https://api.github.com/repos/multica-ai/multica) [contributors API](https://api.github.com/repos/multica-ai/multica/contributors?per_page=10)
- Founder/current-role claims from GitHub profiles and LinkedIn are stronger than Medium-style due-diligence reconstruction. [forrestchang GitHub API](https://api.github.com/users/forrestchang) [Bohan-J GitHub API](https://api.github.com/users/Bohan-J) [Bohan Jiang LinkedIn](https://cn.linkedin.com/in/bohan-jiang-2941a41a3)
- Funding claims should distinguish Multica from Devv.AI. There is public evidence connecting the same people to Devv.AI and Multica, but Devv financing evidence does not automatically become Multica financing evidence.

## Related

- [[sources/multica-shared-project-state-2026-04/summary|multica-shared-project-state-2026-04]]
- [[syntheses/multica-shared-project-state-vs-ai-scientist|multica-shared-project-state-vs-ai-scientist]]
- [[notes/openai-codex-symphony-2026-04-reading-note|openai-codex-symphony-2026-04-reading-note]]
- [[concepts/agent-harness|agent-harness]]

## Sources

- [Multica homepage](https://multica.ai/)
- [Multica docs](https://multica.ai/docs)
- [Multica about](https://multica.ai/about)
- [multica-ai/multica GitHub repo](https://github.com/multica-ai/multica)
- [multica-ai/multica GitHub repo API](https://api.github.com/repos/multica-ai/multica)
- [multica-ai/multica latest release API](https://api.github.com/repos/multica-ai/multica/releases/latest)
- [multica-ai/multica contributors API](https://api.github.com/repos/multica-ai/multica/contributors?per_page=10)
- [Multica license](https://github.com/multica-ai/multica/blob/main/LICENSE)
- [forrestchang GitHub profile](https://github.com/forrestchang)
- [forrestchang GitHub API](https://api.github.com/users/forrestchang)
- [Bohan-J GitHub profile](https://github.com/Bohan-J)
- [Bohan-J GitHub API](https://api.github.com/users/Bohan-J)
- [Bohan Jiang LinkedIn](https://cn.linkedin.com/in/bohan-jiang-2941a41a3)
- [Devv.AI Product Hunt](https://www.producthunt.com/products/devv-ai?launch=devv-ai)
- [EEWorld / Leiphone Devv profile](https://en.eeworld.com.cn/mp/leiphone/a376263.jspx)
- [Latka Devv.AI profile](https://getlatka.com/companies/devv.ai)
- [Devv.ai metadata mirror](https://www.ipaddress.com/website/devv.ai/)
- [Medium due diligence article](https://medium.com/%40ossinvestor.2026/i-traced-an-anonymous-github-team-to-its-founders-d83c2be22ec6)
- [[sources/multica-shared-project-state-2026-04/summary|multica-shared-project-state-2026-04]]
- [[syntheses/multica-shared-project-state-vs-ai-scientist|multica-shared-project-state-vs-ai-scientist]]
- [[notes/openai-codex-symphony-2026-04-reading-note|openai-codex-symphony-2026-04-reading-note]]
