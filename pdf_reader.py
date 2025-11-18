#!/usr/bin/env python3
"""
PDF Reader - 一個簡單的PDF檔案閱讀工具
支持提取PDF文本內容、頁數統計和基本資訊

此模組提供以下功能：
- 讀取PDF檔案的全部或指定頁面內容
- 顯示PDF元資料資訊
- 在PDF中搜尋關鍵詞並顯示匹配位置
- 批次搜尋資料夾中的所有PDF檔案
"""

import sys
import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    from pypdf import PdfReader
except ImportError:
    print("錯誤: 請先安裝 pypdf 函式庫")
    print("執行: pip install -r requirements.txt")
    sys.exit(1)


# =============================================================================
# 常量定義
# =============================================================================

SEPARATOR_WIDTH = 60
SEPARATOR_WIDTH_WIDE = 70
SEPARATOR_DOUBLE = "=" * SEPARATOR_WIDTH
SEPARATOR_SINGLE = "-" * SEPARATOR_WIDTH
SEPARATOR_DOUBLE_WIDE = "=" * SEPARATOR_WIDTH_WIDE
SEPARATOR_SINGLE_WIDE = "-" * SEPARATOR_WIDTH_WIDE

DEFAULT_CONTEXT_CHARS = 50


# =============================================================================
# 資料類別
# =============================================================================

@dataclass
class MatchInfo:
    """儲存單個搜尋匹配的資訊"""
    line_num: int
    before_context: str
    matched_text: str
    after_context: str


@dataclass
class PageMatchResult:
    """儲存單頁的所有匹配結果"""
    page_num: int
    matches: list[MatchInfo] = field(default_factory=list)


@dataclass
class FileMatchResult:
    """儲存單個檔案的所有匹配結果"""
    file_name: str
    file_path: Path
    relative_path: str
    matches: list[MatchInfo] = field(default_factory=list)
    pages_with_matches: list[int] = field(default_factory=list)


# =============================================================================
# 自訂例外
# =============================================================================

class PDFReaderError(Exception):
    """PDF Reader 基礎例外類別"""
    pass


class FileNotFoundError(PDFReaderError):
    """檔案不存在例外"""
    pass


class DirectoryNotFoundError(PDFReaderError):
    """資料夾不存在例外"""
    pass


class InvalidPageNumberError(PDFReaderError):
    """無效頁碼例外"""
    pass


class NoPDFFilesError(PDFReaderError):
    """資料夾中沒有PDF檔案例外"""
    pass


# =============================================================================
# 輔助函式
# =============================================================================

def validate_pdf_path(pdf_path: str) -> Path:
    """
    驗證PDF檔案路徑的有效性

    Args:
        pdf_path: PDF檔案路徑字串

    Returns:
        驗證後的Path物件

    Raises:
        FileNotFoundError: 當檔案不存在時
    """
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"檔案不存在: '{pdf_path}'")

    if path.suffix.lower() != '.pdf':
        print(f"警告: 檔案可能不是PDF格式 '{pdf_path}'")

    return path


def validate_directory_path(dir_path: str) -> Path:
    """
    驗證資料夾路徑的有效性

    Args:
        dir_path: 資料夾路徑字串

    Returns:
        驗證後的Path物件

    Raises:
        DirectoryNotFoundError: 當資料夾不存在時
    """
    path = Path(dir_path)

    if not path.exists():
        raise DirectoryNotFoundError(f"資料夾不存在: '{dir_path}'")

    if not path.is_dir():
        raise DirectoryNotFoundError(f"'{dir_path}' 不是一個資料夾")

    return path


def print_header(title: str, subtitle: Optional[str] = None, wide: bool = False) -> None:
    """
    列印格式化的標題頭部

    Args:
        title: 主標題
        subtitle: 可選的副標題
        wide: 是否使用寬分隔線
    """
    separator = SEPARATOR_DOUBLE_WIDE if wide else SEPARATOR_DOUBLE
    print(f"\n{separator}")
    print(title)
    if subtitle:
        print(subtitle)
    print(f"{separator}\n")


