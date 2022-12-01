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

    # # Average score 
    # # Conditions 1) First innings 2) Total matched >= 10
    # avg_db_1 = avg_db[(avg_db['Total_Score_A_count'] >= 10) & 
    #           (avg_db['innings_number'].str.strip() == 'A')
    #           ].sort_values(by=['avg_score','Total_Score_A_count'], 
    #                         ascending=False)
    return avg_db, db


def batting_bowling_performances(avg_db, utd_db):
    """
    param db: Database ; pandas Dataframe
    """
        
    assert isinstance(avg_db, pd.DataFrame)
    assert isinstance(utd_db, pd.DataFrame)

    utd_db = utd_db.merge(avg_db[['updated_venue','updated_city', 'innings_number',  'avg_score', 'avg_wickets']], 
                            how='left', 
                            on=['updated_venue', 'updated_city', 'innings_number'])

    # bringing match innings level statistics on a unique match id
    refined_db = utd_db[['match_id', 'updated_venue', 'updated_city', 'winner',
                         'avg_score', 'avg_wickets', 'innings_number', 
                         'team_A', 'team_B', 'Total_Score_A','Total_Wicket_A']]
    
    first_innings = refined_db[utd_db['innings_number'].str.strip() == 'A']
    second_innings = refined_db[utd_db['innings_number'].str.strip() == 'B']

    # Renaming second innings columns
    rename_second_cols = {'team_A': 'team_A2', 'team_B': 'team_B2', 
                          'Total_Score_A':'Total_Score_A2', 'Total_Wicket_A': 'Total_Wicket_A2'}
    second_innings = second_innings.rename(columns=rename_second_cols)

    both_innings = first_innings.merge(second_innings[['match_id', 'updated_venue', 'updated_city',
                                                       'team_A2', 'team_B2',
                                                       'Total_Score_A2','Total_Wicket_A2']],
                                       how='left',
                                       on=['match_id', 'updated_venue', 'updated_city'])
    
    # Creating batting and bowling performance in a particular match for both teams
    both_innings['A_batting'] = both_innings.apply(
        lambda row: 1 if row['Total_Score_A'] >= row['avg_score'] \
        else 0, axis=1
    )

    both_innings['B_bowling'] = both_innings.apply(
        lambda row: 0 if row['A_batting'] == 1 else 1, axis=1
    )

    both_innings['B_batting'] = both_innings.apply(
        lambda row: 1 if row['Total_Score_A2'] >= row['Total_Score_A'] \
        else 0, axis=1
    )

    both_innings['A_bowling'] = both_innings.apply(
        lambda row: 0 if row['B_batting'] == 1 else 1, axis=1
    )

    # Splitting by country
    list_1 = both_innings[['team_A', 'team_B', 'winner', 'A_batting', 'A_bowling']]
    list_1['win_or_loss'] = list_1.apply(
        lambda row: 1 if row['team_A'] == row['winner'] else 0, axis=1
    )
    list_2 = both_innings[['team_A2', 'team_B2', 'winner', 'B_batting', 'B_bowling']]
    list_2['win_or_loss'] = list_2.apply(
        lambda row: 1 if row['team_A2'] == row['winner'] else 0, axis=1
    )
    
    # Splitting and concatenating both team matchups as home and opposition to find their overall matchups, wins, losses, and performances
    final_rename_cols = ['home', 'opposition', 'winner', 'batting_perf', \
                         'bowling_perf', 'win_or_loss']
    list_1.columns = final_rename_cols
    list_2.columns = final_rename_cols

    final_list = pd.concat([list_1, list_2])

    ds = final_list.groupby(['home', 'opposition', 'win_or_loss']).agg({
                'batting_perf':['count', 'sum'], 'bowling_perf':'sum'}).reset_index()

    ds.columns = [col[0] if col[1] == "" else '_'.join(col) for col in ds.columns.values]
    ds.rename(columns={ ds.columns[3]: "matchups" }, inplace = True)
    ds.rename(columns={ ds.columns[4]: "batting_perf" }, inplace = True)
    ds.rename(columns={ ds.columns[5]: "bowling_perf" }, inplace = True)
    
    return ds


if __name__ == "__main__":
    BASE_PATH = os.getcwd()
    DATABASE_PATH = os.path.join(BASE_PATH, "DataProcessing", "result_post_step.csv")
    database = pd.read_csv(DATABASE_PATH)
    avg_db, uptd_db = ground_averages(database)
    final_db = batting_bowling_performances(avg_db, uptd_db)