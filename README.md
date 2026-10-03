# QRコード生成ツール

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B%20(tested%203.13)-blue.svg)

URL から簡単に QRコードを生成・保存できるシンプルなデスクトップアプリケーション。完全オフライン動作で、直感的なGUIとファイル保存機能を備えています。

## 特徴

- 📝 **シンプルな操作**: テキストボックスに URL を貼り付けて実行
- 🖼️ **リアルタイム表示**: QRコードを画面にすぐに表示
- 💾 **複数形式対応**: PNG / JPG 形式で保存可能
- 🖱️ **右クリックメニュー**: 画像上での右クリックで保存
- 🌐 **完全オフライン動作**: インターネット接続不要
- ⌨️ **キーボード操作対応**: Enter キーで素早く生成

## 必要な環境

- Python 3.10以上（動作確認・推奨バージョンは **Python 3.13**）
- tkinter（通常Pythonに同梱）
- Pillow ライブラリ
- qrcode ライブラリ

## インストール

### リポジトリのクローン
```bash
git clone https://github.com/git-kazumi/qrcode-generator.git
cd qrcode-generator
```

### 仮想環境の作成（推奨）
```bash
# Windows（Python Install Manager）
py -V:3.13 -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python3.13 -m venv .venv
source .venv/bin/activate
```

### 依存ライブラリのインストール

依存パッケージは、用途に応じて2つのファイルに分けています。

| ファイル | 対象 | 内容 |
|----------|------|------|
| `requirements.txt` | アプリを実行する方 | qrcode・Pillow とその依存パッケージ |
| `requirements-dev.txt` | 開発・exe化を行う方 | `requirements.txt` の内容 + 開発用ツール |

#### アプリを実行する場合

```bash
pip install -r requirements.txt
```

#### 開発・exe化を行う場合

```bash
pip install -r requirements-dev.txt
```

`requirements-dev.txt` は先頭で `requirements.txt` を読み込んでいるため、実行用のパッケージも一緒にインストールされます。追加される開発用ツールは以下のとおりです。

