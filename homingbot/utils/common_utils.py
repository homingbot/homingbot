import arrow

def getDate():
    today = arrow.utcnow()
    return arrow.Arrow(today.year, today.month, today.day).datetime
