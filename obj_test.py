from obj_scheduling_tool import Scheduler

## For reference:
'''
timeslots = {
    "9:00 - 9:45" : 0,
    "9:45 - 10:30" : 1,
    "10:30 - 11:15" : 2,
    "11:15 - 12:00" : 3,
    "12:00 - 12:45" : 4,
    "12:45 - 1:30" : 5,
    "1:30 - 2:15" : 6,
    "2:15 - 3:00" : 7,
} #8 timeslots
'''

time_slots_companies = [1,0,2] ## Starting time period of companies
panel_no_companies = [17, 10, 10] ## No of panels of companies
slots_companies = [8,8,8] ## Slots per company
no_of_companies = 3 ##Number of companies
companies = ['Qualcomm','Micron','TI'] ## Names of companies, correponding csv files must be present in the folder

## Instantiate object like this ->
schedule = Scheduler(no_of_companies,companies,time_slots_companies,panel_no_companies,slots_companies)

df = schedule.get_schedule() ## This is the schedule dataframe
print(df)

df.to_csv('final_ET_schedule.csv') ## To download the csv into the folder