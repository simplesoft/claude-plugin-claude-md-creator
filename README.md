# claude-md-creator


Claude Code 用のスキル。既存のコードベースを解析し、CLAUDE.md および README.md を自動生成します。

## 概要

Claude Code でプロジェクトのドキュメントを効率的に作成するためのスキルです。コードベースの構造・依存関係・設定ファイルを自動解析し、プロジェクトに最適化された CLAUDE.md（Claude Code 用）と README.md（人間用）を生成します。

## 使い方

Claude Code のスキルとしてインストールし、以下のようなフレーズで起動します：

- 「CLAUDE.md を作って」
- 「README を生成」
- 「analyze this project」
- 「create project docs」

## ワークフロー

1. **解析** — `analyze_codebase.py` でコードベースを自動スキャン
2. **深読み** — エントリーポイント、設定ファイル、依存ファイルを詳細に読み込み
3. **確認** — コードから推測できない情報のみユーザーに質問
4. **生成** — ドラフトを作成
5. **レビュー** — ユーザーと反復的に改善

## プロジェクト構造

```
claude-md-creator/
├── SKILL.md                          # スキル定義（メタデータ + ワークフロー）
├── scripts/
│   └── analyze_codebase.py           # コードベース解析スクリプト
├── references/
│   └── claude-md-guide.md            # CLAUDE.md ベストプラクティス
└── LICENSE                           # Apache License 2.0
```

## 解析スクリプト

`analyze_codebase.py` は対象プロジェクトをスキャンし、以下の情報を JSON で出力します：

- 使用言語とファイル数
- 依存関係ファイル（package.json, composer.json, requirements.txt 等）
- 設定ファイル（Docker, CI/CD, Linter 等）
- ディレクトリ構造
- 環境変数
- データベース利用の兆候
- 既存ドキュメント

```bash
python3 scripts/analyze_codebase.py /path/to/project
```

## ライセンス

Copyright 2026 simplesoft, Inc.

Licensed under the [Apache License, Version 2.0](LICENSE).
