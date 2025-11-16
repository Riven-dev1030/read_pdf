# PDF Reader - PDF阅读器

一个简单易用的Python PDF阅读工具，可以提取和显示PDF文件的文本内容。

A simple and easy-to-use Python PDF reading tool that can extract and display text content from PDF files.

## 功能特性 Features

- 📖 读取整个PDF文件或指定页面
- 📊 显示PDF基本信息（总页数）
- 📋 提取PDF元数据（作者、标题等）
- 🔍 **搜索功能**：在PDF中查找关键词并显示位置
- 📍 显示搜索结果的上下文内容
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

#### 搜索PDF内容
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

### 命令行参数

#### 基本参数
- `pdf_file`: PDF文件路径（必需）
- `-h, --help`: 显示帮助信息

#### 阅读模式
- `-p, --page NUM`: 指定要读取的页码（从1开始）
- `-m, --metadata`: 显示PDF元数据信息

#### 搜索模式
- `-s, --search TEXT`: 在PDF中搜索指定文本内容
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