def print_metadata(metadata: dict) -> None:
    """
    列印PDF元資料資訊

    Args:
        metadata: PDF元資料字典
    """
    print("PDF元資料:")
    print(SEPARATOR_SINGLE)
    for key, value in metadata.items():
        print(f"{key}: {value}")
    print(SEPARATOR_SINGLE + "\n")


def extract_page_text(reader: PdfReader, page_index: int) -> str:
    """
    提取指定頁面的文本內容

    Args:
        reader: PdfReader實例
        page_index: 頁面索引（從0開始）

    Returns:
        提取的文本內容
    """
    return reader.pages[page_index].extract_text()


def find_matches_in_line(
    line: str,
    search_term: str,
    case_sensitive: bool,
    context_chars: int,
    line_num: int
) -> list[MatchInfo]:
    """
    在單行文本中查找所有匹配項

    Args:
        line: 要搜尋的文本行
        search_term: 搜尋關鍵詞
        case_sensitive: 是否區分大小寫
        context_chars: 上下文字元數
        line_num: 行號

    Returns:
        該行中所有匹配的MatchInfo列表
    """
    matches = []
    flags = 0 if case_sensitive else re.IGNORECASE

    for match in re.finditer(re.escape(search_term), line, flags):
        start, end = match.start(), match.end()

        # 計算上下文範圍
        context_start = max(0, start - context_chars)
        context_end = min(len(line), end + context_chars)

        matches.append(MatchInfo(
            line_num=line_num,
            before_context=line[context_start:start].strip(),
            matched_text=line[start:end],
            after_context=line[end:context_end].strip()
        ))

    return matches


def search_in_page(
    reader: PdfReader,
    page_index: int,
    search_term: str,
    case_sensitive: bool,
    context_chars: int
) -> Optional[PageMatchResult]:
    """
    在指定頁面中搜尋關鍵詞

    Args:
        reader: PdfReader實例
        page_index: 頁面索引（從0開始）
        search_term: 搜尋關鍵詞
        case_sensitive: 是否區分大小寫
        context_chars: 上下文字元數

    Returns:
        PageMatchResult物件，如果無匹配則返回None
    """
    text = extract_page_text(reader, page_index)
    lines = text.split('\n')
    page_matches = []

    for line_num, line in enumerate(lines, start=1):
        line_matches = find_matches_in_line(
            line, search_term, case_sensitive, context_chars, line_num
        )
        page_matches.extend(line_matches)

    if page_matches:
        return PageMatchResult(
            page_num=page_index + 1,
            matches=page_matches
        )

    return None


def print_page_matches(result: PageMatchResult) -> None:
    """
    列印單頁的搜尋結果

    Args:
        result: PageMatchResult物件
    """
    match_count = len(result.matches)
    print(f"第 {result.page_num} 頁 - 找到 {match_count} 處匹配:")
    print(SEPARATOR_SINGLE)

    for idx, match in enumerate(result.matches, start=1):
        print(
            f"  [{idx}] 第 {match.line_num} 行: "
            f"...{match.before_context}【{match.matched_text}】{match.after_context}..."
        )

    print()


def print_search_summary(total_matches: int, found_pages: list[int]) -> None:
    """
    列印搜尋結果總結

    Args:
        total_matches: 總匹配數
        found_pages: 包含匹配的頁碼列表
    """
    print(SEPARATOR_DOUBLE)

    if total_matches > 0:
        print("搜尋完成！")
        print(f"共在 {len(found_pages)} 頁中找到 {total_matches} 處匹配")
        print(f"頁碼: {', '.join(map(str, found_pages))}")
    else:
        print("未找到匹配內容")

    print(SEPARATOR_DOUBLE)


