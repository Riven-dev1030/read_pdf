# PDF Reader - PDF閱讀器

一個簡單易用的Python PDF閱讀工具，提供命令列和圖形介面兩種使用方式。

A simple and easy-to-use Python PDF reading tool that can extract and display text content from PDF files, with both CLI and GUI versions.

## 版本說明 Versions

- 📟 **命令列版本** (`pdf_reader.py`) - 適合批次處理和腳本調用
- 🖥️ **圖形介面版本** (`pdf_reader_gui.py`) - 提供可視化操作介面

## 功能特性 Features

### 命令列版本 CLI Version
- 📖 讀取整個PDF檔案或指定頁面
- 📊 顯示PDF基本資訊（總頁數）
- 📋 提取PDF元數據（作者、標題等）
- 🔍 **搜尋功能**：在PDF中查找關鍵詞並顯示位置
- 📁 **批量搜尋**：搜尋資料夾中的所有PDF檔案
- 📍 顯示搜尋結果的上下文內容
- 🔤 支援大小寫敏感/不敏感搜尋
- 💻 支援命令列參數
- 🌏 中文友好

### 圖形介面版本 GUI Version
- 🖱️ **可視化操作**：點擊按鈕打開檔案、搜尋內容
- 📁 **批量搜尋模式**：打開資料夾，搜尋所有PDF檔案
- 📑 **左右分欄佈局**：左側搜尋控制，右側內容顯示
- 🔍 **即時搜尋**：輸入關鍵詞即可搜尋整個PDF或多個檔案
- 📍 **搜尋結果列表**：顯示檔案名、頁碼、行號和內容預覽
- 🎯 **快速跳轉**：雙擊搜尋結果直接跳轉到對應位置
- 💡 **黃色高亮**：自動高亮所有匹配的關鍵詞
- 📊 **統計資訊**：顯示匹配數量和所在頁面/檔案
- ⚙️ **搜尋選項**：支援區分/不區分大小寫

## 安裝 Installation

### 1. 複製倉庫或下載檔案

### 2. 安裝 Python 依賴

```bash
pip install -r requirements.txt
```

### 3. 安裝系統依賴（僅圖形介面版本需要）

圖形介面版本需要 tkinter 和中文字體支援。

#### Ubuntu/Debian 系統：

**快速安裝（推薦）：**
```bash
./install_dependencies.sh
```

**或手動安裝：**
```bash
# 安裝 Tkinter
sudo apt-get update
sudo apt-get install python3-tk

# 安裝中文字體
sudo apt-get install fonts-noto-cjk fonts-wqy-microhei
```

#### Fedora 系統：
```bash
# 安裝 Tkinter
sudo dnf install python3-tkinter

# 安裝中文字體
sudo dnf install google-noto-sans-cjk-fonts
```

#### Arch Linux 系統：
```bash
# 安裝 Tkinter
sudo pacman -S tk

# 安裝中文字體
sudo pacman -S noto-fonts-cjk
```

#### macOS 系統：
```bash
# macOS 通常已內建 tkinter 和中文字體
# 如果缺少中文字體，可以從系統設定安裝
```

#### Windows 系統：
```
# Windows 通常已內建 tkinter 和中文字體
# 無需額外安裝
```

> **重要提示**：如果 GUI 介面中文顯示為方框（■），說明系統缺少中文字體。請按照上述說明安裝中文字體後重新啟動程序。

## 使用方法 Usage

### 圖形介面版本 GUI Version

#### 啟動 GUI
```bash
python pdf_reader_gui.py
```

#### 使用步驟

##### 單檔案模式
1. **打開檔案**：點擊「打開 PDF 檔案」按鈕，選擇要閱讀的 PDF
2. **瀏覽內容**：右側視窗會自動顯示所有頁面的文本內容
3. **搜尋關鍵詞**：
   - 在左側搜尋框輸入關鍵詞
   - 可選：勾選「區分大小寫」
   - 點擊「開始搜尋」或按回車鍵
4. **查看結果**：
   - 左側列表顯示所有匹配項（檔案名、頁碼、行號、內容預覽）
   - 右側文本區域會用黃色高亮所有匹配
5. **快速跳轉**：雙擊搜尋結果列表中的任意項，右側內容會自動捲動到對應位置

##### 批量搜尋模式
1. **打開資料夾**：點擊「打開資料夾」按鈕，選擇包含 PDF 檔案的資料夾
2. **查看檔案列表**：右側顯示找到的所有 PDF 檔案
3. **搜尋關鍵詞**：
   - 在左側搜尋框輸入關鍵詞
   - 可選：勾選「區分大小寫」
   - 點擊「開始搜尋」按鈕
4. **查看結果**：
   - 左側列表顯示所有檔案中的匹配項（檔案名、頁碼、行號、內容預覽）
   - 右側顯示搜尋統計資訊
5. **結果排序**：結果按檔案名和頁碼自動排序，方便查看

