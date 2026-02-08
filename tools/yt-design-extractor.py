#!/usr/bin/env python3
"""
YouTube 设计概念提取器
=================================
从 YouTube 视频中提取字幕和关键帧，并生成结构化的
markdown 参考文档，供 agent 使用。

用法：
    python3 tools/yt-design-extractor.py <youtube_url> [选项]

示例：
    python3 tools/yt-design-extractor.py "https://youtu.be/eVnQFWGDEdY"
    python3 tools/yt-design-extractor.py "https://youtu.be/eVnQFWGDEdY" --interval 30
    python3 tools/yt-design-extractor.py "https://youtu.be/eVnQFWGDEdY" --scene-detect --ocr
    python3 tools/yt-design-extractor.py "https://youtu.be/eVnQFWGDEdY" --full  # 所有功能
    python3 tools/yt-design-extractor.py "https://youtu.be/eVnQFWGDEdY" --ocr --ocr-engine easyocr

依赖要求：
    pip install yt-dlp youtube-transcript-api
    apt install ffmpeg

    可选（通过 Tesseract 进行 OCR）：
    pip install Pillow pytesseract
    apt install tesseract-ocr

    可选（更适合样式化文本的 OCR）：
    pip install easyocr

    可选（调色板提取）：
    pip install colorthief
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Optional

# 可选导入 - 如果不可用则优雅降级
PILLOW_AVAILABLE = False
TESSERACT_AVAILABLE = False

try:
    from PIL import Image

    PILLOW_AVAILABLE = True
except ImportError:
    pass

try:
    import pytesseract

    TESSERACT_AVAILABLE = PILLOW_AVAILABLE
except ImportError:
    pass

try:
    import easyocr

    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

try:
    from colorthief import ColorThief

    COLORTHIEF_AVAILABLE = True
except ImportError:
    COLORTHIEF_AVAILABLE = False

# ---------------------------------------------------------------------------
# 字幕提取
# ---------------------------------------------------------------------------


def extract_video_id(url: str) -> str:
    """从任何常见的 YouTube URL 格式中提取 11 个字符的视频 ID。"""
    patterns = [
        r"(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:embed/)([a-zA-Z0-9_-]{11})",
        r"(?:shorts/)([a-zA-Z0-9_-]{11})",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    # 也许用户传递的是原始 ID
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url):
        return url
    sys.exit(f"无法从以下 URL 提取视频 ID：{url}")


def get_video_metadata(url: str) -> dict:
    """使用 yt-dlp 提取标题、描述、章节、时长等信息。"""
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-download",
        "--no-playlist",
        url,
    ]
    print("[*] 正在获取视频元数据…")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        sys.exit("yt-dlp 元数据获取在 120 秒后超时。")
    if result.returncode != 0:
        sys.exit(f"yt-dlp 元数据获取失败：\n{result.stderr}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        sys.exit(
            f"yt-dlp 返回了无效的 JSON：{e}\n前 200 个字符：{result.stdout[:200]}"
        )


def get_transcript(video_id: str) -> list[dict] | None:
    """通过 youtube-transcript-api 获取字幕。返回
    {text, start, duration} 字典列表，如果不可用则返回 None。"""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import (
            TranscriptsDisabled,
            NoTranscriptFound,
            VideoUnavailable,
        )
    except ImportError:
        print("[!] 未安装 youtube-transcript-api。跳过字幕获取。")
        return None

    try:
        print("[*] 正在获取字幕…")
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
        entries = []
        for snippet in transcript:
            entries.append(
                {
                    "text": snippet.text,
                    "start": snippet.start,
                    "duration": snippet.duration,
                }
            )
        return entries
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
        print(f"[!] 字幕不可用（{e}）。将在没有字幕的情况下继续。")
        return None


# ---------------------------------------------------------------------------
# 关键帧提取
# ---------------------------------------------------------------------------


def download_video(url: str, out_dir: Path) -> Path:
    """下载视频，优先选择 720p 或更低。回退到可用的最佳质量。"""
    out_template = str(out_dir / "video.%(ext)s")
    cmd = [
        "yt-dlp",
        "-f",
        "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
        "--merge-output-format",
        "mp4",
        "-o",
        out_template,
        "--no-playlist",
        url,
    ]
    print("[*] 正在下载视频（优先 720p）…")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        sys.exit(
            "视频下载在 10 分钟后超时。"
            "视频可能太大或连接太慢。"
        )
    if result.returncode != 0:
        sys.exit(f"yt-dlp 下载失败：\n{result.stderr}")

    # 查找下载的文件
    for f in out_dir.iterdir():
        if f.name.startswith("video.") and f.suffix in (".mp4", ".mkv", ".webm"):
            return f
    sys.exit("下载成功但无法找到视频文件。")


def extract_frames_interval(
    video_path: Path, out_dir: Path, interval: int = 30
) -> list[Path]:
    """每隔 `interval` 秒提取一帧。"""
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    pattern = str(frames_dir / "frame_%04d.png")
    cmd = [
        "ffmpeg",
        "-i",
        str(video_path),
        "-vf",
        f"fps=1/{interval}",
        "-q:v",
        "2",
        pattern,
        "-y",
    ]
    print(f"[*] 正在每隔 {interval} 秒提取帧…")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        sys.exit("帧提取在 10 分钟后超时。")
    if result.returncode != 0:
        print(f"[!] ffmpeg 帧提取失败（退出代码 {result.returncode}）：")
        print(f"    {result.stderr[:500]}")
        return []
    frames = sorted(frames_dir.glob("frame_*.png"))
    if not frames:
        print(
            "[!] 警告：ffmpeg 运行了但没有产生帧。"
            "视频可能太短或损坏。"
        )
    else:
        print(f"    → 捕获了 {len(frames)} 帧")
    return frames


def extract_frames_scene(
    video_path: Path, out_dir: Path, threshold: float = 0.3
) -> list[Path]:
    """使用 ffmpeg 场景变化检测来捕获视觉上不同的帧。"""
    frames_dir = out_dir / "frames_scene"
    frames_dir.mkdir(exist_ok=True)
    pattern = str(frames_dir / "scene_%04d.png")
    cmd = [
        "ffmpeg",
        "-i",
        str(video_path),
        "-vf",
        f"select='gt(scene,{threshold})',showinfo",
        "-vsync",
        "vfr",
        "-q:v",
        "2",
        pattern,
        "-y",
    ]
    print(f"[*] 正在提取场景变化帧（阈值={threshold}）…")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        sys.exit("场景变化帧提取在 10 分钟后超时。")
    if result.returncode != 0:
        print(f"[!] ffmpeg 场景检测失败（退出代码 {result.returncode}）：")
        print(f"    {result.stderr[:500]}")
        return []
    frames = sorted(frames_dir.glob("scene_*.png"))
    if not frames:
        print("[!] 未检测到场景变化帧（尝试降低 --scene-threshold）。")
    else:
        print(f"    → 捕获了 {len(frames)} 个场景变化帧")
    return frames


# ---------------------------------------------------------------------------
# OCR 提取
# ---------------------------------------------------------------------------


def ocr_frame_tesseract(frame_path: Path) -> str:
    """使用 Tesseract OCR 从帧中提取文本。首先转换为灰度。"""
    if not TESSERACT_AVAILABLE:
        return ""
    try:
        img = Image.open(frame_path)
        if img.mode != "L":
            img = img.convert("L")
        text = pytesseract.image_to_string(img, config="--psm 6")
        return text.strip()
    except Exception as e:
        print(f"[!] {frame_path} 的 OCR 失败：{e}")
        return ""


def ocr_frame_easyocr(frame_path: Path, reader) -> str:
    """使用 EasyOCR 从帧中提取文本（更适合样式化文本）。"""
    try:
        results = reader.readtext(str(frame_path), detail=0)
        return "\n".join(results).strip()
    except Exception as e:
        print(f"[!] {frame_path} 的 OCR 失败：{e}")
        return ""


def run_ocr_on_frames(
    frames: list[Path], ocr_engine: str = "tesseract", workers: int = 4
) -> dict[Path, str]:
    """对帧运行 OCR。Tesseract 并行运行；EasyOCR 顺序运行。
    返回 {frame_path: text}。"""
    if not frames:
        return {}

    results = {}

    if ocr_engine == "easyocr":
        if not EASYOCR_AVAILABLE:
            sys.exit(
                "明确请求了 EasyOCR 但未安装。\n"
                "  安装：pip install torch torchvision --index-url "
                "https://download.pytorch.org/whl/cpu && pip install easyocr\n"
                "  或使用：--ocr-engine tesseract"
            )
        else:
            print("[*] 正在初始化 EasyOCR（这可能需要一点时间）…")
            reader = easyocr.Reader(["en"], gpu=False, verbose=False)

    if ocr_engine == "tesseract" and not TESSERACT_AVAILABLE:
        print("[!] 未安装 Tesseract/pytesseract，跳过 OCR")
        return {}

    print(f"[*] 正在 {len(frames)} 帧上运行 OCR（{ocr_engine}）…")

    if ocr_engine == "easyocr":
        # EasyOCR 不能很好地并行化，顺序运行
        for i, frame in enumerate(frames):
            results[frame] = ocr_frame_easyocr(frame, reader)
            if (i + 1) % 10 == 0:
                print(f"    → 已处理 {i + 1}/{len(frames)} 帧")
    else:
        # Tesseract 可以并行运行
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_frame = {
                executor.submit(ocr_frame_tesseract, f): f for f in frames
            }
            for i, future in enumerate(as_completed(future_to_frame)):
                frame = future_to_frame[future]
                try:
                    results[frame] = future.result()
                except Exception as e:
                    print(f"[!] {frame} 的 OCR 失败：{e}")
                    results[frame] = ""
                if (i + 1) % 10 == 0:
                    print(f"    → 已处理 {i + 1}/{len(frames)} 帧")

    # 统计有意义文本的帧
    with_text = sum(1 for t in results.values() if len(t) > 10)
    print(f"    → 在 {with_text}/{len(frames)} 帧中发现文本")

    return results


# ---------------------------------------------------------------------------
# 调色板提取
# ---------------------------------------------------------------------------


def extract_color_palette(frame_path: Path, color_count: int = 6) -> list[tuple]:
    """从帧中提取主要颜色。返回 RGB 元组列表。"""
    if not COLORTHIEF_AVAILABLE:
        return []
    try:
        ct = ColorThief(str(frame_path))
        palette = ct.get_palette(color_count=color_count, quality=5)
        return palette
    except Exception as e:
        print(f"[!] {frame_path} 的颜色提取失败：{e}")
        return []


def rgb_to_hex(rgb: tuple) -> str:
    """将 RGB 元组转换为十六进制颜色字符串。"""
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def analyze_color_palettes(frames: list[Path], sample_size: int = 10) -> dict:
    """分析跨采样帧的调色板。"""
    if not COLORTHIEF_AVAILABLE:
        return {}
    if not frames:
        return {}

    # 在视频中均匀采样帧
    step = max(1, len(frames) // sample_size)
    sampled = frames[::step][:sample_size]

    print(f"[*] 正在从 {len(sampled)} 帧中提取调色板…")

    all_colors = []
    for frame in sampled:
        palette = extract_color_palette(frame)
        all_colors.extend(palette)

    if not all_colors:
        return {}

    # 查找最常见的颜色（四舍五入以减少相似颜色）
    def round_color(rgb, bucket_size=32):
        return tuple((c // bucket_size) * bucket_size for c in rgb)

    rounded = [round_color(c) for c in all_colors]
    most_common = Counter(rounded).most_common(12)

    return {
        "dominant_colors": [rgb_to_hex(c) for c, _ in most_common[:6]],
        "all_sampled_colors": [rgb_to_hex(c) for c in all_colors[:24]],
    }


# ---------------------------------------------------------------------------
# Markdown 组装
# ---------------------------------------------------------------------------


def fmt_timestamp(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def group_transcript(entries: list[dict], chunk_seconds: int = 60) -> list[dict]:
    """将字幕片段合并为至少 `chunk_seconds` 持续时间的块。"""
    if not entries:
        return []
    groups = []
    current = {"start": entries[0]["start"], "text": ""}
    for e in entries:
        if e["start"] - current["start"] >= chunk_seconds and current["text"]:
            groups.append(current)
            current = {"start": e["start"], "text": ""}
        current["text"] += " " + e["text"]
    if current["text"]:
        groups.append(current)
    for g in groups:
        g["text"] = g["text"].strip()
    return groups


def build_markdown(
    meta: dict,
    transcript: list[dict] | None,
    interval_frames: list[Path],
    scene_frames: list[Path],
    out_dir: Path,
    interval: int,
    ocr_results: Optional[dict[Path, str]] = None,
    color_analysis: Optional[dict] = None,
) -> Path:
    """组装最终的参考 markdown 文档。"""
    title = meta.get("title", "Untitled Video")
    channel = meta.get("channel", meta.get("uploader", "Unknown"))
    duration = meta.get("duration", 0)
    description = meta.get("description", "")
    chapters = meta.get("chapters") or []
    video_url = meta.get("webpage_url", "")
    tags = meta.get("tags") or []

    ocr_results = ocr_results or {}
    color_analysis = color_analysis or {}

    lines: list[str] = []

    # --- 页眉 ---
    lines.append(f"# {title}\n")
    lines.append(f"> **来源：** [{channel}]({video_url})  ")
    lines.append(f"> **时长：** {fmt_timestamp(duration)}  ")
    lines.append(f"> **提取时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
    if tags:
        lines.append(f"> **标签：** {', '.join(tags[:15])}")
    lines.append("")

    # --- 调色板（如果已提取）---
    if color_analysis.get("dominant_colors"):
        lines.append("## 调色板\n")
        lines.append("视频中检测到的主要颜色：\n")
        colors = color_analysis["dominant_colors"]
        # 创建颜色样本表格
        lines.append("| 颜色 | 十六进制 |")
        lines.append("|-------|---------|")
        for hex_color in colors:
            # Unicode 块用于颜色预览（不会显示实际颜色但作为占位符）
            lines.append(f"| ████ | `{hex_color}` |")
        lines.append("")
        lines.append(f"*完整调色板：{', '.join(f'`{c}`' for c in colors)}*\n")

    # --- 描述 ---
    if description:
        lines.append("## 视频描述\n")
        # 裁剪过长的描述
        desc = description[:3000]
        lines.append(f"```\n{desc}\n```\n")

    # --- 章节 ---
    if chapters:
        lines.append("## 章节\n")
        lines.append("| 时间戳 | 标题 |")
        lines.append("|-----------|-------|")
        for ch in chapters:
            ts = fmt_timestamp(ch.get("start_time", 0))
            lines.append(f"| `{ts}` | {ch.get('title', '')} |")
        lines.append("")

    # --- 字幕 ---
    if transcript:
        grouped = group_transcript(transcript, chunk_seconds=60)
        lines.append("## 字幕\n")
        lines.append("<details><summary>完整字幕（点击展开）</summary>\n")
        for g in grouped:
            ts = fmt_timestamp(g["start"])
            lines.append(f"**[{ts}]** {g['text']}\n")
        lines.append("</details>\n")

        # 还要创建一个带有时间戳的精简关键点部分
        lines.append("## 字幕（精简片段）\n")
        lines.append("使用这些带时间戳的片段与帧进行交叉引用。\n")
        for g in grouped:
            ts = fmt_timestamp(g["start"])
            # 每个块的前 ~200 个字符作为预览
            preview = g["text"][:200]
            if len(g["text"]) > 200:
                preview += " …"
            lines.append(f"- **`{ts}`** — {preview}")
        lines.append("")

    # --- 关键帧 ---
    all_frames = []
    if interval_frames:
        lines.append(f"## 关键帧（每 {interval} 秒）\n")
        lines.append("以固定间隔捕获的视觉参考帧。\n")
        for i, f in enumerate(interval_frames):
            rel = os.path.relpath(f, out_dir)
            ts = fmt_timestamp(i * interval)
            lines.append(f"### `{ts}` 处的帧\n")
            lines.append(f"![frame-{ts}]({rel})\n")
            # 包含 OCR 文本（如果有）
            ocr_text = ocr_results.get(f, "").strip()
            if ocr_text and len(ocr_text) > 5:
                lines.append("<details><summary>📝 帧中检测到的文本</summary>\n")
                lines.append(f"```\n{ocr_text}\n```")
                lines.append("</details>\n")
            all_frames.append((ts, rel, ocr_text))
        lines.append("")

    if scene_frames:
        lines.append("## 场景变化帧\n")
        lines.append("视觉内容发生显著变化时捕获的帧。\n")
        for i, f in enumerate(scene_frames):
            rel = os.path.relpath(f, out_dir)
            lines.append(f"### 场景 {i + 1}\n")
            lines.append(f"![scene-{i + 1}]({rel})\n")
            # 包含 OCR 文本（如果有）
            ocr_text = ocr_results.get(f, "").strip()
            if ocr_text and len(ocr_text) > 5:
                lines.append("<details><summary>📝 帧中检测到的文本</summary>\n")
                lines.append(f"```\n{ocr_text}\n```")
                lines.append("</details>\n")
        lines.append("")

    # --- 视觉文本索引（OCR 摘要）---
    frames_with_text = [
        (ts, rel, txt) for ts, rel, txt in all_frames if txt and len(txt) > 10
    ]
    if frames_with_text:
        lines.append("## 视觉文本索引\n")
        lines.append("在视频帧中检测到的所有文本的可搜索索引。\n")
        lines.append("| 时间戳 | 关键文本（预览） |")
        lines.append("|-----------|-------------------|")
        for ts, rel, txt in frames_with_text:
            # 第一行或前 80 个字符作为预览
            preview = txt.split("\n")[0][:80].replace("|", "\\|")
            if len(txt) > 80:
                preview += "…"
            lines.append(f"| `{ts}` | {preview} |")
        lines.append("")

        # 完整文本转储以便搜索
        lines.append("### 所有检测到的文本（完整）\n")
        lines.append("<details><summary>点击展开完整 OCR 文本</summary>\n")
        for ts, rel, txt in frames_with_text:
            lines.append(f"**[{ts}]**")
            lines.append(f"```\n{txt}\n```\n")
        lines.append("</details>\n")

    # --- 帧索引（用于快速参考）---
    if all_frames:
        lines.append("## 帧索引\n")
        lines.append("| 时间戳 | 文件 | 有文本 |")
        lines.append("|-----------|------|----------|")
        for ts, rel, txt in all_frames:
            has_text = "✓" if txt and len(txt) > 10 else ""
            lines.append(f"| `{ts}` | `{rel}` | {has_text} |")
        lines.append("")

    # --- 页脚 ---
    lines.append("---\n")
    lines.append("*由 `yt-design-extractor.py` 生成 — 请审查和整理 ")
    lines.append("上述内容，然后将此文件提供给您的 agent。*\n")

    md_path = out_dir / "extracted-reference.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[✓] Markdown 参考已写入 {md_path}")
    return md_path


# ---------------------------------------------------------------------------
# 主函数
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="从 YouTube 视频中提取设计概念并生成 "
        "结构化的 markdown 参考文档。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            示例：
              %(prog)s "https://youtu.be/eVnQFWGDEdY"
              %(prog)s "https://youtu.be/eVnQFWGDEdY" --full
              %(prog)s "https://youtu.be/eVnQFWGDEdY" --interval 15 --scene-detect --ocr
              %(prog)s "https://youtu.be/eVnQFWGDEdY" --ocr --ocr-engine easyocr --colors
              %(prog)s "https://youtu.be/eVnQFWGDEdY" -o ./my-output
        """),
    )
    parser.add_argument("url", help="YouTube 视频 URL 或 ID")
    parser.add_argument(
        "-o",
        "--output-dir",
        help="输出目录（默认：./yt-extract-<video_id>）",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="关键帧捕获之间的秒数（默认：30）",
    )
    parser.add_argument(
        "--scene-detect",
        action="store_true",
        help="也在场景变化时提取帧（适合视觉密集型视频）",
    )
    parser.add_argument(
        "--scene-threshold",
        type=float,
        default=0.3,
        help="场景变化敏感度 0.0-1.0，越低 = 更多帧（默认：0.3）",
    )
    parser.add_argument(
        "--transcript-only",
        action="store_true",
        help="跳过视频下载，仅获取字幕 + 元数据",
    )
    parser.add_argument(
        "--chunk-seconds",
        type=int,
        default=60,
        help="将字幕分组为 N 秒的块（默认：60）",
    )
    parser.add_argument(
        "--ocr",
        action="store_true",
        help="在帧上运行 OCR 以提取屏幕文本",
    )
    parser.add_argument(
        "--ocr-engine",
        choices=["tesseract", "easyocr"],
        default="tesseract",
        help="OCR 引擎：'tesseract'（快速）或 'easyocr'（更适合样式化文本）",
    )
    parser.add_argument(
        "--colors",
        action="store_true",
        help="从帧中提取调色板",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="启用所有功能：场景检测、OCR 和颜色提取",
    )

    args = parser.parse_args()

    # --full 启用所有功能
    if args.full:
        args.scene_detect = True
        args.ocr = True
        args.colors = True

    # 提前依赖检查
    if not shutil.which("yt-dlp"):
        sys.exit(
            "在 PATH 上找不到必需的工具 'yt-dlp'。安装方法：pip install yt-dlp"
        )
    if not args.transcript_only and not shutil.which("ffmpeg"):
        sys.exit(
            "在 PATH 上找不到必需的工具 'ffmpeg'。"
            "安装方法：make install-ocr（或：brew install ffmpeg）"
        )

    video_id = extract_video_id(args.url)
    out_dir = Path(args.output_dir or f"./yt-extract-{video_id}")
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. 元数据
    meta = get_video_metadata(args.url)

    # 将原始元数据转储以供将来参考
    (out_dir / "metadata.json").write_text(
        json.dumps(meta, indent=2, default=str), encoding="utf-8"
    )
    print(f"    标题：    {meta.get('title')}")
    print(f"    频道：  {meta.get('channel', meta.get('uploader'))}")
    print(f"    时长：{fmt_timestamp(meta.get('duration', 0))}")

    # 2. 字幕
    transcript = get_transcript(video_id)

    # 3. 关键帧
    interval_frames: list[Path] = []
    scene_frames: list[Path] = []

    # OCR 和颜色分析结果
    ocr_results: dict[Path, str] = {}
    color_analysis: dict = {}

    if not args.transcript_only:
        video_path = download_video(args.url, out_dir)
        try:
            interval_frames = extract_frames_interval(
                video_path, out_dir, interval=args.interval
            )
            if args.scene_detect:
                scene_frames = extract_frames_scene(
                    video_path, out_dir, threshold=args.scene_threshold
                )
        finally:
            # 始终清理视频文件以节省空间
            print("[*] 正在删除下载的视频以节省空间…")
            video_path.unlink(missing_ok=True)

        # 4. OCR 提取
        if args.ocr:
            all_frames_for_ocr = interval_frames + scene_frames
            ocr_results = run_ocr_on_frames(
                all_frames_for_ocr,
                ocr_engine=args.ocr_engine,
            )
            # 将 OCR 结果保存到 JSON 以供重用
            ocr_json = {str(k): v for k, v in ocr_results.items()}
            (out_dir / "ocr-results.json").write_text(
                json.dumps(ocr_json, indent=2), encoding="utf-8"
            )

        # 5. 调色板分析
        if args.colors:
            all_frames_for_color = interval_frames + scene_frames
            color_analysis = analyze_color_palettes(all_frames_for_color)
            if color_analysis:
                (out_dir / "color-palette.json").write_text(
                    json.dumps(color_analysis, indent=2), encoding="utf-8"
                )
    else:
        print("[*] --transcript-only：跳过视频下载")

    # 6. 构建 markdown
    md_path = build_markdown(
        meta,
        transcript,
        interval_frames,
        scene_frames,
        out_dir,
        args.interval,
        ocr_results=ocr_results,
        color_analysis=color_analysis,
    )

    # 摘要
    print("\n" + "=" * 60)
    print("完成！输出目录：", out_dir)
    print("=" * 60)
    print(f"  参考文档  : {md_path}")
    print(f"  元数据       : {out_dir / 'metadata.json'}")
    if interval_frames:
        print(f"  间隔帧：{len(interval_frames)} 在 frames/ 中")
    if scene_frames:
        print(f"  场景帧   : {len(scene_frames)} 在 frames_scene/ 中")
    if ocr_results:
        frames_with_text = sum(1 for t in ocr_results.values() if len(t) > 10)
        print(
            f"  OCR 结果    : {frames_with_text} 帧有文本 → ocr-results.json"
        )
    if color_analysis:
        print(
            f"  调色板  : {len(color_analysis.get('dominant_colors', []))} 种颜色 → color-palette.json"
        )
    print()
    print("下一步：")
    print("  1. 审查 extracted-reference.md")
    print("  2. 为您的 agent 整理/注释内容")
    print("  3. 将文件提供给 Claude 以生成 SKILL.md 或 agent 定义")


if __name__ == "__main__":
    main()