def print_batch_search_summary(
    total_files: int,
    files_with_matches: int,
    total_matches: int,
    results: list[FileMatchResult]
) -> None:
    """
    列印批次搜尋結果總結

    Args:
        total_files: 搜尋檔案總數
        files_with_matches: 包含匹配的檔案數
        total_matches: 總匹配數
        results: 檔案匹配結果列表
    """
    print(f"\n{SEPARATOR_DOUBLE_WIDE}")
    print("搜尋完成！")
    print(SEPARATOR_DOUBLE_WIDE)

    if files_with_matches > 0:
        print("📊 總體統計:")
        print(f"   - 搜尋檔案總數: {total_files}")
        print(f"   - 包含匹配的檔案: {files_with_matches}")
        print(f"   - 總匹配次數: {total_matches}")
        print("\n📋 詳細結果:")
        for idx, result in enumerate(results, start=1):
            print(f"   {idx}. {result.file_name}: {len(result.matches)} 處匹配")
    else:
        print(f"在 {total_files} 個PDF檔案中未找到匹配內容")

    print(f"{SEPARATOR_DOUBLE_WIDE}\n")


# =============================================================================
# 主要功能函式
# =============================================================================

def read_pdf(
    pdf_path: str,
    page_num: Optional[int] = None,
    show_metadata: bool = False
) -> bool:
    """
    讀取PDF檔案並提取內容

    Args:
        pdf_path: PDF檔案路徑
        page_num: 指定要讀取的頁碼（從1開始），None表示讀取所有頁
        show_metadata: 是否顯示PDF元資料

    Returns:
        操作是否成功
    """
    try:
        path = validate_pdf_path(pdf_path)
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)

        # 顯示基本資訊
        print_header(
            f"PDF檔案: {path.name}",
            f"總頁數: {num_pages}"
        )

        # 顯示元資料
        if show_metadata and reader.metadata:
            print_metadata(dict(reader.metadata))

        # 提取文本內容
        if page_num is not None:
            # 驗證頁碼範圍
            if page_num < 1 or page_num > num_pages:
                raise InvalidPageNumberError(
                    f"頁碼超出範圍 (有效範圍: 1-{num_pages})"
                )

            # 讀取指定頁
            text = extract_page_text(reader, page_num - 1)
            print(f"第 {page_num} 頁內容:")
            print(SEPARATOR_DOUBLE)
            print(text)
            print(SEPARATOR_DOUBLE)
        else:
            # 讀取所有頁
            for i in range(num_pages):
                text = extract_page_text(reader, i)
                print(f"\n第 {i + 1} 頁:")
                print(SEPARATOR_SINGLE)
                print(text)
                print(SEPARATOR_SINGLE)

        return True

    except PDFReaderError as e:
        print(f"錯誤: {e}")
        return False
    except Exception as e:
        print(f"讀取PDF時出錯: {e}")
        return False


def search_pdf(
    pdf_path: str,
    search_term: str,
    case_sensitive: bool = False,
    context_chars: int = DEFAULT_CONTEXT_CHARS
) -> bool:
    """
    在PDF檔案中搜尋指定內容

    Args:
        pdf_path: PDF檔案路徑
        search_term: 要搜尋的文本
        case_sensitive: 是否區分大小寫
        context_chars: 顯示上下文的字元數

    Returns:
        是否找到匹配內容
    """
    try:
        path = validate_pdf_path(pdf_path)
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)

        # 顯示搜尋資訊
        case_sensitive_text = '是' if case_sensitive else '否'
        print_header(
            f"PDF檔案: {path.name}",
            f"搜尋內容: '{search_term}'\n區分大小寫: {case_sensitive_text}"
        )

        # 執行搜尋
        total_matches = 0
        found_pages = []

        for page_index in range(num_pages):
            result = search_in_page(
                reader, page_index, search_term, case_sensitive, context_chars
            )

            if result:
                found_pages.append(result.page_num)
                total_matches += len(result.matches)
                print_page_matches(result)

        # 顯示總結
        print_search_summary(total_matches, found_pages)

        return total_matches > 0

    except PDFReaderError as e:
        print(f"錯誤: {e}")
        return False
    except Exception as e:
        print(f"搜尋PDF時出錯: {e}")
        return False


