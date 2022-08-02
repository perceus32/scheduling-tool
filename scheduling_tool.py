import pandas as pd
import numpy as np
from functools import reduce

time_slots_companies = [0,0,0]
panel_no_companies = [17, 10, 10] 
slots_companies = [8,8,8]
no_of_companies = 3 
companies = ['Qualcomm','Micron','TI']

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


## Data reading and cleaning

companies_df = []

def read_data(companies):
    for company in companies:
        companies_df.append(pd.read_csv(f"{company}.csv"))


read_data(companies)
#print(companies_df[0].head())

def change_column_name(companies_df, companies):
    i = 0
    for company_df in companies_df:
        company_df.rename(columns = {'Status': f'{companies[i]}_Status'}, inplace = True)
        i+=1

change_column_name(companies_df,companies)
#print(companies_df[0].head())

def merge_df(companies_df):
    df_custom =  reduce(lambda  left,right: pd.merge(left,right,on=["Name","Email ID"],
                                                how='outer'), companies_df)
    df_custom = df_custom.drop_duplicates()
    return df_custom

df_final = merge_df(companies_df)
#print(df_final.head())

def fill_na(df_final):
    df_final = df_final.replace(np.nan, 0)
    return df_final

df_final = fill_na(df_final)

#print(df_final.head())

def assign_PR(df_final, companies):
    df_final['PR'] = 0
    for i in range(0,len(companies)):
        df_final['PR'] = df_final['PR']+df_final[f'{companies[i]}_Status']
    return df_final

df_final = assign_PR(df_final,companies)
#print(df_final.head())

def sort_df(df_final):
    df_final = df_final.sort_values(
        by="PR",
        ascending=False
    )
    df_final = df_final.drop(columns=['PR'])
    return df_final

df_final = sort_df(df_final)
#print(df_final.head())

def reset_index(df_final):
    df_final.reset_index(drop=True, inplace=True)
    return df_final

reset_index(df_final)
#print(df_final)

## Algorithm

possible_combinations = []

def generate_combinations(possible_combinations):
    for k in range(0,no_of_companies):
        (x,y) = (time_slots_companies[k], panel_no_companies[k])
        possible_combinations.append([[[n,m,0] for m in range(1,y+1)] for n in range(x,x+slots_companies[k])])

generate_combinations(possible_combinations)
#print(possible_combinations)

def create_cols(df_final, companies):
    for i in range(0,len(companies)):
        df_final[f'{companies[i]}_ts'] = np.nan
        df_final[f'{companies[i]}_panel'] = np.nan
    return df_final

df_final = create_cols(df_final, companies)
#print(df_final.head())

def allot_ts(df_final, companies):
    # Iterating through all the rows in the dataframe
    for index, row in df_final.iterrows():
        # Non_iter represents the timeslot in which the candidate is busy
        non_iter = []

        # k represents the company index
        k=0

        for itr in range(0,len(companies)): 

            # To check whether candidate has been shortlisted for Qualcomm
            if row[f'{companies[itr]}_Status'] != 0:
                breakout_flag = False
                for i in range(len(possible_combinations[k])):
            
                    # Check whether candidate is busy during this time period, if yes
                    # continue to the next iteration
                    if i in non_iter:
                        continue
                    for j in range(len(possible_combinations[k][0])):
                        
                        # Check for the first panel which is free
                        if possible_combinations[k][i][j][2]==0:
                            # Allot the timeslot and panel no
                            df_final.at[index,f'{companies[itr]}_ts'] = possible_combinations[k][i][j][0]
                            df_final.at[index,f'{companies[itr]}_panel']= possible_combinations[k][i][j][1]

                            # Change the status of the timeslot and panel no combination
                            possible_combinations[k][i][j][2] = 1

                            # Make this timeslot unavailble for the next companies for the candidate
                            non_iter.append(possible_combinations[k][i][j][0])

                            # To break out from the outer loop
                            breakout_flag = True
                            # To break out from the inner loop
                            break
                    if breakout_flag:
                        break
                if row[f'{companies[itr]}_ts']==np.nan:
                    print("Scheduler not working!")
            k=k+1
    return df_final

df_final = allot_ts(df_final, companies)
#print(df_final)

def change_col(df_final, companies):
    for itr in range(0,len(companies)): 
        df_final.loc[df_final[f'{companies[itr]}_Status'] == 1, f'{companies[itr]}_Status'] = 'Shortlisted'
        return df_final

df_final = change_col(df_final, companies)
#print(df_final)

def change_ts(df_final, companies):
    times = ['9:00-9:45', '9:45-10:30', '10:30-11:15', '11:15-12:00', '12:00-12:45', '12:45-1:30', '1:30-2:15', '2:15-3:00']

    for k in range(0,no_of_companies):
        (x,y) = (time_slots_companies[k], panel_no_companies[k])
        for i in range(x, x+slots_companies[k]):
            for itr in range(0,len(companies)):
                df_final.loc[df_final[f'{companies[itr]}_ts'] == i, f'{companies[itr]}_ts'] = times[i]
    return df_final

df_final = change_ts(df_final, companies)
#print(df_final)

def convert_na(val):
  if val==0:
    return np.nan
  else:
    return val

def change_na(df_final, companies):
    for itr in range(0,len(companies)):
        df_final[f'{companies[itr]}_Status'] = df_final[f'{companies[itr]}_Status'].apply(convert_na)
    return df_final

df_final = change_na(df_final, companies)
#print(df_final)

df_final.to_csv('final_ET_schedule.csv')