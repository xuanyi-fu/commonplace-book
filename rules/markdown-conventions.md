# LLM Wiki Markdown 约定

适用于 wiki 层页面，包括：

- `summaries/`
- `notes/`
- `entities/`
- `concepts/`
- `syntheses/`
- `sources/*/summary.md`
- 根目录下的 `index` 类页面

`sources/*/source/**` 下的原始 source 文件默认视为只读。

`sources/` 目录规则：

- `sources/` 下面的直接子项必须全部是文件夹
- 每个 `sources/<collection>/` 文件夹都必须使用 `kebab-case`
- 每个 `sources/<collection>/` 文件夹根下必须且只能有：
  - `summary.md`
  - `source/`
- 不允许把原始 source 文件直接放在 `sources/<collection>/` 根下
- 所有原始 source 文件都必须放在 `sources/<collection>/source/**`
- `sources/<collection>/source/**` 下的所有文件都必须由 Git LFS 管理
- 每个 `sources/<collection>/summary.md` 都必须包含以下 section：
  - `## Structure`
  - `## How To Use`
  - `## Summary`
  - `## Sources`
- 如果 source 文件是从其他格式清洗或整理而来，应尽量保留原文中的 inline citation、脚注标记和文内链接，方便后续跳转回被引用的材料
- 如果原始 raw source 本身可获得，应尽量把 raw source 也保存在 `sources/<collection>/source/**` 中，并优先保留其原生格式，例如 PDF、HTML、导出的邮件或截图
- cleaned markdown source note 可以作为补充，但在 raw source 可保存时，不应拿 cleaned note 替代 raw source
- 每个 `sources/<collection>/summary.md` 都必须明确说明：
  - 这个 source 主要包含什么
  - 这个 source 的结构是什么
  - 应该如何使用这个 source

`notes/` 目录规则：

- canonical source reading note 固定放在 `notes/<collection>-reading-note.md`
- reading note 为了精确引用，可以给 cleaned markdown source note 补最少量的 `^block-id`
- 不要给 raw source 文件补 `^block-id`，例如 PDF、HTML、截图或导出的邮件

## 1. Frontmatter

所有 wiki 页面必须以 frontmatter 开头，而且只允许这四个字段，顺序固定：

```md
---
type: concept
status: draft
created: 2026-04-20
updated: 2026-04-20
---
```

规则：

- 只能有 `type`、`status`、`created`、`updated`
- 不允许新增其他字段
- 字段名统一小写

### `type`

只允许以下值：

| 值 | 含义 |
| --- | --- |
| `source` | 来源说明页或来源配套 note |
| `summary` | 单一来源的总结页 |
| `note` | source-order 阅读过程中的 canonical reading note |
| `entity` | 人物、组织、产品、项目等实体页 |
| `concept` | 术语、方法、观点、模式等概念页 |
| `synthesis` | 跨来源综合分析页 |
| `index` | 导航或索引页 |

规则：

- `type` 必填
- 只能使用上表中的固定枚举值
- 页面所在目录应与 `type` 一致

### `status`

只允许以下值：

| 值 | 含义 |
| --- | --- |
| `draft` | 页面仍在整理、修正或补充 |
| `stable` | 当前可作为主要阅读版本使用 |

规则：

- `status` 必填
- 新建页面默认 `draft`
- 只有内容相对完整且结构稳定时才使用 `stable`

### `created` / `updated`

规则：

- 都必填
- 格式固定为 `YYYY-MM-DD`
- 必须是有效日期
- `updated` 不得早于 `created`
- `created` 只在页面首次创建时写入
- 每次实质性修改页面后，都要更新 `updated`

补充：

- 页面标题通过 markdown 一级标题表达，不放进 frontmatter
- 来源通过正文中的 `## Sources` 和 `[[...]]` 链接表达，不放进 frontmatter
- 标签直接写在正文中，不放进 frontmatter
- source collection 的总结页固定是 `sources/<collection>/summary.md`
- canonical source reading note 固定是 `notes/<collection>-reading-note.md`
- source collection 的原始资料固定放在 `sources/<collection>/source/**`
- 记录语言默认跟随当前讨论语言，除非用户明确要求使用其他语言
- 讨论实现细节时，如果像 `thread`、`raw memory`、`context`、`prompt`、`agent` 这类核心实现术语翻译后会模糊系统结构，应保留原术语，只翻译周围解释

## 2. 内部链接

内部链接统一使用 Obsidian wikilink：

