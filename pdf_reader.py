#!/usr/bin/env python3
"""PDF Reader - PDF檔案閱讀工具，支持讀取、搜尋和批次處理"""

import sys
import argparse
import re
from pathlib import Path
from typing import Optional

try:
    from pypdf import PdfReader
except ImportError:
    print("錯誤: 請先安裝 pypdf 函式庫")
    print("執行: pip install -r requirements.txt")
    sys.exit(1)

# 常量
SEPARATOR_WIDTH = 60
DEFAULT_CONTEXT_CHARS = 50


def read_pdf(pdf_path: str, page_num: Optional[int] = None, show_metadata: bool = False) -> bool:
    """讀取PDF檔案並提取內容"""
    try:
        path = Path(pdf_path)
        if not path.exists():
            print(f"錯誤: 檔案不存在 '{pdf_path}'")
            return False

        if path.suffix.lower() != '.pdf':
            print(f"警告: 檔案可能不是PDF格式 '{pdf_path}'")

        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)

        # 顯示基本資訊
        print(f"\n{'='*SEPARATOR_WIDTH}")
        print(f"PDF檔案: {path.name}")
        print(f"總頁數: {num_pages}")
        print(f"{'='*SEPARATOR_WIDTH}\n")

        # 顯示元資料
        if show_metadata and reader.metadata:
            print("PDF元資料:")
            print("-" * SEPARATOR_WIDTH)
            for key, value in reader.metadata.items():
                print(f"{key}: {value}")
            print("-" * SEPARATOR_WIDTH + "\n")

        # 提取文本內容
        if page_num is not None:
            if page_num < 1 or page_num > num_pages:
                print(f"錯誤: 頁碼超出範圍 (1-{num_pages})")
                return False

            text = reader.pages[page_num - 1].extract_text()
            print(f"第 {page_num} 頁內容:")
            print("=" * SEPARATOR_WIDTH)
            print(text)
            print("=" * SEPARATOR_WIDTH)
        else:
            for i, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                print(f"\n第 {i} 頁:")
                print("-" * SEPARATOR_WIDTH)
                print(text)
                print("-" * SEPARATOR_WIDTH)

        return True

    except Exception as e:
        print(f"讀取PDF時出錯: {e}")
        return False


def search_pdf(pdf_path: str, search_term: str, case_sensitive: bool = False,
               context_chars: int = DEFAULT_CONTEXT_CHARS) -> bool:
    """在PDF檔案中搜尋指定內容"""
    try:
        path = Path(pdf_path)
        if not path.exists():
            print(f"錯誤: 檔案不存在 '{pdf_path}'")
            return False

        if path.suffix.lower() != '.pdf':
            print(f"警告: 檔案可能不是PDF格式 '{pdf_path}'")

        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)

        # 顯示搜尋資訊
        print(f"\n{'='*SEPARATOR_WIDTH}")
        print(f"PDF檔案: {path.name}")
        print(f"搜尋內容: '{search_term}'")
        print(f"區分大小寫: {'是' if case_sensitive else '否'}")
        print(f"{'='*SEPARATOR_WIDTH}\n")

        total_matches = 0
        found_pages = []

        # 遍歷每一頁進行搜尋
        for page_num in range(num_pages):
            text = reader.pages[page_num].extract_text()
            lines = text.split('\n')
            page_matches = []

            # 在每一行中搜尋
            for line_num, line in enumerate(lines, 1):
                flags = 0 if case_sensitive else re.IGNORECASE
                matches = list(re.finditer(re.escape(search_term), line, flags))

                for match in matches:
                    start, end = match.start(), match.end()
                    ctx_start = max(0, start - context_chars)
                    ctx_end = min(len(line), end + context_chars)

                    page_matches.append({
                        'line_num': line_num,
                        'before': line[ctx_start:start].strip(),
                        'matched': line[start:end],
                        'after': line[end:ctx_end].strip()
                    })

            # 顯示當前頁的匹配結果
            if page_matches:
                found_pages.append(page_num + 1)
                total_matches += len(page_matches)

                print(f"第 {page_num + 1} 頁 - 找到 {len(page_matches)} 處匹配:")
                print("-" * SEPARATOR_WIDTH)

                for idx, m in enumerate(page_matches, 1):
                    print(f"  [{idx}] 第 {m['line_num']} 行: ...{m['before']}【{m['matched']}】{m['after']}...")
                print()

        # 顯示總結
        print("=" * SEPARATOR_WIDTH)
        if total_matches > 0:
            print("搜尋完成！")
            print(f"共在 {len(found_pages)} 頁中找到 {total_matches} 處匹配")
            print(f"頁碼: {', '.join(map(str, found_pages))}")
        else:
            print("未找到匹配內容")
        print("=" * SEPARATOR_WIDTH)

        return total_matches > 0

    except Exception as e:
        print(f"搜尋PDF時出錯: {e}")
        return False


