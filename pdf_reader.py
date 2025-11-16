#!/usr/bin/env python3
"""
PDF Reader - 一个简单的PDF文件阅读工具
支持提取PDF文本内容、页数统计和基本信息
"""

import sys
import argparse
from pathlib import Path
try:
    from pypdf import PdfReader
except ImportError:
    print("错误: 请先安装 pypdf 库")
    print("运行: pip install -r requirements.txt")
    sys.exit(1)


def read_pdf(pdf_path, page_num=None, show_metadata=False):
    """
    读取PDF文件并提取内容

    Args:
        pdf_path: PDF文件路径
        page_num: 指定要读取的页码（从1开始），None表示读取所有页
        show_metadata: 是否显示PDF元数据
    """
    try:
        # 检查文件是否存在
        path = Path(pdf_path)
        if not path.exists():
            print(f"错误: 文件不存在 '{pdf_path}'")
            return False

        if not path.suffix.lower() == '.pdf':
            print(f"警告: 文件可能不是PDF格式 '{pdf_path}'")

        # 打开PDF文件
        reader = PdfReader(pdf_path)

        # 显示基本信息
        num_pages = len(reader.pages)
        print(f"\n{'='*60}")
        print(f"PDF文件: {path.name}")
        print(f"总页数: {num_pages}")
        print(f"{'='*60}\n")

        # 显示元数据
        if show_metadata and reader.metadata:
            print("PDF元数据:")
            print("-" * 60)
            for key, value in reader.metadata.items():
                print(f"{key}: {value}")
            print("-" * 60 + "\n")

        # 提取文本内容
        if page_num is not None:
            # 读取指定页
            if page_num < 1 or page_num > num_pages:
                print(f"错误: 页码超出范围 (1-{num_pages})")
                return False

            page = reader.pages[page_num - 1]
            text = page.extract_text()
            print(f"第 {page_num} 页内容:")
            print("=" * 60)
            print(text)
            print("=" * 60)
        else:
            # 读取所有页
            for i, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                print(f"\n第 {i} 页:")
                print("-" * 60)
                print(text)
                print("-" * 60)

        return True

    except Exception as e:
        print(f"读取PDF时出错: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='PDF阅读器 - 提取和显示PDF文件内容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s document.pdf              # 读取整个PDF文件
  %(prog)s document.pdf -p 1         # 只读取第1页
  %(prog)s document.pdf -m           # 显示PDF元数据
  %(prog)s document.pdf -p 3 -m      # 读取第3页并显示元数据
        """
    )

    parser.add_argument(
        'pdf_file',
        help='PDF文件路径'
    )

    parser.add_argument(
        '-p', '--page',
        type=int,
        metavar='NUM',
        help='指定要读取的页码（从1开始）'
    )

    parser.add_argument(
        '-m', '--metadata',
        action='store_true',
        help='显示PDF元数据信息'
    )

    args = parser.parse_args()

    # 读取PDF
    success = read_pdf(args.pdf_file, args.page, args.metadata)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