#### GUI 介面佈局
```
┌─────────────────────────────────────────────────────────┐
│  PDF 閱讀器                                        - □ ×│
├──────────────┬──────────────────────────────────────────┤
│ 檔案操作      │  PDF 內容                                │
│ [打開PDF]    │  ═══════════════════════════════════════│
│ 檔案: xx.pdf │  第 1 頁                                 │
│ 總頁數: 10   │  ═══════════════════════════════════════│
│              │  這是PDF的文本內容...                     │
│ 搜尋功能      │  關鍵詞會被【高亮】顯示                   │
│ 搜尋內容:     │                                          │
│ [         ]  │  ═══════════════════════════════════════│
│ ☐ 區分大小寫  │  第 2 頁                                 │
│ [開始搜尋]    │  ═══════════════════════════════════════│
│              │  繼續顯示內容...                          │
│ 搜尋結果: 5  │                                          │
│              │                                          │
│ 搜尋結果列表: │                                          │
│ ┌──────────┐│                                          │
│ │頁 行 內容 ││                                          │
│ │1  3  ... ││                                          │
│ │1  15 ... ││                                          │
│ │5  7  ... ││                                          │
│ └──────────┘│                                          │
└──────────────┴──────────────────────────────────────────┘
```

---

### 命令列版本 CLI Version

#### 基本用法

##### 閱讀PDF
```bash
# 讀取整個PDF檔案
python pdf_reader.py document.pdf

# 讀取指定頁（例如第1頁）
python pdf_reader.py document.pdf -p 1

# 顯示PDF元數據
python pdf_reader.py document.pdf -m

# 讀取第3頁並顯示元數據
python pdf_reader.py document.pdf -p 3 -m
```

##### 搜尋PDF內容（單檔案）
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

##### 批量搜尋（搜尋資料夾）
```bash
# 搜尋資料夾中所有PDF檔案
python pdf_reader.py -d ./documents -s "關鍵詞"

# 搜尋子資料夾中的所有PDF（遞迴搜尋）
python pdf_reader.py -d ./projects -s "API"

# 批量搜尋時區分大小寫
python pdf_reader.py -d ./pdfs -s "Python" -c

# 自訂上下文字元數
python pdf_reader.py -d ./docs -s "搜尋內容" --context 100
```

### 命令列參數

#### 基本參數
- `pdf_file`: PDF檔案路徑（單檔案模式，可選）
- `-d, --directory DIR`: 批量搜尋：指定包含PDF檔案的資料夾路徑
- `-h, --help`: 顯示幫助資訊

#### 閱讀模式（僅單檔案模式）
- `-p, --page NUM`: 指定要讀取的頁碼（從1開始）
- `-m, --metadata`: 顯示PDF元數據資訊

#### 搜尋模式（單檔案和批量模式）
- `-s, --search TEXT`: 在PDF中搜尋指定文本內容
- `-c, --case-sensitive`: 搜尋時區分大小寫（預設不區分）
- `--context CHARS`: 搜尋結果顯示的上下文字元數（預設50）

**注意**：
- 單檔案模式和批量模式不能同時使用
- 批量搜尋模式（`-d`）必須配合 `-s` 參數使用
- 批量搜尋會遞迴搜尋指定資料夾及其子資料夾中的所有 PDF 檔案

### 範例

#### 單檔案操作
```bash
# 讀取報告PDF的第5頁
python pdf_reader.py report.pdf --page 5

# 查看PDF的元數據資訊
python pdf_reader.py book.pdf --metadata

# 在技術文檔中搜尋"API"關鍵詞
python pdf_reader.py technical_doc.pdf -s "API"

# 在合同中區分大小寫搜尋"Section 3.1"
python pdf_reader.py contract.pdf -s "Section 3.1" -c
```

#### 批量搜尋操作
```bash
# 在所有學術論文中搜尋"機器學習"
python pdf_reader.py -d ./papers -s "機器學習"

# 在專案文檔資料夾中搜尋"TODO"（區分大小寫）
python pdf_reader.py -d ./project_docs -s "TODO" -c

# 在多層級資料夾中搜尋，顯示更多上下文
python pdf_reader.py -d ./archive -s "重要" --context 100
```

### 搜尋功能說明

#### 單檔案搜尋
搜尋功能會：
- 🔍 掃描PDF的所有頁面
- 📄 顯示包含關鍵詞的所有頁碼
- 📍 **精確顯示每個匹配在第幾頁第幾行**
- 📊 統計每頁找到的匹配次數
- 📝 顯示每個匹配項的上下文內容（用【】標記）
- ✅ 支援中英文搜尋

#### 批量搜尋
批量搜尋功能會：
- 📁 遞迴掃描指定資料夾及其子資料夾中的所有 PDF 檔案
- 🔍 在每個 PDF 檔案中搜尋關鍵詞
- 📄 顯示每個檔案中的匹配次數和頁碼
- 📍 精確顯示每個匹配在哪個檔案、第幾頁、第幾行
- 📊 提供總體統計資訊（搜尋檔案數、匹配檔案數、總匹配次數）
- 📝 顯示每個匹配項的上下文內容（用【】標記）
- ⚡ 自動跳過無法讀取的檔案並繼續處理

