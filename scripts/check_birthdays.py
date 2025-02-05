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
            lunar_year, lunar_month, lunar_day = map(int, birthday.split("-"))
            # 直接用今天的农历日期进行判断
            birthday_lunar = ZhDate(today_lunar.lunar_year,lunar_month,lunar_day)
            if  0 > birthday_lunar - today_lunar:
                # 如果农历生日已经过去，则计算下一年
                birthday_lunar = ZhDate(today_lunar.lunar_year + 1, lunar_month, lunar_day)
                if birthday_lunar - today_lunar < reminder_days+1:
                    advance_names.append(name)
            elif  0 < birthday_lunar - today_lunar < reminder_days+1:
                advance_names.append(name)
            elif 0 == birthday_lunar - today_lunar:
                today_names.append(name)
        else:
            birthday_solar = datetime.strptime(birthday, "%Y-%m-%d").date()
            if 0 > birthday_solar - today:
                # 如果公历生日已经过去，则计算下一年
                birthday_solar = birthday_solar.replace(year=today.year + 1)
                if birthday_solar - today < reminder_days+1:
                    advance_names.append(name)
            elif 0 < birthday_solar - today < reminder_days+1:
                advance_names.append(name)
            elif 0 == birthday_solar - today:
                today_names.append(name)

    # 将结果写入环境变量，供后续步骤使用
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

    # 直接打印结果测试
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