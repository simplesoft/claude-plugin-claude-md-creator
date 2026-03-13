---
name: project-docs
description: >
  Analyze an existing codebase and generate CLAUDE.md and/or README.md files for Claude Code development.
  Use when: (1) User wants to create CLAUDE.md for a project, (2) User wants to generate README.md from code,
  (3) User is migrating a project to Claude Code and needs project documentation,
  (4) User says "analyze this project", "create project docs", "generate CLAUDE.md", "generate README".
  Triggers on phrases like: "CLAUDE.mdを作って", "READMEを生成", "プロジェクトドキュメント作成",
  "analyze codebase", "project setup docs". Default output is CLAUDE.md; README.md is optional.
---

# Project Docs Generator

Generate CLAUDE.md and/or README.md by analyzing an existing codebase. Default: CLAUDE.md only.

## Workflow

1. **Analyze** the codebase (run `analyze_codebase.py`)
2. **Deep-read** key files (entry points, configs, dependency files)
3. **Ask** the user only for what cannot be inferred (purpose, priorities, constraints)
4. **Generate** draft document(s)
5. **Present** to user for review and iterate

## Step 1: Analyze

Run the analysis script on the project root:

```bash
python3 SKILL_DIR/scripts/analyze_codebase.py /path/to/project
```

Outputs JSON with: languages, dependencies, directory structure, config files, env vars, database indicators, existing docs.

## Step 2: Deep-read Key Files

Analysis script gives an overview. Go deeper by reading:
- Entry points (index.php, main.py, app.js, manage.py, etc.)
- Dependency files (composer.json, package.json, requirements.txt, Gemfile, etc.)
- Config files (environment configs, DB configs, CI/CD configs)
- .htaccess or nginx config (routing rules)
- Existing documentation (any .md files detected)

This step is critical — the quality of generated docs depends on understanding the actual code, not just file counts.

## Step 3: Ask User (Minimal)

Only ask for information that code analysis cannot reveal. Batch all questions into one message:

- Project purpose / business context
- Current work: what step or task is underway right now
- Development priorities or migration goals
- Technical constraints or rules (e.g., "don't touch X", "must support Y")
- Team conventions (coding standards, commit style, etc.)
- Preferred language for the document (default to user's language)

Do NOT ask about: tech stack, directory structure, dependencies, build commands — these are detectable from code.

## Step 4: Generate

### CLAUDE.md and README.md Have Different Roles

| | CLAUDE.md | README.md |
|---|---|---|
| Reader | Claude Code | Human developers |
| Purpose | Work context + rules | Project overview |
| Content | What Claude can't infer | Comprehensive reference |
| Limit | Under 200 lines (truncated beyond) | No limit |

**They may overlap on "current work status"** — this is intentional since the readers are different.
**Do NOT duplicate detailed information** across files. If README.md has a detailed systems list, CLAUDE.md should not repeat it. Instead, reference the other file.

### CLAUDE.md: What to Include / Exclude

**Include (Claude can't infer these from code):**
- Project context in 2-3 lines (what it does, current status)
- Current work (which step/task, just started or in progress)
- Step overview (numbered list of the migration/development plan)
- Technical constraints and rules (must/must-not)
- Working notes (things Claude gets wrong repeatedly)
- Environment switching logic (if non-obvious)
- Key file paths with brief role descriptions
- Development commands (build, test, run)
- References to related doc files

**Exclude (Claude can read these from code):**
- Detailed tech stack versions (visible in dependency files)
- Full directory listing (visible via ls/glob)
- Related system details (put in README.md or RELATED_SYSTEMS.md)
- Project history/background (put in README.md)
- Generic best practices

**Style rules:**
- Use imperative form ("Use X" not "You should use X")
- Be concise and project-specific, no generic advice
- Use the user's language (日本語 or English)
- Reference files by name only (e.g., `CURRENT_ENVIRONMENT.md`), not with `@./` or link syntax

### CLAUDE.md Template

```markdown
Project Name — One-line description

# プロジェクトコンテキスト
[2-3行。何をするアプリか、現在の状態]

## 現在の作業
[今取り組んでいるステップ/タスク]

## ステップ全体像
[番号付きリスト。現在位置を ← 現在 で示す]

# 技術的な制約・ルール
[箇条書き。やるべきこと、やってはいけないこと]

# 作業時の注意事項
[箇条書き。Claudeが知るべき注意点]

# 現行技術スタック
[1行ずつ簡潔に。詳細はコードを読めばわかるので概要のみ]

# プロジェクト構造
[主要ディレクトリとファイルの役割。ツリー形式]

# 環境判定
[環境切り替えロジックがある場合のみ]

# 開発コマンド
[コードブロックで。build, test, run等]

# 関連ドキュメント
[他のmdファイルへの参照。箇条書き]
```

### README.md Template

```markdown
Project Name — One-line description

# このプロジェクトについて
[プロジェクトの説明、背景、目的]

## 現在の作業
[現在のステップ/タスク]

## ゴール
[当面のゴール、最終ゴール]

## ステップ
[テーブル形式で。現在位置を示す]

# システム構成
## 技術スタック
[フロントエンド、バックエンド、DB、インフラ]

## ディレクトリ構造
[ツリー形式。各ディレクトリに説明コメント]

## 関連するシステム
[テーブル形式: システム名 | 連携概要]

# バッチ処理
[ある場合のみ。cron/手作業を分けて記載]

# 開発環境
## 開発コマンド
[コードブロックで]

## デプロイ
[環境ごとの手順。未整備なら「未整備」と明記]

# ドキュメント
[テーブル形式: ドキュメント名 | ステータス | 内容]
```

### Handling Multiple Documentation Files

大規模プロジェクトでは関連ドキュメントが複数ある。役割分担の原則:

| ファイル | 役割 |
|---|---|
| CLAUDE.md | Claude Code用。制約・ルール・現在の作業コンテキスト |
| README.md | 人間用。プロジェクト全体像・構成・手順 |
| CURRENT_ENVIRONMENT.md等 | 詳細リファレンス（環境構成、機能一覧等） |
| RELATED_SYSTEMS.md等 | 外部連携の詳細 |

README.mdには概要テーブル（索引）、詳細ファイルに本文。CLAUDE.mdは詳細を持たず参照のみ。

### Common Pitfalls to Avoid
- 空セクションを作らない。内容がなければセクション自体を省くか「（未整備）」と明記
- `@./ファイル名` のような独自記法を使わない。ファイル名をそのまま書く
- PHPExcelのような「使っていないが残っている」ものは「使用していない」と明記するか省略
- テーブル形式を活用する（ステップ一覧、関連システム、ドキュメント一覧等）

## Step 5: Review & Iterate

Present the draft and ask:
- "この内容で問題ないですか？追加・修正したい点があれば教えてください。"
- "Does this look good? Any additions or corrections?"

Iterate until the user is satisfied, then write the file.

## Reference

For CLAUDE.md best practices, see [claude-md-guide.md](references/claude-md-guide.md).

---

Copyright 2026 simplesoft, Inc. Licensed under the [Apache License, Version 2.0](LICENSE).
