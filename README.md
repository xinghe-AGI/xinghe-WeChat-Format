# xinghe-WeChat-Format

这是基于 [`xiaohuailabs/xiaohu-wechat-format`](https://github.com/xiaohuailabs/xiaohu-wechat-format) 改造的个人公众号排版 skill。机器可读 skill 名称为 `xinghe-wechat-format`，展示名为 `xinghe-WeChat-Format`。它保留原项目的微信兼容 HTML 渲染、主题系统、标点修复和草稿箱发布能力，并把默认体验收束为星禾个人 IP 风格：冷白/浅蓝灰底、深蓝黑正文、橙色行动线、白板/卡片/便签式信息层。

## 它能做什么

- 把 Markdown、纯文本或粗糙笔记转换成微信公众号可复制的内联样式 HTML。
- 默认使用 `xinghe-light` 主题，形成稳定的个人内容视觉。
- 在不改写作者语气的前提下，补充必要标题、列表、callout、引用和图片容器。
- 可按需衔接 `xinghe-illustrations-skill` 生成公众号封面 brief、prompt-only 或 manifest。
- 在用户明确确认后，可使用 `publish.py` 发布到微信公众号草稿箱。

## 快速开始

安装依赖：

```bash
pip install markdown requests
```

准备配置：

```bash
cp config.example.json config.json
```

建议把 `config.json` 调整为：

```json
{
  "output_dir": "outputs/wechat-format",
  "vault_root": ".",
  "image_search_paths": [],
  "settings": {
    "default_theme": "xinghe-light",
    "auto_open_browser": true,
    "header_author_label": ""
  },
  "wechat": {
    "app_id": "",
    "app_secret": "",
    "author": ""
  }
}
```

真实 AppID、AppSecret、API key 和 token 只放在私有本地配置或环境变量中，不要写进文档、提交记录或聊天内容。

## 排版文章

直接使用星禾主题：

```bash
python scripts/format.py --input article.md --theme xinghe-light
```

测试时不打开浏览器：

```bash
python scripts/format.py --input article.md --theme xinghe-light --no-open --output outputs/wechat-format
```

如需比较少量备选风格：

```bash
python scripts/format.py --input article.md --gallery --recommend xinghe-light fresh-card glass-light notion-doc
```

生成后打开 `preview.html`，点击“复制到微信”，再粘贴到微信公众号后台。

## 推荐工作流

1. 读取文章，确认标题、字数、文章类型和是否包含图片/代码/表格。
2. 在工作副本上运行标点修复，不默认原地改源稿。
3. 只补充必要 Markdown 结构：标题、段落、列表、少量加粗、少量 callout。
4. 使用 `xinghe-light` 渲染预览 HTML。
5. 如需封面，衔接 `xinghe-illustrations-skill`；真实生图前必须确认外部上传授权。
6. 如需发布，确认目标公众号、标题、作者、摘要、封面图、文章目录和凭据使用权限后，再调用 `publish.py`。

## 星禾主题风格

`themes/xinghe-light.json` 的设计目标：

- 冷白或极浅蓝灰背景。
- 深蓝黑正文，阅读稳定。
- 暖橙色用于关键词、行动线和少量强调。
- 低饱和绿、黄、紫、珊瑚粉用于步骤、提示、分支和风险。
- 标题像白板标签，引用像便签，重点块像内容卡片，图片外框像轻量工作台。

避免商业海报、厚重渐变、赛博 UI、大面积黄色、儿童贴纸感和密集 PPT 信息块。

## 常用 Markdown 元素

```markdown
> [!important] 核心判断
> 这里写真正需要读者记住的结论。

> [!tip] 小技巧
> 这里写一个实用方法。

:::gallery[截图组]
![](img1.png)
![](img2.png)
![](img3.png)
:::

:::longimage[流程长图]
![](flow.png)
:::
```

使用边界：

- callout 总数不超过 4 个。
- 加粗每段不超过 2 处。
- 表格不超过 4 列。
- `:::gallery` 只用于 3 张以上相关图片。
- `:::longimage` 只用于真实长截图、流程图或架构图。

## 发布到微信公众号草稿箱

发布前必须在 `config.json` 或安全环境变量中配置公众号凭据，并确认公众号后台 IP 白名单。

只在用户确认所有发布信息后运行：

```bash
python scripts/publish.py --dir "<rendered-article-dir>" --cover "<cover-image-path>"
```

支持参数可查看：

```bash
python scripts/publish.py --help
```

## 文件结构

```text
SKILL.md                         # Codex 调用入口，保持精简
references/
  wechat-engine.md               # 脚本和微信兼容说明
  xinghe-layout-style.md         # 星禾排版风格
  content-structure-rules.md     # 内容结构规则
  cover-and-publish.md           # 封面与发布门禁
themes/
  xinghe-light.json              # 星禾默认主题
scripts/
  format.py                      # Markdown 转微信 HTML
  publish.py                     # 发布到公众号草稿箱
  zh_punctuation_fix.py          # 中文标点质检
  theme_lint.py                  # 主题校验
```

## 验证

```bash
python scripts/theme_lint.py xinghe-light
python scripts/format.py --input article.md --theme xinghe-light --no-open
```

在 Windows 终端遇到中文或勾号输出编码问题时，可先设置：

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
```

## 来源与许可

本工作区副本基于 `xiaohuailabs/xiaohu-wechat-format` 改造，保留原项目 MIT License。星禾风格规则来自本机 `xinghe-illustrations-skill` 的个人 IP 视觉系统。
