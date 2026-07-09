from datetime import timedelta

def ist_time(dt):
    if dt:
        return dt + timedelta(hours=5, minutes=30)
    return dt