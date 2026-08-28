"""
图像+音频压缩脚本（Pillow 压 jpg/png，FFmpeg 压 mp3）
用法: python compress_assets.py
"""
import os, sys
from pathlib import Path

DIR = Path(__file__).parent.resolve()

SKIP_ORIGINALS_SMALLER = True  # 如果压缩后更大就保留原文件

total_before = 0
total_after = 0
report = []

def kb(p): return p.stat().st_size / 1024

# ==========================================
# 1. JPG 压缩: quality 82, 渐进式, 降采样 4:2:0
#    目标：每条线索 330KB → ~170KB, 背景 800KB→~400KB
# ==========================================
def compress_jpg(path: Path):
    from PIL import Image
    before = kb(path)
    tmp = path.with_suffix('.tmp.jpg')
    try:
        with Image.open(path) as im:
            # 背景/人物大图: 限制最长边 1920, 线索卡 1280 足够
            max_side = 1920 if any(k in path.name for k in ('bg0','bgm_')) else 1280
            w,h = im.size
            if max(w,h) > max_side:
                ratio = max_side / max(w,h)
                im = im.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
            if im.mode not in ('RGB','L'):
                im = im.convert('RGB')
            im.save(tmp, 'JPEG', quality=82, optimize=True, progressive=True, subsampling=1)
        after = kb(tmp)
        if SKIP_ORIGINALS_SMALLER and after >= before:
            tmp.unlink(missing_ok=True)
            report.append(f"[jpg keep] {path.name}: {before:.0f} KB (原图更小)")
            return before, before
        # 替换
        path.unlink()
        tmp.rename(path)
        report.append(f"[jpg  ✓ ] {path.name}: {before:.0f}KB -> {after:.0f}KB (-{100*(before-after)/before:.0f}%)")
        return before, after
    except Exception as e:
        tmp.unlink(missing_ok=True)
        report.append(f"[jpg fail] {path.name}: {e}")
        return before, before

# ==========================================
# 2. PNG 压缩: Pillow palette 量化 + 最优
#    注意保留透明通道
# ==========================================
def compress_png(path: Path):
    from PIL import Image
    before = kb(path)
    tmp = path.with_suffix('.tmp.png')
    try:
        with Image.open(path) as im:
            has_alpha = (im.mode == 'RGBA') or ('A' in im.getbands())
            # 立绘人物通常 1600px 高, 缩到 1000px 足够（浏览器显示最大 ~50% 画幅）
            MAX = 1000
            w,h = im.size
            if max(w,h) > MAX:
                ratio = MAX / max(w,h)
                im = im.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
            if has_alpha:
                im = im.convert('RGBA')
                im.save(tmp, 'PNG', optimize=True)
            else:
                im = im.convert('RGB')
                im.save(tmp, 'PNG', optimize=True)
        after = kb(tmp)
        if SKIP_ORIGINALS_SMALLER and after >= before:
            tmp.unlink(missing_ok=True)
            report.append(f"[png keep] {path.name}: {before:.0f} KB")
            return before, before
        path.unlink()
        tmp.rename(path)
        report.append(f"[png  ✓ ] {path.name}: {before:.0f}KB -> {after:.0f}KB (-{100*(before-after)/before:.0f}%)")
        return before, after
    except Exception as e:
        tmp.unlink(missing_ok=True)
        report.append(f"[png fail] {path.name}: {e}")
        return before, before

# ==========================================
# 3. MP3 压缩: FFmpeg 96kbps
#    需要 ffmpeg 在 PATH
# ==========================================
import subprocess, shutil
HAS_FFMPEG = shutil.which('ffmpeg') is not None

def compress_mp3(path: Path):
    before = kb(path)
    if not HAS_FFMPEG:
        report.append(f"[mp3 skip] {path.name}: ffmpeg not in PATH, size {before:.0f} KB")
        return before, before
    tmp = path.with_suffix('.tmp.mp3')
    try:
        cmd = ['ffmpeg','-y','-hide_banner','-loglevel','error',
               '-i', str(path),
               '-codec:a','libmp3lame','-b:a','96k','-ac','2',
               str(tmp)]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if r.returncode != 0 or not tmp.exists():
            raise RuntimeError(r.stderr.strip() or 'ffmpeg failed')
        after = kb(tmp)
        if SKIP_ORIGINALS_SMALLER and after >= before:
            tmp.unlink(missing_ok=True)
            report.append(f"[mp3 keep] {path.name}: {before:.0f} KB")
            return before, before
        path.unlink()
        tmp.rename(path)
        report.append(f"[mp3  ✓ ] {path.name}: {before:.0f}KB -> {after:.0f}KB (-{100*(before-after)/before:.0f}%)")
        return before, after
    except Exception as e:
        tmp.unlink(missing_ok=True)
        report.append(f"[mp3 fail] {path.name}: {e}")
        return before, before

# ==========================================
# MAIN
# ==========================================
print("========== JPG 压缩 ==========")
for p in sorted((DIR/'assets').rglob('*.jpg')):
    b,a = compress_jpg(p)
    total_before += b; total_after += a

print("\n========== PNG 压缩 ==========")
for p in sorted((DIR/'assets/characters').rglob('*.png')):
    b,a = compress_png(p)
    total_before += b; total_after += a

print("\n========== MP3 压缩 ==========")
for p in sorted((DIR/'assets/bgm').rglob('*.mp3')):
    b,a = compress_mp3(p)
    total_before += b; total_after += a

print("\n========== 详情 ==========")
for line in report: print(line)

print(f"\n========== TOTAL: {total_before/1024:.2f} MB -> {total_after/1024:.2f} MB  "
      f"(save {100*(total_before-total_after)/total_before:.0f}%, {(total_before-total_after)/1024:.2f} MB)")
if not HAS_FFMPEG:
    print("\n⚠  未检测到 ffmpeg，BGM 未压缩。安装 ffmpeg 后重新运行本脚本即可压 BGM:")
    print("   方案 1: winget install Gyan.FFmpeg")
    print("   方案 2: 下载 https://www.gyan.dev/ffmpeg/builds/ 解压 bin 目录加入 PATH")
