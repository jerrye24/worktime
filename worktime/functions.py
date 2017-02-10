#coding:utf8
import datetime

def time_delta(delta):
    seconds = delta.seconds
    hour = seconds // 3600
    minute = seconds % 3600 // 60
    time_at_work = datetime.time(hour, minute)
    return time_at_work


def hello_message(time):
    time = time.hour
    if time < 10 and time >= 5:
	return 'Доброе утро,'
    elif time < 16 and time >= 10:
	return 'Добрый день,'
    elif time < 23 and time >= 16:
	return 'Добрый вечер,'
    else:
	return 'Здравствуйте, '