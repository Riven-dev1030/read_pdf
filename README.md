# PDF Reader - PDF阅读器

一个简单易用的Python PDF阅读工具，提供命令行和图形界面两种使用方式。

A simple and easy-to-use Python PDF reading tool that can extract and display text content from PDF files, with both CLI and GUI versions.

## 版本说明 Versions

- 📟 **命令行版本** (`pdf_reader.py`) - 适合批处理和脚本调用
- 🖥️ **图形界面版本** (`pdf_reader_gui.py`) - 提供可视化操作界面

## 功能特性 Features

### 命令行版本 CLI Version
- 📖 读取整个PDF文件或指定页面
- 📊 显示PDF基本信息（总页数）
- 📋 提取PDF元数据（作者、标题等）
- 🔍 **搜索功能**：在PDF中查找关键词并显示位置
- 📁 **批量搜索**：搜索文件夹中的所有PDF文件
- 📍 显示搜索结果的上下文内容
- 🔤 支持大小写敏感/不敏感搜索
- 💻 支持命令行参数
- 🌏 中文友好

### 图形界面版本 GUI Version
- 🖱️ **可视化操作**：点击按钮打开文件、搜索内容
- 📁 **批量搜索模式**：打开文件夹，搜索所有PDF文件
- 📑 **左右分栏布局**：左侧搜索控制，右侧内容显示
- 🔍 **实时搜索**：输入关键词即可搜索整个PDF或多个文件
- 📍 **搜索结果列表**：显示文件名、页码、行号和内容预览
- 🎯 **快速跳转**：双击搜索结果直接跳转到对应位置
- 💡 **黄色高亮**：自动高亮所有匹配的关键词
- 📊 **统计信息**：显示匹配数量和所在页面/文件
- ⚙️ **搜索选项**：支持区分/不区分大小写

## 安装 Installation

1. 克隆仓库或下载文件
2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方法 Usage

### 图形界面版本 GUI Version

#### 启动 GUI
```bash
python pdf_reader_gui.py
```

#### 使用步骤

##### 单文件模式
1. **打开文件**：点击「打开 PDF 文件」按钮，选择要阅读的 PDF
2. **浏览内容**：右侧窗口会自动显示所有页面的文本内容
3. **搜索关键词**：
   - 在左侧搜索框输入关键词
   - 可选：勾选「区分大小写」
   - 点击「开始搜索」或按回车键
4. **查看结果**：
   - 左侧列表显示所有匹配项（文件名、页码、行号、内容预览）
   - 右侧文本区域会用黄色高亮所有匹配
5. **快速跳转**：双击搜索结果列表中的任意项，右侧内容会自动滚动到对应位置

##### 批量搜索模式
1. **打开文件夹**：点击「打开文件夹」按钮，选择包含 PDF 文件的文件夹
2. **查看文件列表**：右侧显示找到的所有 PDF 文件
3. **搜索关键词**：
   - 在左侧搜索框输入关键词
   - 可选：勾选「区分大小写」
   - 点击「开始搜索」按钮
4. **查看结果**：
   - 左侧列表显示所有文件中的匹配项（文件名、页码、行号、内容预览）
   - 右侧显示搜索统计信息
5. **结果排序**：结果按文件名和页码自动排序，方便查看

#### GUI 界面布局
```
┌─────────────────────────────────────────────────────────┐
│  PDF 阅读器                                        - □ ×│
├──────────────┬──────────────────────────────────────────┤
│ 文件操作      │  PDF 内容                                │
│ [打开PDF]    │  ═══════════════════════════════════════│
│ 文件: xx.pdf │  第 1 页                                 │
│ 总页数: 10   │  ═══════════════════════════════════════│
│              │  这是PDF的文本内容...                     │
│ 搜索功能      │  关键词会被【高亮】显示                   │
│ 搜索内容:     │                                          │
│ [         ]  │  ═══════════════════════════════════════│
│ ☐ 区分大小写  │  第 2 页                                 │
│ [开始搜索]    │  ═══════════════════════════════════════│
│              │  继续显示内容...                          │
│ 搜索结果: 5  │                                          │
│              │                                          │
│ 搜索结果列表: │                                          │
│ ┌──────────┐│                                          │
│ │页 行 内容 ││                                          │
│ │1  3  ... ││                                          │
│ │1  15 ... ││                                          │
│ │5  7  ... ││                                          │
│ └──────────┘│                                          │
└──────────────┴──────────────────────────────────────────┘
```

---

### 命令行版本 CLI Version

#### 基本用法

