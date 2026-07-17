#!/usr/bin/env python3
"""安全的星禾公众号排版入口：在工作副本上修复标点并渲染。"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
THEMES = ("xinghe-light", "xinghe-card", "xinghe-note")


def run(command):
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        command,
        cwd=SKILL_DIR,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    result.check_returncode()


def main():
    parser = argparse.ArgumentParser(description="安全生成星禾风格微信公众号排版")
    parser.add_argument("--input", "-i", required=True, help="输入 Markdown 文件")
    parser.add_argument("--output", "-o", default="outputs/wechat-format", help="输出根目录")
    parser.add_argument("--theme", "-t", choices=THEMES, default="xinghe-light", help="星禾主题")
    parser.add_argument("--gallery", action="store_true", help="同时预览三个星禾主题")
    parser.add_argument("--no-open", action="store_true", help="不自动打开浏览器")
    parser.add_argument("--force", action="store_true", help="允许覆盖已有工作副本和预览")
    args = parser.parse_args()

    source = Path(args.input).resolve()
    if not source.is_file():
        parser.error(f"输入文件不存在: {source}")

    output = Path(args.output).resolve()
    working_dir = output / "_working"
    working_copy = working_dir / source.name
    preview = output / source.stem / "preview.html"
    if not args.force and (working_copy.exists() or preview.exists()):
        parser.error("输出已存在；请更换 --output，或确认后使用 --force")

    working_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, working_copy)

    try:
        run([sys.executable, str(SCRIPT_DIR / "zh_punctuation_fix.py"), str(working_copy), "--write"])
        command = [
            sys.executable,
            str(SCRIPT_DIR / "format.py"),
            "--input",
            str(working_copy),
            "--theme",
            args.theme,
            "--vault-root",
            str(source.parent),
            "--asset-root",
            str(source.parent),
            "--output",
            str(output),
        ]
        if args.gallery:
            command.extend(["--gallery", "--recommend", *THEMES])
        if args.no_open:
            command.append("--no-open")
        run(command)
    except subprocess.CalledProcessError as exc:
        print(f"排版失败，工作副本保留在: {working_copy}", file=sys.stderr)
        return exc.returncode

    print(f"源稿未修改: {source}")
    print(f"工作副本: {working_copy}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
