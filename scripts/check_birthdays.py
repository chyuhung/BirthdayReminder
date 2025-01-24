import json
import os
from datetime import datetime, timedelta, timezone
from zhdate import ZhDate

def clear_output_variable(variable_name):
    """清除特定环境变量的值"""
    output_file = os.environ.get('GITHUB_OUTPUT')
    if output_file:
        with open(output_file, 'r') as file:
            lines = file.readlines()
        
        with open(output_file, 'w') as file:
            for line in lines:
                if not line.startswith(f"{variable_name}="):
                    file.write(line)

def check_birthdays():
    # 获取当前日期（UTC时区）
    today = datetime.now(timezone.utc).date()
    
    # 打开并读取包含生日信息的JSON文件
    with open("birthdays.json") as f:
        config = json.load(f)
        reminder_days = config["reminder_days"]
        birthdays = config["birthdays"]

    remind_dates = [today + timedelta(days=i) for i in range(reminder_days + 1)]
    advance_names = []
    today_names = []

    for entry in birthdays:
        name = entry["name"]
        birthday = entry["birthday"]
        lunar = entry.get("lunar", True)

        if lunar:
            year, month, day = map(int, birthday.split("-"))
            solar_date = ZhDate(year, month, day).to_datetime().date()
        else:
            solar_date = datetime.strptime(birthday, "%Y-%m-%d").date()

        if solar_date in remind_dates:
            if solar_date == today:
                today_names.append(name)
            else:
                advance_names.append(name)

    # 在写入新的值之前，清除旧的环境变量值
    clear_output_variable('SEND_ADVANCE_EMAIL')
    clear_output_variable('ADVANCE_NAMES')
    clear_output_variable('SEND_TODAY_EMAIL')
    clear_output_variable('TODAY_NAMES')

    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        if advance_names:
            print(f'SEND_ADVANCE_EMAIL=true', file=fh)
            print(f'ADVANCE_NAMES={"、".join(advance_names)}', file=fh)
        else:
            print(f'SEND_ADVANCE_EMAIL=false', file=fh)
        
        if today_names:
            print(f'SEND_TODAY_EMAIL=true', file=fh)
            print(f'TODAY_NAMES={"、".join(today_names)}', file=fh)
        else:
            print(f'SEND_TODAY_EMAIL=false', file=fh)

if __name__ == "__main__":
    check_birthdays()