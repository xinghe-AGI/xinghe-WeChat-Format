# 封面与发布

用户要求封面、发布包或微信公众号草稿箱发布时读取本文件。

## 封面衔接

封面默认停在 prompt-only 或 manifest 输出。使用 `xinghe-illustrations-skill`，并遵守公众号封面标准：

- 比例：`2.35:1`
- 标题：尽量 8-18 个中文字符，1-2 行
- 背景：冷白或极浅蓝灰
- 星禾动作：整理卡片、连接流程线、标注关键点或铺开证据
- 气质：清爽、个人化、可信，不像销售海报

真实生图前必须确认外部上传授权，因为文章衍生文本、prompt、本地参考图和图片资产可能会发送到图片 API。

## 发布门禁

运行 `scripts/publish.py` 前必须确认：

- 目标公众号或草稿箱目标
- 标题
- 作者
- 摘要
- 封面图片路径
- 已渲染文章目录
- 是否只创建草稿
- 是否允许使用本地配置凭据

缺任何一项都必须暂停询问，不要猜发布元数据。

## 凭据边界

永远不要写入真实值：

- 微信 AppID
- 微信 AppSecret
- API key
- access token
- permission code
- 私有完整 endpoint

真实凭据只能放在环境变量或私有本地 `config.json` 中。示例必须为空值或占位符。

## 发布命令

只有确认后才运行：

```bash
python scripts/publish.py --dir "<rendered-article-dir>" --cover "<cover-image-path>"
```

API 返回成功不等于用户已能阅读草稿。报告命令结果，并在必要时请用户到微信公众号后台验证草稿是否可见。

