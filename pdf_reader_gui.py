#!/usr/bin/env python3
"""
PDF Reader GUI - 基於 Tkinter 的 PDF 閱讀器圖形介面
支持搜尋、文本顯示和導航功能

此模組提供以下功能：
- 圖形化介面讀取和顯示PDF內容
- 在PDF中搜尋關鍵詞並高亮顯示
- 批次搜尋資料夾中的所有PDF檔案
- 雙擊搜尋結果跳轉到對應位置
"""

import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    from pypdf import PdfReader
except ImportError:
    print("錯誤: 請先安裝 pypdf 函式庫")
    print("執行: pip install pypdf")
    sys.exit(1)


# =============================================================================
# 常量定義
# =============================================================================

# 視窗設定
WINDOW_TITLE = "PDF 閱讀器"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

# 字型設定
TEXT_FONT = ('Microsoft YaHei', 10)

# 搜尋設定
DEFAULT_CONTEXT_CHARS = 30
PAGE_SEPARATOR_LINES = 4

# 顏色設定
HIGHLIGHT_BG = 'yellow'
HIGHLIGHT_FG = 'black'
CURRENT_HIGHLIGHT_BG = 'orange'
CURRENT_HIGHLIGHT_FG = 'black'

# 標籤名稱
TAG_HIGHLIGHT = 'highlight'
TAG_CURRENT_HIGHLIGHT = 'current_highlight'
TAG_PAGE_HEADER = 'page_header'


# =============================================================================
# 資料類別
# =============================================================================

@dataclass
class SearchResult:
    """儲存單個搜尋結果的資訊"""
    file_name: str
    file_path: Optional[Path]
    page_num: int
    line_num: int
    preview: str
    matched_text: str
    full_line: str


# =============================================================================
# 主要類別
# =============================================================================