##### 阅读PDF
```bash
# 读取整个PDF文件
python pdf_reader.py document.pdf

# 读取指定页（例如第1页）
python pdf_reader.py document.pdf -p 1

# 显示PDF元数据
python pdf_reader.py document.pdf -m

# 读取第3页并显示元数据
python pdf_reader.py document.pdf -p 3 -m
```

##### 搜索PDF内容（单文件）
```bash
# 搜索PDF中的关键词（不区分大小写）
python pdf_reader.py document.pdf -s "关键词"

# 搜索英文关键词
python pdf_reader.py document.pdf -s "keyword"

# 区分大小写搜索
python pdf_reader.py document.pdf -s "KeyWord" -c

# 自定义显示的上下文字符数（默认50字符）
python pdf_reader.py document.pdf -s "搜索内容" --context 100
```

##### 批量搜索（搜索文件夹）
```bash
# 搜索文件夹中所有PDF文件
python pdf_reader.py -d ./documents -s "关键词"

# 搜索子文件夹中的所有PDF（递归搜索）
python pdf_reader.py -d ./projects -s "API"

# 批量搜索时区分大小写
python pdf_reader.py -d ./pdfs -s "Python" -c

# 自定义上下文字符数
python pdf_reader.py -d ./docs -s "搜索内容" --context 100
```

### 命令行参数

#### 基本参数
- `pdf_file`: PDF文件路径（单文件模式，可选）
- `-d, --directory DIR`: 批量搜索：指定包含PDF文件的文件夹路径
- `-h, --help`: 显示帮助信息

#### 阅读模式（仅单文件模式）
- `-p, --page NUM`: 指定要读取的页码（从1开始）
- `-m, --metadata`: 显示PDF元数据信息

#### 搜索模式（单文件和批量模式）
- `-s, --search TEXT`: 在PDF中搜索指定文本内容
- `-c, --case-sensitive`: 搜索时区分大小写（默认不区分）
- `--context CHARS`: 搜索结果显示的上下文字符数（默认50）

**注意**：
- 单文件模式和批量模式不能同时使用
- 批量搜索模式（`-d`）必须配合 `-s` 参数使用
- 批量搜索会递归搜索指定文件夹及其子文件夹中的所有 PDF 文件

### 示例

#### 单文件操作
```bash
# 读取报告PDF的第5页
python pdf_reader.py report.pdf --page 5

# 查看PDF的元数据信息
python pdf_reader.py book.pdf --metadata

# 在技术文档中搜索"API"关键词
python pdf_reader.py technical_doc.pdf -s "API"

# 在合同中区分大小写搜索"Section 3.1"
python pdf_reader.py contract.pdf -s "Section 3.1" -c
```

#### 批量搜索操作
```bash
# 在所有学术论文中搜索"机器学习"
python pdf_reader.py -d ./papers -s "机器学习"

# 在项目文档文件夹中搜索"TODO"（区分大小写）
python pdf_reader.py -d ./project_docs -s "TODO" -c

# 在多层级文件夹中搜索，显示更多上下文
python pdf_reader.py -d ./archive -s "重要" --context 100
```

### 搜索功能说明

#### 单文件搜索
搜索功能会：
- 🔍 扫描PDF的所有页面
- 📄 显示包含关键词的所有页码
- 📍 **精确显示每个匹配在第几页第几行**
- 📊 统计每页找到的匹配次数
- 📝 显示每个匹配项的上下文内容（用【】标记）
- ✅ 支持中英文搜索

#### 批量搜索
批量搜索功能会：
- 📁 递归扫描指定文件夹及其子文件夹中的所有 PDF 文件
- 🔍 在每个 PDF 文件中搜索关键词
- 📄 显示每个文件中的匹配次数和页码
- 📍 精确显示每个匹配在哪个文件、第几页、第几行
- 📊 提供总体统计信息（搜索文件数、匹配文件数、总匹配次数）
- 📝 显示每个匹配项的上下文内容（用【】标记）
- ⚡ 自动跳过无法读取的文件并继续处理

#### 单文件搜索结果示例：
```
============================================================
PDF文件: example.pdf
搜索内容: 'Python'
区分大小写: 否
============================================================

第 1 页 - 找到 2 处匹配:
------------------------------------------------------------
  [1] 第 3 行: ...This guide introduces【Python】programming language...
  [2] 第 15 行: ...Learn【Python】in 30 days with...

第 5 页 - 找到 1 处匹配:
------------------------------------------------------------
  [1] 第 7 行: ...Advanced【Python】techniques for...

============================================================
搜索完成！
共在 2 页中找到 3 处匹配
页码: 1, 5
============================================================
```

