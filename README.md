# xinghe-WeChat-Format

面向个人公众号创作的星禾风格排版 Skill。它把 Markdown 文章转换为微信公众号兼容的内联样式 HTML，只保留三种用途清晰的星禾主题，并可在确认后衔接封面与草稿箱发布。

本项目基于 [xiaohuailabs/xiaohu-wechat-format](https://github.com/xiaohuailabs/xiaohu-wechat-format) 改造，保留原项目的微信渲染、标点检查和发布能力。

## 三个主题

| 主题 | 风格 | 适合内容 |
|---|---|---|
| `xinghe-light` | 冷白长文、橙色行动线、轻量白板标签 | 技术长文、产品分析、通用文章 |
| `xinghe-card` | 分区和卡片更明确、步骤感更强 | 教程、清单、工具拆解 |
| `xinghe-note` | 边界更轻、段落更松弛、便签引用 | 方法论、复盘、随笔 |

画廊只展示这三个主题，不再附带通用主题库。

## 安装

```bash
pip install -r requirements.txt
```

仅排版时可以直接运行，不必先创建 `config.json`。需要设置输出目录、作者或公众号凭据时，再复制私有配置：

```bash
cp config.example.json config.json
```

`config.json` 已被 Git 忽略。真实 AppID、AppSecret、API key 和 token 不应写入文档或提交记录。

## 快速使用

默认主题：

```bash
python scripts/xinghe_format.py --input article.md
```

指定知识卡片主题：

```bash
python scripts/xinghe_format.py --input article.md --theme xinghe-card
```

比较全部三个主题：

```bash
python scripts/xinghe_format.py --input article.md --gallery
```

自动化或测试时不打开浏览器：

```bash
python scripts/xinghe_format.py --input article.md --no-open --output outputs/wechat-format
```

安全入口会：

1. 把文章复制到 `<output>/_working/`。
2. 只在工作副本上修复中文标点。
3. 保留源稿相对图片的解析位置。
4. 生成 `preview.html` 和 `article.html`。
5. 发现已有输出时停止；确认覆盖后才使用 `--force`。

## 输出结构

```text
outputs/wechat-format/
  _working/
    article.md
  article/
    article.html
    preview.html
    images/
```

打开 `preview.html`，点击“复制到微信”，再粘贴到微信公众号后台。

## 封面与发布

封面统一衔接 `xinghe-illustrations-skill`。默认先生成 prompt-only 或 manifest；真实生图上传文章内容或参考图前需要确认。公众号封面比例使用 `2.35:1`。

发布前确认目标公众号、标题、作者、摘要、封面图、文章目录和凭据使用权限，然后运行：

先做完全离线的发布前检查：

```bash
python scripts/publish.py --dir "<rendered-article-dir>" --cover "<cover-image-path>" --dry-run --yes
```

确认无误后再运行真实发布：

```bash
python scripts/publish.py --dir "<rendered-article-dir>" --cover "<cover-image-path>"
```

发布是外部投递，不会由默认排版流程自动触发。

## 主要文件

```text
SKILL.md
agents/openai.yaml
themes/
  xinghe-light.json
  xinghe-card.json
  xinghe-note.json
scripts/
  xinghe_format.py
  format.py
  zh_punctuation_fix.py
  theme_lint.py
  publish.py
references/
  wechat-engine.md
  xinghe-layout-style.md
  content-structure-rules.md
  cover-and-publish.md
```

## 验证

```bash
python -X utf8 -m unittest tests.test_skill_contract -v
python scripts/theme_lint.py
```

## 许可与来源

本项目基于 `xiaohuailabs/xiaohu-wechat-format` 改造，沿用原项目许可与归因。星禾视觉规则来自 `xinghe-illustrations-skill` 的个人 IP 风格系统。
