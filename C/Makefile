# Makefile

# コンパイラ
CC = gcc

# インクルードディレクトリ
INCLUDE_DIR = "C:/Program Files (x86)/National Instruments/NI-DAQ/DAQmx ANSI C Dev/include"

# ライブラリディレクトリ
LIB_DIR = "C:/Program Files (x86)/National Instruments/Shared/ExternalCompilerSupport/C/lib64/msvc"

# 出力ファイル名
OUTPUT = bin/main.exe

# ソースファイル
SRC = src/main.c

# コンパイルフラグ
CFLAGS = -I$(INCLUDE_DIR) -L$(LIB_DIR) -lNIDAQmx

# デフォルトのターゲット（main.exeをビルド）
all: $(OUTPUT)

# 出力ファイルを生成
$(OUTPUT): $(SRC)
	$(CC) $(SRC) $(CFLAGS) -o $(OUTPUT)

# クリーンアップ（生成された実行ファイルを削除）
clean:
	rm -f $(OUTPUT)
