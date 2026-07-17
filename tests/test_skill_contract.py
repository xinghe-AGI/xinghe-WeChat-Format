import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_THEMES = {
    "xinghe-light.json",
    "xinghe-card.json",
    "xinghe-note.json",
}


class SkillContractTests(unittest.TestCase):
    def test_only_curated_xinghe_themes_are_shipped(self):
        theme_files = {path.name for path in (ROOT / "themes").glob("*.json")}
        self.assertEqual(EXPECTED_THEMES, theme_files)

    def test_example_config_is_ready_for_local_formatting(self):
        config = json.loads((ROOT / "config.example.json").read_text(encoding="utf-8"))
        self.assertEqual("xinghe-light", config["settings"]["default_theme"])
        self.assertEqual("outputs/wechat-format", config["output_dir"])
        self.assertEqual("", config["wechat"]["app_id"])
        self.assertEqual("", config["wechat"]["app_secret"])
        self.assertNotIn("smart_api", config)
        self.assertNotIn("ai", config)

    def test_skill_docs_only_recommend_xinghe_themes(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for theme in ("xinghe-light", "xinghe-card", "xinghe-note"):
            self.assertIn(theme, skill)
            self.assertIn(theme, readme)
        for old_theme in ("fresh-card", "glass-light", "notion-doc"):
            self.assertNotIn(old_theme, skill)
            self.assertNotIn(old_theme, readme)

    def test_cover_flow_delegates_to_xinghe_illustrations(self):
        cover_reference = (ROOT / "references" / "cover-and-publish.md").read_text(encoding="utf-8")
        self.assertIn("xinghe-illustrations-skill", cover_reference)
        self.assertFalse((ROOT / "cover" / "SKILL.md").exists(), "旧封面子 Skill 应移除")
        self.assertFalse((ROOT / "cover" / "config.example.json").exists(), "旧封面配置应移除")
        self.assertFalse((ROOT / "scripts" / "generate.py").exists(), "旧生图脚本应移除")

    def test_runtime_metadata_and_dependencies_exist(self):
        requirements_path = ROOT / "requirements.txt"
        metadata_path = ROOT / "agents" / "openai.yaml"
        self.assertTrue(requirements_path.exists(), "缺少 requirements.txt")
        self.assertTrue(metadata_path.exists(), "缺少 agents/openai.yaml")
        requirements = requirements_path.read_text(encoding="utf-8")
        metadata = metadata_path.read_text(encoding="utf-8")
        self.assertIn("markdown", requirements)
        self.assertIn("requests", requirements)
        self.assertIn("$xinghe-wechat-format", metadata)

    def test_only_core_workflow_scripts_are_shipped(self):
        scripts = {path.name for path in (ROOT / "scripts").glob("*.py")}
        self.assertEqual(
            {
                "format.py",
                "publish.py",
                "theme_lint.py",
                "xinghe_format.py",
                "zh_punctuation_fix.py",
            },
            scripts,
        )

    def test_old_personal_brand_and_generic_ai_flow_are_removed(self):
        format_script = (ROOT / "scripts" / "format.py").read_text(encoding="utf-8")
        publish_script = (ROOT / "scripts" / "publish.py").read_text(encoding="utf-8")
        gallery = (ROOT / "templates" / "gallery.html").read_text(encoding="utf-8")
        self.assertNotIn("小互说", format_script)
        self.assertNotIn("--smart", format_script)
        self.assertNotIn('author="小互"', publish_script)
        self.assertNotIn("Claude Code", gallery)

    def test_safe_entrypoint_preserves_source(self):
        entrypoint = ROOT / "scripts" / "xinghe_format.py"
        self.assertTrue(entrypoint.exists(), "缺少安全排版入口 scripts/xinghe_format.py")
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "article.md"
            output = temp / "output"
            image = temp / "diagram.png"
            image.write_bytes(b"test-image")
            original = "# 测试文章\n\n这是测试,包含中文标点!\n\n![示意图](diagram.png)\n"
            source.write_text(original, encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(entrypoint),
                    "--input",
                    str(source),
                    "--output",
                    str(output),
                    "--no-open",
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONUTF8": "1"},
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )

            self.assertEqual(0, result.returncode, (result.stdout or "") + (result.stderr or ""))
            self.assertEqual(original, source.read_text(encoding="utf-8"))
            self.assertTrue((output / "article" / "preview.html").exists())
            self.assertTrue((output / "_working" / "article.md").exists())
            self.assertTrue((output / "article" / "images" / "diagram.png").exists())

    def test_publish_dry_run_is_offline(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            article_dir = Path(temp_dir) / "article"
            image_dir = article_dir / "images"
            image_dir.mkdir(parents=True)
            (article_dir / "article.html").write_text(
                '<h1 style="font-size:24px">离线发布检查</h1><p>正文</p>',
                encoding="utf-8",
            )
            cover = image_dir / "cover.png"
            cover.write_bytes(b"test-cover")

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "publish.py"),
                    "--dir",
                    str(article_dir),
                    "--cover",
                    str(cover),
                    "--dry-run",
                    "--yes",
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONUTF8": "1"},
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )

            output = (result.stdout or "") + (result.stderr or "")
            self.assertEqual(0, result.returncode, output)
            self.assertIn("不会访问微信 API", output)
            self.assertNotIn("获取 access_token", output)

    def test_gallery_runs_on_windows_gbk_console(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "gallery.md"
            output = temp / "output"
            source.write_text("# 画廊测试\n\n正文内容。\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "xinghe_format.py"),
                    "--input",
                    str(source),
                    "--output",
                    str(output),
                    "--gallery",
                    "--no-open",
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONIOENCODING": "cp936"},
                capture_output=True,
                text=True,
                encoding="cp936",
                errors="replace",
                timeout=30,
            )

            message = (result.stdout or "") + (result.stderr or "")
            self.assertEqual(0, result.returncode, message)
            gallery_path = output / "gallery" / "gallery.html"
            self.assertTrue(gallery_path.exists())
            gallery_html = gallery_path.read_text(encoding="utf-8")
            for theme in ("xinghe-card", "xinghe-note"):
                marker = f'class="theme-preview" data-theme="{theme}"'
                start = gallery_html.index(marker)
                preview_head = gallery_html[start:start + 1800]
                self.assertIn("font-size:16px", preview_head, f"{theme} 未继承正文样式")
                self.assertIn("color:#263443", preview_head, f"{theme} 未继承正文颜色")

    def test_safe_entrypoint_does_not_mix_child_output_encodings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "encoding.md"
            source.write_text("# 编码测试\n\n正文。\n", encoding="utf-8")
            env = dict(os.environ)
            env.pop("PYTHONUTF8", None)
            env.pop("PYTHONIOENCODING", None)

            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    str(ROOT / "scripts" / "xinghe_format.py"),
                    "--input",
                    str(source),
                    "--output",
                    str(temp / "output"),
                    "--no-open",
                ],
                cwd=ROOT,
                env=env,
                capture_output=True,
                timeout=30,
            )

            output = (result.stdout or b"") + (result.stderr or b"")
            try:
                decoded = output.decode("utf-8")
            except UnicodeDecodeError as exc:
                self.fail(f"父子进程输出编码混用: {exc}")
            self.assertEqual(0, result.returncode, decoded)
            self.assertIn("源稿未修改", decoded)
            self.assertIn("星禾冷白卡片", decoded)


if __name__ == "__main__":
    unittest.main()
