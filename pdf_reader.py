#!/usr/bin/env python3
"""
PDF Reader - 一个简单的PDF文件阅读工具
支持提取PDF文本内容、页数统计和基本信息
"""

import sys
import argparse
import re
from pathlib import Path
from typing import List, Dict
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


def search_pdf_directory(dir_path, search_term, case_sensitive=False, context_chars=50):
    """
    在指定文件夹中的所有PDF文件中搜索关键词

    Args:
        dir_path: 文件夹路径
        search_term: 要搜索的文本
        case_sensitive: 是否区分大小写
        context_chars: 显示上下文的字符数
    """
    try:
        # 检查文件夹是否存在
        path = Path(dir_path)
        if not path.exists():
            print(f"错误: 文件夹不存在 '{dir_path}'")
            return False

        if not path.is_dir():
            print(f"错误: '{dir_path}' 不是一个文件夹")
            return False

        # 查找所有PDF文件
        pdf_files = sorted(path.glob('**/*.pdf'))

        if not pdf_files:
            print(f"错误: 在 '{dir_path}' 中没有找到PDF文件")
            return False

        # 显示搜索信息
        print(f"\n{'='*70}")
        print(f"批量搜索模式")
        print(f"文件夹: {path.absolute()}")
        print(f"搜索内容: '{search_term}'")
        print(f"区分大小写: {'是' if case_sensitive else '否'}")
        print(f"找到 {len(pdf_files)} 个PDF文件")
        print(f"{'='*70}\n")

        # 统计信息
        total_files_with_matches = 0
        total_matches = 0
        results_summary: List[Dict] = []

        # 遍历每个PDF文件
        for pdf_file in pdf_files:
            try:
                reader = PdfReader(pdf_file)
                num_pages = len(reader.pages)
                file_matches = 0
                file_pages_with_matches = []

                # 遍历每一页
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    lines = text.split('\n')

                    # 在每一行中搜索
                    for line_num, line in enumerate(lines, 1):
                        if case_sensitive:
                            matches = list(re.finditer(re.escape(search_term), line))
                        else:
                            matches = list(re.finditer(re.escape(search_term), line, re.IGNORECASE))

                        if matches:
                            # 第一次找到匹配时，打印文件名
                            if file_matches == 0:
                                print(f"\n📄 文件: {pdf_file.name}")
                                print(f"   路径: {pdf_file.relative_to(path)}")
                                print("-" * 70)

                            # 记录页码
                            if page_num + 1 not in file_pages_with_matches:
                                file_pages_with_matches.append(page_num + 1)

                            # 显示每个匹配
                            for match in matches:
                                start = match.start()
                                end = match.end()
                                context_start = max(0, start - context_chars)
                                context_end = min(len(line), end + context_chars)

                                before = line[context_start:start].strip()
                                matched = line[start:end]
                                after = line[end:context_end].strip()

                                file_matches += 1
                                print(f"   ✓ 第 {page_num + 1} 页, 第 {line_num} 行: ...{before}【{matched}】{after}...")

                # 如果该文件有匹配，记录统计信息
                if file_matches > 0:
                    total_files_with_matches += 1
                    total_matches += file_matches
                    results_summary.append({
                        'file': pdf_file.name,
                        'matches': file_matches,
                        'pages': file_pages_with_matches
                    })
                    print(f"   📊 小计: {file_matches} 处匹配，分布在第 {', '.join(map(str, file_pages_with_matches))} 页")

            except Exception as e:
                print(f"⚠️  处理文件 {pdf_file.name} 时出错: {e}")
                continue

        # 显示总结
        print(f"\n{'='*70}")
        print(f"搜索完成！")
        print(f"{'='*70}")

        if total_files_with_matches > 0:
            print(f"📊 总体统计:")
            print(f"   - 搜索文件总数: {len(pdf_files)}")
            print(f"   - 包含匹配的文件: {total_files_with_matches}")
            print(f"   - 总匹配次数: {total_matches}")
            print(f"\n📋 详细结果:")
            for idx, result in enumerate(results_summary, 1):
                print(f"   {idx}. {result['file']}: {result['matches']} 处匹配")
        else:
            print(f"在 {len(pdf_files)} 个PDF文件中未找到匹配内容")

        print(f"{'='*70}\n")

        return total_files_with_matches > 0

    except Exception as e:
        print(f"批量搜索时出错: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='PDF阅读器 - 提取和显示PDF文件内容，支持单文件和批量搜索',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  单文件模式:
    %(prog)s document.pdf              # 读取整个PDF文件
    %(prog)s document.pdf -p 1         # 只读取第1页
    %(prog)s document.pdf -m           # 显示PDF元数据
    %(prog)s document.pdf -p 3 -m      # 读取第3页并显示元数据
    %(prog)s document.pdf -s "关键词"  # 搜索PDF中的关键词
    %(prog)s document.pdf -s "word" -c # 区分大小写搜索

  批量搜索模式:
    %(prog)s -d ./pdfs -s "关键词"     # 搜索文件夹中所有PDF
    %(prog)s -d ./docs -s "API" -c     # 区分大小写批量搜索
        """
    )

    parser.add_argument(
        'pdf_file',
        nargs='?',
        help='PDF文件路径（单文件模式）'
    )

    parser.add_argument(
        '-d', '--directory',
        type=str,
        metavar='DIR',
        help='批量搜索：指定包含PDF文件的文件夹路径'
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

    # 验证参数
    if args.directory and args.pdf_file:
        print("错误: 不能同时指定文件和文件夹")
        print("使用 -h 查看帮助信息")
        sys.exit(1)

    if not args.directory and not args.pdf_file:
        print("错误: 必须指定PDF文件或文件夹")
        print("使用 -h 查看帮助信息")
        sys.exit(1)

    # 批量搜索模式
    if args.directory:
        if not args.search:
            print("错误: 批量搜索模式必须使用 -s/--search 参数指定搜索内容")
            sys.exit(1)
        success = search_pdf_directory(args.directory, args.search, args.case_sensitive, args.context)

    # 单文件模式
    elif args.search:
        success = search_pdf(args.pdf_file, args.search, args.case_sensitive, args.context)
    else:
        # 读取PDF
        success = read_pdf(args.pdf_file, args.page, args.metadata)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
