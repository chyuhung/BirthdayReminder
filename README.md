```markdown
# BirthdayReminder

## 简介

`BirthdayReminder` 是一个自动化的 GitHub Actions 工作流，旨在帮助用户管理和发送生日祝福邮件。通过定期检查生日信息，该工作流能够在特定的日期向指定收件人发送生日提醒，确保您不会错过祝福的机会。

## 特性

- 自动检查生日信息。
- 在生日当天发送邮件提醒。
- 使用 `dawidd6/action-send-mail` 发送邮件，支持 HTML 格式。
- 可通过 GitHub Actions 定时触发或手动触发工作流。

## 工作原理

1. **触发条件**：
   - 手动触发（`workflow_dispatch`）。
   - 当有新的提交或 PR 合并到 `main` 分支时。
   - 每天定时触发（使用 cron 表达式）。

2. **生日检查**：
   - 从 `birthdays.json` 文件中读取生日数据。
   - 检查今天是否有任何人的生日。

3. **发送邮件**：
   - 如果今天是某人的生日，使用配置的 SMTP 服务器发送祝福邮件。

## 使用指南

### 先决条件

1. 确保您有一个 GitHub 仓库。
2. 准备一个 `birthdays.json` 文件，格式如下：

   ```json
   [
     {
       "name": "Alice",
       "birthday": "2023-01-24"
     },
     {
       "name": "Bob",
       "birthday": "2023-10-15"
     }
   ]
   ```

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
3. 在生日当天，您将收到邮件提醒。
```

### 说明

- **项目结构**：README 现在包含了对项目结构的描述，特别是核心逻辑放置在 `scripts/` 目录中的说明。
- **工作流配置**：更新为新的工作流文件名 `birthday_reminder.yml`。
- **核心逻辑**：新增了关于核心逻辑代码的位置和作用的描述，以便用户了解代码组织方式。
