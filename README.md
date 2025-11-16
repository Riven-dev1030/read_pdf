# PDF Reader - PDF阅读器

一个简单易用的Python PDF阅读工具，可以提取和显示PDF文件的文本内容。

A simple and easy-to-use Python PDF reading tool that can extract and display text content from PDF files.

## 功能特性 Features

- 📖 读取整个PDF文件或指定页面
- 📊 显示PDF基本信息（总页数）
- 📋 提取PDF元数据（作者、标题等）
- 🔍 **搜索功能**：在PDF中查找关键词并显示位置
- 📁 **批量搜索**：在整个文件夹中搜索所有PDF文件
- 📍 精确显示每个匹配在第几页第几行
- 📈 统计分析：显示匹配次数和文件列表
- 🔤 支持大小写敏感/不敏感搜索
- 💻 支持命令行参数
- 🌏 中文友好

## 安装 Installation

1. 克隆仓库或下载文件
2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方法 Usage

### 基本用法

#### 阅读PDF
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

#### 搜索PDF内容（单文件）
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

#### 批量搜索PDF文件（整个文件夹）
```bash
# 在文件夹中搜索所有PDF文件
python pdf_reader.py -d ./documents -s "关键词"

# 在文件夹中区分大小写搜索
python pdf_reader.py -d ./reports -s "API" -c

# 搜索包含子文件夹的所有PDF（递归搜索）
python pdf_reader.py -d ./project -s "function"

# 批量搜索并自定义上下文长度
python pdf_reader.py -d ./pdfs -s "重要" --context 80
```

### 命令行参数

#### 基本参数
- `pdf_file`: PDF文件路径（单文件模式时必需）
- `-d, --directory DIR`: 批量搜索模式，指定包含PDF文件的文件夹
- `-h, --help`: 显示帮助信息

#### 阅读模式（仅单文件）
- `-p, --page NUM`: 指定要读取的页码（从1开始）
- `-m, --metadata`: 显示PDF元数据信息

#### 搜索模式（单文件和批量搜索）
- `-s, --search TEXT`: 搜索指定文本内容
- `-c, --case-sensitive`: 搜索时区分大小写（默认不区分）
- `--context CHARS`: 搜索结果显示的上下文字符数（默认50）

### 示例

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

### 搜索功能说明

搜索功能会：
- 🔍 扫描PDF的所有页面
- 📄 显示包含关键词的所有页码
- 📍 **精确显示每个匹配在第几页第几行**
- 📊 统计每页找到的匹配次数
- 📝 显示每个匹配项的上下文内容（用【】标记）
- ✅ 支持中英文搜索

搜索结果示例：
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

### 批量搜索功能说明

批量搜索会：
- 📁 递归扫描指定文件夹中的所有PDF文件（包括子文件夹）
- 📊 显示每个文件的搜索结果和统计信息
- 📈 提供总体统计：文件总数、包含匹配的文件数、总匹配次数
- 🎯 清晰显示每个匹配在哪个文件、哪一页、哪一行
- 📝 显示每个匹配项的上下文内容

批量搜索结果示例：
```
======================================================================
批量搜索模式
文件夹: /home/user/documents
搜索内容: 'Python'
区分大小写: 否
找到 3 个PDF文件
======================================================================

📄 文件: tutorial.pdf
   路径: tutorial.pdf
----------------------------------------------------------------------
   ✓ 第 1 页, 第 5 行: ...Introduction to【Python】programming...
   ✓ 第 1 页, 第 12 行: ...【Python】is a versatile language...
   ✓ 第 3 页, 第 8 行: ...Advanced【Python】features...
   📊 小计: 3 处匹配，分布在第 1, 3 页

📄 文件: reference.pdf
   路径: guides/reference.pdf
----------------------------------------------------------------------
   ✓ 第 2 页, 第 10 行: ...【Python】documentation...
   📊 小计: 1 处匹配，分布在第 2 页

======================================================================
搜索完成！
======================================================================
📊 总体统计:
   - 搜索文件总数: 3
   - 包含匹配的文件: 2
   - 总匹配次数: 4

📋 详细结果:
   1. tutorial.pdf: 3 处匹配
   2. reference.pdf: 1 处匹配
======================================================================
```

## 系统要求 Requirements

- Python 3.6+
- pypdf 库

## 许可证 License

MIT License

## 贡献 Contributing

欢迎提交Issue和Pull Request！

## 注意事项 Notes

- 此工具提取的是PDF中的文本内容，对于图片型PDF（扫描件）可能无法提取文字
- 复杂排版的PDF可能会影响文本提取的格式
- This tool extracts text content from PDFs. It may not work well with image-based PDFs (scanned documents)
- Complex PDF layouts may affect the formatting of extracted text
