#!/usr/bin/env python3
"""
PDF Reader - 一個簡單的PDF檔案閱讀工具
支援提取PDF文本內容、頁數統計和基本資訊
"""

import sys
import argparse
import re
from pathlib import Path
try:
    from pypdf import PdfReader
except ImportError:
    print("錯誤: 請先安裝 pypdf 函式庫")
    print("執行: pip install -r requirements.txt")
    sys.exit(1)


def read_pdf(pdf_path, page_num=None, show_metadata=False):
    """
    讀取PDF檔案並提取內容

    Args:
        pdf_path: PDF檔案路徑
        page_num: 指定要讀取的頁碼（從1開始），None表示讀取所有頁
        show_metadata: 是否顯示PDF元資料
    """
    try:
        # 檢查檔案是否存在
        path = Path(pdf_path)
        if not path.exists():
            print(f"錯誤: 檔案不存在 '{pdf_path}'")
            return False

        if not path.suffix.lower() == '.pdf':
            print(f"警告: 檔案可能不是PDF格式 '{pdf_path}'")

        # 開啟PDF檔案
        reader = PdfReader(pdf_path)

        # 顯示基本資訊
        num_pages = len(reader.pages)
        print(f"\n{'='*60}")
        print(f"PDF檔案: {path.name}")
        print(f"總頁數: {num_pages}")
        print(f"{'='*60}\n")

        # 顯示元資料
        if show_metadata and reader.metadata:
            print("PDF元資料:")
            print("-" * 60)
            for key, value in reader.metadata.items():
                print(f"{key}: {value}")
            print("-" * 60 + "\n")

        # 提取文本內容
        if page_num is not None:
            # 讀取指定頁
            if page_num < 1 or page_num > num_pages:
                print(f"錯誤: 頁碼超出範圍 (1-{num_pages})")
                return False

            page = reader.pages[page_num - 1]
            text = page.extract_text()
            print(f"第 {page_num} 頁內容:")
            print("=" * 60)
            print(text)
            print("=" * 60)
        else:
            # 讀取所有頁
            for i, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                print(f"\n第 {i} 頁:")
                print("-" * 60)
                print(text)
                print("-" * 60)

        return True

    except Exception as e:
        print(f"讀取PDF時出錯: {e}")
        return False


def search_pdf(pdf_path, search_term, case_sensitive=False, context_chars=50):
    """
    在PDF檔案中搜尋指定內容

    Args:
        pdf_path: PDF檔案路徑
        search_term: 要搜尋的文本
        case_sensitive: 是否區分大小寫
        context_chars: 顯示上下文的字元數
    """
    try:
        # 檢查檔案是否存在
        path = Path(pdf_path)
        if not path.exists():
            print(f"錯誤: 檔案不存在 '{pdf_path}'")
            return False

        if not path.suffix.lower() == '.pdf':
            print(f"警告: 檔案可能不是PDF格式 '{pdf_path}'")

        # 開啟PDF檔案
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)

        # 顯示搜尋資訊
        print(f"\n{'='*60}")
        print(f"PDF檔案: {path.name}")
        print(f"搜尋內容: '{search_term}'")
        print(f"區分大小寫: {'是' if case_sensitive else '否'}")
        print(f"{'='*60}\n")

        # 搜尋結果統計
        total_matches = 0
        found_pages = []

        # 遍歷每一頁進行搜尋
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()

            # 將文本按行分割
            lines = text.split('\n')

            # 儲存當前頁的匹配結果
            page_matches = []

            # 在每一行中搜尋
            for line_num, line in enumerate(lines, 1):
                # 根據是否區分大小寫進行搜尋
                if case_sensitive:
                    matches = list(re.finditer(re.escape(search_term), line))
                else:
                    matches = list(re.finditer(re.escape(search_term), line, re.IGNORECASE))

                # 如果在這一行找到匹配
                for match in matches:
                    start = match.start()
                    end = match.end()

                    # 獲取上下文
                    context_start = max(0, start - context_chars)
                    context_end = min(len(line), end + context_chars)

                    # 提取上下文文本
                    before = line[context_start:start]
                    matched = line[start:end]
                    after = line[end:context_end]

                    # 儲存匹配資訊
                    page_matches.append({
                        'line_num': line_num,
                        'before': before.strip(),
                        'matched': matched,
                        'after': after.strip()
                    })

            # 如果當前頁有匹配項
            if page_matches:
                found_pages.append(page_num + 1)
                match_count = len(page_matches)
                total_matches += match_count

                print(f"第 {page_num + 1} 頁 - 找到 {match_count} 處匹配:")
                print("-" * 60)

                # 顯示每個匹配的詳細資訊
                for idx, match_info in enumerate(page_matches, 1):
                    line_num = match_info['line_num']
                    before = match_info['before']
                    matched = match_info['matched']
                    after = match_info['after']

                    # 顯示結果（包含行號）
                    print(f"  [{idx}] 第 {line_num} 行: ...{before}【{matched}】{after}...")

                print()

        # 顯示總結
        print("=" * 60)
        if total_matches > 0:
            print(f"搜尋完成！")
            print(f"共在 {len(found_pages)} 頁中找到 {total_matches} 處匹配")
            print(f"頁碼: {', '.join(map(str, found_pages))}")
        else:
            print(f"未找到匹配內容")
        print("=" * 60)

        return total_matches > 0

    except Exception as e:
        print(f"搜尋PDF時出錯: {e}")
        return False


def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description='PDF閱讀器 - 提取和顯示PDF檔案內容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s document.pdf              # 讀取整個PDF檔案
  %(prog)s document.pdf -p 1         # 只讀取第1頁
  %(prog)s document.pdf -m           # 顯示PDF元資料
  %(prog)s document.pdf -p 3 -m      # 讀取第3頁並顯示元資料
  %(prog)s document.pdf -s "關鍵詞"  # 搜尋PDF中的關鍵詞
  %(prog)s document.pdf -s "word" -c # 區分大小寫搜尋
        """
    )

    parser.add_argument(
        'pdf_file',
        help='PDF檔案路徑'
    )

    parser.add_argument(
        '-p', '--page',
        type=int,
        metavar='NUM',
        help='指定要讀取的頁碼（從1開始）'
    )

    parser.add_argument(
        '-m', '--metadata',
        action='store_true',
        help='顯示PDF元資料資訊'
    )

    parser.add_argument(
        '-s', '--search',
        type=str,
        metavar='TEXT',
        help='在PDF中搜尋指定文本內容'
    )

    parser.add_argument(
        '-c', '--case-sensitive',
        action='store_true',
        help='搜尋時區分大小寫（預設不區分）'
    )

    parser.add_argument(
        '--context',
        type=int,
        default=50,
        metavar='CHARS',
        help='搜尋結果顯示的上下文字元數（預設50）'
    )

    args = parser.parse_args()

    # 如果是搜尋模式
    if args.search:
        success = search_pdf(args.pdf_file, args.search, args.case_sensitive, args.context)
    else:
        # 讀取PDF
        success = read_pdf(args.pdf_file, args.page, args.metadata)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
