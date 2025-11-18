#!/usr/bin/env python3
"""
PDF Reader - 一个简单的PDF文件阅读工具
支持提取PDF文本内容、页数统计和基本信息

此模块提供以下功能：
- 读取PDF文件的全部或指定页面内容
- 显示PDF元数据信息
- 在PDF中搜索关键词并显示匹配位置
"""

import sys
import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    from pypdf import PdfReader
except ImportError:
    print("错误: 请先安装 pypdf 库")
    print("运行: pip install -r requirements.txt")
    sys.exit(1)


# =============================================================================
# 常量定义
# =============================================================================

SEPARATOR_WIDTH = 60
SEPARATOR_DOUBLE = "=" * SEPARATOR_WIDTH
SEPARATOR_SINGLE = "-" * SEPARATOR_WIDTH

DEFAULT_CONTEXT_CHARS = 50


# =============================================================================
# 数据类
# =============================================================================

@dataclass
class MatchInfo:
    """存储单个搜索匹配的信息"""
    line_num: int
    before_context: str
    matched_text: str
    after_context: str


@dataclass
class PageMatchResult:
    """存储单页的所有匹配结果"""
    page_num: int
    matches: list[MatchInfo]


# =============================================================================
# 自定义异常
# =============================================================================

class PDFReaderError(Exception):
    """PDF Reader 基础异常类"""
    pass


class FileNotFoundError(PDFReaderError):
    """文件不存在异常"""
    pass


class InvalidPageNumberError(PDFReaderError):
    """无效页码异常"""
    pass


# =============================================================================
# 辅助函数
# =============================================================================

def validate_pdf_path(pdf_path: str) -> Path:
    """
    验证PDF文件路径的有效性

    Args:
        pdf_path: PDF文件路径字符串

    Returns:
        验证后的Path对象

    Raises:
        FileNotFoundError: 当文件不存在时
    """
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在: '{pdf_path}'")

    if path.suffix.lower() != '.pdf':
        print(f"警告: 文件可能不是PDF格式 '{pdf_path}'")

    return path


def print_header(title: str, subtitle: Optional[str] = None) -> None:
    """
    打印格式化的标题头部

    Args:
        title: 主标题
        subtitle: 可选的副标题
    """
    print(f"\n{SEPARATOR_DOUBLE}")
    print(title)
    if subtitle:
        print(subtitle)
    print(f"{SEPARATOR_DOUBLE}\n")


def print_section(title: str) -> None:
    """打印带分隔线的区块标题"""
    print(f"{title}")
    print(SEPARATOR_SINGLE)


def print_metadata(metadata: dict) -> None:
    """
    打印PDF元数据信息

    Args:
        metadata: PDF元数据字典
    """
    print("PDF元数据:")
    print(SEPARATOR_SINGLE)
    for key, value in metadata.items():
        print(f"{key}: {value}")
    print(SEPARATOR_SINGLE + "\n")


