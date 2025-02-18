import json
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from zhdate import ZhDate


def check_birthdays():
    # 创建东八区时区（UTC+8）
    utc_plus_8 = ZoneInfo("Asia/Shanghai")
    
    # 获取当前日期（东八区时间）
    today_dt = datetime.now(utc_plus_8)
    today = today_dt.date()
    print(f"今天的公历日期: {today}")

    # 将当前时间转换为不带时区的datetime对象
    today_naive = today_dt.replace(tzinfo=None)

    # 将公历日期转换为农历日期
    today_lunar = ZhDate.from_datetime(today_naive)
    print(f"今天的农历日期: {today_lunar}")
    
    # 读取从 Secret 中获取的 JSON 数据
    birthdays_json = os.environ['BIRTHDAYS_JSON']
    # 加载 JSON 数据
    config = json.loads(birthdays_json)
    reminder_days = config["reminder_days"]
    birthdays = config["birthdays"]

    remind_dates = [today + timedelta(days=i) for i in range(reminder_days + 1)]
    advance_names = []
    today_names = []
    days_difference = -1

    for entry in birthdays:
        name = entry["name"]
        birthday = entry["birthday"]
        lunar = entry.get("lunar", True)

        if lunar:
            lunar_year, lunar_month, lunar_day = map(int, birthday.split("-"))
            # 直接用今天的农历日期进行判断
            birthday_lunar = ZhDate(today_lunar.lunar_year,lunar_month,lunar_day)
            if birthday_lunar - today_lunar < 0:
                # 如果农历生日已经过去，则计算下一年
                birthday_lunar = ZhDate(today_lunar.lunar_year + 1, lunar_month, lunar_day)
            days_difference = birthday_lunar - today_lunar
        else:
            birthday_solar = datetime.strptime(birthday, "%Y-%m-%d").date()
            if birthday_solar - today < 0:
                # 如果公历生日已经过去，则计算下一年
                birthday_solar = birthday_solar.replace(year=today.year + 1)
            days_difference = birthday_solar - today

        # 统一处理逻辑
        if days_difference == reminder_days:
            advance_names.append(name)
        elif days_difference == 0:
            today_names.append(name)

    # 将结果写入环境变量，供后续步骤使用
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'REMINDER_DAYS={reminder_days}', file=fh)
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
