import pandas as pd
import numpy as np
from functools import reduce

class Scheduler():
    def __init__(self, _no_of_companies, _companies, _time_slots_companies, _panel_no_companies, _slots_companies) -> None:
        self.no_of_companies = _no_of_companies                        #for ex. 3
        self.companies = _companies                                    #for ex. Qualcomm
        self.time_slots_companies = _time_slots_companies              #starting times
        self.panel_no_companies = _panel_no_companies
        self.slots_companies = _slots_companies
        self.companies_df = []
        self.possible_combinations = []
    def read_data(self):
        for company in self.companies:
            self.companies_df.append(pd.read_csv(f"{company}.csv"))                 #companies_df is a list with no_of_companies number of elements
    def change_column_name(self):
        i = 0
        for company_df in self.companies_df:
            company_df.rename(columns = {'Status': f'{self.companies[i]}_Status'}, inplace = True)
            i+=1
    def merge_df(self):
        df_custom =  reduce(lambda  left,right: pd.merge(left,right,on=["Name","Email ID"],
                                                how='outer'), self.companies_df)
        df_custom = df_custom.drop_duplicates()
        self.df_final = df_custom
    def fill_na(self):
        self.df_final = self.df_final.replace(np.nan, 0)
    def assign_PR(self):
        self.df_final['PR'] = 0
        for i in range(0,len(self.companies)):
            self.df_final['PR'] = self.df_final['PR']+self.df_final[f'{self.companies[i]}_Status']
    def sort_df(self):
        self.df_final = self.df_final.sort_values(
            by="PR",
            ascending=False
        )
        self.df_final = self.df_final.drop(columns=['PR'])
    def reset_index(self):
        self.df_final.reset_index(drop=True, inplace=True)
    def generate_combinations(self):
        for k in range(0,self.no_of_companies):
            (x,y) = (self.time_slots_companies[k], self.panel_no_companies[k])
            self.possible_combinations.append([[[n,m,0] for m in range(1,y+1)] for n in range(x,x+self.slots_companies[k])])
    def create_cols(self):
        for i in range(0,len(self.companies)):
            self.df_final[f'{self.companies[i]}_ts'] = np.nan
            self.df_final[f'{self.companies[i]}_panel'] = np.nan
    def allot_ts(self):
        # Iterating through all the rows in the dataframe
        for index, row in self.df_final.iterrows():
            # Non_iter represents the timeslot in which the candidate is busy
            non_iter = []

            # k represents the company index
            k=0

            for itr in range(0,len(self.companies)): 

                # To check whether candidate has been shortlisted for Qualcomm
                if row[f'{self.companies[itr]}_Status'] != 0:
                    breakout_flag = False
                    for i in range(len(self.possible_combinations[k])):
                
                        # Check whether candidate is busy during this time period, if yes
                        # continue to the next iteration
                        if i in non_iter:
                            continue
                        for j in range(len(self.possible_combinations[k][0])):
                            
                            # Check for the first panel which is free
                            if self.possible_combinations[k][i][j][2]==0:
                                # Allot the timeslot and panel no
                                self.df_final.at[index,f'{self.companies[itr]}_ts'] = self.possible_combinations[k][i][j][0]
                                self.df_final.at[index,f'{self.companies[itr]}_panel']= self.possible_combinations[k][i][j][1]

                                # Change the status of the timeslot and panel no combination
                                self.possible_combinations[k][i][j][2] = 1

                                # Make this timeslot unavailble for the next companies for the candidate
                                non_iter.append(self.possible_combinations[k][i][j][0])

                                # To break out from the outer loop
                                breakout_flag = True
                                # To break out from the inner loop
                                break
                        if breakout_flag:
                            break
                    if row[f'{self.companies[itr]}_ts']==np.nan:
                        print("Scheduler not working!")
                k=k+1
    def change_col(self):
        for itr in range(0,len(self.companies)): 
            self.df_final.loc[self.df_final[f'{self.companies[itr]}_Status'] == 1, f'{self.companies[itr]}_Status'] = 'Shortlisted'
    def change_ts(self):
        times = ['9:00-9:45', '9:45-10:30', '10:30-11:15', '11:15-12:00', '12:00-12:45', '12:45-1:30', '1:30-2:15', '2:15-3:00']

        for k in range(0,self.no_of_companies):
            #(x,y) = (self.time_slots_companies[k], self.panel_no_companies[k])
            x = self.time_slots_companies[k]
            for i in range(x, x+self.slots_companies[k]):
                self.df_final.loc[self.df_final[f'{self.companies[k]}_ts'] == i, f'{self.companies[k]}_ts'] = times[i]
    def change_na(self):
        def convert_na(val):
            if val==0:
                return np.nan
            else:
                return val
        for itr in range(0,len(self.companies)):
            self.df_final[f'{self.companies[itr]}_Status'] = self.df_final[f'{self.companies[itr]}_Status'].apply(convert_na)
    def get_df(self):
        return self.df_final
    def get_schedule(self):
        self.read_data()
        self.change_column_name()
        self.merge_df()
        self.fill_na()
        self.assign_PR()
        self.sort_df()
        self.reset_index()
        self.generate_combinations()
        self.create_cols()
        self.allot_ts()
        self.change_col()
        self.change_ts()
        self.change_na()
        df = self.get_df()
        return df
    