#### 批量搜索结果示例：
```
======================================================================
批量搜索模式
文件夹: /home/user/documents
搜索内容: 'Python'
区分大小写: 否
找到 3 个PDF文件
======================================================================

📄 文件: tutorial.pdf
   路径: tutorials/tutorial.pdf
----------------------------------------------------------------------
   ✓ 第 1 页, 第 5 行: ...Introduction to【Python】programming...
   ✓ 第 2 页, 第 12 行: ...【Python】is a high-level language...
   📊 小计: 2 处匹配，分布在第 1, 2 页

📄 文件: guide.pdf
   路径: guides/guide.pdf
----------------------------------------------------------------------
   ✓ 第 3 页, 第 8 行: ...Learning【Python】basics...
   📊 小计: 1 处匹配，分布在第 3 页

======================================================================
搜索完成！
======================================================================
📊 总体统计:
   - 搜索文件总数: 3
   - 包含匹配的文件: 2
   - 总匹配次数: 3

📋 详细结果:
   1. tutorial.pdf: 2 处匹配
   2. guide.pdf: 1 处匹配
======================================================================
```

## 系统要求 Requirements

### 命令行版本 CLI Version
- Python 3.6+
- pypdf 库

### 图形界面版本 GUI Version
- Python 3.6+
- pypdf 库
- tkinter（Python 内置，通常无需单独安装）

> **注意**：在某些 Linux 系统上，可能需要安装 tkinter：
> - Ubuntu/Debian: `sudo apt-get install python3-tk`
> - Fedora: `sudo dnf install python3-tkinter`
> - Arch Linux: `sudo pacman -S tk`

## 许可证 License

MIT License

## 贡献 Contributing

欢迎提交Issue和Pull Request！

## 注意事项 Notes

- 此工具提取的是PDF中的文本内容，对于图片型PDF（扫描件）可能无法提取文字
- 复杂排版的PDF可能会影响文本提取的格式
- This tool extracts text content from PDFs. It may not work well with image-based PDFs (scanned documents)
- Complex PDF layouts may affect the formatting of extracted text

---

## 开发历史 Development History

### 2025-11-16: 合并 GUI 功能分支
**合并分支**: `claude/merge-feature-branches-01Chx3cpQ5JXSEtR9LbsxVJP`

**合并来源**:
1. `claude/gui-new-branch-01K1mT1Ji6LsdptPLuY4SuWZ`
2. `claude/double-click-string-location-01TpmCLx87NqjZzi8xyH7DNd`

**合并原因**:
- 将两个独立开发的 GUI 功能整合到一起
- 第一个分支提供了基础的 GUI 界面和批量搜索功能
- 第二个分支改进了用户体验，修复了双击跳转功能和提示文字

**主要变更**:
1. **GUI 基础功能** (来自 gui-new-branch):
   - ✅ 添加了完整的 Tkinter GUI 界面 (`pdf_reader_gui.py`)
   - ✅ 实现批量搜索功能：可打开文件夹搜索多个 PDF 文件
   - ✅ 添加 `.gitignore` 文件排除 Python 缓存文件
   - ✅ 左右分栏布局：搜索控制面板 + 内容显示区域
   - ✅ 搜索结果以树状列表显示（文件名、页码、行号、内容预览）

2. **用户体验改进** (来自 double-click-string-location):
   - ✅ 修复了双击搜索结果的跳转功能
   - ✅ 改进了提示文字："双击结果可跳转！"
   - ✅ 优化了变量初始化（`target_line` 使用整数而非浮点数）
   - ✅ 批量搜索模式下也有清晰的双击提示

**解决的冲突**:
- 文件: `pdf_reader_gui.py`
- 冲突位置: 搜索结果提示文字、批量搜索提示文字、target_line 变量初始化
- 解决方案: 保留了更详细、用户友好的提示信息，确保用户知道可以双击跳转

**技术细节**:
- 搜索结果统计提示: `"搜索结果: {N} 处匹配，共 {M} 页。双击结果可跳转！"`
- 批量搜索提示: `"请在左侧查看详细结果，双击可查看具体位置。"`
- 跳转功能使用整数行号计算，避免浮点数精度问题

**为什么要合并**:
这两个分支都是对 GUI 功能的增强，分开维护会导致功能碎片化。合并后：
- 用户可以同时使用批量搜索和精确跳转功能
- 界面提示更加清晰，用户体验更好
- 代码库更整洁，便于后续维护和功能扩展
