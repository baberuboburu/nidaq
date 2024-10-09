# NI-DAQmx C Program Project

## プロジェクト概要
このプロジェクトでは、Windows環境でNI-DAQmxドライバを使用してC言語プログラムを作成・コンパイルします。VSCodeを使用して、Makefileを使った簡単なビルドおよび`tasks.json`によるコンパイルを行います。
  
  
## ディレクトリ構成
nidaq(root)  
|_ .vscode  
  |_ tasks.json (実行するときに必要なファイル)  
|_ bin/ (コンパイルされたファイルが格納される)  
  |_  
|_ src/  
  |_ main.c (処理が記述されたファイル)  
|_ Makefile (実行するときに必要なファイル)  
  
  

## 環境構築

1. **WindowsでC言語の環境を構築する**
   - **VSCodeをインストールする**: [VSCodeのダウンロード](https://code.visualstudio.com/)
   - **VSCodeの拡張機能「C/C++」をインストールする**:
     - VSCode内の拡張機能マーケットプレースで「C/C++」を検索してインストール。

2. **GCCのインストール**
   - [MSYS2のインストール](https://www.msys2.org) に従ってMSYS2をインストール。
   - インストール後、以下のコマンドでGCCをインストール:
     ```bash
     pacman -S mingw-w64-ucrt-x86_64-gcc
     ```
   - **環境変数にMSYS2のパスを追加**:
     - `C:\msys64\ucrt64\bin` を `Path` に追加。
   - VSCodeを再起動して、設定を反映させる。

3. **Makeコマンドのインストール**
   - MSYS2で以下のコマンドを実行して`make`をインストール:
     ```bash
     pacman -S make
     ```
   - **環境変数にMakeのパスを追加**:
     - `C:\msys64\usr\bin` を `Path` に追加。
   - VSCodeを再起動。

4. **NI-DAQmxのドライバをダウンロード/インストール**
   - [NI-DAQmx ドライバのダウンロード](https://www.ni.com/ja/support/downloads/drivers/download.ni-daq-mx.html)からWindows用NI-DAQmxドライバをダウンロード。
   - インストーラーを開き、手順に従ってインストール。

5. **`tasks.json`の確認**
   - `tasks.json` の `args` プロパティで次の項目を確認し、正しいパスを指定:
     - **`-I`**: `NIDAQmx.h` があるディレクトリのパス。
     - **`-L`**: `NIDAQmx.lib` があるディレクトリのパス。

6. **`Makefile`の確認**
   - `Makefile` でも、同様に `-I` と `-L` のパスを変更し、正しいパスを指定。

## 実行方法

### 方法 1: VSCodeの`tasks.json`を使ってコンパイル
1. **`Ctrl + Shift + B`** で `main.c` をコンパイル。
2. **`./bin/main.exe`** で実行。

### 方法 2: Makefileを使ってビルド
1. プロジェクトのルートディレクトリ（`nidaq`）で、以下のコマンドを実行してビルド:
   ```bash
   make
2. ./bin/main.exe で実行。