def extract_page_text(reader: PdfReader, page_index: int) -> str:
    """
    提取指定页面的文本内容

    Args:
        reader: PdfReader实例
        page_index: 页面索引（从0开始）

    Returns:
        提取的文本内容
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
    在单行文本中查找所有匹配项

    Args:
        line: 要搜索的文本行
        search_term: 搜索关键词
        case_sensitive: 是否区分大小写
        context_chars: 上下文字符数
        line_num: 行号

    Returns:
        该行中所有匹配的MatchInfo列表
    """
    matches = []
    flags = 0 if case_sensitive else re.IGNORECASE

    for match in re.finditer(re.escape(search_term), line, flags):
        start, end = match.start(), match.end()

        # 计算上下文范围
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
    在指定页面中搜索关键词

    Args:
        reader: PdfReader实例
        page_index: 页面索引（从0开始）
        search_term: 搜索关键词
        case_sensitive: 是否区分大小写
        context_chars: 上下文字符数

    Returns:
        PageMatchResult对象，如果无匹配则返回None
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
    打印单页的搜索结果

    Args:
        result: PageMatchResult对象
    """
    match_count = len(result.matches)
    print(f"第 {result.page_num} 页 - 找到 {match_count} 处匹配:")
    print(SEPARATOR_SINGLE)

    for idx, match in enumerate(result.matches, start=1):
        print(
            f"  [{idx}] 第 {match.line_num} 行: "
            f"...{match.before_context}【{match.matched_text}】{match.after_context}..."
        )

    print()


def print_search_summary(total_matches: int, found_pages: list[int]) -> None:
    """
    打印搜索结果总结

    Args:
        total_matches: 总匹配数
        found_pages: 包含匹配的页码列表
    """
    print(SEPARATOR_DOUBLE)

    if total_matches > 0:
        print("搜索完成！")
        print(f"共在 {len(found_pages)} 页中找到 {total_matches} 处匹配")
        print(f"页码: {', '.join(map(str, found_pages))}")
    else:
        print("未找到匹配内容")

    print(SEPARATOR_DOUBLE)


# =============================================================================
# 主要功能函数
# =============================================================================

def read_pdf(
    pdf_path: str,
    page_num: Optional[int] = None,
    show_metadata: bool = False
) -> bool:
    """
    读取PDF文件并提取内容

    Args:
        pdf_path: PDF文件路径
        page_num: 指定要读取的页码（从1开始），None表示读取所有页
        show_metadata: 是否显示PDF元数据

    Returns:
        操作是否成功
    """
    try:
        path = validate_pdf_path(pdf_path)
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)

        # 显示基本信息
        print_header(
            f"PDF文件: {path.name}",
            f"总页数: {num_pages}"
        )

        # 显示元数据
        if show_metadata and reader.metadata:
            print_metadata(dict(reader.metadata))

        # 提取文本内容
        if page_num is not None:
            # 验证页码范围
            if page_num < 1 or page_num > num_pages:
                raise InvalidPageNumberError(
                    f"页码超出范围 (有效范围: 1-{num_pages})"
                )

            # 读取指定页
            text = extract_page_text(reader, page_num - 1)
            print(f"第 {page_num} 页内容:")
            print(SEPARATOR_DOUBLE)
            print(text)
            print(SEPARATOR_DOUBLE)
        else:
            # 读取所有页
            for i in range(num_pages):
                text = extract_page_text(reader, i)
                print(f"\n第 {i + 1} 页:")
                print(SEPARATOR_SINGLE)
                print(text)
                print(SEPARATOR_SINGLE)

        return True

    except PDFReaderError as e:
        print(f"错误: {e}")
        return False
    except Exception as e:
        print(f"读取PDF时出错: {e}")
        return False


def search_pdf(
    pdf_path: str,
    search_term: str,
    case_sensitive: bool = False,
    context_chars: int = DEFAULT_CONTEXT_CHARS
) -> bool:
    """
    在PDF文件中搜索指定内容

    Args:
        pdf_path: PDF文件路径
        search_term: 要搜索的文本
        case_sensitive: 是否区分大小写
        context_chars: 显示上下文的字符数

    Returns:
        是否找到匹配内容
    """
    try:
        path = validate_pdf_path(pdf_path)
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)

        # 显示搜索信息
        case_sensitive_text = '是' if case_sensitive else '否'
        print_header(
            f"PDF文件: {path.name}",
            f"搜索内容: '{search_term}'\n区分大小写: {case_sensitive_text}"
        )

        # 执行搜索
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

        # 显示总结
        print_search_summary(total_matches, found_pages)

        return total_matches > 0

    except PDFReaderError as e:
        print(f"错误: {e}")
        return False
    except Exception as e:
        print(f"搜索PDF时出错: {e}")
        return False


# =============================================================================
# 命令行接口
# =============================================================================

def create_argument_parser() -> argparse.ArgumentParser:
    """
    创建并配置命令行参数解析器

    Returns:
        配置好的ArgumentParser实例
    """
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

    # 必需参数
    parser.add_argument(
        'pdf_file',
        help='PDF文件路径'
    )

    # 阅读模式参数
    read_group = parser.add_argument_group('阅读模式')
    read_group.add_argument(
        '-p', '--page',
        type=int,
        metavar='NUM',
        help='指定要读取的页码（从1开始）'
    )
    read_group.add_argument(
        '-m', '--metadata',
        action='store_true',
        help='显示PDF元数据信息'
    )

    # 搜索模式参数
    search_group = parser.add_argument_group('搜索模式')
    search_group.add_argument(
        '-s', '--search',
        type=str,
        metavar='TEXT',
        help='在PDF中搜索指定文本内容'
    )
    search_group.add_argument(
        '-c', '--case-sensitive',
        action='store_true',
        help='搜索时区分大小写（默认不区分）'
    )
    search_group.add_argument(
        '--context',
        type=int,
        default=DEFAULT_CONTEXT_CHARS,
        metavar='CHARS',
        help=f'搜索结果显示的上下文字符数（默认{DEFAULT_CONTEXT_CHARS}）'
    )

    return parser


def main() -> None:
    """程序主入口函数"""
    parser = create_argument_parser()
    args = parser.parse_args()

    # 根据模式执行相应功能
    if args.search:
        success = search_pdf(
            args.pdf_file,
            args.search,
            args.case_sensitive,
            args.context
        )
    else:
        success = read_pdf(
            args.pdf_file,
            args.page,
            args.metadata
        )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