def search_pdf_directory(
    dir_path: str,
    search_term: str,
    case_sensitive: bool = False,
    context_chars: int = DEFAULT_CONTEXT_CHARS
) -> bool:
    """
    在指定資料夾中的所有PDF檔案中搜尋關鍵詞

    Args:
        dir_path: 資料夾路徑
        search_term: 要搜尋的文本
        case_sensitive: 是否區分大小寫
        context_chars: 顯示上下文的字元數

    Returns:
        是否找到匹配內容
    """
    try:
        path = validate_directory_path(dir_path)

        # 尋找所有PDF檔案
        pdf_files = sorted(path.glob('**/*.pdf'))

        if not pdf_files:
            raise NoPDFFilesError(f"在 '{dir_path}' 中沒有找到PDF檔案")

        # 顯示搜尋資訊
        case_sensitive_text = '是' if case_sensitive else '否'
        print_header(
            "批次搜尋模式",
            f"資料夾: {path.absolute()}\n"
            f"搜尋內容: '{search_term}'\n"
            f"區分大小寫: {case_sensitive_text}\n"
            f"找到 {len(pdf_files)} 個PDF檔案",
            wide=True
        )

        # 統計資訊
        total_matches = 0
        results: list[FileMatchResult] = []

        # 遍歷每個PDF檔案
        for pdf_file in pdf_files:
            file_result = _search_single_file_in_batch(
                pdf_file, path, search_term, case_sensitive, context_chars
            )

            if file_result and file_result.matches:
                results.append(file_result)
                total_matches += len(file_result.matches)

        # 顯示總結
        print_batch_search_summary(
            len(pdf_files),
            len(results),
            total_matches,
            results
        )

        return len(results) > 0

    except PDFReaderError as e:
        print(f"錯誤: {e}")
        return False
    except Exception as e:
        print(f"批次搜尋時出錯: {e}")
        return False


def _search_single_file_in_batch(
    pdf_file: Path,
    base_path: Path,
    search_term: str,
    case_sensitive: bool,
    context_chars: int
) -> Optional[FileMatchResult]:
    """
    批次搜尋中處理單個檔案

    Args:
        pdf_file: PDF檔案路徑
        base_path: 基礎資料夾路徑
        search_term: 搜尋關鍵詞
        case_sensitive: 是否區分大小寫
        context_chars: 上下文字元數

    Returns:
        FileMatchResult物件，如果處理失敗則返回None
    """
    try:
        reader = PdfReader(pdf_file)
        num_pages = len(reader.pages)

        file_result = FileMatchResult(
            file_name=pdf_file.name,
            file_path=pdf_file,
            relative_path=str(pdf_file.relative_to(base_path))
        )

        # 遍歷每一頁
        for page_num in range(num_pages):
            page_result = search_in_page(
                reader, page_num, search_term, case_sensitive, context_chars
            )

            if page_result:
                if page_result.page_num not in file_result.pages_with_matches:
                    file_result.pages_with_matches.append(page_result.page_num)
                file_result.matches.extend(page_result.matches)

        # 如果該檔案有匹配，列印結果
        if file_result.matches:
            _print_file_matches(file_result)

        return file_result

    except Exception as e:
        print(f"⚠️  處理檔案 {pdf_file.name} 時出錯: {e}")
        return None


def _print_file_matches(result: FileMatchResult) -> None:
    """
    列印單個檔案的批次搜尋結果

    Args:
        result: FileMatchResult物件
    """
    print(f"\n📄 檔案: {result.file_name}")
    print(f"   路徑: {result.relative_path}")
    print(SEPARATOR_SINGLE_WIDE)

    # 按頁碼分組顯示
    current_page = 0
    for match in result.matches:
        print(
            f"   ✓ 第 {result.pages_with_matches[0] if len(result.pages_with_matches) == 1 else '?'} 頁, "
            f"第 {match.line_num} 行: "
            f"...{match.before_context}【{match.matched_text}】{match.after_context}..."
        )

    pages_str = ', '.join(map(str, result.pages_with_matches))
    print(f"   📊 小計: {len(result.matches)} 處匹配，分布在第 {pages_str} 頁")


