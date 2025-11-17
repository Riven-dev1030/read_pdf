@echo off
:: PDF閱讀器 - Windows 啟動腳本
:: 此腳本會自動啟動 PDF 閱讀器 GUI

title PDF閱讀器

:: 檢查是否已安裝 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 錯誤：未找到 Python！
    echo 請先安裝 Python 3.6 或更高版本
    echo 下載地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 檢查是否已安裝必要的套件
python -c "import pypdf" >nul 2>&1
if errorlevel 1 (
    echo 正在安裝必要的套件...
    python -m pip install pypdf
    if errorlevel 1 (
        echo 套件安裝失敗！
        pause
        exit /b 1
    )
)

:: 啟動 GUI
echo 正在啟動 PDF 閱讀器...
python pdf_reader_gui.py

if errorlevel 1 (
    echo.
    echo 程式執行出錯！
    pause
)
