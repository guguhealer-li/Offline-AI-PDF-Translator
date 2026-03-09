# Offline AI PDF Translator

这是一个完全基于本地离线推理的 AI PDF 翻译工具。
本项目采用 Python 构建，使用 `PyMuPDF` 进行极速 PDF 解析，并利用 `CTranslate2` 和 `int8` 量化技术实现大语言模型在 CPU 上的极速本地翻译。

## 🚀 核心特性

- **纯离线运行**：无需调用任何外部 API，保护本地文档隐私。
- **极速推理**：将 Hugging Face 模型量化为 int8 格式，普通电脑 CPU 即可流畅运行。

## 🛠️ 安装与部署指南

### 1. 安装依赖环境
请确保你的 Python 环境在 3.8 以上，然后安装核心依赖：
```bash
pip install -r requirements.txt