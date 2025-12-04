# Software Design Document (SDD)
# PDF Reader Application

**文檔版本**: 1.0
**最後更新**: 2025-12-04
**專案名稱**: PDF Reader
**作者**: Claude & Development Team

---

## 目錄

1. [文檔資訊](#1-文檔資訊)
2. [系統概述](#2-系統概述)
3. [系統架構](#3-系統架構)
4. [模組設計](#4-模組設計)
5. [資料結構](#5-資料結構)
6. [介面設計](#6-介面設計)
7. [使用者介面設計](#7-使用者介面設計)
8. [錯誤處理](#8-錯誤處理)
9. [效能考量](#9-效能考量)
10. [安全性考量](#10-安全性考量)
11. [測試策略](#11-測試策略)
12. [部署考量](#12-部署考量)

---

## 1. 文檔資訊

### 1.1 文檔目的

本軟體設計文件 (SDD) 描述 PDF Reader 應用程式的詳細設計，包括系統架構、模組設計、資料結構和介面設計。本文件旨在為開發人員提供實作指南，並為維護人員提供系統理解的基礎。

### 1.2 適用範圍

本文件適用於：
- 開發人員：了解系統設計並進行實作
- 測試人員：制定測試計畫和測試案例
- 維護人員：理解系統架構以進行維護和升級
- 專案管理人員：評估技術風險和資源需求

### 1.3 參考文件

- `README.md` - 使用者手冊和功能說明
- `requirements.txt` - 專案依賴清單
- `pdf_reader.py` - CLI 版本原始碼
- `pdf_reader_gui.py` - GUI 版本原始碼

### 1.4 術語與縮寫

| 術語 | 說明 |
|------|------|
| PDF | Portable Document Format，可攜式文件格式 |
| CLI | Command Line Interface，命令列介面 |
| GUI | Graphical User Interface，圖形使用者介面 |
| SDD | Software Design Document，軟體設計文件 |
| API | Application Programming Interface，應用程式介面 |

---

## 2. 系統概述

### 2.1 系統目標

PDF Reader 是一個輕量級的 PDF 文件閱讀和搜尋工具，提供以下核心功能：

1. **文件閱讀**：提取並顯示 PDF 文件的文字內容
2. **內容搜尋**：在 PDF 中快速定位關鍵字
3. **批次處理**：支援在多個 PDF 檔案中進行批次搜尋
4. **雙介面支援**：提供 CLI 和 GUI 兩種操作模式

### 2.2 設計原則

1. **簡潔性**：保持程式碼簡潔易懂，避免過度工程化
2. **模組化**：功能分離，便於維護和擴展
3. **使用者友善**：提供清晰的錯誤訊息和操作提示
4. **效能優先**：針對大型 PDF 和批次操作進行優化
5. **跨平台**：支援 Windows、macOS 和 Linux

### 2.3 技術棧

| 元件 | 技術 | 版本 |
|------|------|------|
| 程式語言 | Python | 3.6+ |
| PDF 處理 | pypdf | 4.0.0+ |
| GUI 框架 | tkinter | 內建 |
| 命令列解析 | argparse | 內建 |
| 檔案處理 | pathlib | 內建 |
| 正則表達式 | re | 內建 |

---

## 3. 系統架構

### 3.1 整體架構

系統採用**分層架構**設計，包含以下層次：

```
┌─────────────────────────────────────────┐
│      使用者介面層 (UI Layer)             │
│  ┌─────────────┐      ┌──────────────┐ │
│  │  CLI 介面   │      │  GUI 介面    │ │
│  └─────────────┘      └──────────────┘ │
└─────────────────────────────────────────┘
              ↓                ↓
┌─────────────────────────────────────────┐
│      業務邏輯層 (Business Logic Layer)   │
│  ┌─────────────────────────────────────┐│
│  │  • 檔案讀取                          ││
│  │  • 內容搜尋                          ││
│  │  • 批次處理                          ││
│  │  • 結果格式化                        ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
              ↓                ↓
┌─────────────────────────────────────────┐
│      資料存取層 (Data Access Layer)      │
│  ┌─────────────────────────────────────┐│
│  │  • pypdf 函式庫                      ││
│  │  • 檔案系統存取                      ││
│  │  • 文字提取                          ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

### 3.2 元件關係圖

```
┌──────────────┐
│   main()     │
└──────┬───────┘
       │
       ├─────────────┬──────────────┐
       ↓             ↓              ↓
┌─────────────┐ ┌─────────────┐ ┌──────────────────┐
│  read_pdf() │ │search_pdf() │ │search_pdf_       │
│             │ │             │ │directory()       │
└─────────────┘ └─────────────┘ └──────────────────┘
       │             │              │
       └─────────────┴──────────────┘
                     ↓
              ┌─────────────┐
              │  PdfReader  │
              │  (pypdf)    │
              └─────────────┘
```

### 3.3 模組組織

```
read_pdf/
├── pdf_reader.py          # CLI 版本主程式
├── pdf_reader_gui.py      # GUI 版本主程式
├── requirements.txt       # 依賴清單
├── README.md             # 使用者手冊
├── SDD.md                # 本文件
└── .gitignore            # Git 忽略檔案
```

---

## 4. 模組設計

### 4.1 CLI 模組 (`pdf_reader.py`)

#### 4.1.1 模組概述

提供命令列介面的 PDF 閱讀和搜尋功能。

#### 4.1.2 主要函式

##### `read_pdf(pdf_path, page_num=None, show_metadata=False)`

**功能描述**：讀取並顯示 PDF 內容

**輸入參數**：
- `pdf_path` (str): PDF 檔案路徑
- `page_num` (int, optional): 指定頁碼（1-based）
- `show_metadata` (bool): 是否顯示元資料

**輸出**：
- `bool`: 操作成功返回 True，失敗返回 False

**處理流程**：
1. 驗證檔案路徑
2. 開啟 PDF 檔案
3. 顯示基本資訊（檔名、總頁數）
4. 如需要，顯示元資料
5. 提取並顯示文字內容（單頁或全部）

**錯誤處理**：
- 檔案不存在：顯示錯誤訊息並返回 False
- 檔案格式錯誤：顯示警告並嘗試處理
- 頁碼超出範圍：顯示錯誤訊息並返回 False
- 其他例外：捕獲並顯示錯誤訊息

##### `search_pdf(pdf_path, search_term, case_sensitive=False, context_chars=50)`

**功能描述**：在單個 PDF 檔案中搜尋關鍵字

**輸入參數**：
- `pdf_path` (str): PDF 檔案路徑
- `search_term` (str): 搜尋關鍵字
- `case_sensitive` (bool): 是否區分大小寫
- `context_chars` (int): 上下文字元數

**輸出**：
- `bool`: 找到匹配返回 True，否則返回 False

**處理流程**：
1. 驗證檔案路徑
2. 開啟 PDF 檔案
3. 逐頁提取文字
4. 逐行搜尋關鍵字
5. 記錄匹配位置和上下文
6. 格式化並顯示結果
7. 顯示統計摘要

**搜尋演算法**：
```python
for page in pdf:
    for line in page:
        matches = regex.finditer(search_term, line)
        for match in matches:
            extract_context(match, context_chars)
            store_result(page_num, line_num, context)
```

##### `search_pdf_directory(dir_path, search_term, case_sensitive=False, context_chars=50)`

**功能描述**：在資料夾中的所有 PDF 檔案中批次搜尋

**輸入參數**：
- `dir_path` (str): 資料夾路徑
- `search_term` (str): 搜尋關鍵字
- `case_sensitive` (bool): 是否區分大小寫
- `context_chars` (int): 上下文字元數

**輸出**：
- `bool`: 找到匹配返回 True，否則返回 False

**處理流程**：
1. 驗證資料夾路徑
2. 遞迴搜尋所有 PDF 檔案
3. 對每個檔案執行 `search_pdf` 邏輯
4. 彙總所有檔案的結果
5. 顯示總體統計資訊

**效能優化**：
- 使用生成器避免一次載入所有檔案
- 錯誤檔案跳過繼續處理
- 顯示處理進度

##### `main()`

**功能描述**：程式入口點，處理命令列參數

**處理流程**：
1. 建立 `ArgumentParser` 物件
2. 定義所有命令列參數
3. 解析使用者輸入
4. 驗證參數有效性
5. 根據參數呼叫對應功能
6. 返回退出碼（0 成功，1 失敗）

**參數驗證規則**：
- 必須指定檔案或資料夾（二選一）
- 批次模式必須配合搜尋參數
- 頁碼必須為正整數

---

### 4.2 GUI 模組 (`pdf_reader_gui.py`)

#### 4.2.1 模組概述

提供基於 Tkinter 的圖形使用者介面，支援視覺化操作和即時回饋。

#### 4.2.2 主要類別

##### `PDFReaderGUI`

**類別說明**：主視窗類別，管理所有 GUI 元件和互動邏輯

**屬性**：

| 屬性名稱 | 型別 | 說明 |
|---------|------|------|
| `root` | `tk.Tk` | 主視窗物件 |
| `pdf_reader` | `PdfReader` | PDF 讀取器物件 |
| `pdf_path` | `Path` | 當前 PDF 檔案路徑 |
| `all_pages_text` | `List[str]` | 所有頁面文字 |
| `search_results` | `List[Dict]` | 搜尋結果列表 |
| `batch_mode` | `bool` | 是否為批次模式 |
| `pdf_directory` | `Path` | 批次模式資料夾路徑 |
| `pdf_files` | `List[Path]` | 批次模式檔案列表 |

**主要方法**：

##### `__init__(self, root)`

初始化 GUI 應用程式

```python
def __init__(self, root):
    self.root = root
    self.root.title("PDF 閱讀器")
    self.root.geometry("1200x700")
    # 初始化資料成員
    # 建立介面元件
```

##### `create_widgets(self)`

建立所有 GUI 元件

**介面佈局**：
- 使用 `PanedWindow` 實現可調整的左右分欄
- 左側：檔案操作、搜尋控制、結果列表
- 右側：PDF 內容顯示區域

**元件樹**：
```
root (Tk)
└── PanedWindow (HORIZONTAL)
    ├── left_frame
    │   ├── file_frame (LabelFrame)
    │   │   ├── button_frame
    │   │   │   ├── 開啟檔案按鈕
    │   │   │   └── 開啟資料夾按鈕
    │   │   ├── file_label
    │   │   └── info_label
    │   └── search_frame (LabelFrame)
    │       ├── search_entry
    │       ├── case_sensitive_var
    │       ├── 搜尋按鈕
    │       ├── result_count_label
    │       └── result_tree (Treeview)
    └── right_frame
        └── content_frame (LabelFrame)
            └── text_display (ScrolledText)
```

##### `open_file(self)`

開啟單個 PDF 檔案

**處理流程**：
1. 顯示檔案選擇對話框
2. 讀取 PDF 檔案
3. 提取所有頁面文字
4. 更新介面顯示
5. 切換到單檔案模式
6. 清空之前的搜尋結果

##### `open_directory(self)`

開啟資料夾（批次模式）

**處理流程**：
1. 顯示資料夾選擇對話框
2. 遞迴搜尋所有 PDF 檔案
3. 顯示檔案列表
4. 切換到批次模式
5. 清空之前的搜尋結果

##### `search_pdf(self)`

執行搜尋（單檔案或批次）

**處理流程**：
1. 獲取搜尋關鍵字
2. 驗證輸入有效性
3. 根據模式呼叫對應搜尋方法

##### `search_single_file(self)`

單檔案搜尋模式

**處理流程**：
1. 遍歷所有頁面文字
2. 使用正則表達式搜尋
3. 提取匹配上下文
4. 儲存結果到 `search_results`
5. 更新結果列表
6. 高亮顯示匹配項
7. 顯示統計資訊

##### `search_batch(self)`

批次搜尋模式

**處理流程**：
1. 顯示搜尋進度
2. 遍歷所有 PDF 檔案
3. 對每個檔案執行搜尋邏輯
4. 彙總結果
5. 顯示統計摘要

**效能優化**：
- 使用 `root.update()` 更新 UI
- 錯誤檔案跳過繼續處理

##### `display_search_results(self)`

顯示搜尋結果到 Treeview

**資料格式**：
```python
{
    'file': '檔案名稱',
    'page': 頁碼,
    'line': 行號,
    'preview': '...上下文【匹配】上下文...'
}
```

##### `highlight_all_matches(self, search_term, case_sensitive)`

高亮顯示所有匹配項

**處理流程**：
1. 移除之前的高亮標籤
2. 使用 `text_display.search()` 查找所有匹配
3. 為每個匹配添加 'highlight' 標籤

**標籤樣式**：
- `highlight`: 黃色背景，黑色文字
- `current_highlight`: 橙色背景，黑色文字

##### `on_result_click(self, event)`

處理搜尋結果點擊事件

**處理流程**：
1. 獲取選中的結果
2. 計算目標行位置
3. 使用 `text_display.see()` 捲動到目標

**行號計算**：
```python
target_line = 1
for i in range(page_num - 1):
    target_line += lines_in_page[i] + 4  # +4 為頁面分隔符
target_line += line_num + 3
```

##### `clear_search_results(self)`

清空搜尋結果

**處理流程**：
1. 清空 `search_results` 列表
2. 清空 Treeview
3. 重置統計標籤
4. 移除所有高亮標籤

---

## 5. 資料結構

### 5.1 搜尋結果資料結構

#### 5.1.1 單個匹配資料

```python
match_info = {
    'line_num': int,      # 行號（1-based）
    'before': str,        # 匹配前的上下文
    'matched': str,       # 匹配的文字
    'after': str          # 匹配後的上下文
}
```

#### 5.1.2 頁面匹配資料

```python
page_result = {
    'page_num': int,           # 頁碼（1-based）
    'matches': List[match_info]  # 該頁所有匹配
}
```

#### 5.1.3 檔案匹配資料（批次模式）

```python
file_result = {
    'file': str,              # 檔案名稱
    'file_path': Path,        # 檔案完整路徑
    'matches': int,           # 匹配總數
    'pages': List[int]        # 包含匹配的頁碼列表
}
```

#### 5.1.4 GUI 搜尋結果資料

```python
search_result = {
    'file': str,          # 檔案名稱
    'page': int,          # 頁碼
    'line': int,          # 行號
    'preview': str,       # 內容預覽
    'matched_text': str,  # 匹配文字
    'full_line': str,     # 完整行文字
    'file_path': Path     # 檔案路徑（批次模式）
}
```

### 5.2 狀態管理

#### 5.2.1 GUI 應用狀態

```python
class PDFReaderGUI:
    # 檔案狀態
    pdf_reader: Optional[PdfReader]
    pdf_path: Optional[Path]
    all_pages_text: List[str]

    # 搜尋狀態
    search_results: List[Dict]

    # 批次模式狀態
    batch_mode: bool
    pdf_directory: Optional[Path]
    pdf_files: List[Path]
```

---

## 6. 介面設計

### 6.1 函式介面

#### 6.1.1 CLI 函式介面

##### `read_pdf(pdf_path, page_num=None, show_metadata=False) -> bool`

| 參數 | 型別 | 必填 | 預設值 | 說明 |
|------|------|------|-------|------|
| pdf_path | str | 是 | - | PDF 檔案路徑 |
| page_num | int | 否 | None | 指定頁碼（1-based） |
| show_metadata | bool | 否 | False | 是否顯示元資料 |

**返回值**：成功返回 True，失敗返回 False

##### `search_pdf(pdf_path, search_term, case_sensitive=False, context_chars=50) -> bool`

| 參數 | 型別 | 必填 | 預設值 | 說明 |
|------|------|------|-------|------|
| pdf_path | str | 是 | - | PDF 檔案路徑 |
| search_term | str | 是 | - | 搜尋關鍵字 |
| case_sensitive | bool | 否 | False | 是否區分大小寫 |
| context_chars | int | 否 | 50 | 上下文字元數 |

**返回值**：找到匹配返回 True，否則返回 False

##### `search_pdf_directory(dir_path, search_term, case_sensitive=False, context_chars=50) -> bool`

| 參數 | 型別 | 必填 | 預設值 | 說明 |
|------|------|------|-------|------|
| dir_path | str | 是 | - | 資料夾路徑 |
| search_term | str | 是 | - | 搜尋關鍵字 |
| case_sensitive | bool | 否 | False | 是否區分大小寫 |
| context_chars | int | 否 | 50 | 上下文字元數 |

**返回值**：找到匹配返回 True，否則返回 False

### 6.2 命令列介面

#### 6.2.1 命令格式

```
pdf_reader.py [檔案路徑] [選項]
```

#### 6.2.2 參數說明

| 參數 | 簡寫 | 型別 | 說明 |
|------|------|------|------|
| pdf_file | - | str | PDF 檔案路徑（位置參數） |
| --directory | -d | str | 批次搜尋資料夾路徑 |
| --page | -p | int | 指定讀取頁碼 |
| --metadata | -m | flag | 顯示元資料 |
| --search | -s | str | 搜尋關鍵字 |
| --case-sensitive | -c | flag | 區分大小寫 |
| --context | - | int | 上下文字元數 |
| --help | -h | flag | 顯示幫助資訊 |

#### 6.2.3 使用範例

```bash
# 讀取整個 PDF
python pdf_reader.py document.pdf

# 讀取第 3 頁
python pdf_reader.py document.pdf -p 3

# 搜尋關鍵字
python pdf_reader.py document.pdf -s "Python"

# 批次搜尋
python pdf_reader.py -d ./docs -s "API"

# 區分大小寫搜尋
python pdf_reader.py document.pdf -s "API" -c

# 自訂上下文長度
python pdf_reader.py document.pdf -s "test" --context 100
```

### 6.3 外部依賴介面

#### 6.3.1 pypdf 函式庫

```python
from pypdf import PdfReader

# 開啟 PDF
reader = PdfReader(file_path)

# 獲取頁數
num_pages = len(reader.pages)

# 獲取頁面
page = reader.pages[index]

# 提取文字
text = page.extract_text()

# 獲取元資料
metadata = reader.metadata
```

---

## 7. 使用者介面設計

### 7.1 CLI 介面設計

#### 7.1.1 輸出格式

##### 標題格式

```
============================================================
PDF檔案: example.pdf
總頁數: 10
============================================================
```

##### 內容格式

```
第 1 頁:
------------------------------------------------------------
[頁面內容文字...]
------------------------------------------------------------
```

##### 搜尋結果格式

```
第 1 頁 - 找到 2 處匹配:
------------------------------------------------------------
  [1] 第 3 行: ...前文【匹配字】後文...
  [2] 第 15 行: ...前文【匹配字】後文...

============================================================
搜尋完成！
共在 2 頁中找到 3 處匹配
頁碼: 1, 5
============================================================
```

##### 批次搜尋結果格式

```
======================================================================
批次搜尋模式
資料夾: /path/to/directory
搜尋內容: 'keyword'
區分大小寫: 否
找到 5 個PDF檔案
======================================================================

📄 檔案: file1.pdf
   路徑: subdir/file1.pdf
----------------------------------------------------------------------
   ✓ 第 1 頁, 第 5 行: ...前文【keyword】後文...
   📊 小計: 2 處匹配，分布在第 1, 2 頁

======================================================================
搜尋完成！
======================================================================
📊 總體統計:
   - 搜尋檔案總數: 5
   - 包含匹配的檔案: 2
   - 總匹配次數: 10

📋 詳細結果:
   1. file1.pdf: 5 處匹配
   2. file2.pdf: 5 處匹配
======================================================================
```

#### 7.1.2 錯誤訊息格式

```
錯誤: 檔案不存在 'nonexistent.pdf'
錯誤: 頁碼超出範圍 (1-10)
錯誤: 不能同時指定檔案和資料夾
警告: 檔案可能不是PDF格式
⚠️  處理檔案 broken.pdf 時出錯: [錯誤詳情]
```

### 7.2 GUI 介面設計

#### 7.2.1 視窗佈局

```
┌─────────────────────────────────────────────────────────┐
│  PDF 閱讀器                                        - □ ×│
├──────────────┬──────────────────────────────────────────┤
│              │                                          │
│  檔案操作     │          PDF 內容                        │
│ ┌──────────┐│  ═══════════════════════════════════════│
│ │開啟檔案  ││  第 1 頁                                 │
│ │開啟資料夾││  ═══════════════════════════════════════│
│ └──────────┘│  [PDF 文字內容顯示]                      │
│              │  關鍵字會被【高亮】                       │
│  搜尋功能     │                                          │
│ ┌──────────┐│                                          │
│ │搜尋內容  ││  ═══════════════════════════════════════│
│ │          ││  第 2 頁                                 │
│ │☐區分大小寫││  ═══════════════════════════════════════│
│ │[開始搜尋]││  [更多內容...]                           │
│ └──────────┘│                                          │
│              │                                          │
│ 搜尋結果列表  │                                          │
│┌────────────┐│                                          │
││檔案|頁|行號││                                          │
││────────────││                                          │
││示例|1 |5   ││                                          │
││示例|2 |10  ││                                          │
││示例|5 |3   ││                                          │
│└────────────┘│                                          │
└──────────────┴──────────────────────────────────────────┘
```

#### 7.2.2 元件規格

##### 主視窗

- **尺寸**：1200x700 像素
- **標題**：PDF 閱讀器
- **可調整大小**：是
- **最小尺寸**：800x600

##### 左側面板（檔案操作區）

- **寬度**：400 像素（可調整）
- **背景色**：系統預設

**檔案操作區域**：
- 標題：檔案操作
- 內距：10 像素
- 包含元件：
  - 開啟 PDF 檔案按鈕
  - 開啟資料夾按鈕
  - 檔案資訊標籤

**搜尋功能區域**：
- 標題：搜尋功能
- 內距：10 像素
- 包含元件：
  - 搜尋輸入框
  - 區分大小寫複選框
  - 開始搜尋按鈕
  - 結果統計標籤
  - 結果列表（Treeview）

##### 右側面板（內容顯示區）

- **標題**：PDF 內容
- **內距**：5 像素
- **字型**：Microsoft YaHei, 10pt
- **自動換行**：是
- **可編輯**：否
- **滾動條**：垂直滾動條

##### 搜尋結果列表（Treeview）

| 欄位 | 寬度 | 對齊 | 說明 |
|------|------|------|------|
| 檔案 | 100px | 左 | 檔案名稱 |
| 頁碼 | 50px | 中 | 頁碼 |
| 行號 | 50px | 中 | 行號 |
| 內容預覽 | 200px | 左 | 匹配內容預覽 |

- **高度**：10 行
- **選擇模式**：單選
- **雙擊事件**：跳轉到對應位置

#### 7.2.3 色彩方案

| 元素 | 色彩 | 說明 |
|------|------|------|
| 主視窗背景 | 系統預設 | - |
| 文字 | #000000 | 黑色 |
| 檔案標籤（未開啟） | #808080 | 灰色 |
| 檔案標籤（已開啟） | #000000 | 黑色 |
| 資訊標籤 | #0000FF | 藍色 |
| 結果統計（成功） | #008000 | 綠色 |
| 結果統計（失敗） | #FF0000 | 紅色 |
| 匹配高亮 | #FFFF00 | 黃色背景 |
| 當前高亮 | #FFA500 | 橙色背景 |

#### 7.2.4 互動流程

##### 開啟檔案流程

```
使用者點擊「開啟 PDF 檔案」
    ↓
顯示檔案選擇對話框
    ↓
使用者選擇檔案
    ↓
讀取 PDF 並提取文字
    ↓
更新檔案資訊標籤
    ↓
在右側顯示 PDF 內容
    ↓
顯示成功訊息框
```

##### 搜尋流程

```
使用者輸入搜尋關鍵字
    ↓
使用者點擊「開始搜尋」或按 Enter
    ↓
驗證輸入
    ↓
執行搜尋（單檔案或批次）
    ↓
更新結果列表
    ↓
高亮顯示匹配項
    ↓
更新統計資訊
```

##### 結果跳轉流程

```
使用者雙擊搜尋結果
    ↓
獲取結果資料（頁碼、行號）
    ↓
計算目標行位置
    ↓
滾動到目標位置
    ↓
（可選）高亮當前匹配
```

#### 7.2.5 使用者提示

| 情境 | 訊息 | 類型 |
|------|------|------|
| 成功開啟檔案 | 已成功開啟 PDF 檔案\n總頁數: N | Info |
| 成功開啟資料夾 | 已開啟資料夾\n找到 N 個 PDF 檔案 | Info |
| 檔案讀取錯誤 | 開啟 PDF 檔案時出錯:\n[錯誤詳情] | Error |
| 資料夾讀取錯誤 | 開啟資料夾時出錯:\n[錯誤詳情] | Error |
| 未找到 PDF | 在資料夾中沒有找到 PDF 檔案 | Warning |
| 搜尋前未開啟 | 請先開啟 PDF 檔案 | Warning |
| 搜尋前未輸入 | 請輸入搜尋內容 | Warning |
| 搜尋無結果 | 未找到匹配內容 | Info |
| 搜尋成功 | 搜尋結果: N 處匹配，共 M 頁。雙擊結果可跳轉！ | Label |

---

## 8. 錯誤處理

### 8.1 錯誤分類

#### 8.1.1 使用者輸入錯誤

| 錯誤類型 | 檢測位置 | 處理方式 |
|---------|---------|---------|
| 檔案不存在 | `read_pdf()`, `search_pdf()` | 顯示錯誤訊息，返回 False |
| 資料夾不存在 | `search_pdf_directory()` | 顯示錯誤訊息，返回 False |
| 頁碼超出範圍 | `read_pdf()` | 顯示錯誤訊息，返回 False |
| 參數衝突 | `main()` | 顯示錯誤訊息，退出程式 |
| 搜尋關鍵字為空 | GUI `search_pdf()` | 顯示警告對話框 |

#### 8.1.2 檔案處理錯誤

| 錯誤類型 | 檢測位置 | 處理方式 |
|---------|---------|---------|
| PDF 格式錯誤 | 所有讀取函式 | 顯示警告，嘗試繼續 |
| PDF 無法開啟 | `PdfReader()` | 捕獲例外，顯示錯誤 |
| 權限不足 | 檔案操作 | 捕獲例外，顯示錯誤 |
| 檔案損壞 | 文字提取 | 捕獲例外，跳過該檔案 |

#### 8.1.3 系統錯誤

| 錯誤類型 | 檢測位置 | 處理方式 |
|---------|---------|---------|
| 記憶體不足 | 大檔案處理 | 捕獲例外，建議分頁處理 |
| 依賴函式庫缺失 | 匯入階段 | 顯示安裝指示，退出程式 |
| GUI 初始化失敗 | `PDFReaderGUI.__init__()` | 捕獲例外，顯示錯誤 |

### 8.2 錯誤處理策略

#### 8.2.1 CLI 錯誤處理

```python
def read_pdf(pdf_path, page_num=None, show_metadata=False):
    try:
        # 輸入驗證
        path = Path(pdf_path)
        if not path.exists():
            print(f"錯誤: 檔案不存在 '{pdf_path}'")
            return False

        # 核心邏輯
        reader = PdfReader(pdf_path)
        # ... 處理 ...

        return True

    except Exception as e:
        # 通用例外處理
        print(f"讀取PDF時出錯: {e}")
        return False
```

#### 8.2.2 GUI 錯誤處理

```python
def open_file(self):
    try:
        # 核心邏輯
        self.pdf_reader = PdfReader(file_path)
        # ... 處理 ...

        messagebox.showinfo("成功", "已成功開啟 PDF 檔案")

    except Exception as e:
        # 顯示使用者友善的錯誤訊息
        messagebox.showerror("錯誤", f"開啟 PDF 檔案時出錯:\n{str(e)}")
```

#### 8.2.3 批次處理錯誤處理

```python
for pdf_file in pdf_files:
    try:
        # 處理單個檔案
        reader = PdfReader(pdf_file)
        # ... 搜尋邏輯 ...

    except Exception as e:
        # 記錄錯誤但繼續處理其他檔案
        print(f"⚠️  處理檔案 {pdf_file.name} 時出錯: {e}")
        continue
```

### 8.3 錯誤訊息設計

#### 8.3.1 錯誤訊息格式

**CLI 錯誤訊息**：
```
錯誤: [簡短描述]
```

**CLI 警告訊息**：
```
警告: [簡短描述]
```

**GUI 錯誤對話框**：
- 標題：錯誤
- 內容：[操作名稱]時出錯:\n[錯誤詳情]
- 按鈕：確定

**GUI 警告對話框**：
- 標題：警告
- 內容：[警告訊息]
- 按鈕：確定

#### 8.3.2 錯誤訊息清單

| 錯誤代碼 | 訊息 | 說明 |
|---------|------|------|
| E001 | 檔案不存在 '{path}' | 指定的檔案不存在 |
| E002 | 資料夾不存在 '{path}' | 指定的資料夾不存在 |
| E003 | '{path}' 不是一個資料夾 | 路徑不是資料夾 |
| E004 | 頁碼超出範圍 (1-{max}) | 頁碼無效 |
| E005 | 不能同時指定檔案和資料夾 | 參數衝突 |
| E006 | 必須指定PDF檔案或資料夾 | 缺少必要參數 |
| E007 | 批次搜尋模式必須使用 -s/--search 參數 | 缺少搜尋參數 |
| W001 | 檔案可能不是PDF格式 '{path}' | 檔案副檔名不是 .pdf |
| W002 | 在資料夾中沒有找到 PDF 檔案 | 資料夾內無 PDF 檔案 |
| W003 | 處理檔案 {file} 時出錯: {error} | 單個檔案處理失敗 |

### 8.4 日誌記錄

#### 8.4.1 日誌等級

| 等級 | 用途 | 範例 |
|------|------|------|
| ERROR | 嚴重錯誤 | 無法開啟檔案、依賴缺失 |
| WARNING | 警告訊息 | 檔案格式可疑、權限問題 |
| INFO | 一般資訊 | 檔案載入成功、搜尋完成 |
| DEBUG | 偵錯資訊 | 函式呼叫、變數狀態 |

#### 8.4.2 日誌位置

- **CLI**：輸出到標準錯誤流 (stderr)
- **GUI**：輸出到標準輸出流 (stdout)，可擴展為檔案日誌

---

## 9. 效能考量

### 9.1 效能指標

| 指標 | 目標值 | 測試條件 |
|------|--------|---------|
| 單頁載入時間 | < 100ms | 普通 PDF，文字型 |
| 搜尋速度 | < 1s/頁 | 中等長度文字 |
| 批次搜尋速度 | < 2s/檔案 | 平均 10 頁/檔案 |
| 記憶體使用 | < 100MB | 開啟 50 頁 PDF |
| GUI 響應時間 | < 50ms | UI 操作到畫面更新 |

### 9.2 效能優化策略

#### 9.2.1 文字提取優化

**問題**：大型 PDF 載入慢

**解決方案**：
1. 按需載入：僅在需要時提取頁面文字
2. 快取機制：已提取的頁面文字存入快取
3. 分頁處理：一次處理固定數量的頁面

```python
# 優化前
all_pages_text = [page.extract_text() for page in reader.pages]

# 優化後
all_pages_text = []
for page in reader.pages:
    text = page.extract_text()
    all_pages_text.append(text)
    # 可以在這裡加入進度更新
```

#### 9.2.2 搜尋效能優化

**問題**：大量文字搜尋慢

**解決方案**：
1. 使用正則表達式的編譯版本
2. 並行處理：多執行緒搜尋不同頁面
3. 提前終止：達到匹配上限時停止

```python
# 優化前
for line in lines:
    matches = re.finditer(pattern, line, flags)

# 優化後
compiled_pattern = re.compile(pattern, flags)
for line in lines:
    matches = compiled_pattern.finditer(line)
```

#### 9.2.3 批次處理優化

**問題**：批次處理大量檔案時記憶體佔用過高

**解決方案**：
1. 串流處理：逐個處理檔案，不保留所有結果
2. 結果限制：設定最大結果數量
3. 錯誤隔離：單個檔案失敗不影響其他檔案

```python
# 優化策略
for pdf_file in pdf_files:
    try:
        reader = PdfReader(pdf_file)
        # 處理完立即釋放
        del reader
    except Exception as e:
        # 記錄錯誤繼續處理
        continue
```

#### 9.2.4 GUI 效能優化

**問題**：大量結果更新 UI 卡頓

**解決方案**：
1. 批次更新：累積多個結果後一次更新
2. 虛擬捲動：Treeview 使用虛擬模式
3. 背景執行緒：將搜尋移到背景執行緒

```python
# 批次更新 UI
batch = []
for result in results:
    batch.append(result)
    if len(batch) >= 100:
        self.update_ui(batch)
        batch = []
        self.root.update()  # 更新 UI
```

### 9.3 記憶體管理

#### 9.3.1 記憶體使用估算

| 元件 | 記憶體佔用 | 說明 |
|------|-----------|------|
| 基礎程式 | ~10MB | Python 直譯器和函式庫 |
| PDF 讀取器 | ~5MB/檔案 | pypdf 函式庫開銷 |
| 文字快取 | ~1MB/10頁 | 儲存提取的文字 |
| 搜尋結果 | ~1KB/結果 | 結果資料結構 |
| GUI 框架 | ~20MB | Tkinter 開銷 |

#### 9.3.2 記憶體優化策略

1. **及時釋放**：處理完畢立即釋放 PDF 物件
2. **限制快取**：設定最大快取頁面數
3. **結果分頁**：搜尋結果分頁顯示
4. **垃圾回收**：定期呼叫 `gc.collect()`

### 9.4 效能監控

#### 9.4.1 監控指標

```python
import time

start_time = time.time()
# 執行操作
elapsed_time = time.time() - start_time
print(f"操作耗時: {elapsed_time:.2f} 秒")
```

#### 9.4.2 效能分析工具

- **cProfile**：Python 內建效能分析器
- **memory_profiler**：記憶體使用分析
- **line_profiler**：逐行效能分析

---

## 10. 安全性考量

### 10.1 安全威脅分析

#### 10.1.1 潛在威脅

| 威脅類型 | 風險等級 | 說明 |
|---------|---------|------|
| 惡意 PDF | 高 | 包含惡意腳本的 PDF 檔案 |
| 路徑遍歷 | 中 | 使用者輸入包含 `../` 等路徑 |
| 拒絕服務 | 中 | 巨型 PDF 導致記憶體耗盡 |
| 資料洩漏 | 低 | 敏感資訊意外顯示 |
| 依賴漏洞 | 中 | pypdf 函式庫存在漏洞 |

#### 10.1.2 威脅模型

```
使用者 → 輸入檔案路徑 → 程式讀取 PDF → 顯示內容
              ↓                  ↓
        路徑驗證           安全解析
              ↓                  ↓
        防止遍歷       防止惡意腳本執行
```

### 10.2 安全措施

#### 10.2.1 輸入驗證

**檔案路徑驗證**：
```python
def validate_pdf_path(pdf_path):
    # 使用 pathlib 標準化路徑
    path = Path(pdf_path).resolve()

    # 檢查路徑是否在允許的目錄內
    # 防止路徑遍歷攻擊

    # 檢查檔案副檔名
    if path.suffix.lower() != '.pdf':
        warn("檔案可能不是PDF格式")

    # 檢查檔案存在性
    if not path.exists():
        raise FileNotFoundError()

    return path
```

**搜尋關鍵字驗證**：
```python
def validate_search_term(search_term):
    # 限制長度
    if len(search_term) > 1000:
        raise ValueError("搜尋關鍵字過長")

    # 使用 re.escape() 防止正則注入
    escaped_term = re.escape(search_term)

    return escaped_term
```

#### 10.2.2 資源限制

**檔案大小限制**：
```python
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

def check_file_size(file_path):
    size = Path(file_path).stat().st_size
    if size > MAX_FILE_SIZE:
        raise ValueError(f"檔案過大: {size / 1024 / 1024:.2f} MB")
```

**處理超時**：
```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("處理超時")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(60)  # 60 秒超時
```

#### 10.2.3 錯誤處理安全

**避免洩漏敏感資訊**：
```python
try:
    reader = PdfReader(file_path)
except Exception as e:
    # 不要直接顯示完整例外訊息
    print("讀取PDF時出錯")
    # 記錄詳細錯誤到日誌
    logging.error(f"PDF讀取失敗: {file_path}, {e}")
```

#### 10.2.4 依賴安全

**定期更新依賴**：
```bash
pip install --upgrade pypdf
pip list --outdated
```

**使用安全版本**：
```
# requirements.txt
pypdf>=4.0.0,<5.0.0
```

### 10.3 安全最佳實踐

#### 10.3.1 開發階段

1. **程式碼審查**：所有程式碼變更需經審查
2. **靜態分析**：使用 `bandit` 掃描安全問題
3. **依賴檢查**：使用 `safety` 檢查已知漏洞

#### 10.3.2 部署階段

1. **最小權限**：程式以最小權限執行
2. **沙盒執行**：考慮使用容器隔離
3. **監控告警**：監控異常行為

#### 10.3.3 使用階段

1. **使用者教育**：提醒使用者不要開啟不信任的 PDF
2. **更新通知**：提示使用者更新到最新版本
3. **錯誤回報**：提供安全的錯誤回報機制

---

## 11. 測試策略

### 11.1 測試等級

#### 11.1.1 單元測試

**測試範圍**：個別函式和方法

**測試框架**：pytest

**測試覆蓋率目標**：> 80%

**測試案例範例**：

```python
import pytest
from pdf_reader import read_pdf, search_pdf

def test_read_pdf_valid_file():
    """測試讀取有效的 PDF 檔案"""
    result = read_pdf("test_data/sample.pdf")
    assert result == True

def test_read_pdf_nonexistent_file():
    """測試讀取不存在的檔案"""
    result = read_pdf("nonexistent.pdf")
    assert result == False

def test_search_pdf_with_matches():
    """測試搜尋有匹配的情況"""
    result = search_pdf("test_data/sample.pdf", "test")
    assert result == True

def test_search_pdf_case_sensitive():
    """測試區分大小寫搜尋"""
    result = search_pdf("test_data/sample.pdf", "TEST", case_sensitive=True)
    # 根據測試資料驗證結果
```

#### 11.1.2 整合測試

**測試範圍**：多個模組協同工作

**測試案例**：

| 測試案例 | 說明 | 預期結果 |
|---------|------|---------|
| TC-INT-001 | CLI 讀取 PDF 並搜尋 | 正確顯示搜尋結果 |
| TC-INT-002 | GUI 開啟檔案並搜尋 | UI 正確更新結果 |
| TC-INT-003 | 批次搜尋多個檔案 | 所有檔案都被處理 |
| TC-INT-004 | 搜尋結果跳轉 | 正確捲動到目標位置 |

#### 11.1.3 系統測試

**測試範圍**：完整系統端到端測試

**測試案例**：

| 測試案例 | 說明 | 預期結果 |
|---------|------|---------|
| TC-SYS-001 | 啟動程式到退出 | 正常啟動和退出 |
| TC-SYS-002 | 完整工作流程 | 使用者任務完成 |
| TC-SYS-003 | 錯誤恢復 | 錯誤後程式繼續運行 |
| TC-SYS-004 | 效能測試 | 符合效能指標 |

#### 11.1.4 驗收測試

**測試範圍**：使用者接受度測試

**測試標準**：
- 功能完整性：所有需求功能實現
- 易用性：非技術使用者能獨立使用
- 效能：符合預期效能指標
- 穩定性：無重大缺陷

### 11.2 測試資料

#### 11.2.1 測試 PDF 檔案

| 檔案名稱 | 特徵 | 用途 |
|---------|------|------|
| sample.pdf | 10 頁，普通文字 | 基本功能測試 |
| large.pdf | 100 頁，大檔案 | 效能測試 |
| chinese.pdf | 中文內容 | 國際化測試 |
| complex.pdf | 複雜排版 | 邊界案例測試 |
| empty.pdf | 空白頁面 | 邊界案例測試 |
| corrupt.pdf | 損壞的檔案 | 錯誤處理測試 |

#### 11.2.2 測試搜尋關鍵字

| 關鍵字 | 特徵 | 用途 |
|--------|------|------|
| test | 普通英文 | 基本搜尋 |
| Test | 大小寫 | 大小寫測試 |
| 測試 | 中文 | 中文搜尋 |
| test123 | 數字混合 | 特殊字元 |
| `.*test` | 正則字元 | 轉義測試 |

### 11.3 測試環境

#### 11.3.1 開發環境

- **作業系統**：開發者本機
- **Python 版本**：3.6, 3.8, 3.10
- **依賴**：requirements.txt

#### 11.3.2 CI/CD 環境

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.6, 3.8, 3.10]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: pytest tests/
```

### 11.4 測試自動化

#### 11.4.1 自動化測試腳本

```bash
#!/bin/bash
# run_tests.sh

# 執行單元測試
pytest tests/unit/ -v --cov=pdf_reader

# 執行整合測試
pytest tests/integration/ -v

# 產生覆蓋率報告
coverage html

# 執行靜態分析
pylint pdf_reader.py
bandit -r .

# 執行效能測試
python tests/performance_test.py
```

#### 11.4.2 測試報告

**測試結果報告**：
- 測試通過率
- 覆蓋率報告
- 失敗案例詳情
- 效能指標

### 11.5 缺陷管理

#### 11.5.1 缺陷等級

| 等級 | 說明 | 範例 | 處理時限 |
|------|------|------|---------|
| P0 - 緊急 | 阻塞使用 | 程式無法啟動 | 24 小時 |
| P1 - 高 | 核心功能失效 | 搜尋無結果 | 3 天 |
| P2 - 中 | 次要功能問題 | UI 顯示異常 | 1 週 |
| P3 - 低 | 優化建議 | 效能改進 | 下版本 |

#### 11.5.2 缺陷追蹤流程

```
發現缺陷 → 記錄 Bug → 分配等級 → 指派開發者
    ↓
修復缺陷 → 程式碼審查 → 合併程式碼 → 驗證修復
    ↓
關閉 Bug → 更新文件
```

---

## 12. 部署考量

### 12.1 系統需求

#### 12.1.1 硬體需求

| 元件 | 最低需求 | 建議需求 |
|------|---------|---------|
| 處理器 | 1 GHz | 2 GHz+ |
| 記憶體 | 512 MB | 2 GB |
| 硬碟空間 | 50 MB | 200 MB |
| 顯示器 | 800x600 | 1920x1080 |

#### 12.1.2 軟體需求

| 元件 | 版本 | 說明 |
|------|------|------|
| 作業系統 | Windows 7+, macOS 10.12+, Linux | 任何支援 Python 的系統 |
| Python | 3.6+ | 必需 |
| pypdf | 4.0.0+ | 必需 |
| tkinter | 內建 | GUI 版本必需 |

### 12.2 安裝方式

#### 12.2.1 標準安裝

```bash
# 1. 複製專案
git clone https://github.com/user/pdf_reader.git
cd pdf_reader

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 執行程式
python pdf_reader.py  # CLI 版本
python pdf_reader_gui.py  # GUI 版本
```

#### 12.2.2 虛擬環境安裝

```bash
# 1. 建立虛擬環境
python -m venv venv

# 2. 啟用虛擬環境
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 執行程式
python pdf_reader.py
```

#### 12.2.3 套件安裝

```bash
# 建立 setup.py
pip install -e .

# 執行
pdf-reader document.pdf
pdf-reader-gui
```

### 12.3 打包發布

#### 12.3.1 PyPI 發布

```bash
# 1. 建立發布檔案
python setup.py sdist bdist_wheel

# 2. 上傳到 PyPI
twine upload dist/*

# 3. 使用者安裝
pip install pdf-reader
```

#### 12.3.2 可執行檔打包

**使用 PyInstaller**：

```bash
# 安裝 PyInstaller
pip install pyinstaller

# 打包 CLI 版本
pyinstaller --onefile pdf_reader.py

# 打包 GUI 版本
pyinstaller --onefile --windowed pdf_reader_gui.py

# 輸出位於 dist/ 目錄
```

**使用 cx_Freeze**：

```python
# setup.py
from cx_Freeze import setup, Executable

setup(
    name="PDF Reader",
    version="1.0",
    description="PDF 閱讀和搜尋工具",
    executables=[
        Executable("pdf_reader.py"),
        Executable("pdf_reader_gui.py", base="Win32GUI")
    ]
)
```

```bash
python setup.py build
```

### 12.4 跨平台考量

#### 12.4.1 路徑處理

```python
# 使用 pathlib 保證跨平台相容
from pathlib import Path

path = Path("folder") / "file.pdf"  # 自動使用正確的分隔符
```

#### 12.4.2 字元編碼

```python
# 明確指定 UTF-8 編碼
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
```

#### 12.4.3 GUI 字型

```python
# 根據平台選擇字型
import platform

if platform.system() == 'Windows':
    font = ('Microsoft YaHei', 10)
elif platform.system() == 'Darwin':  # macOS
    font = ('PingFang SC', 10)
else:  # Linux
    font = ('WenQuanYi Micro Hei', 10)
```

### 12.5 版本控制

#### 12.5.1 版本號規則

採用語意化版本（Semantic Versioning）：

```
主版本.次版本.修訂號

例如: 1.2.3
- 主版本: 不相容的 API 變更
- 次版本: 向下相容的功能新增
- 修訂號: 向下相容的問題修正
```

#### 12.5.2 版本歷史

| 版本 | 日期 | 說明 |
|------|------|------|
| 1.0.0 | 2025-12-04 | 初始版本 |
| 1.1.0 | TBD | 新增批次搜尋功能 |
| 1.2.0 | TBD | 新增 GUI 介面 |
| 2.0.0 | TBD | 重大架構重構 |

### 12.6 維護計畫

#### 12.6.1 定期維護

- **每月**：檢查依賴更新、安全漏洞掃描
- **每季**：效能優化、程式碼審查
- **每年**：架構評估、技術升級

#### 12.6.2 使用者支援

- **文件**：維護 README.md 和 SDD.md
- **問題追蹤**：使用 GitHub Issues
- **社群**：建立使用者論壇或 Discord

#### 12.6.3 更新策略

- **自動更新檢查**：啟動時檢查新版本
- **更新通知**：提示使用者有新版本可用
- **更新日誌**：記錄每個版本的變更

---

## 附錄

### A. 術語表

| 術語 | 英文 | 說明 |
|------|------|------|
| PDF | Portable Document Format | 可攜式文件格式 |
| CLI | Command Line Interface | 命令列介面 |
| GUI | Graphical User Interface | 圖形使用者介面 |
| 元資料 | Metadata | 描述資料的資料 |
| 正則表達式 | Regular Expression | 字串匹配模式 |
| 批次處理 | Batch Processing | 一次處理多個項目 |
| 高亮 | Highlight | 視覺強調顯示 |
| 上下文 | Context | 周圍的文字或環境 |

### B. 參考資料

1. **pypdf 文件**：https://pypdf.readthedocs.io/
2. **Python 官方文件**：https://docs.python.org/3/
3. **Tkinter 教學**：https://docs.python.org/3/library/tkinter.html
4. **Semantic Versioning**：https://semver.org/
5. **Python Packaging**：https://packaging.python.org/

### C. 變更歷史

| 版本 | 日期 | 作者 | 變更說明 |
|------|------|------|---------|
| 1.0 | 2025-12-04 | Claude | 初始版本，完整 SDD |

### D. 審查記錄

| 日期 | 審查者 | 意見 | 狀態 |
|------|--------|------|------|
| 2025-12-04 | - | - | 待審查 |

---

**文件結束**

*本文件為 PDF Reader 專案的官方軟體設計文件，所有設計和實作應以本文件為準。*
