---
name: xinghe-wechat-format
description: 将中文 Markdown、纯文本或粗糙笔记排版为星禾个人风格的微信公众号文章。用户要求公众号排版、微信排版、format、xinghe-WeChat-Format、发布草稿准备、星禾个人 IP 文章排版、封面衔接或公众号草稿箱发布时使用。默认使用 xinghe-light 主题，保留原文措辞；封面真实生图和微信公众号发布前必须获得用户明确确认。
---

# xinghe-WeChat-Format

这个 skill 把中文 Markdown、纯文本或粗糙笔记转换为微信公众号兼容的内联样式 HTML，并默认使用星禾个人风格排版。保持 skill 精简：稳定渲染交给脚本，细节规则按需读取 references。

## 按需读取

- `references/wechat-engine.md`：脚本入口、必要配置、输出行为和微信兼容说明。
- `references/xinghe-layout-style.md`：星禾排版风格、默认主题、配色和反模式。
- `references/content-structure-rules.md`：标题、列表、callout、引用、金句卡、画廊、长图、表格和代码块的使用边界。
- `references/cover-and-publish.md`：封面衔接、发布确认、凭据边界和外部投递检查。

## 默认工作流

### 1. 确认来源

接受文件路径、粘贴正文、Markdown 草稿或粗糙笔记。用户没有提供内容或路径时，先请用户提供文章来源。

读取来源后，确认：

- 标题或可能的标题
- 近似字数
- 文章类型：分析、教程、产品/工具笔记、访谈、随笔、方法论或发布说明
- 是否包含图片、代码、表格、链接或对话

不要改写作者语气。只添加阅读和微信渲染需要的结构。

### 2. 准备 Markdown

先在工作副本上运行标点质检；除非用户明确要求修改源文件，否则不要直接改原稿。

```bash
python scripts/zh_punctuation_fix.py "<working-article.md>" --write
```

如果文章已有可用 Markdown 结构，保留原结构。若文章是纯文本或粗糙笔记，只添加必要结构标记：

- 在真实主题转换处添加 `##` 标题
- 在语义转换处拆段
- 对真实并列项或步骤使用列表
- 用 `**加粗**` 做少量扫读锚点
- 只给高价值判断、技巧、风险或补充信息使用 callout

把准备后的文件保存到配置输出目录或本次任务的临时输出目录。默认避免原地覆盖源草稿。

### 3. 应用星禾排版

默认使用 `xinghe-light` 主题。除非用户要求比较风格，否则优先直接渲染，不默认打开完整主题画廊。

```bash
python scripts/format.py --input "<prepared-article.md>" --theme xinghe-light
```

如果用户想比较备选风格，打开画廊并只推荐星禾兼容主题：

```bash
python scripts/format.py --input "<prepared-article.md>" --gallery --recommend xinghe-light fresh-card glass-light notion-doc
```

测试或自动化检查时使用 `--no-open`。

### 4. 封面与发布门禁

默认交付点是已检查的预览 HTML，用户可复制到微信公众号后台。

如需封面，衔接 `xinghe-illustrations-skill`，默认只输出 prompt-only 或 manifest。只有用户明确授权真实生图和外部上传文章衍生内容后，才进入真实图片生成。公众号封面比例使用 `2.35:1`。

发布前，绝不直接调用 `scripts/publish.py`。必须先确认：

- 目标公众号或草稿箱目标
- 标题、作者、摘要和封面图
- 要发布的文章目录
- 披露范围
- 是否允许使用本地配置的微信凭据

不要把 AppID、AppSecret、API key、access token、permission code 或真实 endpoint 写入 skill 文档、示例、references 或最终回复。

## 默认主题策略

- 主主题：`xinghe-light`
- 备选主题：`fresh-card`、`glass-light`、`notion-doc`
- 默认保持个人风格稳定，不做花哨主题轮换。
- 只有用户明确要求其他视觉方向时，才使用其他主题。

## 必须暂停的情况

遇到以下情况先暂停确认：

- 缺少文章来源
- 操作会原地修改源文件
- 封面生成会上传本地内容或参考图
- 发布会向微信或其他外部系统发送数据
- 凭据缺失、仍是占位符，或被意外写入文件
- 输出文件会覆盖已有交付物