# =============================================================================
# 命令列介面
# =============================================================================

def create_argument_parser() -> argparse.ArgumentParser:
    """
    建立並配置命令列參數解析器

    Returns:
        配置好的ArgumentParser實例
    """
    parser = argparse.ArgumentParser(
        description='PDF閱讀器 - 提取和顯示PDF檔案內容，支持單檔案和批次搜尋',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  單檔案模式:
    %(prog)s document.pdf              # 讀取整個PDF檔案
    %(prog)s document.pdf -p 1         # 只讀取第1頁
    %(prog)s document.pdf -m           # 顯示PDF元資料
    %(prog)s document.pdf -p 3 -m      # 讀取第3頁並顯示元資料
    %(prog)s document.pdf -s "關鍵詞"  # 搜尋PDF中的關鍵詞
    %(prog)s document.pdf -s "word" -c # 區分大小寫搜尋

  批次搜尋模式:
    %(prog)s -d ./pdfs -s "關鍵詞"     # 搜尋資料夾中所有PDF
    %(prog)s -d ./docs -s "API" -c     # 區分大小寫批次搜尋
        """
    )

    # 必需參數
    parser.add_argument(
        'pdf_file',
        nargs='?',
        help='PDF檔案路徑（單檔案模式）'
    )

    # 批次搜尋參數
    batch_group = parser.add_argument_group('批次搜尋模式')
    batch_group.add_argument(
        '-d', '--directory',
        type=str,
        metavar='DIR',
        help='批次搜尋：指定包含PDF檔案的資料夾路徑'
    )

    # 閱讀模式參數
    read_group = parser.add_argument_group('閱讀模式')
    read_group.add_argument(
        '-p', '--page',
        type=int,
        metavar='NUM',
        help='指定要讀取的頁碼（從1開始）'
    )
    read_group.add_argument(
        '-m', '--metadata',
        action='store_true',
        help='顯示PDF元資料資訊'
    )

    # 搜尋模式參數
    search_group = parser.add_argument_group('搜尋模式')
    search_group.add_argument(
        '-s', '--search',
        type=str,
        metavar='TEXT',
        help='在PDF中搜尋指定文本內容'
    )
    search_group.add_argument(
        '-c', '--case-sensitive',
        action='store_true',
        help='搜尋時區分大小寫（預設不區分）'
    )
    search_group.add_argument(
        '--context',
        type=int,
        default=DEFAULT_CONTEXT_CHARS,
        metavar='CHARS',
        help=f'搜尋結果顯示的上下文字元數（預設{DEFAULT_CONTEXT_CHARS}）'
    )

    return parser


def validate_arguments(args: argparse.Namespace) -> None:
    """
    驗證命令列參數的有效性

    Args:
        args: 解析後的命令列參數

    Raises:
        SystemExit: 當參數無效時
    """
    if args.directory and args.pdf_file:
        print("錯誤: 不能同時指定檔案和資料夾")
        print("使用 -h 查看幫助資訊")
        sys.exit(1)

    if not args.directory and not args.pdf_file:
        print("錯誤: 必須指定PDF檔案或資料夾")
        print("使用 -h 查看幫助資訊")
        sys.exit(1)

    if args.directory and not args.search:
        print("錯誤: 批次搜尋模式必須使用 -s/--search 參數指定搜尋內容")
        sys.exit(1)


def main() -> None:
    """程式主入口函式"""
    parser = create_argument_parser()
    args = parser.parse_args()

    # 驗證參數
    validate_arguments(args)

    # 根據模式執行相應功能
    if args.directory:
        # 批次搜尋模式
        success = search_pdf_directory(
            args.directory,
            args.search,
            args.case_sensitive,
            args.context
        )
    elif args.search:
        # 單檔案搜尋模式
        success = search_pdf(
            args.pdf_file,
            args.search,
            args.case_sensitive,
            args.context
        )
    else:
        # 讀取PDF模式
        success = read_pdf(
            args.pdf_file,
            args.page,
            args.metadata
        )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
