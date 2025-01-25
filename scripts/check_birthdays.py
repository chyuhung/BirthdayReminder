import json
import os
from datetime import datetime, timedelta, timezone
from zhdate import ZhDate

def check_birthdays():
    # # 获取当前日期（UTC时区）
    # today = datetime.now(timezone.utc).date()

    # 创建东八区时区（UTC+8）
    utc_plus_8 = timezone(timedelta(hours=8))
    # 获取当前日期（东八区时间）
    today = datetime.now(utc_plus_8).date()
    print(today)
    
    # 打开并读取包含生日信息的JSON文件
    with open("birthdays.json") as f:
        config = json.load(f)
        reminder_days = config["reminder_days"]
        birthdays = config["birthdays"]

    remind_dates = [today + timedelta(days=i) for i in range(reminder_days + 1)]
    print(remind_dates)
    advance_names = []
    today_names = []

    for entry in birthdays:
        name = entry["name"]
        birthday = entry["birthday"]
        lunar = entry.get("lunar", True)

        if lunar:
            year, month, day = map(int, birthday.split("-"))
            # 农历年特殊处理，需要传入正确的农历年（春节分割），才能正确转换成公历日期
            solar_date = ZhDate(today.year, month, day).to_datetime().date()
        else:
            solar_date = datetime.strptime(birthday, "%Y-%m-%d").date()

        if solar_date in remind_dates:
            if solar_date == today:
                today_names.append(name)
            else:
                advance_names.append(name)

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

    # # 直接打印结果测试
    # if advance_names:
    #     print(f'SEND_ADVANCE_EMAIL=true')
    #     print(f'ADVANCE_NAMES={"、".join(advance_names)}')
    # else:
    #     print(f'SEND_ADVANCE_EMAIL=false')

    # if today_names:
    #     print(f'SEND_TODAY_EMAIL=true')
    #     print(f'TODAY_NAMES={"、".join(today_names)}')
    # else:
    #     print(f'SEND_TODAY_EMAIL=false')

if __name__ == "__main__":
    check_birthdays()