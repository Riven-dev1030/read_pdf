#!/usr/bin/env python3
"""
PDF Reader GUI - 基於 Tkinter 的 PDF 閱讀器圖形界面
支持搜尋、文本顯示和導航功能
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import re
from pathlib import Path
try:
    from pypdf import PdfReader
except ImportError:
    print("錯誤: 請先安裝 pypdf 函式庫")
    print("執行: pip install pypdf")
    import sys
    sys.exit(1)


class PDFReaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 閱讀器")
        self.root.geometry("1200x700")

        # 資料儲存
        self.pdf_reader = None
        self.pdf_path = None
        self.all_pages_text = []  # 儲存所有頁面的文本
        self.search_results = []  # 搜尋結果列表
        self.batch_mode = False  # 是否為批次搜尋模式
        self.pdf_directory = None  # 批次搜尋的資料夾路徑
        self.pdf_files = []  # 批次搜尋的PDF檔案列表

        # 建立界面
        self.create_widgets()

    def create_widgets(self):
        """建立所有界面組件"""

        # 主容器 - 使用 PanedWindow 實現可調整大小的分欄
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ===== 左側面板 =====
        left_frame = ttk.Frame(main_paned, width=400)
        main_paned.add(left_frame, weight=1)

        # 檔案操作區域
        file_frame = ttk.LabelFrame(left_frame, text="檔案操作", padding=10)
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

        # 開啟資料夾按鈕（批次搜尋）
        ttk.Button(
            button_frame,
            text="開啟資料夾",
            command=self.open_directory
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        # 當前檔案/資料夾顯示
        self.file_label = ttk.Label(file_frame, text="未開啟檔案", foreground="gray")
        self.file_label.pack(fill=tk.X, pady=(5, 0))

        # PDF 資訊顯示
        self.info_label = ttk.Label(file_frame, text="", foreground="blue")
        self.info_label.pack(fill=tk.X)

        # 搜尋區域
        search_frame = ttk.LabelFrame(left_frame, text="搜尋功能", padding=10)
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
        ttk.Label(search_frame, text="搜尋結果列表:").pack(anchor=tk.W, pady=(10, 0))

        # 建立 Treeview 來顯示搜尋結果
        result_frame = ttk.Frame(search_frame)
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
        self.result_tree.heading('file', text='檔案')
        self.result_tree.heading('page', text='頁碼')
        self.result_tree.heading('line', text='行號')
        self.result_tree.heading('content', text='內容預覽')

        self.result_tree.column('file', width=100, anchor=tk.W)
        self.result_tree.column('page', width=50, anchor=tk.CENTER)
        self.result_tree.column('line', width=50, anchor=tk.CENTER)
        self.result_tree.column('content', width=200)

        # 綁定雙擊事件
        self.result_tree.bind('<Double-1>', self.on_result_click)

        # ===== 右側面板 =====
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)

        # 內容顯示區域
        content_frame = ttk.LabelFrame(right_frame, text="PDF 內容", padding=5)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 文本顯示區域（帶滾動條）
        self.text_display = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            font=('Microsoft YaHei', 10),
            state=tk.DISABLED
        )
        self.text_display.pack(fill=tk.BOTH, expand=True)

        # 設定文本標籤用於高亮
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
            # 開啟 PDF
            self.pdf_reader = PdfReader(file_path)
            self.pdf_path = Path(file_path)

            # 切換到單檔案模式
            self.batch_mode = False
            self.pdf_directory = None
            self.pdf_files = []

            # 提取所有頁面文本
            self.all_pages_text = []
            for page in self.pdf_reader.pages:
                text = page.extract_text()
                self.all_pages_text.append(text)

            # 更新界面顯示
            num_pages = len(self.pdf_reader.pages)
            self.file_label.config(text=f"檔案: {self.pdf_path.name}", foreground="black")
            self.info_label.config(text=f"總頁數: {num_pages}")

            # 顯示所有頁面內容
            self.display_all_pages()

            # 清空搜尋結果
            self.clear_search_results()

            messagebox.showinfo("成功", f"已成功開啟 PDF 檔案\n總頁數: {num_pages}")

        except Exception as e:
            messagebox.showerror("錯誤", f"開啟 PDF 檔案時出錯:\n{str(e)}")

    def open_directory(self):
        """開啟資料夾（批次搜尋模式）"""
        dir_path = filedialog.askdirectory(
            title="選擇包含 PDF 檔案的資料夾"
        )

        if not dir_path:
            return

        try:
            dir_path = Path(dir_path)

            # 尋找所有PDF檔案
            pdf_files = sorted(dir_path.glob('**/*.pdf'))

            if not pdf_files:
                messagebox.showwarning("警告", f"在資料夾中沒有找到 PDF 檔案")
                return

            # 切換到批次搜尋模式
            self.batch_mode = True
            self.pdf_directory = dir_path
            self.pdf_files = pdf_files

            # 更新界面顯示
            self.file_label.config(
                text=f"資料夾: {dir_path.name}",
                foreground="black"
            )
            self.info_label.config(
                text=f"找到 {len(pdf_files)} 個 PDF 檔案"
            )

            # 清空右側顯示
            self.text_display.config(state=tk.NORMAL)
            self.text_display.delete(1.0, tk.END)
            info_text = f"批次搜尋模式\n\n"
            info_text += f"資料夾: {dir_path}\n"
            info_text += f"PDF 檔案數: {len(pdf_files)}\n\n"
            info_text += "請輸入搜尋內容並點擊「開始搜尋」\n\n"
            info_text += "檔案列表:\n" + "-" * 60 + "\n"
            for i, pdf_file in enumerate(pdf_files, 1):
                info_text += f"{i}. {pdf_file.relative_to(dir_path)}\n"
            self.text_display.insert(tk.END, info_text)
            self.text_display.config(state=tk.DISABLED)

            # 清空搜尋結果
            self.clear_search_results()

            messagebox.showinfo("成功", f"已開啟資料夾\n找到 {len(pdf_files)} 個 PDF 檔案")

        except Exception as e:
            messagebox.showerror("錯誤", f"開啟資料夾時出錯:\n{str(e)}")

    def display_all_pages(self):
        """顯示所有頁面內容"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)

        for i, page_text in enumerate(self.all_pages_text, 1):
            # 新增頁面分隔
            separator = f"\n{'='*80}\n第 {i} 頁\n{'='*80}\n"
            self.text_display.insert(tk.END, separator, 'page_header')
            self.text_display.insert(tk.END, page_text + "\n")

        self.text_display.config(state=tk.DISABLED)
        self.text_display.see(1.0)  # 滾動到頂部

    def search_pdf(self):
        """搜尋 PDF 內容"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("警告", "請輸入搜尋內容")
            return

        if self.batch_mode:
            # 批次搜尋模式
            self.search_batch()
        else:
            # 單檔案搜尋模式
            self.search_single_file()

    def search_single_file(self):
        """單檔案搜尋模式"""
        if not self.pdf_reader:
            messagebox.showwarning("警告", "請先開啟 PDF 檔案")
            return

        search_term = self.search_entry.get().strip()
        case_sensitive = self.case_sensitive_var.get()

        # 清空之前的搜尋結果
        self.clear_search_results()

        # 搜尋所有頁面
        total_matches = 0

        for page_num, page_text in enumerate(self.all_pages_text, 1):
            # 將文本按行分割
            lines = page_text.split('\n')

            # 在每一行中搜尋
            for line_num, line in enumerate(lines, 1):
                # 根據是否區分大小寫進行搜尋
                if case_sensitive:
                    matches = list(re.finditer(re.escape(search_term), line))
                else:
                    matches = list(re.finditer(re.escape(search_term), line, re.IGNORECASE))

                # 儲存匹配結果
                for match in matches:
                    start = match.start()
                    end = match.end()

                    # 獲取上下文（前後各30個字符）
                    context_start = max(0, start - 30)
                    context_end = min(len(line), end + 30)

                    before = line[context_start:start]
                    matched = line[start:end]
                    after = line[end:context_end]

                    # 構建顯示內容
                    preview = f"...{before}【{matched}】{after}..."

                    # 儲存結果
                    result_data = {
                        'file': self.pdf_path.name,
                        'page': page_num,
                        'line': line_num,
                        'preview': preview,
                        'matched_text': matched,
                        'full_line': line
                    }
                    self.search_results.append(result_data)
                    total_matches += 1

        # 顯示搜尋結果
        self.display_search_results()

        # 更新統計資訊
        if total_matches > 0:
            pages_with_matches = len(set(r['page'] for r in self.search_results))
            self.result_count_label.config(
                text=f"搜尋結果: {total_matches} 處匹配，共 {pages_with_matches} 頁。雙擊結果可跳轉！",
                foreground="green"
            )

            # 高亮顯示所有匹配
            self.highlight_all_matches(search_term, case_sensitive)
        else:
            self.result_count_label.config(
                text="搜尋結果: 未找到匹配內容",
                foreground="red"
            )
            messagebox.showinfo("搜尋結果", "未找到匹配內容")

    def search_batch(self):
        """批次搜尋模式"""
        if not self.pdf_files:
            messagebox.showwarning("警告", "請先開啟資料夾")
            return

        search_term = self.search_entry.get().strip()
        case_sensitive = self.case_sensitive_var.get()

        # 清空之前的搜尋結果
        self.clear_search_results()

        # 更新右側顯示
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, f"正在搜尋 {len(self.pdf_files)} 個 PDF 檔案...\n\n")
        self.text_display.config(state=tk.DISABLED)
        self.root.update()

        # 統計資訊
        total_matches = 0
        total_files_with_matches = 0

        # 遍歷每個PDF檔案
        for pdf_file in self.pdf_files:
            try:
                reader = PdfReader(pdf_file)
                file_matches = 0

                # 遍歷每一頁
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    lines = text.split('\n')

                    # 在每一行中搜尋
                    for line_num, line in enumerate(lines, 1):
                        if case_sensitive:
                            matches = list(re.finditer(re.escape(search_term), line))
                        else:
                            matches = list(re.finditer(re.escape(search_term), line, re.IGNORECASE))

                        # 儲存匹配結果
                        for match in matches:
                            start = match.start()
                            end = match.end()

                            # 獲取上下文（前後各30個字符）
                            context_start = max(0, start - 30)
                            context_end = min(len(line), end + 30)

                            before = line[context_start:start]
                            matched = line[start:end]
                            after = line[end:context_end]

                            # 構建顯示內容
                            preview = f"...{before}【{matched}】{after}..."

                            # 儲存結果
                            result_data = {
                                'file': pdf_file.name,
                                'file_path': pdf_file,
                                'page': page_num + 1,
                                'line': line_num,
                                'preview': preview,
                                'matched_text': matched,
                                'full_line': line
                            }
                            self.search_results.append(result_data)
                            file_matches += 1
                            total_matches += 1

                if file_matches > 0:
                    total_files_with_matches += 1

            except Exception as e:
                print(f"處理檔案 {pdf_file.name} 時出錯: {e}")
                continue

        # 顯示搜尋結果
        self.display_search_results()

        # 顯示搜尋總結
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)

        summary = f"批次搜尋完成！\n\n"
        summary += f"搜尋內容: '{search_term}'\n"
        summary += f"區分大小寫: {'是' if case_sensitive else '否'}\n"
        summary += f"{'-' * 60}\n\n"
        summary += f"📊 統計資訊:\n"
        summary += f"  - 搜尋檔案總數: {len(self.pdf_files)}\n"
        summary += f"  - 包含匹配的檔案: {total_files_with_matches}\n"
        summary += f"  - 總匹配次數: {total_matches}\n\n"

        if total_matches > 0:
            summary += f"請在左側查看詳細結果。\n"
        else:
            summary += f"未找到匹配內容。\n"

        self.text_display.insert(tk.END, summary)
        self.text_display.config(state=tk.DISABLED)

        # 更新統計資訊
        if total_matches > 0:
            self.result_count_label.config(
                text=f"搜尋結果: {total_matches} 處匹配，{total_files_with_matches} 個檔案",
                foreground="green"
            )
        else:
            self.result_count_label.config(
                text="搜尋結果: 未找到匹配內容",
                foreground="red"
            )
            messagebox.showinfo("搜尋結果", "未找到匹配內容")

    def display_search_results(self):
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
                    result['file'],
                    result['page'],
                    result['line'],
                    result['preview']
                )
            )

    def highlight_all_matches(self, search_term, case_sensitive):
        """高亮顯示所有匹配項"""
        self.text_display.config(state=tk.NORMAL)

        # 移除之前的高亮
        self.text_display.tag_remove('highlight', 1.0, tk.END)

        # 搜尋並高亮
        start_pos = '1.0'
        while True:
            if case_sensitive:
                pos = self.text_display.search(
                    search_term,
                    start_pos,
                    stopindex=tk.END,
                    nocase=False
                )
            else:
                pos = self.text_display.search(
                    search_term,
                    start_pos,
                    stopindex=tk.END,
                    nocase=True
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

        # 獲取選中的結果索引
        idx = int(selection[0])
        result = self.search_results[idx]

        page_num = result['page']

        # 計算目標位置
        # 需要找到對應頁面在文本框中的位置
        target_line = 1

        # 累計前面所有頁面的行數
        for i in range(page_num - 1):
            page_text = self.all_pages_text[i]
            lines_count = page_text.count('\n') + 1
            # 加上頁面分隔符的行數（大約4行）
            target_line += lines_count + 4

        # 加上當前頁內的行號
        target_line += result['line'] + 3  # 加3是因為頁面分隔符

        # 跳轉到目標位置
        self.text_display.see(f"{target_line}.0")

        # 高亮當前選中的匹配項（可選）
        # 這裡可以新增一個臨時的特殊高亮效果

    def clear_search_results(self):
        """清空搜尋結果"""
        self.search_results = []
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        self.result_count_label.config(text="搜尋結果: 0", foreground="green")

        # 移除高亮
        self.text_display.config(state=tk.NORMAL)
        self.text_display.tag_remove('highlight', 1.0, tk.END)
        self.text_display.tag_remove('current_highlight', 1.0, tk.END)
        self.text_display.config(state=tk.DISABLED)


def main():
    """主函數"""
    root = tk.Tk()
    app = PDFReaderGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