#### 單檔案搜尋結果範例：
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

#### 批量搜尋結果範例：
```
======================================================================
批量搜尋模式
資料夾: /home/user/documents
搜尋內容: 'Python'
區分大小寫: 否
找到 3 個PDF檔案
======================================================================

📄 檔案: tutorial.pdf
   路徑: tutorials/tutorial.pdf
----------------------------------------------------------------------
   ✓ 第 1 頁, 第 5 行: ...Introduction to【Python】programming...
   ✓ 第 2 頁, 第 12 行: ...【Python】is a high-level language...
   📊 小計: 2 處匹配，分布在第 1, 2 頁

📄 檔案: guide.pdf
   路徑: guides/guide.pdf
----------------------------------------------------------------------
   ✓ 第 3 頁, 第 8 行: ...Learning【Python】basics...
   📊 小計: 1 處匹配，分布在第 3 頁

======================================================================
搜尋完成！
======================================================================
📊 總體統計:
   - 搜尋檔案總數: 3
   - 包含匹配的檔案: 2
   - 總匹配次數: 3

📋 詳細結果:
   1. tutorial.pdf: 2 處匹配
   2. guide.pdf: 1 處匹配
======================================================================
```

## 系統要求 Requirements

### 命令列版本 CLI Version
- Python 3.6+
- pypdf 函式庫

### 圖形介面版本 GUI Version
- Python 3.6+
- pypdf 函式庫
- tkinter（Python 內建，通常無需單獨安裝）

> **注意**：在某些 Linux 系統上，可能需要安裝 tkinter：
> - Ubuntu/Debian: `sudo apt-get install python3-tk`
> - Fedora: `sudo dnf install python3-tkinter`
> - Arch Linux: `sudo pacman -S tk`

## 許可證 License

MIT License

## 貢獻 Contributing

歡迎提交Issue和Pull Request！

## 注意事項 Notes

- 此工具提取的是PDF中的文本內容，對於圖片型PDF（掃描件）可能無法提取文字
- 複雜排版的PDF可能會影響文本提取的格式
- This tool extracts text content from PDFs. It may not work well with image-based PDFs (scanned documents)
- Complex PDF layouts may affect the formatting of extracted text

---

## 開發歷史 Development History

### 2025-11-16: 合併 GUI 功能分支
**合併分支**: `claude/merge-feature-branches-01Chx3cpQ5JXSEtR9LbsxVJP`

**合併來源**:
1. `claude/gui-new-branch-01K1mT1Ji6LsdptPLuY4SuWZ`
2. `claude/double-click-string-location-01TpmCLx87NqjZzi8xyH7DNd`

**合併原因**:
- 將兩個獨立開發的 GUI 功能整合到一起
- 第一個分支提供了基礎的 GUI 介面和批量搜尋功能
- 第二個分支改進了使用者體驗，修復了雙擊跳轉功能和提示文字

**主要變更**:
1. **GUI 基礎功能** (來自 gui-new-branch):
   - ✅ 添加了完整的 Tkinter GUI 介面 (`pdf_reader_gui.py`)
   - ✅ 實現批量搜尋功能：可打開資料夾搜尋多個 PDF 檔案
   - ✅ 添加 `.gitignore` 檔案排除 Python 快取檔案
   - ✅ 左右分欄佈局：搜尋控制面板 + 內容顯示區域
   - ✅ 搜尋結果以樹狀列表顯示（檔案名、頁碼、行號、內容預覽）

2. **使用者體驗改進** (來自 double-click-string-location):
   - ✅ 修復了雙擊搜尋結果的跳轉功能
   - ✅ 改進了提示文字："雙擊結果可跳轉！"
   - ✅ 優化了變數初始化（`target_line` 使用整數而非浮點數）
   - ✅ 批量搜尋模式下也有清晰的雙擊提示

**解決的衝突**:
- 檔案: `pdf_reader_gui.py`
- 衝突位置: 搜尋結果提示文字、批量搜尋提示文字、target_line 變數初始化
- 解決方案: 保留了更詳細、使用者友好的提示資訊，確保使用者知道可以雙擊跳轉

**技術細節**:
- 搜尋結果統計提示: `"搜尋結果: {N} 處匹配，共 {M} 頁。雙擊結果可跳轉！"`
- 批量搜尋提示: `"請在左側查看詳細結果，雙擊可查看具體位置。"`
- 跳轉功能使用整數行號計算，避免浮點數精度問題

**為什麼要合併**:
這兩個分支都是對 GUI 功能的增強，分開維護會導致功能碎片化。合併後：
- 使用者可以同時使用批量搜尋和精確跳轉功能
- 介面提示更加清晰，使用者體驗更好
- 程式碼庫更整潔，便於後續維護和功能擴展
