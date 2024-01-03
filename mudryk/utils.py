def translate_date(date):
    day = date.split(',')[0]
    number = date.split(' ')[1]
    month = date.split(' ')[2]
    translated_day = None
    translated_month = None
    if day == 'Monday':
        translated_day = 'Понеділок'
    elif day == 'Tuesday':
        translated_day = 'Вівторок'
    elif day == 'Wednesday':
        translated_day = 'Середа'
    elif day == 'Thursday':
        translated_day = 'Четвер'
    elif day == 'Friday':
        translated_day = "П'ятниця"
    elif day == 'Saturday':
        translated_day = 'Субота'
    elif day == 'Sunday':
        translated_day = 'Неділя'

    if month == 'January':
        translated_month = 'Січень'
    elif month == 'February':
        translated_month = 'Лютий'
    elif month == 'March':
        translated_month = 'Березень'
    elif month == 'April':
        translated_month = 'Квітень'
    elif month == 'May':
        translated_month = 'Травень'
    elif month == 'June':
        translated_month = 'Червень'
    elif month == 'July':
        translated_month = 'Липень'
    elif month == 'August':
        translated_month = 'Серпень'
    elif month == 'September':
        translated_month = 'Вересень'
    elif month == 'October':
        translated_month = 'Жовтень'
    elif month == 'November':
        translated_month = 'Листопад'
    elif month == 'December':
        translated_month = 'Грудень'
    translated_date = f'{translated_day}, {number} {translated_month}'
    return translated_date
