#!/usr/bin/env python3
"""
PDF Reader GUI - 基于 Tkinter 的 PDF 阅读器图形界面
支持搜索、文本显示和导航功能
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import re
from pathlib import Path
try:
    from pypdf import PdfReader
except ImportError:
    print("错误: 请先安装 pypdf 库")
    print("运行: pip install pypdf")
    import sys
    sys.exit(1)


class PDFReaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 阅读器")
        self.root.geometry("1200x700")

        # 数据存储
        self.pdf_reader = None
        self.pdf_path = None
        self.all_pages_text = []  # 存储所有页面的文本
        self.search_results = []  # 搜索结果列表

        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        """创建所有界面组件"""

        # 主容器 - 使用 PanedWindow 实现可调整大小的分栏
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ===== 左侧面板 =====
        left_frame = ttk.Frame(main_paned, width=400)
        main_paned.add(left_frame, weight=1)

        # 文件操作区域
        file_frame = ttk.LabelFrame(left_frame, text="文件操作", padding=10)
        file_frame.pack(fill=tk.X, padx=5, pady=5)

        # 打开文件按钮
        ttk.Button(
            file_frame,
            text="打开 PDF 文件",
            command=self.open_file
        ).pack(fill=tk.X)

        # 当前文件显示
        self.file_label = ttk.Label(file_frame, text="未打开文件", foreground="gray")
        self.file_label.pack(fill=tk.X, pady=(5, 0))

        # PDF 信息显示
        self.info_label = ttk.Label(file_frame, text="", foreground="blue")
        self.info_label.pack(fill=tk.X)

        # 搜索区域
        search_frame = ttk.LabelFrame(left_frame, text="搜索功能", padding=10)
        search_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 搜索输入框
        ttk.Label(search_frame, text="搜索内容:").pack(anchor=tk.W)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(fill=tk.X, pady=(0, 5))
        self.search_entry.bind('<Return>', lambda e: self.search_pdf())

        # 搜索选项
        options_frame = ttk.Frame(search_frame)
        options_frame.pack(fill=tk.X, pady=(0, 5))

        self.case_sensitive_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_frame,
            text="区分大小写",
            variable=self.case_sensitive_var
        ).pack(side=tk.LEFT)

        # 搜索按钮
        ttk.Button(
            search_frame,
            text="开始搜索",
            command=self.search_pdf
        ).pack(fill=tk.X)

        # 搜索结果统计
        self.result_count_label = ttk.Label(
            search_frame,
            text="搜索结果: 0",
            foreground="green"
        )
        self.result_count_label.pack(fill=tk.X, pady=(5, 0))

        # 搜索结果列表
        ttk.Label(search_frame, text="搜索结果列表:").pack(anchor=tk.W, pady=(10, 0))

        # 创建 Treeview 来显示搜索结果
        result_frame = ttk.Frame(search_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # 滚动条
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 结果列表
        self.result_tree = ttk.Treeview(
            result_frame,
            columns=('page', 'line', 'content'),
            show='headings',
            yscrollcommand=scrollbar.set,
            height=10
        )
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_tree.yview)

        # 配置列
        self.result_tree.heading('page', text='页码')
        self.result_tree.heading('line', text='行号')
        self.result_tree.heading('content', text='内容预览')

        self.result_tree.column('page', width=50, anchor=tk.CENTER)
        self.result_tree.column('line', width=50, anchor=tk.CENTER)
        self.result_tree.column('content', width=250)

        # 绑定双击事件
        self.result_tree.bind('<Double-1>', self.on_result_click)

        # ===== 右侧面板 =====
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)

        # 内容显示区域
        content_frame = ttk.LabelFrame(right_frame, text="PDF 内容", padding=5)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 文本显示区域（带滚动条）
        self.text_display = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            font=('Microsoft YaHei', 10),
            state=tk.DISABLED
        )
        self.text_display.pack(fill=tk.BOTH, expand=True)

        # 配置文本标签用于高亮
        self.text_display.tag_config('highlight', background='yellow', foreground='black')
        self.text_display.tag_config('current_highlight', background='orange', foreground='black')

    def open_file(self):
        """打开 PDF 文件"""
        file_path = filedialog.askopenfilename(
            title="选择 PDF 文件",
            filetypes=[("PDF 文件", "*.pdf"), ("所有文件", "*.*")]
        )

        if not file_path:
            return

        try:
            # 打开 PDF
            self.pdf_reader = PdfReader(file_path)
            self.pdf_path = Path(file_path)

            # 提取所有页面文本
            self.all_pages_text = []
            for page in self.pdf_reader.pages:
                text = page.extract_text()
                self.all_pages_text.append(text)

            # 更新界面显示
            num_pages = len(self.pdf_reader.pages)
            self.file_label.config(text=f"文件: {self.pdf_path.name}", foreground="black")
            self.info_label.config(text=f"总页数: {num_pages}")

            # 显示所有页面内容
            self.display_all_pages()

            # 清空搜索结果
            self.clear_search_results()

            messagebox.showinfo("成功", f"已成功打开 PDF 文件\n总页数: {num_pages}")

        except Exception as e:
            messagebox.showerror("错误", f"打开 PDF 文件时出错:\n{str(e)}")

    def display_all_pages(self):
        """显示所有页面内容"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)

        for i, page_text in enumerate(self.all_pages_text, 1):
            # 添加页面分隔
            separator = f"\n{'='*80}\n第 {i} 页\n{'='*80}\n"
            self.text_display.insert(tk.END, separator, 'page_header')
            self.text_display.insert(tk.END, page_text + "\n")

        self.text_display.config(state=tk.DISABLED)
        self.text_display.see(1.0)  # 滚动到顶部

    def search_pdf(self):
        """搜索 PDF 内容"""
        if not self.pdf_reader:
            messagebox.showwarning("警告", "请先打开 PDF 文件")
            return

        search_term = self.search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("警告", "请输入搜索内容")
            return

        case_sensitive = self.case_sensitive_var.get()

        # 清空之前的搜索结果
        self.clear_search_results()

        # 搜索所有页面
        total_matches = 0

        for page_num, page_text in enumerate(self.all_pages_text, 1):
            # 将文本按行分割
            lines = page_text.split('\n')

            # 在每一行中搜索
            for line_num, line in enumerate(lines, 1):
                # 根据是否区分大小写进行搜索
                if case_sensitive:
                    matches = list(re.finditer(re.escape(search_term), line))
                else:
                    matches = list(re.finditer(re.escape(search_term), line, re.IGNORECASE))

                # 保存匹配结果
                for match in matches:
                    start = match.start()
                    end = match.end()

                    # 获取上下文（前后各30个字符）
                    context_start = max(0, start - 30)
                    context_end = min(len(line), end + 30)

                    before = line[context_start:start]
                    matched = line[start:end]
                    after = line[end:context_end]

                    # 构建显示内容
                    preview = f"...{before}【{matched}】{after}..."

                    # 保存结果
                    result_data = {
                        'page': page_num,
                        'line': line_num,
                        'preview': preview,
                        'matched_text': matched,
                        'full_line': line
                    }
                    self.search_results.append(result_data)
                    total_matches += 1

        # 显示搜索结果
        self.display_search_results()

        # 更新统计信息
        if total_matches > 0:
            pages_with_matches = len(set(r['page'] for r in self.search_results))
            self.result_count_label.config(
                text=f"搜索结果: {total_matches} 处匹配，共 {pages_with_matches} 页",
                foreground="green"
            )

            # 高亮显示所有匹配
            self.highlight_all_matches(search_term, case_sensitive)
        else:
            self.result_count_label.config(
                text="搜索结果: 未找到匹配内容",
                foreground="red"
            )
            messagebox.showinfo("搜索结果", "未找到匹配内容")

    def display_search_results(self):
        """显示搜索结果到列表"""
        # 清空列表
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        # 添加结果
        for idx, result in enumerate(self.search_results):
            self.result_tree.insert(
                '',
                tk.END,
                iid=str(idx),
                values=(
                    result['page'],
                    result['line'],
                    result['preview']
                )
            )

    def highlight_all_matches(self, search_term, case_sensitive):
        """高亮显示所有匹配项"""
        self.text_display.config(state=tk.NORMAL)

        # 移除之前的高亮
        self.text_display.tag_remove('highlight', 1.0, tk.END)

        # 搜索并高亮
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
        """点击搜索结果，跳转到对应位置"""
        selection = self.result_tree.selection()
        if not selection:
            return

        # 获取选中的结果索引
        idx = int(selection[0])
        result = self.search_results[idx]

        page_num = result['page']

        # 计算目标位置
        # 需要找到对应页面在文本框中的位置
        target_line = 1.0

        # 累计前面所有页面的行数
        for i in range(page_num - 1):
            page_text = self.all_pages_text[i]
            lines_count = page_text.count('\n') + 1
            # 加上页面分隔符的行数（大约4行）
            target_line += lines_count + 4

        # 加上当前页内的行号
        target_line += result['line'] + 3  # 加3是因为页面分隔符

        # 跳转到目标位置
        self.text_display.see(f"{target_line}.0")

        # 高亮当前选中的匹配项（可选）
        # 这里可以添加一个临时的特殊高亮效果

    def clear_search_results(self):
        """清空搜索结果"""
        self.search_results = []
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        self.result_count_label.config(text="搜索结果: 0", foreground="green")

        # 移除高亮
        self.text_display.config(state=tk.NORMAL)
        self.text_display.tag_remove('highlight', 1.0, tk.END)
        self.text_display.tag_remove('current_highlight', 1.0, tk.END)
        self.text_display.config(state=tk.DISABLED)


def main():
    """主函数"""
    root = tk.Tk()
    app = PDFReaderGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
