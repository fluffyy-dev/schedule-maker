import pandas as pd

# lo mean 'list of'

loDays = pd.read_csv('schedule-info.csv')

# types of days
#   1 - normal day (one person, reg on-call)
#   2 - 2 person day (two people, reg on-call)
#   3 - 24 hour day (one person, 24 hr on-call)
#   4 - 24 hour, 2 person day (two people, 24 hr on-call)

# weekday types
#   mon-thu - 1
#   fri - 2
#   sat - 4
#   sun - 3

# special days (type 3)
#  - vetrens day (Nov 11)
#  - columbus day (Oct 12)
#  - thanksgiving (fourth thursday of nov) + fri and sat after

## 12 RAs, 6 new, 6 old

# Create day type list
loTypes = pd.DataFrame(columns=['Day', 'Type'])
thursOfNov = 0
tgDay = -1
for i, dayData in loDays.iterrows():
    day = dayData.at['Day']
    dayOfWeek = day.split("-")[0]
    dayOfMonth = int(day.split("-")[2])
    month = day.split("-")[1]

    ## for thanksgiving
    if month == "Nov" and dayOfWeek == "Thu":
        thursOfNov += 1

    ## holidays
    ColumbusDay = month == "Oct" and dayOfMonth == 12
    VetsDay = month == "Nov" and dayOfMonth == 11
    Thanksgiving = month == "Nov" and dayOfWeek == "Thu" and thursOfNov == 4
    tgFri = month == "Nov" and dayOfWeek == "Fri" and dayOfMonth == tgDay + 1
    tgSat = month == "Nov" and dayOfWeek == "Sat" and dayOfMonth == tgDay + 2

    ## determines day type
    dayType = 1
    if Thanksgiving:
        tgDay = dayOfMonth
        dayType = 3
    elif ColumbusDay or VetsDay or dayOfWeek == "Sun" or tgFri or tgSat:
        dayType = 3
    elif dayOfWeek == "Fri":
        dayType = 2
    elif dayOfWeek == "Sat":
        dayType = 4
    
    loTypes.loc[len(loTypes)] = [day, dayType]



# with pd.ExcelWriter("created-type-list.xlsx") as writer: # saves the data to a spreadsheet
#     loTypes.to_excel(writer)