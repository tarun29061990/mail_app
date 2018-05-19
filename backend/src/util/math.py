import datetime
######
# This function calculate the rent on pro rata basis by taking into account
# whichever date is greater notice period end date or move out date
# params:
# nped - notice period end date in python date format
# mod - move out date in python date format
# amount - amount for the whole month on which the calculation should be based
######

def get_days_array():
    if datetime.datetime.now().year % 4 == 0: #if its a leap year
        days_arr = [31,29,31,30,31,30,31,31,30,31,30,31]
    else:
        days_arr = [31,28,31,30,31,30,31,31,30,31,30,31]

    return days_arr

def calculate_pro_rata_rent(nped, mod, amount):
    today_date = datetime.datetime.now()
    td = datetime.date(today_date.year, today_date.month, today_date.day)

    days_arr = get_days_array()

    if (nped - mod).days < 0:
        calculation_date = mod
    else:
        calculation_date = nped

    if calculation_date.month == td.month:
        days = (calculation_date -td).days + 1
        pro_rata_amount = int(amount/days_arr[calculation_date.month -1])*days
    else:
        pro_rata_amount = int(amount) + int(amount/days_arr[calculation_date.month-1])*calculation_date.day

    return pro_rata_amount

def calculate_fmr_amount(amount, occupancy_date):
    days_arr = get_days_array()
    return int(((amount)/days_arr[occupancy_date.month-1])*(days_arr[occupancy_date.month-1] - occupancy_date.day+1))