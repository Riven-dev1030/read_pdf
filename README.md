# PDF Reader - PDF阅读器

一个简单易用的Python PDF阅读工具，可以提取和显示PDF文件的文本内容。

A simple and easy-to-use Python PDF reading tool that can extract and display text content from PDF files.

## 功能特性 Features

- 📖 读取整个PDF文件或指定页面
- 📊 显示PDF基本信息（总页数）
- 📋 提取PDF元数据（作者、标题等）
- 🔍 支持命令行参数
- 🌏 中文友好

## 安装 Installation

1. 克隆仓库或下载文件
2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方法 Usage

### 基本用法

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

### 命令行参数

- `pdf_file`: PDF文件路径（必需）
- `-p, --page NUM`: 指定要读取的页码（从1开始）
- `-m, --metadata`: 显示PDF元数据信息
- `-h, --help`: 显示帮助信息

### 示例

```bash
# 读取报告PDF的第5页
python pdf_reader.py report.pdf --page 5

# 查看PDF的元数据信息
python pdf_reader.py book.pdf --metadata
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
