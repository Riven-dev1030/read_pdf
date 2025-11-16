#!/usr/bin/env python3
"""
PDF Reader - 一个简单的PDF文件阅读工具
支持提取PDF文本内容、页数统计和基本信息
"""

import sys
import argparse
import re
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


def search_pdf(pdf_path, search_term, case_sensitive=False, context_chars=50):
    """
    在PDF文件中搜索指定内容

    Args:
        pdf_path: PDF文件路径
        search_term: 要搜索的文本
        case_sensitive: 是否区分大小写
        context_chars: 显示上下文的字符数
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
        num_pages = len(reader.pages)

        # 显示搜索信息
        print(f"\n{'='*60}")
        print(f"PDF文件: {path.name}")
        print(f"搜索内容: '{search_term}'")
        print(f"区分大小写: {'是' if case_sensitive else '否'}")
        print(f"{'='*60}\n")

        # 搜索结果统计
        total_matches = 0
        found_pages = []

        # 遍历每一页进行搜索
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()

            # 将文本按行分割
            lines = text.split('\n')

            # 存储当前页的匹配结果
            page_matches = []

            # 在每一行中搜索
            for line_num, line in enumerate(lines, 1):
                # 根据是否区分大小写进行搜索
                if case_sensitive:
                    matches = list(re.finditer(re.escape(search_term), line))
                else:
                    matches = list(re.finditer(re.escape(search_term), line, re.IGNORECASE))

                # 如果在这一行找到匹配
                for match in matches:
                    start = match.start()
                    end = match.end()

                    # 获取上下文
                    context_start = max(0, start - context_chars)
                    context_end = min(len(line), end + context_chars)

                    # 提取上下文文本
                    before = line[context_start:start]
                    matched = line[start:end]
                    after = line[end:context_end]

                    # 保存匹配信息
                    page_matches.append({
                        'line_num': line_num,
                        'before': before.strip(),
                        'matched': matched,
                        'after': after.strip()
                    })

            # 如果当前页有匹配项
            if page_matches:
                found_pages.append(page_num + 1)
                match_count = len(page_matches)
                total_matches += match_count

                print(f"第 {page_num + 1} 页 - 找到 {match_count} 处匹配:")
                print("-" * 60)

                # 显示每个匹配的详细信息
                for idx, match_info in enumerate(page_matches, 1):
                    line_num = match_info['line_num']
                    before = match_info['before']
                    matched = match_info['matched']
                    after = match_info['after']

                    # 显示结果（包含行号）
                    print(f"  [{idx}] 第 {line_num} 行: ...{before}【{matched}】{after}...")

                print()

        # 显示总结
        print("=" * 60)
        if total_matches > 0:
            print(f"搜索完成！")
            print(f"共在 {len(found_pages)} 页中找到 {total_matches} 处匹配")
            print(f"页码: {', '.join(map(str, found_pages))}")
        else:
            print(f"未找到匹配内容")
        print("=" * 60)

        return total_matches > 0

    except Exception as e:
        print(f"搜索PDF时出错: {e}")
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
  %(prog)s document.pdf -s "关键词"  # 搜索PDF中的关键词
  %(prog)s document.pdf -s "word" -c # 区分大小写搜索
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

    parser.add_argument(
        '-s', '--search',
        type=str,
        metavar='TEXT',
        help='在PDF中搜索指定文本内容'
    )

    parser.add_argument(
        '-c', '--case-sensitive',
        action='store_true',
        help='搜索时区分大小写（默认不区分）'
    )

    parser.add_argument(
        '--context',
        type=int,
        default=50,
        metavar='CHARS',
        help='搜索结果显示的上下文字符数（默认50）'
    )

    args = parser.parse_args()

    # 如果是搜索模式
    if args.search:
        success = search_pdf(args.pdf_file, args.search, args.case_sensitive, args.context)
    else:
        # 读取PDF
        success = read_pdf(args.pdf_file, args.page, args.metadata)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
