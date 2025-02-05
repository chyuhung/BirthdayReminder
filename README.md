# BirthdayReminder

## 简介

`BirthdayReminder` 是一个自动化的生日提醒系统，使用 Python 脚本和 GitHub Actions 工作流来管理和发送生日提醒邮件。实现在特定日期提醒用户当天或即将到来的亲友生日，确保不会错过送出生日祝福的机会。

## 特性

- 支持农历和阳历生日。
- 在生日当天或提前几天发送邮件提醒。
- 使用 `dawidd6/action-send-mail` 发送邮件，支持 HTML 格式。
- 通过 GitHub Actions 定时触发或手动触发工作流。

## 工作原理

1. **触发条件**：
   - 手动触发（`workflow_dispatch`）。
   - 当有新的提交或 PR 合并到 `main` 分支时。
   - 每天定时触发（使用 cron 表达式）。

2. **生日检查**：
   - 从 GitHub Secrets 中读取生日数据，而不是直接从文件中读取。
   - 检查当天和接下来几天的生日。

3. **发送邮件**：
   - 如果今天是某人的生日，或在未来几天内有生日，使用配置的 SMTP 服务器发送提醒邮件到用户邮箱。

## 使用指南

### 先决条件

1. 确保您有一个 GitHub 仓库。
2. 在 GitHub 仓库设置中添加以下 Secrets：
   - **BIRTHDAYS_JSON**: 包含生日数据的 JSON 字符串（格式见下）。
   - **EMAIL**: 发件人的邮件地址。
   - **EMAIL_PASSWORD**: 发件人的邮件密码。
   - **TO_EMAIL**: 用户的邮箱地址（可以是多个，需用逗号分隔）。

   *Tips: 推荐使用腾讯企业邮箱（使用密码而非授权码，避免过期无法发送邮件）。*

### JSON 文件格式

以下是 `BIRTHDAYS_JSON` 的示例格式：

```json
{
  "reminder_days": 5,
  "birthdays": [
    {
      "name": "农历Tom",
      "birthday": "2024-12-26",
      "lunar": true
    },
    {
      "name": "新历Bob",
      "birthday": "2025-01-25",
      "lunar": false
    }
  ]
}
```

### 工作流配置

将工作流配置添加到 `.github/workflows/birthday_reminder.yml` 文件中。

### 核心逻辑

核心逻辑代码保存在 `scripts/check_birthdays.py` 文件中，负责读取生日数据并检查是否需要发送提醒邮件。

### 运行工作流

1. 提交更改并推送到 `main` 分支。
2. 在 GitHub Actions 页面上监控工作流的运行状态。
3. 在生日当天或提前几天，用户将收到亲友生日提醒邮件。

## 代码结构

- **`check_birthdays.py`**: 主要逻辑代码，负责检查生日并输出人员名单。
- **`BIRTHDAYS_JSON`**: 存储生日信息的配置文件（数据从 Secrets 中读取）。

## 注意事项

- 确保日期格式正确，农历日期需使用正确的农历年份。
- 本项目使用 `zhdate` 库进行农历转换，请确保已正确安装依赖。
- 请遵循 GitHub Secrets 的使用规范，确保敏感信息的安全性。