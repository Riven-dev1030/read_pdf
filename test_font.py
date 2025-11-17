#!/usr/bin/env python3
"""
字體診斷工具 - 檢查系統是否支持中文顯示
"""

import tkinter as tk
from tkinter import font as tkfont

def test_fonts():
    """測試系統中可用的字體"""
    print("="*70)
    print("字體診斷工具")
    print("="*70)

    # 創建一個臨時窗口來獲取字體列表
    root = tk.Tk()
    root.withdraw()  # 隱藏主窗口

    # 獲取所有可用字體
    available_fonts = list(tkfont.families())
    available_fonts.sort()

    print(f"\n系統共有 {len(available_fonts)} 種字體")
    print("\n正在檢查常見中文字體...\n")

    # 常見中文字體列表
    chinese_fonts = [
        'Microsoft YaHei',
        '微軟正黑體',
        'Microsoft JhengHei',
        'PingFang TC',
        'PingFang SC',
        'Noto Sans CJK TC',
        'Noto Sans CJK SC',
        'Noto Sans TC',
        'Noto Sans SC',
        'WenQuanYi Micro Hei',
        'WenQuanYi Zen Hei',
        'AR PL UMing TW',
        'AR PL UKai TW',
        'SimSun',
        'SimHei',
        'KaiTi',
        'FangSong',
        'STHeiti',
        'STKaiti',
        'Heiti TC',
        'Songti TC',
    ]

    found_fonts = []
    for font_name in chinese_fonts:
        if font_name in available_fonts:
            found_fonts.append(font_name)
            print(f"✓ 找到: {font_name}")

    if not found_fonts:
        print("✗ 沒有找到任何常見的中文字體！")
        print("\n建議安裝中文字體：")
        print("  Ubuntu/Debian:")
        print("    sudo apt-get install fonts-noto-cjk")
        print("    sudo apt-get install fonts-wqy-microhei")
        print("  Fedora:")
        print("    sudo dnf install google-noto-sans-cjk-fonts")
        print("  Arch Linux:")
        print("    sudo pacman -S noto-fonts-cjk")
    else:
        print(f"\n共找到 {len(found_fonts)} 種中文字體")

    # 測試文本顯示
    print("\n" + "="*70)
    print("測試文本渲染")
    print("="*70)

    test_text = "測試中文顯示：繁體中文 简体中文 English 123"

    # 創建測試窗口
    root.deiconify()
    root.title("字體測試")
    root.geometry("800x600")

    # 創建滾動文本框
    text_widget = tk.Text(root, wrap=tk.WORD)
    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    text_widget.insert(tk.END, "字體測試結果\n")
    text_widget.insert(tk.END, "="*70 + "\n\n")
    text_widget.insert(tk.END, f"測試文本: {test_text}\n\n")
    text_widget.insert(tk.END, "使用不同字體渲染:\n")
    text_widget.insert(tk.END, "-"*70 + "\n\n")

    # 測試找到的中文字體
    if found_fonts:
        for font_name in found_fonts:
            text_widget.insert(tk.END, f"{font_name}:\n")
            text_widget.insert(tk.END, test_text + "\n", (font_name,))
            text_widget.tag_config(font_name, font=(font_name, 11))
            text_widget.insert(tk.END, "\n")
    else:
        text_widget.insert(tk.END, "警告: 沒有找到中文字體！\n")
        text_widget.insert(tk.END, "嘗試使用默認字體:\n")
        text_widget.insert(tk.END, test_text + "\n")

    text_widget.insert(tk.END, "\n" + "="*70 + "\n")
    text_widget.insert(tk.END, "如果上面的中文顯示正常，說明字體可用\n")
    text_widget.insert(tk.END, "如果顯示為方框(■)，說明需要安裝中文字體\n")

    text_widget.config(state=tk.DISABLED)

    print("\n已打開測試窗口，請檢查中文是否正常顯示")
    print("關閉窗口結束測試\n")

    root.mainloop()

if __name__ == '__main__':
    test_fonts()
