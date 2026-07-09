# 微信排版引擎

运行或排查 `xinghe-wechat-format` 脚本时读取本文件。

## 脚本入口

- `scripts/zh_punctuation_fix.py`：渲染前修复中文正文附近的半角标点。
- `scripts/format.py`：把 Markdown 转换为微信公众号兼容预览 HTML 和可复制内联 HTML。
- `scripts/publish.py`：在用户明确确认后，把已渲染文章目录发布到微信公众号草稿箱。
- `scripts/theme_lint.py`：校验主题字号层级和移动端可读性。

## 必要配置

`scripts/format.py` 会从 skill 根目录读取 `config.json`。本地配置必须保持私有，不要提交真实凭据。

安全本地默认值：

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

## 排版命令

直接使用星禾主题：

```bash
python scripts/format.py --input "<article.md>" --theme xinghe-light
```

打开限定推荐的主题画廊：

```bash
python scripts/format.py --input "<article.md>" --gallery --recommend xinghe-light fresh-card glass-light notion-doc
```

自动化或测试运行：

```bash
python scripts/format.py --input "<article.md>" --theme xinghe-light --no-open --output "<output-dir>"
```

## 微信兼容说明

排版引擎会处理微信公众号编辑器限制：

- 把 CSS 写成每个元素上的内联 `style`。
- 用微信安全 HTML 模拟列表。
- 把外部链接转换为脚注。
- 把本地 Markdown 图片复制到输出目录。
- 支持部分 Obsidian 风格图片链接。
- 渲染 `:::dialogue`、`:::gallery`、`:::longimage` 等特殊容器。
- 渲染 `[!important]`、`[!tip]`、`[!warning]`、`[!note]` 等 callout。

不要在微信公众号文章里依赖 Mermaid、外部 JavaScript、远程 CSS 或不受支持的交互式嵌入。
