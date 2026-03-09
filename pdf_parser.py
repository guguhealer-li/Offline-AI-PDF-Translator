import fitz

def extract_text_from_pdf(pdf_path):
    """
        负责从给定的 PDF 文件中提取文本。
        返回一个列表，列表里的每一个元素代表一页的文字。
    """
    print(f"[*] 正在加载 PDF 文件: {pdf_path}")
    try:
        # 1. 打开 PDF 文档
        doc = fitz.open(pdf_path)
        extracted_pages = []

        # 2. 遍历 PDF 的每一页
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            # 提取当前页的文本
            # get_text("text") 会尽可能保持原有的段落顺序
            text = page.get_text("text")
            extracted_pages.append(text)

            print(f"[+] 成功提取第 {page_num + 1}/{len(doc)} 页，共 {len(text)} 个字符。")
        doc.close()
        print("[*] PDF 解析完成！\n" + "-" * 30)
        return extracted_pages
    except FileNotFoundError:
        print(f"[!] 错误：找不到文件 {pdf_path}。请检查路径！")
        return []
    except Exception as e:
        print(f"[!] 解析 PDF 时发生未知错误：{e}")
        return []

if __name__ == "__main__":
    # 指定测试文件的路径
    test_pdf = "test_files/sample.pdf"
    # 调用我们写好的函数
    pages_text = extract_text_from_pdf(test_pdf)
    # 如果成功提取到了文字，打印第一页的前 500 个字符看看效果
    if pages_text:
        print("\n>>> 第一页内容预览 (前500字符) >>>\n")
        print(pages_text[0][:500])
        print("\n<<< 预览结束 <<<")