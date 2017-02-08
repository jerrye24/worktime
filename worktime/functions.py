import datetime

def time_delta(delta):
    seconds = delta.seconds
    hour = seconds // 3600
    minute = seconds % 3600 // 60
    time_at_work = datetime.time(hour, minute)
    return time_at_work
