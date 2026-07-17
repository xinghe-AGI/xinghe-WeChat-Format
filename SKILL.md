---
name: xinghe-wechat-format
description: 将中文 Markdown、纯文本或粗糙笔记排版为星禾个人风格的微信公众号文章。用户要求公众号排版、微信排版、xinghe-WeChat-Format、星禾主题、封面衔接或公众号草稿箱发布时使用。提供 xinghe-light、xinghe-card、xinghe-note 三种主题；默认保留原文措辞和源文件，封面真实生图与发布前必须获得明确确认。
---

# xinghe-WeChat-Format

把文章转换为微信公众号兼容的内联样式 HTML，并稳定输出星禾个人风格。默认只做排版，不自动生图，不自动发布。

## 按需读取

- 脚本、配置或微信兼容问题：读取 `references/wechat-engine.md`。
- 选择主题或判断视觉风格：读取 `references/xinghe-layout-style.md`。
- 需要增强文章结构：读取 `references/content-structure-rules.md`。
- 需要封面或发布：读取 `references/cover-and-publish.md`。

## 工作流

### 1. 读取文章

确认标题、文章类型、图片、代码、表格和链接。保留作者措辞，只补充阅读所需的标题、段落、列表、少量加粗和 callout。

### 2. 选择主题

| 主题 | 适用内容 |
|---|---|
| `xinghe-light` | 默认；技术长文、产品分析、通用公众号文章 |
| `xinghe-card` | 教程、清单、工具拆解、知识密度较高的文章 |
| `xinghe-note` | 方法论、复盘、随笔和个人观察 |

用户未指定时使用 `xinghe-light`。只有用户要求比较时才打开三主题画廊。

### 3. 安全排版

默认使用安全入口。它复制工作稿、在副本上修复中文标点，再调用渲染脚本，不修改源文件：

```bash
python scripts/xinghe_format.py --input "<article.md>" --theme xinghe-light
```

比较三个主题：

```bash
python scripts/xinghe_format.py --input "<article.md>" --gallery
```

输出已存在时不要擅自覆盖；先更换输出目录，或获得确认后使用 `--force`。

### 4. 交付与门禁

默认交付 `preview.html` 和 `article.html`。如需封面，衔接 `xinghe-illustrations-skill`，先输出 prompt-only 或 manifest；真实生图涉及外部上传时必须确认。公众号封面比例为 `2.35:1`。

调用 `scripts/publish.py` 前必须确认：

- 目标公众号或草稿箱
- 标题、作者、摘要和封面图
- 文章目录与披露范围
- 是否允许使用本地微信凭据

不在 Skill、文档、示例或回复中写入 AppID、AppSecret、API key 或 access token。

## 必须暂停

- 缺少文章来源。
- 用户要求的操作会修改源稿。
- 输出已存在且未获得覆盖确认。
- 封面生成会上传本地内容或参考图。
- 发布会向微信或其他外部系统发送数据。
- 凭据缺失、仍是占位符或意外出现在待提交文件中。
