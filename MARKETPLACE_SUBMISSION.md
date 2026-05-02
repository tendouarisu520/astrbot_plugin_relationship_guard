# AstrBot 插件市场提交信息

> 官方流程：先将插件代码推送到 GitHub 插件仓库，再到 https://plugins.astrbot.app 点击右下角 `+` 填写信息，提交后会跳转到 AstrBot 仓库 Issue 页面确认创建。

## 基本信息

- 插件名称: `astrbot_plugin_relationship_guard`
- 展示名称: `Relationship Guard`
- 作者: `tendouarisu520`
- 版本: `0.1.0`
- 仓库: `https://github.com/tendouarisu520/astrbot_plugin_relationship_guard`
- AstrBot 版本: `>=4.16,<5`

## 简介

防破限、防括号剧情注入、防好感度/关系状态伪造的角色状态守卫插件。支持温和互动自然通过，重点审查提示词泄露、状态伪造、关系跳跃、剧情强行写入和情感勒索式引导。

## 支持平台

本插件基于 AstrBot LLM 请求/响应钩子工作，不绑定具体平台适配器。`metadata.yaml` 中声明了官方文档列出的主流平台适配器：

- `aiocqhttp`
- `qq_official`
- `telegram`
- `discord`
- `slack`
- `kook`
- `satori`
- `wecom`
- `lark`
- `dingtalk`
- `vocechat`
- `weixin_official_account`
- `misskey`
- `line`

## 测试

```powershell
python -m unittest discover -s tests -p 'test_*.py' -v
```

当前发布目录测试结果：9 tests OK。
