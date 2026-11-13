import datetime, exercise41_bday_messages

today = datetime.date.today()
next_birthday = datetime.date(year=2027, month=11, day=13)

days_away = next_birthday - today

if today == next_birthday:
    print(exercise41_bday_messages.random_message)
else:
    print(f'My next birthday is {days_away.days} days away!')
