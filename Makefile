# YouTube 设计提取器 - 设置和使用
# ==========================================

PYTHON := python3
PIP := pip3
SCRIPT := tools/yt-design-extractor.py

.PHONY: help install install-ocr install-easyocr deps check run run-full run-ocr run-transcript clean

help:
	@echo "YouTube 设计提取器"
	@echo "========================"
	@echo ""
	@echo "设置（按顺序运行）："
	@echo "  make install-ocr     安装系统工具（tesseract + ffmpeg）"
	@echo "  make install         安装 Python 依赖"
	@echo "  make deps            显示已安装的内容"
	@echo ""
	@echo "可选："
	@echo "  make install-easyocr 安装 EasyOCR + PyTorch（约 2GB，用于样式化文本）"
	@echo ""
	@echo "用法："
	@echo "  make run URL=<youtube-url>           基本提取"
	@echo "  make run-full URL=<youtube-url>      完整提取（OCR + 颜色 + 场景）"
	@echo "  make run-ocr URL=<youtube-url>       仅 OCR"
	@echo "  make run-transcript URL=<youtube-url> 仅字幕 + 元数据"
	@echo ""
	@echo "示例："
	@echo "  make run URL='https://youtu.be/eVnQFWGDEdY'"
	@echo "  make run-full URL='https://youtu.be/eVnQFWGDEdY' INTERVAL=15"
	@echo ""
	@echo "选项（作为 make 变量传递）："
	@echo "  URL=<url>          YouTube 视频 URL（必需）"
	@echo "  INTERVAL=<secs>    帧间隔秒数（默认：30）"
	@echo "  OUTPUT=<dir>       输出目录"
	@echo "  ENGINE=<engine>    OCR 引擎：tesseract（默认）或 easyocr"

# 安装目标
install:
	$(PIP) install -r tools/requirements.txt

install-ocr:
	@echo "正在安装 Tesseract OCR + ffmpeg..."
	@if command -v apt-get >/dev/null 2>&1; then \
		sudo apt-get update && sudo apt-get install -y tesseract-ocr ffmpeg; \
	elif command -v brew >/dev/null 2>&1; then \
		brew install tesseract ffmpeg; \
	elif command -v dnf >/dev/null 2>&1; then \
		sudo dnf install -y tesseract ffmpeg; \
	else \
		echo "请手动安装 tesseract-ocr 和 ffmpeg"; \
		exit 1; \
	fi

install-easyocr:
	@echo "正在安装 PyTorch (CPU) + EasyOCR（约 2GB 下载）..."
	$(PIP) install torch torchvision --index-url https://download.pytorch.org/whl/cpu
	$(PIP) install easyocr

deps:
	@echo "检查依赖..."
	@echo ""
	@echo "系统工具："
	@command -v ffmpeg >/dev/null 2>&1 && echo "  ✓ ffmpeg" || echo "  ✗ ffmpeg（运行：make install-ocr）"
	@command -v tesseract >/dev/null 2>&1 && echo "  ✓ tesseract" || echo "  ✗ tesseract（运行：make install-ocr）"
	@echo ""
	@echo "Python 包（必需）："
	@$(PYTHON) -c "import yt_dlp; print('  ✓ yt-dlp', yt_dlp.version.__version__)" 2>/dev/null || echo "  ✗ yt-dlp（运行：make install）"
	@$(PYTHON) -c "from youtube_transcript_api import YouTubeTranscriptApi; print('  ✓ youtube-transcript-api')" 2>/dev/null || echo "  ✗ youtube-transcript-api（运行：make install）"
	@$(PYTHON) -c "from PIL import Image; print('  ✓ Pillow')" 2>/dev/null || echo "  ✗ Pillow（运行：make install）"
	@$(PYTHON) -c "import pytesseract; print('  ✓ pytesseract')" 2>/dev/null || echo "  ✗ pytesseract（运行：make install）"
	@$(PYTHON) -c "from colorthief import ColorThief; print('  ✓ colorthief')" 2>/dev/null || echo "  ✗ colorthief（运行：make install）"
	@echo ""
	@echo "可选（用于样式化文本 OCR）："
	@$(PYTHON) -c "import easyocr; print('  ✓ easyocr')" 2>/dev/null || echo "  ○ easyocr（运行：make install-easyocr）"

check:
	@$(PYTHON) $(SCRIPT) --help >/dev/null && echo "✓ 脚本工作正常" || echo "✗ 脚本失败"

# 运行目标
INTERVAL ?= 30
ENGINE ?= tesseract
OUTPUT ?=

run:
ifndef URL
	@echo "错误：URL 是必需的"
	@echo "用法：make run URL='https://youtu.be/VIDEO_ID'"
	@exit 1
endif
	$(PYTHON) $(SCRIPT) "$(URL)" --interval $(INTERVAL) $(if $(OUTPUT),-o $(OUTPUT))

run-full:
ifndef URL
	@echo "错误：URL 是必需的"
	@echo "用法：make run-full URL='https://youtu.be/VIDEO_ID'"
	@exit 1
endif
	$(PYTHON) $(SCRIPT) "$(URL)" --full --interval $(INTERVAL) --ocr-engine $(ENGINE) $(if $(OUTPUT),-o $(OUTPUT))

run-ocr:
ifndef URL
	@echo "错误：URL 是必需的"
	@echo "用法：make run-ocr URL='https://youtu.be/VIDEO_ID'"
	@exit 1
endif
	$(PYTHON) $(SCRIPT) "$(URL)" --ocr --interval $(INTERVAL) --ocr-engine $(ENGINE) $(if $(OUTPUT),-o $(OUTPUT))

run-transcript:
ifndef URL
	@echo "错误：URL 是必需的"
	@echo "用法：make run-transcript URL='https://youtu.be/VIDEO_ID'"
	@exit 1
endif
	$(PYTHON) $(SCRIPT) "$(URL)" --transcript-only $(if $(OUTPUT),-o $(OUTPUT))

# 清理
clean:
	rm -rf yt-extract-*
	@echo "已清理提取目录"