class PDFReaderGUI:
    """PDF閱讀器圖形介面主類別"""

    def __init__(self, root: tk.Tk) -> None:
        """
        初始化PDF閱讀器GUI

        Args:
            root: Tkinter根視窗
        """
        self.root = root
        self._configure_window()
        self._initialize_state()
        self._create_widgets()

    def _configure_window(self) -> None:
        """配置主視窗"""
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    def _initialize_state(self) -> None:
        """初始化應用程式狀態"""
        # PDF 資料
        self.pdf_reader: Optional[PdfReader] = None
        self.pdf_path: Optional[Path] = None
        self.all_pages_text: list[str] = []

        # 搜尋狀態
        self.search_results: list[SearchResult] = []

        # 批次模式
        self.batch_mode: bool = False
        self.pdf_directory: Optional[Path] = None
        self.pdf_files: list[Path] = []

    def _create_widgets(self) -> None:
        """建立所有介面組件"""
        # 主容器 - 使用 PanedWindow 實現可調整大小的分欄
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 建立左右面板
        left_frame = self._create_left_panel(main_paned)
        right_frame = self._create_right_panel(main_paned)

        main_paned.add(left_frame, weight=1)
        main_paned.add(right_frame, weight=2)

    def _create_left_panel(self, parent: ttk.PanedWindow) -> ttk.Frame:
        """
        建立左側控制面板

        Args:
            parent: 父容器

        Returns:
            左側框架
        """
        left_frame = ttk.Frame(parent, width=400)

        # 檔案操作區域
        self._create_file_section(left_frame)

        # 搜尋區域
        self._create_search_section(left_frame)

        return left_frame

    def _create_file_section(self, parent: ttk.Frame) -> None:
        """
        建立檔案操作區域

        Args:
            parent: 父框架
        """
        file_frame = ttk.LabelFrame(parent, text="檔案操作", padding=10)
        file_frame.pack(fill=tk.X, padx=5, pady=5)

        # 按鈕容器
        button_frame = ttk.Frame(file_frame)
        button_frame.pack(fill=tk.X, pady=(0, 5))

        # 開啟檔案按鈕
        ttk.Button(
            button_frame,
            text="開啟 PDF 檔案",
            command=self.open_file
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        # 開啟資料夾按鈕
        ttk.Button(
            button_frame,
            text="開啟資料夾",
            command=self.open_directory
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        # 檔案資訊標籤
        self.file_label = ttk.Label(
            file_frame,
            text="未開啟檔案",
            foreground="gray"
        )
        self.file_label.pack(fill=tk.X, pady=(5, 0))

        self.info_label = ttk.Label(file_frame, text="", foreground="blue")
        self.info_label.pack(fill=tk.X)

    def _create_search_section(self, parent: ttk.Frame) -> None:
        """
        建立搜尋功能區域

        Args:
            parent: 父框架
        """
        search_frame = ttk.LabelFrame(parent, text="搜尋功能", padding=10)
        search_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 搜尋輸入框
        ttk.Label(search_frame, text="搜尋內容:").pack(anchor=tk.W)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(fill=tk.X, pady=(0, 5))
        self.search_entry.bind('<Return>', lambda e: self.search_pdf())

        # 搜尋選項
        options_frame = ttk.Frame(search_frame)
        options_frame.pack(fill=tk.X, pady=(0, 5))

        self.case_sensitive_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_frame,
            text="區分大小寫",
            variable=self.case_sensitive_var
        ).pack(side=tk.LEFT)

        # 搜尋按鈕
        ttk.Button(
            search_frame,
            text="開始搜尋",
            command=self.search_pdf
        ).pack(fill=tk.X)

        # 搜尋結果統計
        self.result_count_label = ttk.Label(
            search_frame,
            text="搜尋結果: 0",
            foreground="green"
        )
        self.result_count_label.pack(fill=tk.X, pady=(5, 0))

        # 搜尋結果列表
        self._create_result_tree(search_frame)

    def _create_result_tree(self, parent: ttk.LabelFrame) -> None:
        """
        建立搜尋結果樹狀列表

        Args:
            parent: 父框架
        """
        ttk.Label(parent, text="搜尋結果列表:").pack(anchor=tk.W, pady=(10, 0))

        result_frame = ttk.Frame(parent)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # 滾動條
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 結果列表
        self.result_tree = ttk.Treeview(
            result_frame,
            columns=('file', 'page', 'line', 'content'),
            show='headings',
            yscrollcommand=scrollbar.set,
            height=10
        )
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_tree.yview)

        # 設定欄位
        self._configure_result_tree_columns()

        # 綁定雙擊事件
        self.result_tree.bind('<Double-1>', self.on_result_click)

    def _configure_result_tree_columns(self) -> None:
        """配置結果樹狀列表的欄位"""
        columns = [
            ('file', '檔案', 100, tk.W),
            ('page', '頁碼', 50, tk.CENTER),
            ('line', '行號', 50, tk.CENTER),
            ('content', '內容預覽', 200, tk.W)
        ]

        for col_id, heading, width, anchor in columns:
            self.result_tree.heading(col_id, text=heading)
            self.result_tree.column(col_id, width=width, anchor=anchor)

    def _create_right_panel(self, parent: ttk.PanedWindow) -> ttk.Frame:
        """
        建立右側內容面板

        Args:
            parent: 父容器

        Returns:
            右側框架
        """
        right_frame = ttk.Frame(parent)

        # 內容顯示區域
        content_frame = ttk.LabelFrame(right_frame, text="PDF 內容", padding=5)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 文本顯示區域
        self.text_display = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            font=TEXT_FONT,
            state=tk.DISABLED
        )
        self.text_display.pack(fill=tk.BOTH, expand=True)

        # 配置文本標籤
        self._configure_text_tags()

        return right_frame

    def _configure_text_tags(self) -> None:
        """配置文本顯示區域的標籤樣式"""
        self.text_display.tag_config(
            TAG_HIGHLIGHT,
            background=HIGHLIGHT_BG,
            foreground=HIGHLIGHT_FG
        )
        self.text_display.tag_config(
            TAG_CURRENT_HIGHLIGHT,
            background=CURRENT_HIGHLIGHT_BG,
            foreground=CURRENT_HIGHLIGHT_FG
        )

    # =========================================================================
    # 檔案操作方法
    # =========================================================================

    def open_file(self) -> None:
        """開啟單個PDF檔案"""
        file_path = filedialog.askopenfilename(
            title="選擇 PDF 檔案",
            filetypes=[("PDF 檔案", "*.pdf"), ("所有檔案", "*.*")]
        )

        if not file_path:
            return

        try:
            self._load_pdf_file(file_path)
            self._switch_to_single_file_mode()
            self._display_all_pages()
            self._clear_search_results()

            num_pages = len(self.pdf_reader.pages)
            messagebox.showinfo("成功", f"已成功開啟 PDF 檔案\n總頁數: {num_pages}")

        except Exception as e:
            messagebox.showerror("錯誤", f"開啟 PDF 檔案時出錯:\n{str(e)}")

    def _load_pdf_file(self, file_path: str) -> None:
        """
        載入PDF檔案

        Args:
            file_path: 檔案路徑
        """
        self.pdf_reader = PdfReader(file_path)
        self.pdf_path = Path(file_path)

        # 提取所有頁面文本
        self.all_pages_text = [
            page.extract_text() for page in self.pdf_reader.pages
        ]

        # 更新介面顯示
        num_pages = len(self.pdf_reader.pages)
        self.file_label.config(
            text=f"檔案: {self.pdf_path.name}",
            foreground="black"
        )
        self.info_label.config(text=f"總頁數: {num_pages}")

    def _switch_to_single_file_mode(self) -> None:
        """切換到單檔案模式"""
        self.batch_mode = False
        self.pdf_directory = None
        self.pdf_files = []

    def open_directory(self) -> None:
        """開啟資料夾進行批次搜尋"""
        dir_path = filedialog.askdirectory(
            title="選擇包含 PDF 檔案的資料夾"
        )

        if not dir_path:
            return

        try:
            self._load_directory(dir_path)

        except Exception as e:
            messagebox.showerror("錯誤", f"開啟資料夾時出錯:\n{str(e)}")

    def _load_directory(self, dir_path: str) -> None:
        """
        載入資料夾中的PDF檔案

        Args:
            dir_path: 資料夾路徑
        """
        path = Path(dir_path)
        pdf_files = sorted(path.glob('**/*.pdf'))

        if not pdf_files:
            messagebox.showwarning("警告", "在資料夾中沒有找到 PDF 檔案")
            return

        # 切換到批次模式
        self.batch_mode = True
        self.pdf_directory = path
        self.pdf_files = pdf_files

        # 更新介面顯示
        self.file_label.config(
            text=f"資料夾: {path.name}",
            foreground="black"
        )
        self.info_label.config(
            text=f"找到 {len(pdf_files)} 個 PDF 檔案"
        )

        # 顯示檔案列表
        self._display_directory_info()
        self._clear_search_results()

        messagebox.showinfo("成功", f"已開啟資料夾\n找到 {len(pdf_files)} 個 PDF 檔案")

    def _display_directory_info(self) -> None:
        """顯示資料夾資訊和檔案列表"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)

        info_lines = [
            "批次搜尋模式\n",
            f"資料夾: {self.pdf_directory}\n",
            f"PDF 檔案數: {len(self.pdf_files)}\n\n",
            "請輸入搜尋內容並點擊「開始搜尋」\n\n",
            "檔案列表:\n",
            "-" * 60 + "\n"
        ]

        for i, pdf_file in enumerate(self.pdf_files, 1):
            info_lines.append(
                f"{i}. {pdf_file.relative_to(self.pdf_directory)}\n"
            )

        self.text_display.insert(tk.END, "".join(info_lines))
        self.text_display.config(state=tk.DISABLED)

    # =========================================================================
    # 內容顯示方法
    # =========================================================================

    def _display_all_pages(self) -> None:
        """顯示所有頁面內容"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)

        for i, page_text in enumerate(self.all_pages_text, 1):
            separator = f"\n{'='*80}\n第 {i} 頁\n{'='*80}\n"
            self.text_display.insert(tk.END, separator, TAG_PAGE_HEADER)
            self.text_display.insert(tk.END, page_text + "\n")

        self.text_display.config(state=tk.DISABLED)
        self.text_display.see(1.0)

    # =========================================================================
    # 搜尋方法
    # =========================================================================

    def search_pdf(self) -> None:
        """執行PDF搜尋"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("警告", "請輸入搜尋內容")
            return

        if self.batch_mode:
            self._search_batch()
        else:
            self._search_single_file()

    def _search_single_file(self) -> None:
        """單檔案搜尋模式"""
        if not self.pdf_reader:
            messagebox.showwarning("警告", "請先開啟 PDF 檔案")
            return

        search_term = self.search_entry.get().strip()
        case_sensitive = self.case_sensitive_var.get()

        self._clear_search_results()

        # 搜尋所有頁面
        for page_num, page_text in enumerate(self.all_pages_text, 1):
            self._search_in_page_text(
                page_text,
                page_num,
                search_term,
                case_sensitive,
                self.pdf_path.name,
                None
            )

        # 顯示結果
        self._display_search_results()
        self._update_single_file_search_stats(search_term, case_sensitive)

    def _search_in_page_text(
        self,
        page_text: str,
        page_num: int,
        search_term: str,
        case_sensitive: bool,
        file_name: str,
        file_path: Optional[Path]
    ) -> int:
        """
        在頁面文本中搜尋

        Args:
            page_text: 頁面文本
            page_num: 頁碼
            search_term: 搜尋關鍵詞
            case_sensitive: 是否區分大小寫
            file_name: 檔案名稱
            file_path: 檔案路徑

        Returns:
            找到的匹配數量
        """
        lines = page_text.split('\n')
        match_count = 0
        flags = 0 if case_sensitive else re.IGNORECASE

        for line_num, line in enumerate(lines, 1):
            matches = list(re.finditer(re.escape(search_term), line, flags))

            for match in matches:
                result = self._create_search_result(
                    match, line, page_num, line_num, file_name, file_path
                )
                self.search_results.append(result)
                match_count += 1

        return match_count

    def _create_search_result(
        self,
        match: re.Match,
        line: str,
        page_num: int,
        line_num: int,
        file_name: str,
        file_path: Optional[Path]
    ) -> SearchResult:
        """
        建立搜尋結果物件

        Args:
            match: 正則匹配物件
            line: 完整行文本
            page_num: 頁碼
            line_num: 行號
            file_name: 檔案名稱
            file_path: 檔案路徑

        Returns:
            SearchResult物件
        """
        start, end = match.start(), match.end()

        # 計算上下文範圍
        context_start = max(0, start - DEFAULT_CONTEXT_CHARS)
        context_end = min(len(line), end + DEFAULT_CONTEXT_CHARS)

        before = line[context_start:start]
        matched = line[start:end]
        after = line[end:context_end]

        preview = f"...{before}【{matched}】{after}..."

        return SearchResult(
            file_name=file_name,
            file_path=file_path,
            page_num=page_num,
            line_num=line_num,
            preview=preview,
            matched_text=matched,
            full_line=line
        )

    def _update_single_file_search_stats(
        self,
        search_term: str,
        case_sensitive: bool
    ) -> None:
        """
        更新單檔案搜尋統計資訊

        Args:
            search_term: 搜尋關鍵詞
            case_sensitive: 是否區分大小寫
        """
        total_matches = len(self.search_results)

        if total_matches > 0:
            pages_with_matches = len(set(r.page_num for r in self.search_results))
            self.result_count_label.config(
                text=f"搜尋結果: {total_matches} 處匹配，共 {pages_with_matches} 頁。雙擊結果可跳轉！",
                foreground="green"
            )
            self._highlight_all_matches(search_term, case_sensitive)
        else:
            self.result_count_label.config(
                text="搜尋結果: 未找到匹配內容",
                foreground="red"
            )
            messagebox.showinfo("搜尋結果", "未找到匹配內容")

    def _search_batch(self) -> None:
        """批次搜尋模式"""
        if not self.pdf_files:
            messagebox.showwarning("警告", "請先開啟資料夾")
            return

        search_term = self.search_entry.get().strip()
        case_sensitive = self.case_sensitive_var.get()

        self._clear_search_results()
        self._show_batch_search_progress()

        # 統計資訊
        total_files_with_matches = 0

        # 遍歷每個PDF檔案
        for pdf_file in self.pdf_files:
            file_matches = self._search_in_pdf_file(
                pdf_file, search_term, case_sensitive
            )
            if file_matches > 0:
                total_files_with_matches += 1

        # 顯示結果
        self._display_search_results()
        self._display_batch_search_summary(
            search_term,
            case_sensitive,
            total_files_with_matches
        )

    def _show_batch_search_progress(self) -> None:
        """顯示批次搜尋進度"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(
            tk.END,
            f"正在搜尋 {len(self.pdf_files)} 個 PDF 檔案...\n\n"
        )
        self.text_display.config(state=tk.DISABLED)
        self.root.update()

    def _search_in_pdf_file(
        self,
        pdf_file: Path,
        search_term: str,
        case_sensitive: bool
    ) -> int:
        """
        在單個PDF檔案中搜尋

        Args:
            pdf_file: PDF檔案路徑
            search_term: 搜尋關鍵詞
            case_sensitive: 是否區分大小寫

        Returns:
            找到的匹配數量
        """
        try:
            reader = PdfReader(pdf_file)
            file_matches = 0

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()

                matches = self._search_in_page_text(
                    text,
                    page_num + 1,
                    search_term,
                    case_sensitive,
                    pdf_file.name,
                    pdf_file
                )
                file_matches += matches

            return file_matches

        except Exception as e:
            print(f"處理檔案 {pdf_file.name} 時出錯: {e}")
            return 0

    def _display_batch_search_summary(
        self,
        search_term: str,
        case_sensitive: bool,
        files_with_matches: int
    ) -> None:
        """
        顯示批次搜尋總結

        Args:
            search_term: 搜尋關鍵詞
            case_sensitive: 是否區分大小寫
            files_with_matches: 包含匹配的檔案數
        """
        total_matches = len(self.search_results)

        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)

        summary_lines = [
            "批次搜尋完成！\n\n",
            f"搜尋內容: '{search_term}'\n",
            f"區分大小寫: {'是' if case_sensitive else '否'}\n",
            f"{'-' * 60}\n\n",
            "📊 統計資訊:\n",
            f"  - 搜尋檔案總數: {len(self.pdf_files)}\n",
            f"  - 包含匹配的檔案: {files_with_matches}\n",
            f"  - 總匹配次數: {total_matches}\n\n"
        ]

        if total_matches > 0:
            summary_lines.append("請在左側查看詳細結果，雙擊可查看具體位置。\n")
        else:
            summary_lines.append("未找到匹配內容。\n")

        self.text_display.insert(tk.END, "".join(summary_lines))
        self.text_display.config(state=tk.DISABLED)

        # 更新統計標籤
        if total_matches > 0:
            self.result_count_label.config(
                text=f"搜尋結果: {total_matches} 處匹配，{files_with_matches} 個檔案",
                foreground="green"
            )
        else:
            self.result_count_label.config(
                text="搜尋結果: 未找到匹配內容",
                foreground="red"
            )
            messagebox.showinfo("搜尋結果", "未找到匹配內容")

    # =========================================================================
    # 結果顯示方法
    # =========================================================================

    def _display_search_results(self) -> None:
        """顯示搜尋結果到列表"""
        # 清空列表
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        # 新增結果
        for idx, result in enumerate(self.search_results):
            self.result_tree.insert(
                '',
                tk.END,
                iid=str(idx),
                values=(
                    result.file_name,
                    result.page_num,
                    result.line_num,
                    result.preview
                )
            )

    def _highlight_all_matches(
        self,
        search_term: str,
        case_sensitive: bool
    ) -> None:
        """
        高亮顯示所有匹配項

        Args:
            search_term: 搜尋關鍵詞
            case_sensitive: 是否區分大小寫
        """
        self.text_display.config(state=tk.NORMAL)
        self.text_display.tag_remove(TAG_HIGHLIGHT, 1.0, tk.END)

        start_pos = '1.0'
        while True:
            pos = self.text_display.search(
                search_term,
                start_pos,
                stopindex=tk.END,
                nocase=not case_sensitive
            )

            if not pos:
                break

            end_pos = f"{pos}+{len(search_term)}c"
            self.text_display.tag_add(TAG_HIGHLIGHT, pos, end_pos)
            start_pos = end_pos

        self.text_display.config(state=tk.DISABLED)

    def on_result_click(self, event: tk.Event) -> None:
        """
        處理搜尋結果點擊事件

        Args:
            event: 點擊事件
        """
        selection = self.result_tree.selection()
        if not selection:
            return

        idx = int(selection[0])
        result = self.search_results[idx]

        # 計算目標行位置
        target_line = self._calculate_target_line(result.page_num, result.line_num)

        # 跳轉到目標位置
        self.text_display.see(f"{target_line}.0")

    def _calculate_target_line(self, page_num: int, line_num: int) -> int:
        """
        計算目標行在文本框中的位置

        Args:
            page_num: 頁碼
            line_num: 頁面內行號

        Returns:
            文本框中的行號
        """
        target_line = 1

        # 累計前面所有頁面的行數
        for i in range(page_num - 1):
            page_text = self.all_pages_text[i]
            lines_count = page_text.count('\n') + 1
            target_line += lines_count + PAGE_SEPARATOR_LINES

        # 加上當前頁內的行號和分隔符
        target_line += line_num + 3

        return target_line

    def _clear_search_results(self) -> None:
        """清空搜尋結果"""
        self.search_results = []

        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        self.result_count_label.config(text="搜尋結果: 0", foreground="green")

        # 移除高亮
        self.text_display.config(state=tk.NORMAL)
        self.text_display.tag_remove(TAG_HIGHLIGHT, 1.0, tk.END)
        self.text_display.tag_remove(TAG_CURRENT_HIGHLIGHT, 1.0, tk.END)
        self.text_display.config(state=tk.DISABLED)


# =============================================================================
# 主程式入口
# =============================================================================

def main() -> None:
    """程式主入口函式"""
    root = tk.Tk()
    PDFReaderGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
