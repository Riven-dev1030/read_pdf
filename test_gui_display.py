#!/usr/bin/env python3
"""
GUI 文本顯示測試 - 測試 PDF 提取文本在 GUI 中的顯示
"""

import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from tkinter import font as tkfont
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("錯誤: 請先安裝 pypdf 函式庫")
    sys.exit(1)

def get_chinese_font():
    """獲取適合的中文字體"""
    font_candidates = [
        ('Microsoft YaHei', 11),
        ('微軟正黑體', 11),
        ('PingFang TC', 11),
        ('PingFang SC', 11),
        ('Noto Sans CJK TC', 11),
        ('Noto Sans CJK SC', 11),
        ('WenQuanYi Micro Hei', 11),
        ('AR PL UMing TW', 11),
        ('TkDefaultFont', 11)
    ]

    available_fonts = tkfont.families()
    for font_name, font_size in font_candidates:
        if font_name in available_fonts or font_name == 'TkDefaultFont':
            return (font_name, font_size)
    return ('TkDefaultFont', 11)

class TestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 文本顯示測試")
        self.root.geometry("900x700")

        # 設置字體
        self.chinese_font = get_chinese_font()
        print(f"使用字體: {self.chinese_font}")

        # 頂部按鈕區
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(btn_frame, text="選擇 PDF 檔案", command=self.open_pdf, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="測試中文顯示", command=self.test_chinese, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="清除", command=self.clear, width=15).pack(side=tk.LEFT, padx=5)

        # 資訊標籤
        self.info_label = tk.Label(root, text="請選擇 PDF 檔案", fg="blue")
        self.info_label.pack(padx=10, pady=5)

        # 文本顯示區域
        self.text_display = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=self.chinese_font,
            width=100,
            height=35
        )
        self.text_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 底部統計信息
        self.stats_label = tk.Label(root, text="", fg="green")
        self.stats_label.pack(padx=10, pady=5)

    def test_chinese(self):
        """測試中文顯示"""
        self.text_display.delete(1.0, tk.END)
        test_text = """
字體測試
========================================

繁體中文：測試繁體中文顯示效果
簡體中文：测试简体中文显示效果
English: Test English display
數字: 0123456789
符號: !@#$%^&*()

常用漢字測試：
你好世界 中文字體 閱讀器 檔案 資料夾
搜尋 顯示 錯誤 警告 成功 失敗

如果上面的文字都能正常顯示，說明字體沒有問題。
如果顯示為方框（■），說明字體有問題。

當前使用字體: {}
========================================
""".format(self.chinese_font[0])

        self.text_display.insert(tk.END, test_text)
        self.info_label.config(text=f"測試文本已顯示，使用字體: {self.chinese_font[0]}")

    def open_pdf(self):
        """開啟 PDF 並顯示內容"""
        file_path = filedialog.askopenfilename(
            title="選擇 PDF 檔案",
            filetypes=[("PDF 檔案", "*.pdf"), ("所有檔案", "*.*")]
        )

        if not file_path:
            return

        try:
            path = Path(file_path)
            reader = PdfReader(file_path)
            num_pages = len(reader.pages)

            self.info_label.config(text=f"檔案: {path.name}, 頁數: {num_pages}")

            # 清空顯示
            self.text_display.delete(1.0, tk.END)

            # 顯示 PDF 資訊
            info_text = f"PDF 檔案: {path.name}\n"
            info_text += f"總頁數: {num_pages}\n"
            info_text += f"使用字體: {self.chinese_font[0]}\n"
            info_text += "="*70 + "\n\n"
            self.text_display.insert(tk.END, info_text)

            # 提取並顯示前 3 頁（或全部頁面如果少於 3 頁）
            pages_to_show = min(3, num_pages)
            total_chars = 0
            chinese_chars = 0

            for i in range(pages_to_show):
                page = reader.pages[i]
                text = page.extract_text()

                # 統計字符
                total_chars += len(text)
                chinese_chars += sum(1 for c in text if '\u4e00' <= c <= '\u9fff')

                # 顯示頁面
                separator = f"\n{'='*70}\n第 {i+1} 頁\n{'='*70}\n"
                self.text_display.insert(tk.END, separator)
                self.text_display.insert(tk.END, text + "\n")

            # 顯示統計
            stats = f"提取字符數: {total_chars}, 中文字符數: {chinese_chars}"
            self.stats_label.config(text=stats)

            # 檢查私有區字符
            all_text = ""
            for i in range(num_pages):
                all_text += reader.pages[i].extract_text()

            pua_chars = [c for c in all_text if '\ue000' <= c <= '\uf8ff']
            if pua_chars:
                warning = f"\n\n⚠️ 警告: 發現 {len(pua_chars)} 個私有區字符（PUA）\n"
                warning += "這可能導致文字顯示異常。PDF 可能使用了自定義字體映射。\n"
                warning += f"前 10 個 PUA 字符: {pua_chars[:10]}\n"
                self.text_display.insert(tk.END, warning)
                messagebox.showwarning(
                    "字體映射問題",
                    f"此 PDF 包含 {len(pua_chars)} 個私有區字符，\n"
                    "可能是使用了自定義字體映射。\n"
                    "文字可能無法正常顯示。"
                )

            if chinese_chars == 0:
                warning = "\n\n⚠️ 警告: 沒有提取到中文字符\n"
                warning += "可能原因：\n"
                warning += "1. PDF 不包含中文\n"
                warning += "2. 這是掃描版 PDF（需要 OCR）\n"
                warning += "3. PDF 使用了特殊編碼\n"
                self.text_display.insert(tk.END, warning)

        except Exception as e:
            messagebox.showerror("錯誤", f"開啟 PDF 時出錯:\n{str(e)}")
            import traceback
            traceback.print_exc()

    def clear(self):
        """清除顯示"""
        self.text_display.delete(1.0, tk.END)
        self.info_label.config(text="已清除")
        self.stats_label.config(text="")

if __name__ == '__main__':
    root = tk.Tk()
    app = TestGUI(root)
    print("\n" + "="*70)
    print("PDF 文本顯示測試程序")
    print("="*70)
    print("1. 點擊「測試中文顯示」按鈕，確認中文字體可以正常顯示")
    print("2. 點擊「選擇 PDF 檔案」按鈕，查看 PDF 提取的文本")
    print("3. 如果測試文本正常但 PDF 文本異常，說明是 PDF 編碼問題")
    print("="*70 + "\n")
    root.mainloop()
