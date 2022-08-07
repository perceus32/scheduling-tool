from obj_scheduling_tool import Scheduler ## Import the scheduler class

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

time_slots_companies = [1,0,2,0,2] ## Starting time period of companies
panel_no_companies = [5,14,7,20,3] ## No of panels of companies
slots_companies = [12,12,12,12,12] ## Slots per company
no_of_companies = 5 ##Number of companies
companies = ['Indeed','Microsoft','GS','Cisco','Uber'] ## Names of companies, correponding csv files must be present in the folder

## Instantiate object like this ->
schedule = Scheduler(no_of_companies,companies,time_slots_companies,panel_no_companies,slots_companies)
'''
schedule.read_data()
schedule.change_column_name()
schedule.merge_df()
schedule.fill_na()
schedule.assign_PR()
schedule.sort_df()
schedule.reset_index()
schedule.generate_combinations()
schedule.create_cols()
schedule.allot_ts()
schedule.change_col()
'''
# df = schedule.get_df()
# print(df)
df = schedule.get_schedule() ## This is the schedule dataframe
df.to_csv('test_day1-1.csv')
print(df)

# csv_file = schedule.get_csv() ## To download the csv into the folder