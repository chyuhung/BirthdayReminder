import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from zhdate import ZhDate


def _load_config():
    birthdays_json = os.environ.get('BIRTHDAYS_JSON')
    if not birthdays_json:
        raise RuntimeError('Missing BIRTHDAYS_JSON environment variable')

    config = json.loads(birthdays_json)
    reminder_days = config.get('reminder_days')
    birthdays = config.get('birthdays')

    if not isinstance(reminder_days, int) or reminder_days < 0:
        raise ValueError('reminder_days must be a non-negative integer')
    if not isinstance(birthdays, list):
        raise ValueError('birthdays must be a list')

    return reminder_days, birthdays


def _write_output(name, value):
    with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as fh:
        print(f'{name}={value}', file=fh)


def _days_between(left, right):
    delta = left - right
    return delta.days if hasattr(delta, 'days') else delta


def _classify_birthdays(today, today_lunar, birthdays, reminder_days):
    advance_names = []
    today_names = []
    tomorrow_names = []

    for entry in birthdays:
        name = entry.get("name")
        birthday = entry.get("birthday")
        if not name or not birthday:
            raise ValueError('Each birthday entry must include name and birthday')

        lunar = entry.get("lunar", True)

        if lunar:
            _, lunar_month, lunar_day = map(int, birthday.split("-"))
            birthday_lunar = ZhDate(today_lunar.lunar_year, lunar_month, lunar_day)
            if _days_between(birthday_lunar, today_lunar) < 0:
                # 如果农历生日已经过去，则计算下一年
                birthday_lunar = ZhDate(today_lunar.lunar_year + 1, lunar_month, lunar_day)
            days_difference = _days_between(birthday_lunar, today_lunar)
        else:
            birthday_solar = datetime.strptime(birthday, "%Y-%m-%d").date()
            if _days_between(birthday_solar, today) < 0:
                # 如果公历生日已经过去，则计算下一年
                birthday_solar = birthday_solar.replace(year=today.year + 1)
            days_difference = _days_between(birthday_solar, today)

        if days_difference == reminder_days:
            advance_names.append(name)
        elif days_difference == 0:
            today_names.append(name)
        elif days_difference == 1:
            tomorrow_names.append(name)

    return advance_names, today_names, tomorrow_names


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
    reminder_days, birthdays = _load_config()

    advance_names, today_names, tomorrow_names = _classify_birthdays(
        today,
        today_lunar,
        birthdays,
        reminder_days,
    )

    # 将结果写入环境变量，供后续步骤使用
    _write_output('REMINDER_DAYS', str(reminder_days))
    _write_output('SEND_ADVANCE_EMAIL', 'true' if advance_names else 'false')
    _write_output('SEND_TODAY_EMAIL', 'true' if today_names else 'false')
    _write_output('SEND_TOMORROW_EMAIL', 'true' if tomorrow_names else 'false')

    if advance_names:
        _write_output('ADVANCE_NAMES', '、'.join(advance_names))
    if today_names:
        _write_output('TODAY_NAMES', '、'.join(today_names))
    if tomorrow_names:
        _write_output('TOMORROW_NAMES', '、'.join(tomorrow_names))

if __name__ == "__main__":
    check_birthdays()
