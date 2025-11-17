#!/bin/bash
# PDF Reader GUI 依賴安裝腳本
# 適用於 Ubuntu/Debian 系統

echo "======================================================================"
echo "PDF Reader GUI - 安裝必要組件"
echo "======================================================================"
echo ""

# 更新套件列表
echo "[1/3] 更新套件列表..."
sudo apt-get update

echo ""
echo "[2/3] 安裝 Python Tkinter..."
sudo apt-get install -y python3-tk

echo ""
echo "[3/3] 安裝中文字體..."
echo "  - 安裝 Noto Sans CJK (思源黑體)"
sudo apt-get install -y fonts-noto-cjk

echo "  - 安裝文泉驛微米黑"
sudo apt-get install -y fonts-wqy-microhei

echo ""
echo "======================================================================"
echo "安裝完成！"
echo "======================================================================"
echo ""
echo "已安裝的組件："
echo "  ✓ Python Tkinter (圖形界面庫)"
echo "  ✓ Noto Sans CJK (思源黑體 - 支援繁體/簡體中文)"
echo "  ✓ WenQuanYi Micro Hei (文泉驛微米黑)"
echo ""
echo "請重新啟動 PDF Reader GUI："
echo "  python3 pdf_reader_gui.py"
echo ""
