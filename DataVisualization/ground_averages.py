# -*- coding: utf-8 -*-
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def ground_averages(db):
    """
    param db: Database ; pandas Dataframe
    """

    assert isinstance(db, pd.DataFrame)
    
    # Some more cleaning
    missing_cities = {'Harare Sports Club':'Harare',
                    'Sylhet International Cricket Stadium':'Sylhet',
                    'Dubai International Cricket Stadium':'Dubai',
                    'Sydney Cricket Ground':'Sydney',
                    'Sylhet Stadium':'Sylhet',
                    'Pallekele International Cricket Stadium':'Kandy',
                    'Sharjah Cricket Stadium':'Sharjah',
                    'Melbourne Cricket Ground':'Melbourne',
                    'Moara Vlasiei Cricket Ground':'Ilfov County',
                    'Rawalpindi Cricket Stadium':'Rawalpindi',
                    'Adelaide Oval':'Adelaide',
                    'Mombasa Sports Club Ground':'Mombasa',
                    'Carrara Oval':'Carrara'
                    }

    db['updated_city'] = db.apply(lambda x: missing_cities[x['updated_venue']] \
                                  if str(x['updated_venue']) in missing_cities.keys() \
                                  else x['update_city'], axis=1
                                  )
    
    # Finding various averages 
    avg_db = db.groupby(['updated_venue', 'updated_city', 'innings_number']).agg({
            'Total_Score_A':['sum', 'count'], 'Total_Wicket_A':'sum', 'Runs_in_Death_overs':'sum',
            'Runs_in_middle_overs':'sum' 
    }).reset_index()
    
    # Renaming columns
    avg_db.columns = [col[0] if col[1] == "" else '_'.join(col) for col in avg_db.columns.values]

    # Creating average columns
    avg_cols = ['avg_score', 'avg_wickets', 'avg_death_over_score', 'avg_middle_over_score']
    total_cols = ['Total_Score_A_sum', 'Total_Wicket_A_sum', 'Runs_in_Death_overs_sum',
                  'Runs_in_middle_overs_sum']

    for idx in range(len(avg_cols)):
        avg_db[avg_cols[idx]] = avg_db.apply(lambda row: row[total_cols[idx]] // \
                                       row['Total_Score_A_count'], axis=1)

    # Average score 
    # Conditions 1) First innings 2) Total matched >= 10
    avg_db_1 = avg_db[(avg_db['Total_Score_A_count'] >= 10) & 
              (avg_db['innings_number'].str.strip() == 'A')
              ].sort_values(by=['avg_score','Total_Score_A_count'], 
                            ascending=False)


if __name__ == "__main__":
    BASE_PATH = os.getcwd()
    DATABASE_PATH = os.path.join(BASE_PATH, "DataProcessing", "result_post_step_2.csv")
    database = pd.read_csv(DATABASE_PATH)
    ground_averages(database)