| ツール | 用途 |
|--------|------|
| [Nuitka](https://nuitka.net/) | exeファイルの作成 |
| [zstandard](https://pypi.org/project/zstandard/) | Nuitka（onefile形式）での圧縮 |
| [pip-audit](https://pypi.org/project/pip-audit/) | 依存パッケージの脆弱性チェック |

## 使い方

### 基本的な起動
```bash
python qrcode_generator.py
```

ウィンドウが起動し、URL 入力フィールドが表示されます。

### 基本的な操作

1. **URL を入力** - テキストボックスに URL を貼り付け
2. **QRコード生成** - 「QRコード生成」ボタンをクリックするか Enter キーを押す
3. **画像を保存** - 表示された QRコード上で右クリック
4. **ファイル形式を選択** - PNG または JPG で保存

## 操作方法

### キーボード操作

| キー | 機能 |
|------|------|
| Enter | 入力フィールドの Enter キーで QRコード生成 |

### マウス操作

| 操作 | 機能 |
|------|------|
| 右クリック（QRコード上） | コンテキストメニューを表示 |
| PNG として保存 | PNG 形式で保存ダイアログを開く |
| JPG として保存 | JPG 形式で保存ダイアログを開く |
| クリップボードにコピー | 未実装（PNG/JPG での保存方法を案内するダイアログを表示） |

### ボタン

- **QRコード生成** - テキストボックスの URL からQRコードを生成
- **クリア** - 入力欄とQRコード表示をリセット

## exeファイルの作成（Windows）

[Nuitka](https://nuitka.net/) を使用して、単体で動作するexeファイルを作成できます。

### 事前準備

開発用ツールをインストールしておきます。

```powershell
pip install -r requirements-dev.txt
```

Python 3.13 では Nuitka の MinGW64 が使用できないため、**Visual Studio Build Tools**（C++ によるデスクトップ開発）が必要です。

```powershell
winget install Microsoft.VisualStudio.2022.BuildTools --override "--wait --passive --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
```

### ビルド

```powershell
# 実行用パッケージの脆弱性チェック（問題がないことを確認してからビルドする）
pip-audit -r requirements.txt

# exeファイルの作成
python -m nuitka `
  --mode=onefile `
  --windows-console-mode=disable `
  --enable-plugin=tk-inter `
  --msvc=latest `
  --output-dir=build `
  --output-filename=qrcode_generator.exe `
  --onefile-tempdir-spec="{CACHE_DIR}/QRCodeGenerator/{VERSION}" `
  --product-name="QRコード生成ツール" `
  --file-version=1.1.0 `
  --product-version=1.1.0 `
  --assume-yes-for-downloads `
  --remove-output `
  qrcode_generator.py
```

`build\qrcode_generator.exe` が作成されます。

> ⚠️ `--file-version` / `--product-version` はリリースごとに必ず更新してください。展開先フォルダがバージョンごとに分かれているため、更新しないと古いファイルが使われる場合があります。

## 動作仕様

### オフライン動作
このアプリケーションは完全にオフライン環境で動作します。外部サービスへの通信は一切発生しません。

### ファイル保存
生成されたQRコードは以下の形式で保存できます：

| 形式 | 特徴 | 用途 |
|------|------|------|
| PNG | ロスレス圧縮、透明度対応 | Web・文書・アーカイブ |
| JPG | 圧縮率高、色数豊富 | メール・SNS共有 |

### エラーハンドリング

| 状況 | 動作 |
|------|------|
| URL未入力 | 警告ダイアログを表示 |
| URLの形式でない文字列 | 確認ダイアログを表示（「はい」でそのまま生成、「いいえ」で中止） |
| QRコード生成失敗 | エラーダイアログを表示 |
| ファイル保存失敗 | エラーダイアログを表示 |

URLの形式は、`http://` または `https://` で始まり、ホスト名（ドメイン）を含むものとして判定します。QRコード自体はURL以外の文字列も格納できるため、形式が異なる場合も確認のうえで生成できます。

## 出力例

```
            QRコード生成ツール
┌─ URL入力 ──────────────────────────┐
│ URL: [https://github.com         ] │
└────────────────────────────────────┘
       [QRコード生成] [クリア]
┌─ QRコード ─────────────────────────┐
│                                    │
│           ███████████              │
│           ███████████              │
│           ███████████              │
│                                    │
└────────────────────────────────────┘
 ✓ QRコード生成完了: https://github.com...
```

## ソースコード構成

```python
QRCodeGeneratorApp          # アプリケーション本体のクラス
├ setup_ui()                # 画面部品の配置
├ is_valid_url(text)        # URLの形式かどうかを判定
├ generate_qrcode()         # URL→QRコード生成
├ display_qrcode_on_canvas()# QRコードを画面に表示
├ clear_qrcode()            # 入力欄と表示をリセット
├ show_context_menu()       # 右クリックメニュー表示
├ save_as_png()             # PNG形式で保存
├ save_as_jpg()             # JPG形式で保存
└ copy_to_clipboard()       # 未実装（保存方法を案内）

main()                      # 起動処理
```

## カスタマイズ例

### デフォルトウィンドウサイズの変更

`__init__`メソッドの以下の行を修正：

```python
self.root.geometry("600x700")  # 幅x高さ
self.root.geometry("800x900")  # より大きいサイズに変更
```

### QRコード生成オプションの調整

`generate_qrcode()`メソッドの QRCode 初期化部分を修正：

```python
qr = qrcode.QRCode(
    version=1,                          # 1-40 (大きいほど詳細)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # L/M/Q/H
    box_size=10,                        # ピクセルサイズ
    border=4,                           # 枠のサイズ
)
```

### フォント・色のカスタマイズ

各ウィジェット作成時のフォント・色を変更：

```python
title_label = ttk.Label(
    self.root,
    text="QRコード生成ツール",
    font=("Arial", 20, "bold")  # フォント変更
)
```

## 日本語対応

このアプリケーションは日本語環境を前提としています。タイトルのみ`Arial`を指定し、それ以外はOS標準のフォント（ttkの既定フォント）を使用しています。`Arial`に含まれない日本語の文字は、OSが自動的に日本語フォントで代替表示します。

## ライセンス

MIT License - 詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 著作権

Copyright (c) 2026 大杉一実 (ohsugi kazumi)

## 既知の制限事項

- Windows/macOS/Linuxで動作確認済み（GUIはplatform依存）
- ネットワーク接続は不要（完全オフライン動作）
- QRコードのサイズは自動調整（キャンバスに合わせてリサイズ）
- クリップボード直接コピー機能は未実装（ファイル保存で対応）

## トラブルシューティング

### tkinterが見つからないエラー
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (Homebrew)
brew install python-tk@3.13
```

Windows では、tkinter は pip ではインストールできません（PyPI の `tk` は tkinter とは無関係のパッケージです）。Python をインストールし直し、オプション「**tcl/tk and IDLE**」を有効にしてください。

### Pillow/qrcode のインストールに失敗する場合

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### QRコードが表示されない

- URL が正しく入力されているか確認
- ウィンドウをリサイズしてキャンバスを大きくする
- クリアボタンで一度リセットして再度生成

### exe作成時に「cannot locate suitable C compiler」と表示される

Python 3.13 では MinGW64 が使用できません。「[exeファイルの作成（Windows）](#exeファイルの作成windows)」の事前準備に従って Visual Studio Build Tools をインストールし、`--msvc=latest` を指定してください。

## 貢献

バグ報告や機能提案は[Issues](https://github.com/git-kazumi/qrcode-generator/issues)セクションにお願いします。

## 更新履歴

### v1.1.0 (2026-10-03)
- 開発・動作確認環境を Python 3.11 から **Python 3.13** へ移行
- 動作環境を Python 3.10以上に変更（Pillow 12 系が Python 3.9 に非対応のため）
- URLの形式でない文字列を入力した場合に、生成してよいか確認するダイアログを追加
- 例外処理のコメントを実際の処理内容に合わせて修正
- 依存パッケージを更新し、実行用の `requirements.txt` と開発用の `requirements-dev.txt` に分割
- colorama を Windows 環境でのみインストールするよう変更（qrcode の Windows 専用の依存のため）
- 脆弱性チェックツール [pip-audit](https://pypi.org/project/pip-audit/) を開発環境に導入
- Nuitka によるexeファイル作成手順を追加（Python 3.13 対応のため MSVC を使用）
- README の記載をソースコードの実際の動作に合わせて修正（フォント、エラーハンドリング、右クリックメニュー、画面構成、Windows での tkinter の導入方法）

### v1.0.0 (2026-04-16)
- 初回リリース
- URL からの QRコード生成・表示
- PNG / JPG 形式での保存（右クリックメニュー）

---

**最終更新**: 2026年10月
