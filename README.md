# QRコード生成ツール

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

URL から簡単に QRコードを生成・保存できるシンプルなデスクトップアプリケーション。完全オフライン動作で、直感的なGUIとファイル保存機能を備えています。

## 特徴

- 📝 **シンプルな操作**: テキストボックスに URL を貼り付けて実行
- 🖼️ **リアルタイム表示**: QRコードを画面にすぐに表示
- 💾 **複数形式対応**: PNG / JPG 形式で保存可能
- 🖱️ **右クリックメニュー**: 画像上での右クリックで保存
- 🌐 **完全オフライン動作**: インターネット接続不要
- ⌨️ **キーボード操作対応**: Enter キーで素早く生成

## 必要な環境

- Python 3.9以上
- tkinter（通常Pythonに同梱）
- Pillow ライブラリ
- qrcode ライブラリ

## インストール

### リポジトリのクローン
```bash
git clone https://github.com/git-kazumi/qrcode-generator.git
cd qrcode-generator
```

### 依存ライブラリのインストール
```bash
pip install qrcode[pil] pillow
```

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

### ボタン

- **QRコード生成** - テキストボックスの URL からQRコードを生成
- **クリア** - 入力欄とQRコード表示をリセット

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
| 無効なURL | QRコード生成時に警告 |
| ファイル保存失敗 | エラーダイアログを表示 |

## 出力例

```
QRコード生成ツール
┌────────────────────────────────────┐
│ URL: https://github.com           │
│        [生成] [クリア]              │
├────────────────────────────────────┤
│                                    │
│           ███████████              │
│           ███████████              │
│           ███████████              │
│                                    │
├────────────────────────────────────┤
│ ✓ QRコード生成完了: https://g...  │
└────────────────────────────────────┘
```

## ソースコード構成

```python
generate_qrcode()           # URL→QRコード生成
display_qrcode_on_canvas()  # QRコードを画面に表示
save_as_png()               # PNG形式で保存
save_as_jpg()               # JPG形式で保存
show_context_menu()         # 右クリックメニュー表示
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

このアプリケーションは日本語環境を前提としています。フォントは`Arial`と`MS Gothic`のフォールバックを使用しています。

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
brew install python-tk@3.11

# Windows
pip install tk
```

### Pillow/qrcode のインストールに失敗する場合

```bash
pip install --upgrade pip
pip install qrcode[pil] pillow --upgrade
```

### QRコードが表示されない

- URL が正しく入力されているか確認
- ウィンドウをリサイズしてキャンバスを大きくする
- クリアボタンで一度リセットして再度生成

## 貢献

バグ報告や機能提案は[Issues](https://github.com/git-kazumi/qrcode-generator/issues)セクションにお願いします。

---

**最終更新**: 2026年4月
