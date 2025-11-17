# PDF Reader - PDF閱讀器

一個簡單易用的Python PDF閱讀工具，可以提取和顯示PDF檔案的文本內容。

A simple and easy-to-use Python PDF reading tool that can extract and display text content from PDF files.

## 功能特性 Features

- 📖 讀取整個PDF檔案或指定頁面
- 📊 顯示PDF基本資訊（總頁數）
- 📋 提取PDF元資料（作者、標題等）
- 🔍 **搜尋功能**：在PDF中查找關鍵詞並顯示位置
- 📍 顯示搜尋結果的上下文內容
- 🔤 支援大小寫敏感/不敏感搜尋
- 💻 支援命令列參數
- 🌏 中文友好

## 安裝 Installation

1. 複製倉庫或下載檔案
2. 安裝依賴：

```bash
pip install -r requirements.txt
```

## 使用方法 Usage

### 基本用法

#### 閱讀PDF
```bash
# 讀取整個PDF檔案
python pdf_reader.py document.pdf

# 讀取指定頁（例如第1頁）
python pdf_reader.py document.pdf -p 1

# 顯示PDF元資料
python pdf_reader.py document.pdf -m

# 讀取第3頁並顯示元資料
python pdf_reader.py document.pdf -p 3 -m
```

#### 搜尋PDF內容
```bash
# 搜尋PDF中的關鍵詞（不區分大小寫）
python pdf_reader.py document.pdf -s "關鍵詞"

# 搜尋英文關鍵詞
python pdf_reader.py document.pdf -s "keyword"

# 區分大小寫搜尋
python pdf_reader.py document.pdf -s "KeyWord" -c

# 自訂顯示的上下文字元數（預設50字元）
python pdf_reader.py document.pdf -s "搜尋內容" --context 100
```

### 命令列參數

#### 基本參數
- `pdf_file`: PDF檔案路徑（必需）
- `-h, --help`: 顯示幫助資訊

#### 閱讀模式
- `-p, --page NUM`: 指定要讀取的頁碼（從1開始）
- `-m, --metadata`: 顯示PDF元資料資訊

#### 搜尋模式
- `-s, --search TEXT`: 在PDF中搜尋指定文本內容
- `-c, --case-sensitive`: 搜尋時區分大小寫（預設不區分）
- `--context CHARS`: 搜尋結果顯示的上下文字元數（預設50）

### 示例

```bash
# 讀取報告PDF的第5頁
python pdf_reader.py report.pdf --page 5

# 查看PDF的元資料資訊
python pdf_reader.py book.pdf --metadata

# 在技術文檔中搜尋"API"關鍵詞
python pdf_reader.py technical_doc.pdf -s "API"

# 在合同中區分大小寫搜尋"Section 3.1"
python pdf_reader.py contract.pdf -s "Section 3.1" -c
```

### 搜尋功能說明

搜尋功能會：
- 🔍 掃描PDF的所有頁面
- 📄 顯示包含關鍵詞的所有頁碼
- 📍 **精確顯示每個匹配在第幾頁第幾行**
- 📊 統計每頁找到的匹配次數
- 📝 顯示每個匹配項的上下文內容（用【】標記）
- ✅ 支援中英文搜尋

搜尋結果示例：
```
============================================================
PDF檔案: example.pdf
搜尋內容: 'Python'
區分大小寫: 否
============================================================

第 1 頁 - 找到 2 處匹配:
------------------------------------------------------------
  [1] 第 3 行: ...This guide introduces【Python】programming language...
  [2] 第 15 行: ...Learn【Python】in 30 days with...

第 5 頁 - 找到 1 處匹配:
------------------------------------------------------------
  [1] 第 7 行: ...Advanced【Python】techniques for...

============================================================
搜尋完成！
共在 2 頁中找到 3 處匹配
頁碼: 1, 5
============================================================
```

## 系統要求 Requirements

- Python 3.6+
- pypdf 函式庫

## 授權條款 License

MIT License

## 貢獻 Contributing

歡迎提交Issue和Pull Request！

## 注意事項 Notes

- 此工具提取的是PDF中的文本內容，對於圖片型PDF（掃描檔）可能無法提取文字
- 複雜排版的PDF可能會影響文本提取的格式
- This tool extracts text content from PDFs. It may not work well with image-based PDFs (scanned documents)
- Complex PDF layouts may affect the formatting of extracted text
