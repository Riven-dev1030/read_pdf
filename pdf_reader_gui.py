#!/usr/bin/env python3
"""PDF Reader GUI - 基於 Tkinter 的 PDF 閱讀器圖形介面"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import re
from pathlib import Path
from typing import Optional

try:
    from pypdf import PdfReader
except ImportError:
    print("錯誤: 請先安裝 pypdf 函式庫")
    print("執行: pip install pypdf")
    import sys
    sys.exit(1)

# 常量
WINDOW_TITLE = "PDF 閱讀器"
WINDOW_SIZE = "1200x700"
TEXT_FONT = ('Microsoft YaHei', 10)
CONTEXT_CHARS = 30


class PDFReaderGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)

        # 資料儲存
        self.pdf_reader: Optional[PdfReader] = None
        self.pdf_path: Optional[Path] = None
        self.all_pages_text: list[str] = []
        self.search_results: list[dict] = []

        # 批次模式
        self.batch_mode = False
        self.pdf_directory: Optional[Path] = None
        self.pdf_files: list[Path] = []

        self._create_widgets()

    def _create_widgets(self):
        """建立所有介面組件"""
        # 主容器
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 左側面板
        left_frame = ttk.Frame(main_paned, width=400)
        main_paned.add(left_frame, weight=1)

        # 檔案操作區域
        file_frame = ttk.LabelFrame(left_frame, text="檔案操作", padding=10)
        file_frame.pack(fill=tk.X, padx=5, pady=5)

        button_frame = ttk.Frame(file_frame)
        button_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(button_frame, text="開啟 PDF 檔案", command=self.open_file
                   ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        ttk.Button(button_frame, text="開啟資料夾", command=self.open_directory
                   ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        self.file_label = ttk.Label(file_frame, text="未開啟檔案", foreground="gray")
        self.file_label.pack(fill=tk.X, pady=(5, 0))

        self.info_label = ttk.Label(file_frame, text="", foreground="blue")
        self.info_label.pack(fill=tk.X)

        # 搜尋區域
        search_frame = ttk.LabelFrame(left_frame, text="搜尋功能", padding=10)
        search_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Label(search_frame, text="搜尋內容:").pack(anchor=tk.W)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(fill=tk.X, pady=(0, 5))
        self.search_entry.bind('<Return>', lambda e: self.search_pdf())

        options_frame = ttk.Frame(search_frame)
        options_frame.pack(fill=tk.X, pady=(0, 5))

        self.case_sensitive_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="區分大小寫", variable=self.case_sensitive_var
                        ).pack(side=tk.LEFT)

        ttk.Button(search_frame, text="開始搜尋", command=self.search_pdf).pack(fill=tk.X)

        self.result_count_label = ttk.Label(search_frame, text="搜尋結果: 0", foreground="green")
        self.result_count_label.pack(fill=tk.X, pady=(5, 0))

        # 搜尋結果列表
        ttk.Label(search_frame, text="搜尋結果列表:").pack(anchor=tk.W, pady=(10, 0))

        result_frame = ttk.Frame(search_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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
        self.result_tree.heading('file', text='檔案')
        self.result_tree.heading('page', text='頁碼')
        self.result_tree.heading('line', text='行號')
        self.result_tree.heading('content', text='內容預覽')

        self.result_tree.column('file', width=100, anchor=tk.W)
        self.result_tree.column('page', width=50, anchor=tk.CENTER)
        self.result_tree.column('line', width=50, anchor=tk.CENTER)
        self.result_tree.column('content', width=200)

        self.result_tree.bind('<Double-1>', self.on_result_click)

        # 右側面板
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)

        content_frame = ttk.LabelFrame(right_frame, text="PDF 內容", padding=5)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.text_display = scrolledtext.ScrolledText(
            content_frame, wrap=tk.WORD, font=TEXT_FONT, state=tk.DISABLED
        )
        self.text_display.pack(fill=tk.BOTH, expand=True)

        # 設定高亮標籤
        self.text_display.tag_config('highlight', background='yellow', foreground='black')
        self.text_display.tag_config('current_highlight', background='orange', foreground='black')

    def open_file(self):
        """開啟 PDF 檔案"""
        file_path = filedialog.askopenfilename(
            title="選擇 PDF 檔案",
            filetypes=[("PDF 檔案", "*.pdf"), ("所有檔案", "*.*")]
        )

        if not file_path:
            return

        try:
            self.pdf_reader = PdfReader(file_path)
            self.pdf_path = Path(file_path)

            # 切換到單檔案模式
            self.batch_mode = False
            self.pdf_directory = None
            self.pdf_files = []

            # 提取所有頁面文本
            self.all_pages_text = [page.extract_text() for page in self.pdf_reader.pages]

            # 更新介面
            num_pages = len(self.pdf_reader.pages)
            self.file_label.config(text=f"檔案: {self.pdf_path.name}", foreground="black")
            self.info_label.config(text=f"總頁數: {num_pages}")

            self._display_all_pages()
            self._clear_search_results()

            messagebox.showinfo("成功", f"已成功開啟 PDF 檔案\n總頁數: {num_pages}")

        except Exception as e:
            messagebox.showerror("錯誤", f"開啟 PDF 檔案時出錯:\n{str(e)}")

    def open_directory(self):
        """開啟資料夾（批次搜尋模式）"""
        dir_path = filedialog.askdirectory(title="選擇包含 PDF 檔案的資料夾")

        if not dir_path:
            return

        try:
            path = Path(dir_path)
            pdf_files = sorted(path.glob('**/*.pdf'))

            if not pdf_files:
                messagebox.showwarning("警告", "在資料夾中沒有找到 PDF 檔案")
                return

            # 切換到批次模式
            self.batch_mode = True
            self.pdf_directory = path
            self.pdf_files = pdf_files

            # 更新介面
            self.file_label.config(text=f"資料夾: {path.name}", foreground="black")
            self.info_label.config(text=f"找到 {len(pdf_files)} 個 PDF 檔案")

            # 顯示檔案列表
            self.text_display.config(state=tk.NORMAL)
            self.text_display.delete(1.0, tk.END)

            info_text = f"批次搜尋模式\n\n"
            info_text += f"資料夾: {path}\n"
            info_text += f"PDF 檔案數: {len(pdf_files)}\n\n"
            info_text += "請輸入搜尋內容並點擊「開始搜尋」\n\n"
            info_text += "檔案列表:\n" + "-" * 60 + "\n"

            for i, pdf_file in enumerate(pdf_files, 1):
                info_text += f"{i}. {pdf_file.relative_to(path)}\n"

            self.text_display.insert(tk.END, info_text)
            self.text_display.config(state=tk.DISABLED)

            self._clear_search_results()
            messagebox.showinfo("成功", f"已開啟資料夾\n找到 {len(pdf_files)} 個 PDF 檔案")

        except Exception as e:
            messagebox.showerror("錯誤", f"開啟資料夾時出錯:\n{str(e)}")

    def _display_all_pages(self):
        """顯示所有頁面內容"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)

        for i, page_text in enumerate(self.all_pages_text, 1):
            separator = f"\n{'='*80}\n第 {i} 頁\n{'='*80}\n"
            self.text_display.insert(tk.END, separator)
            self.text_display.insert(tk.END, page_text + "\n")

        self.text_display.config(state=tk.DISABLED)
        self.text_display.see(1.0)

    def search_pdf(self):
        """搜尋 PDF 內容"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("警告", "請輸入搜尋內容")
            return

        if self.batch_mode:
            self._search_batch(search_term)
        else:
            self._search_single_file(search_term)

    def _search_single_file(self, search_term: str):
        """單檔案搜尋模式"""
        if not self.pdf_reader:
            messagebox.showwarning("警告", "請先開啟 PDF 檔案")
            return

        case_sensitive = self.case_sensitive_var.get()
        self._clear_search_results()

        # 搜尋所有頁面
        for page_num, page_text in enumerate(self.all_pages_text, 1):
            lines = page_text.split('\n')

            for line_num, line in enumerate(lines, 1):
                flags = 0 if case_sensitive else re.IGNORECASE
                matches = list(re.finditer(re.escape(search_term), line, flags))

                for match in matches:
                    start, end = match.start(), match.end()
                    ctx_start = max(0, start - CONTEXT_CHARS)
                    ctx_end = min(len(line), end + CONTEXT_CHARS)

                    preview = f"...{line[ctx_start:start]}【{line[start:end]}】{line[end:ctx_end]}..."

                    self.search_results.append({
                        'file': self.pdf_path.name,
                        'page': page_num,
                        'line': line_num,
                        'preview': preview
                    })

        # 顯示結果
        self._display_search_results()

        total = len(self.search_results)
        if total > 0:
            pages = len(set(r['page'] for r in self.search_results))
            self.result_count_label.config(
                text=f"搜尋結果: {total} 處匹配，共 {pages} 頁。雙擊結果可跳轉！",
                foreground="green"
            )
            self._highlight_all_matches(search_term, case_sensitive)
        else:
            self.result_count_label.config(text="搜尋結果: 未找到匹配內容", foreground="red")
            messagebox.showinfo("搜尋結果", "未找到匹配內容")

    def _search_batch(self, search_term: str):
        """批次搜尋模式"""
        if not self.pdf_files:
            messagebox.showwarning("警告", "請先開啟資料夾")
            return

        case_sensitive = self.case_sensitive_var.get()
        self._clear_search_results()

        # 顯示進度
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, f"正在搜尋 {len(self.pdf_files)} 個 PDF 檔案...\n\n")
        self.text_display.config(state=tk.DISABLED)
        self.root.update()

        files_with_matches = 0

        # 遍歷每個PDF檔案
        for pdf_file in self.pdf_files:
            try:
                reader = PdfReader(pdf_file)
                file_matches = 0

                for page_num in range(len(reader.pages)):
                    text = reader.pages[page_num].extract_text()
                    lines = text.split('\n')

                    for line_num, line in enumerate(lines, 1):
                        flags = 0 if case_sensitive else re.IGNORECASE
                        matches = list(re.finditer(re.escape(search_term), line, flags))

                        for match in matches:
                            start, end = match.start(), match.end()
                            ctx_start = max(0, start - CONTEXT_CHARS)
                            ctx_end = min(len(line), end + CONTEXT_CHARS)

                            preview = f"...{line[ctx_start:start]}【{line[start:end]}】{line[end:ctx_end]}..."

                            self.search_results.append({
                                'file': pdf_file.name,
                                'file_path': pdf_file,
                                'page': page_num + 1,
                                'line': line_num,
                                'preview': preview
                            })
                            file_matches += 1

                if file_matches > 0:
                    files_with_matches += 1

            except Exception as e:
                print(f"處理檔案 {pdf_file.name} 時出錯: {e}")

        # 顯示結果
        self._display_search_results()

        # 顯示總結
        total = len(self.search_results)
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)

        summary = f"批次搜尋完成！\n\n"
        summary += f"搜尋內容: '{search_term}'\n"
        summary += f"區分大小寫: {'是' if case_sensitive else '否'}\n"
        summary += f"{'-' * 60}\n\n"
        summary += f"📊 統計資訊:\n"
        summary += f"  - 搜尋檔案總數: {len(self.pdf_files)}\n"
        summary += f"  - 包含匹配的檔案: {files_with_matches}\n"
        summary += f"  - 總匹配次數: {total}\n\n"

        if total > 0:
            summary += "請在左側查看詳細結果，雙擊可查看具體位置。\n"
        else:
            summary += "未找到匹配內容。\n"

        self.text_display.insert(tk.END, summary)
        self.text_display.config(state=tk.DISABLED)

        # 更新統計
        if total > 0:
            self.result_count_label.config(
                text=f"搜尋結果: {total} 處匹配，{files_with_matches} 個檔案",
                foreground="green"
            )
        else:
            self.result_count_label.config(text="搜尋結果: 未找到匹配內容", foreground="red")
            messagebox.showinfo("搜尋結果", "未找到匹配內容")

    def _display_search_results(self):
        """顯示搜尋結果到列表"""
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        for idx, result in enumerate(self.search_results):
            self.result_tree.insert('', tk.END, iid=str(idx), values=(
                result['file'], result['page'], result['line'], result['preview']
            ))

    def _highlight_all_matches(self, search_term: str, case_sensitive: bool):
        """高亮顯示所有匹配項"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.tag_remove('highlight', 1.0, tk.END)

        start_pos = '1.0'
        while True:
            pos = self.text_display.search(
                search_term, start_pos, stopindex=tk.END, nocase=not case_sensitive
            )
            if not pos:
                break

            end_pos = f"{pos}+{len(search_term)}c"
            self.text_display.tag_add('highlight', pos, end_pos)
            start_pos = end_pos

        self.text_display.config(state=tk.DISABLED)

    def on_result_click(self, event):
        """點擊搜尋結果，跳轉到對應位置"""
        selection = self.result_tree.selection()
        if not selection:
            return

        idx = int(selection[0])
        result = self.search_results[idx]
        page_num = result['page']

        # 計算目標位置
        target_line = 1
        for i in range(page_num - 1):
            lines_count = self.all_pages_text[i].count('\n') + 1
            target_line += lines_count + 4  # 加上頁面分隔符

        target_line += result['line'] + 3

        self.text_display.see(f"{target_line}.0")

    def _clear_search_results(self):
        """清空搜尋結果"""
        self.search_results = []
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        self.result_count_label.config(text="搜尋結果: 0", foreground="green")

        self.text_display.config(state=tk.NORMAL)
        self.text_display.tag_remove('highlight', 1.0, tk.END)
        self.text_display.tag_remove('current_highlight', 1.0, tk.END)
        self.text_display.config(state=tk.DISABLED)


def main():
    """主函式"""
    root = tk.Tk()
    PDFReaderGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
