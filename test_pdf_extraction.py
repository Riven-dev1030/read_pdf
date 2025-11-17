#!/usr/bin/env python3
"""
PDF 文本提取診斷工具 - 檢查 pypdf 提取的文本內容
"""

import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("錯誤: 請先安裝 pypdf 函式庫")
    print("執行: pip install pypdf")
    sys.exit(1)

def diagnose_pdf(pdf_path):
    """診斷 PDF 文本提取"""
    print("="*70)
    print("PDF 文本提取診斷")
    print("="*70)

    # 檢查文件是否存在
    path = Path(pdf_path)
    if not path.exists():
        print(f"錯誤: 檔案不存在 '{pdf_path}'")
        return

    print(f"\nPDF 檔案: {path.name}")
    print(f"檔案大小: {path.stat().st_size / 1024:.2f} KB")

    try:
        # 開啟 PDF
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)
        print(f"總頁數: {num_pages}")

        # 顯示元數據
        if reader.metadata:
            print("\n元數據:")
            for key, value in reader.metadata.items():
                print(f"  {key}: {value}")

        # 提取第一頁文本進行診斷
        print("\n" + "="*70)
        print("提取第 1 頁文本進行診斷")
        print("="*70)

        if num_pages > 0:
            page = reader.pages[0]
            text = page.extract_text()

            # 檢查文本長度
            print(f"\n提取的文本長度: {len(text)} 字符")

            # 檢查是否包含中文字符
            chinese_chars = [c for c in text if '\u4e00' <= c <= '\u9fff']
            print(f"包含中文字符數: {len(chinese_chars)}")

            # 顯示文本的前 500 個字符（原始）
            print("\n原始文本（前 500 字符）:")
            print("-"*70)
            preview = text[:500] if len(text) > 500 else text
            print(repr(preview))  # 使用 repr 顯示，可以看到實際的字符編碼

            # 顯示文本的前 500 個字符（格式化）
            print("\n格式化文本（前 500 字符）:")
            print("-"*70)
            print(preview)

            # 檢查特殊字符
            print("\n" + "="*70)
            print("字符編碼分析")
            print("="*70)

            # 統計字符類型
            latin = sum(1 for c in text if ord(c) < 128)
            cjk = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
            other = len(text) - latin - cjk

            print(f"Latin/ASCII 字符: {latin}")
            print(f"CJK 中文字符: {cjk}")
            print(f"其他字符: {other}")

            # 檢查是否有亂碼字符
            print("\n檢查特殊字符（前 20 個中文字符的 Unicode）:")
            chinese_samples = [(c, hex(ord(c))) for c in text if '\u4e00' <= c <= '\u9fff'][:20]
            for char, code in chinese_samples:
                print(f"  字符: '{char}' -> Unicode: {code}")

            # 檢查是否有私有區字符（可能是映射問題）
            pua_chars = [c for c in text if '\ue000' <= c <= '\uf8ff']
            if pua_chars:
                print(f"\n警告: 發現 {len(pua_chars)} 個私有區字符（Private Use Area）")
                print("這可能表示 PDF 使用了自定義字體映射")
                print("前 10 個私有區字符:")
                for c in pua_chars[:10]:
                    print(f"  {repr(c)} (U+{ord(c):04X})")

            # 測試編碼轉換
            print("\n" + "="*70)
            print("編碼測試")
            print("="*70)

            try:
                utf8_bytes = text.encode('utf-8')
                print(f"UTF-8 編碼: 成功 ({len(utf8_bytes)} bytes)")
            except Exception as e:
                print(f"UTF-8 編碼: 失敗 - {e}")

            try:
                # 嘗試不同的編碼
                for encoding in ['utf-8', 'gbk', 'big5', 'gb2312']:
                    try:
                        decoded = text.encode(encoding)
                        print(f"{encoding} 編碼: 成功")
                    except:
                        print(f"{encoding} 編碼: 失敗")
            except Exception as e:
                print(f"編碼測試失敗: {e}")

        else:
            print("PDF 沒有頁面")

        print("\n" + "="*70)
        print("診斷建議")
        print("="*70)

        if cjk == 0 and pua_chars:
            print("\n⚠️  問題診斷:")
            print("  - PDF 中沒有提取到標準 CJK 中文字符")
            print("  - 發現私有區字符（PUA）")
            print("\n可能原因:")
            print("  1. PDF 使用了嵌入字體但沒有正確的 ToUnicode 映射")
            print("  2. PDF 使用了自定義字體編碼")
            print("  3. 這是掃描版 PDF（圖片型 PDF）")
            print("\n解決方案:")
            print("  - 如果是掃描版 PDF，需要使用 OCR 技術")
            print("  - 如果是文字型 PDF，可能需要使用其他 PDF 庫（如 pdfplumber）")
        elif cjk > 0:
            print("\n✓ 提取的文本包含中文字符，應該可以正常顯示")
            print("\n如果 GUI 中還是顯示方框，請檢查:")
            print("  1. 確認已安裝中文字體（運行 test_font.py）")
            print("  2. 確認字體自動檢測功能正常工作")
        else:
            print("\n⚠️  沒有提取到中文字符")
            print("  這個 PDF 可能不包含中文，或是掃描版 PDF")

    except Exception as e:
        print(f"\n錯誤: 處理 PDF 時出錯")
        print(f"詳細信息: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 test_pdf_extraction.py <PDF檔案路徑>")
        print("\n範例:")
        print("  python3 test_pdf_extraction.py document.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]
    diagnose_pdf(pdf_path)
