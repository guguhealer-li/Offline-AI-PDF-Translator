import os
import subprocess
import ctranslate2
import transformers

MODEL_DIR = "models/opus-mt-en-zh"


class AITranslator:
    def __init__(self):
        """
        初始化翻译引擎：全自动检查并构建本地模型
        """
        print("[*] 正在初始化 AI 翻译引擎...")

        # 1. 自动检查并构建模型
        self._ensure_model_ready()

        print("[*] 正在将模型加载到内存 (基于 CPU 的 int8 极速推理)...")
        # 2. 从官方缓存读取分词器词典
        self.tokenizer = transformers.AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-zh")
        # 3. 加载本地转化好的加速模型
        self.translator = ctranslate2.Translator(MODEL_DIR, device="cpu")
        print("[+] AI 翻译引擎准备就绪！\n" + "-" * 30)

    def _ensure_model_ready(self):
        """
        私有方法：如果本地没有模型，则自动调用转换工具进行构建
        """
        if not os.path.exists(MODEL_DIR) or not os.listdir(MODEL_DIR):
            print("[!] 首次运行检测：未找到本地加速模型。")
            print("[*] 正在为您全自动下载并构建离线量化模型，请耐心等待（视网络情况可能需要几分钟）...")

            # 使用 subprocess 自动在后台执行那条复杂的转换命令
            command = [
                "ct2-transformers-converter",
                "--model", "Helsinki-NLP/opus-mt-en-zh",
                "--output_dir", MODEL_DIR,
                "--quantization", "int8",
                "--force"
            ]

            try:
                # 运行命令，如果报错会抛出异常
                subprocess.run(command, check=True)
                print("[+] 本地模型全自动构建成功！以后的运行将完全断网且秒开。")
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"[!] 模型自动化构建失败，请检查网络环境。详细报错: {e}")

    def translate(self, text):
        """核心翻译方法"""
        if not text.strip():
            return ""

        try:
            source = self.tokenizer.convert_ids_to_tokens(self.tokenizer.encode(text))
            results = self.translator.translate_batch([source])
            target = results[0].hypotheses[0]
            translated_text = self.tokenizer.decode(self.tokenizer.convert_tokens_to_ids(target))
            return translated_text
        except Exception as e:
            print(f"[!] 翻译过程中出现错误: {e}")
            return "[翻译失败]"


# === 独立测试代码 ===
if __name__ == "__main__":
    engine = AITranslator()
    sample_text = "Artificial intelligence is revolutionizing software engineering. This project demonstrates local offline inference."
    print(f"原文: {sample_text}")
    result = engine.translate(sample_text)
    print(f"译文: {result}")