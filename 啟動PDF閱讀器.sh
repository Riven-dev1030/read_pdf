#!/bin/bash
# PDF閱讀器 - Linux/Mac 啟動腳本
# 此腳本會自動啟動 PDF 閱讀器 GUI

echo "PDF閱讀器 啟動中..."

# 檢查是否已安裝 Python
if ! command -v python3 &> /dev/null; then
    echo "錯誤：未找到 Python！"
    echo "請先安裝 Python 3.6 或更高版本"
    exit 1
fi

# 檢查是否已安裝必要的套件
if ! python3 -c "import pypdf" &> /dev/null; then
    echo "正在安裝必要的套件..."
    python3 -m pip install pypdf
    if [ $? -ne 0 ]; then
        echo "套件安裝失敗！"
        exit 1
    fi
fi

# 啟動 GUI
echo "正在啟動 PDF 閱讀器..."
python3 pdf_reader_gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo "程式執行出錯！"
    read -p "按任意鍵退出..."
fi
