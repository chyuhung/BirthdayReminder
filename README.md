# BirthdayReminder

## 简介

`BirthdayReminder` 是一个自动化的生日提醒系统，使用 Python 脚本和 GitHub Actions 工作流来管理和发送生日祝福邮件。该系统能够在特定日期提醒用户即将到来的生日或当天的生日，确保用户不会错过祝福的机会。

## 特性

- 支持农历和阳历生日的检查。
- 在生日当天或提前几天发送邮件提醒。
- 使用 `dawidd6/action-send-mail` 发送邮件，支持 HTML 格式。
- 可通过 GitHub Actions 定时触发或手动触发工作流。

## 工作原理

1. **触发条件**：
   - 手动触发（`workflow_dispatch`）。
   - 当有新的提交或 PR 合并到 `main` 分支时。
   - 每天定时触发（使用 cron 表达式）。

2. **生日检查**：
   - 从 `birthdays.json` 文件中读取生日数据，包括农历和阳历生日。
   - 检查当天和接下来几天的生日。

3. **发送邮件**：
   - 如果今天是某人的生日，或在未来几天内有生日，使用配置的 SMTP 服务器发送祝福邮件。

## 使用指南

### 先决条件

1. 确保您有一个 GitHub 仓库。
2. 准备一个 `birthdays.json` 文件，格式如下：

   json
   {
     "reminder_days": 3,
     "birthdays": [
       {
         "name": "农历今天测试Tom",
         "birthday": "2024-12-26",
         "lunar": true
       },
       {
         "name": "新历今天测试Bob",
         "birthday": "2025-01-25",
         "lunar": false
       }
     ]
   }
   

3. 在 GitHub 仓库设置中添加以下 Secrets：
   - **EMAIL**: 您的邮件地址。
   - **EMAIL_PASSWORD**: 您的邮件密码或应用程序密码。
   - **TO_EMAIL**: 收件人的邮箱地址（可以是多个，需用逗号分隔）。

### 工作流配置

将工作流配置添加到您的 `.github/workflows/birthday_reminder.yml` 文件中。

### 核心逻辑

核心逻辑代码保存在 `scripts/check_birthdays.py` 文件中，负责读取生日数据并检查是否需要发送邮件。

### 运行工作流

1. 提交更改并推送到 `main` 分支。
2. 在 GitHub Actions 页面上监控工作流的运行状态。
3. 在生日当天或提前几天，您将收到邮件提醒。

## 代码结构

- **`check_birthdays.py`**: 主要逻辑代码，负责检查生日并输出需要发送邮件的人员名单。
- **`birthdays.json`**: 存储生日信息的配置文件，包括每个人的姓名、生日和是否为农历生日。

## 注意事项

- 确保日期格式正确，农历日期需使用正确的农历年份。
- 本项目使用 `zhdate` 库进行农历转换，请确保已正确安装依赖。
