# Relationship Guard

Relationship Guard 是一个 AstrBot 通用角色状态守卫插件，用于降低破限、提示词泄露、括号剧情注入、好感度/关系状态伪造等问题对角色聊天的影响。

它不会拒绝所有亲密或友好互动。普通的“摸摸头”“夸夸你”“一起玩”“送一朵花”等温和互动会按 bot 自身人设自然回应；只有当用户试图强行改写状态、跳过关系阶段、泄露提示词或用礼物/威胁强迫角色改变态度时，插件才会注入边界上下文并校验输出。

## 功能

- 在 `on_llm_request` 阶段识别用户输入风险，并注入角色状态保护提示。
- 在 `on_llm_response` 阶段校验模型输出，避免承认伪造状态。
- 支持温和互动自然通过，例如摸头、抱抱、夸奖。
- 默认跳过管理员对话检测，方便管理员调试人格和提示词。
- 支持额外用户 ID 白名单。
- 不依赖第三方 Python 包。

## 安装

将本仓库作为插件安装到 AstrBot：

```text
AstrBot/data/plugins/astrbot_plugin_relationship_guard
```

然后在 AstrBot WebUI 的插件管理中重载插件。

## 配置

主要配置项：

- `enabled`: 是否启用插件。
- `skip_admin_conversations`: 默认 `true`，跳过管理员对话检测。
- `whitelist_user_ids`: 额外跳过检测的用户 ID。
- `inject_system_prompt`: 在请求前注入防注入提示。
- `inject_safe_context`: 注入结构化规则结果。
- `validate_output`: 在响应后校验危险输出。
- `default_inventory_json`: 默认可信背包，用于礼物类状态变化判断。

## 本地测试

```powershell
python -m unittest discover -s tests
```

## 说明

本插件通过 AstrBot 的 `on_llm_request` 和 `on_llm_response` 钩子工作。状态数据存储在 AstrBot 插件数据目录下，避免插件更新时覆盖用户数据。