```md
[[llm-wiki]]
[[llm-wiki#architecture]]
[[large-language-models|LLMs]]
```

规则：

- 内部链接优先使用 `[[...]]`
- alias 写法为 `[[目标页|显示文字]]`
- 首次出现的重要概念或实体，应尽量加内部链接

## 3. Block ID

只有在需要精确引用某一段内容时，才使用 block id：

```md
LLM wiki 的关键不是临时检索，而是维护一层持续演化的知识中间层。 ^core-thesis
```

引用方式：

```md
[[llm-wiki#^core-thesis]]
![[llm-wiki#^core-thesis]]
```

规则：

- 不要为每个段落机械地添加 block id
- block id 应简短、稳定、可读

## 4. Sources

来源信息统一放在 `## Sources` 小节。

示例：

```md
## Sources

- [[andrej-llm-wiki-git-gist]]
- [[some-paper]]
```

规则：

- 固定使用 `## Sources`
- 不使用 `## References`、`## Citations` 等变体
- 这里只列直接来源

## 5. Callout

语义性提示优先使用 Obsidian callout。

推荐类型：

- `summary`
- `info`
- `warning`
- `question`
- `todo`

## 6. Tags

标签直接写在正文中，例如：

```md
#llm #wiki
```

规则：

- 标签只做轻量分类
- 不要用标签替代页面和链接

## 7. 文件命名

所有文档文件名统一使用 `kebab-case`。

规则：

- 只使用小写字母、数字和连字符 `-`
- 不使用空格、下划线 `_`、驼峰或中文文件名
- 文件名应短且有语义
- 避免 `note-1`、`draft-final`、`misc` 这类名称
- canonical source reading note 使用 `<collection>-reading-note.md`

`summary` 页面额外要求：

- 文件名必须同时表达“总结对象”和“总结意图”
- 例外：如果该页面是 source collection 的总结页，则文件名固定为 `summary.md`

示例：

- `andrej-llm-wiki-summary.md`
- `obsidian-cli-help-overview.md`
- `obsidian-search-cli-comparison.md`
- `transformer-moe-2026-04-reading-note.md`

反例：

- `summary.md`
- `obsidian_cli.md`
- `MySummary.md`
- `notes.md`

## 8. `index`

### `index.md`

`index.md` 只做导航，回答“现在有什么”。

规则：

- 根目录 `index.md` 是全局索引
- `index` 只列页面链接和一句话说明
- 根目录 `index.md` 不会直接索引 `sources/**/source/**` 下的原始文件
- `sources/<collection>/` 这类资料包应通过 `sources/<collection>/summary.md` 暴露给 wiki
- `notes/` 下的 canonical reading note 在存在时应通过根目录 `index.md` 暴露给 wiki
- 页面新增、重命名或删除后，应同步更新对应的 `index`

推荐写法：

```md
- [[sources/obsidian-cli/summary|obsidian-cli]]: summary page for the `sources/obsidian-cli/` collection
- [[sources/andrej-llm-wiki-git-gist/summary|andrej-llm-wiki-git-gist]]: summary page for the `sources/andrej-llm-wiki-git-gist/` collection
```

## 9. Git History

Git history is the only change history. Do not use `log.md`.

规则：

- `scripts/lint.py` 实现了当前 deterministic 规则子集
- `scripts/check_links.py` 负责检查 wiki-layer 页面中的内部链接、heading anchor 和 block-id citation 是否可解析
- 通过 `uv run pre-commit install` 安装 repo-managed commit hooks
- 通过 `uv run pre-commit run --all-files` 手动运行完整 hook 套件
- 每次逻辑更新在 commit 之前都必须先运行 `uv run python scripts/lint.py`
- commit-time hook 会在每次 commit 时运行全库 `scripts/lint.py`，并对 staged wiki-layer markdown 页面运行 `scripts/check_links.py`
- 只有 lint 通过后，才能创建 commit
- 每次逻辑更新都必须以一个 git commit 结束
- commit 格式固定为 `<type>(<scope>): <subject>`
- `type` 只允许 `docs`、`chore`、`refactor`
- `subject` 使用小写英文、动词开头、简短、不加句号

推荐写法：

```md
chore(repo): initialize git repository
docs(source/obsidian-cli): add official cli snapshots
docs(summary/obsidian-cli): summarize source collection
```

## 当前待讨论问题

1. section 标题是否坚持用英文，还是允许中文标题？
2. `source` 配套页面如果存在，最小结构应该是什么？