def search_pdf_directory(dir_path: str, search_term: str, case_sensitive: bool = False,
                         context_chars: int = DEFAULT_CONTEXT_CHARS) -> bool:
    """在資料夾中的所有PDF檔案中搜尋關鍵詞"""
    try:
        path = Path(dir_path)
        if not path.exists():
            print(f"錯誤: 資料夾不存在 '{dir_path}'")
            return False

        if not path.is_dir():
            print(f"錯誤: '{dir_path}' 不是一個資料夾")
            return False

        pdf_files = sorted(path.glob('**/*.pdf'))
        if not pdf_files:
            print(f"錯誤: 在 '{dir_path}' 中沒有找到PDF檔案")
            return False

        # 顯示搜尋資訊
        print(f"\n{'='*70}")
        print("批次搜尋模式")
        print(f"資料夾: {path.absolute()}")
        print(f"搜尋內容: '{search_term}'")
        print(f"區分大小寫: {'是' if case_sensitive else '否'}")
        print(f"找到 {len(pdf_files)} 個PDF檔案")
        print(f"{'='*70}\n")

        total_matches = 0
        files_with_matches = 0
        results = []

        # 遍歷每個PDF檔案
        for pdf_file in pdf_files:
            try:
                reader = PdfReader(pdf_file)
                file_matches = []
                pages_with_matches = []

                for page_num in range(len(reader.pages)):
                    text = reader.pages[page_num].extract_text()
                    lines = text.split('\n')

                    for line_num, line in enumerate(lines, 1):
                        flags = 0 if case_sensitive else re.IGNORECASE
                        matches = list(re.finditer(re.escape(search_term), line, flags))

                        for match in matches:
                            start, end = match.start(), match.end()
                            ctx_start = max(0, start - context_chars)
                            ctx_end = min(len(line), end + context_chars)

                            file_matches.append({
                                'page': page_num + 1,
                                'line': line_num,
                                'before': line[ctx_start:start].strip(),
                                'matched': line[start:end],
                                'after': line[end:ctx_end].strip()
                            })

                            if page_num + 1 not in pages_with_matches:
                                pages_with_matches.append(page_num + 1)

                # 顯示該檔案的結果
                if file_matches:
                    files_with_matches += 1
                    total_matches += len(file_matches)
                    results.append((pdf_file.name, len(file_matches)))

                    rel_path = pdf_file.relative_to(path)
                    print(f"📄 檔案: {pdf_file.name}")
                    print(f"   路徑: {rel_path}")
                    print("-" * 70)

                    for m in file_matches:
                        print(f"   ✓ 第 {m['page']} 頁, 第 {m['line']} 行: ...{m['before']}【{m['matched']}】{m['after']}...")

                    pages_str = ', '.join(map(str, pages_with_matches))
                    print(f"   📊 小計: {len(file_matches)} 處匹配，分布在第 {pages_str} 頁\n")

            except Exception as e:
                print(f"⚠️  處理檔案 {pdf_file.name} 時出錯: {e}")

        # 顯示總結
        print(f"\n{'='*70}")
        print("搜尋完成！")
        print("=" * 70)

        if files_with_matches > 0:
            print("📊 總體統計:")
            print(f"   - 搜尋檔案總數: {len(pdf_files)}")
            print(f"   - 包含匹配的檔案: {files_with_matches}")
            print(f"   - 總匹配次數: {total_matches}")
            print("\n📋 詳細結果:")
            for idx, (name, count) in enumerate(results, 1):
                print(f"   {idx}. {name}: {count} 處匹配")
        else:
            print(f"在 {len(pdf_files)} 個PDF檔案中未找到匹配內容")

        print(f"{'='*70}\n")

        return files_with_matches > 0

    except Exception as e:
        print(f"批次搜尋時出錯: {e}")
        return False


def main():
    """主函式"""
    parser = argparse.ArgumentParser(
        description='PDF閱讀器 - 提取和顯示PDF檔案內容，支持單檔案和批次搜尋',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  單檔案模式:
    %(prog)s document.pdf              # 讀取整個PDF檔案
    %(prog)s document.pdf -p 1         # 只讀取第1頁
    %(prog)s document.pdf -m           # 顯示PDF元資料
    %(prog)s document.pdf -s "關鍵詞"  # 搜尋PDF中的關鍵詞

  批次搜尋模式:
    %(prog)s -d ./pdfs -s "關鍵詞"     # 搜尋資料夾中所有PDF
        """
    )

    parser.add_argument('pdf_file', nargs='?', help='PDF檔案路徑（單檔案模式）')
    parser.add_argument('-d', '--directory', type=str, metavar='DIR',
                        help='批次搜尋：指定包含PDF檔案的資料夾路徑')
    parser.add_argument('-p', '--page', type=int, metavar='NUM',
                        help='指定要讀取的頁碼（從1開始）')
    parser.add_argument('-m', '--metadata', action='store_true',
                        help='顯示PDF元資料資訊')
    parser.add_argument('-s', '--search', type=str, metavar='TEXT',
                        help='在PDF中搜尋指定文本內容')
    parser.add_argument('-c', '--case-sensitive', action='store_true',
                        help='搜尋時區分大小寫（預設不區分）')
    parser.add_argument('--context', type=int, default=DEFAULT_CONTEXT_CHARS, metavar='CHARS',
                        help=f'搜尋結果顯示的上下文字元數（預設{DEFAULT_CONTEXT_CHARS}）')

    args = parser.parse_args()

    # 驗證參數
    if args.directory and args.pdf_file:
        print("錯誤: 不能同時指定檔案和資料夾")
        sys.exit(1)

    if not args.directory and not args.pdf_file:
        print("錯誤: 必須指定PDF檔案或資料夾")
        sys.exit(1)

    if args.directory and not args.search:
        print("錯誤: 批次搜尋模式必須使用 -s/--search 參數指定搜尋內容")
        sys.exit(1)

    # 執行相應功能
    if args.directory:
        success = search_pdf_directory(args.directory, args.search, args.case_sensitive, args.context)
    elif args.search:
        success = search_pdf(args.pdf_file, args.search, args.case_sensitive, args.context)
    else:
        success = read_pdf(args.pdf_file, args.page, args.metadata)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
