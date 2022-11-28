import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


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
    return avg_db_1

def performance(db,averages):
    """
    :This function creates visuals (pie charts) relating good bowling and batting performances
    to whether the teams closed out the performance with a win. Additionally, one of the visuals
    is a general pie chart displaying the breakdown of good batting/bowling performances regardless
    of result.
    """
    wc_countries = ["New Zealand","England","Australia","Sri Lanka","Ireland","Afghanistan","India","Pakistan","South Africa","Netherlands","Bangladesh","Zimbabwe"]
    final_four=["New Zealand","England","India","Pakistan"]
    good_batting_performance=0
    good_bowling_performance=0
    good_batting_performance_and_win=0
    good_bowling_performance_and_win=0
    both=0
    neither=0
    for index, row in db.iterrows():
        for i, r in averages.iterrows():
            if (row['updated_venue'] in r['updated_venue'])&(row['team_A'] =='India'):   #change this line (individual team vs final four vs all 12 teams)
                if((row['team_A']==row['toss_winner'])&(row['toss_decision']=='bat')) | ((row['team_A']!=row['toss_winner'])&(row['toss_decision']=='field')):
                    if (row['Total_Score_A']>r['avg_score'])&(row['team_A']==row['winner']):
                        good_batting_performance+=1
                        good_batting_performance_and_win+=1
                        good_bowling_performance+=1
                        good_bowling_performance_and_win+=1 
                        both+=1
                    elif row['Total_Score_A']>r['avg_score']:
                        good_batting_performance+=1
                    elif (row['Total_Score_A']<r['avg_score'])&(row['team_A']==row['winner']):
                        good_bowling_performance+=2
                        good_bowling_performance_and_win+=1 
                    else:
                        neither+=1
                else:
                    if (row['Total_Score_A']<r['avg_score'])&(row['team_A']==row['winner']):
                        good_bowling_performance+=1
                        good_bowling_performance_and_win+=1
                        good_batting_performance+=1
                        good_batting_performance_and_win+=1
                        both+=1
                    elif (row['Total_Score_A']>r['avg_score'])&(row['team_A']==row['winner']):
                        good_batting_performance+=1
                        good_batting_performance_and_win+=1
                    elif (row['Total_Score_A']<r['avg_score'])&(row['team_A']!=row['winner']):
                        continue
                    else:
                        neither+=1       
            else:
                continue
    batting = np.array([good_batting_performance_and_win,good_batting_performance-good_batting_performance_and_win])
    labels=["Win","Loss"]
    plt.pie(batting,labels=labels,autopct='%1.1f%%')
    plt.title("Conversion of a Good Batting Performance to a Win")
    plt.show()
    bowling = np.array([good_bowling_performance_and_win,good_bowling_performance-good_bowling_performance_and_win])
    labels2=["Win","Loss"]
    plt.pie(bowling,labels=labels2,autopct='%1.1f%%')
    plt.title("Conversion of a Good Bowling Performance to a Win")
    plt.show()
    general = np.array([good_batting_performance,good_bowling_performance,both,neither])
    labels3=["Good Batting","Good Bowling","Both","Neither"]
    plt.pie(general,labels=labels3,autopct='%1.1f%%')
    plt.title("General Breakdown of Performance (Regardless of Result)")
    plt.show()
    
def win_composition(db,averages):
    """
    :This function creates visuals (pie charts) with breakdowns of good batting/bowling
    performances given that the result is a win (opposite of the previous function)
    """
    wc_countries = ["New Zealand","England","Australia","Sri Lanka","Ireland","Afghanistan","India","Pakistan","South Africa","Netherlands","Bangladesh","Zimbabwe"]
    final_four=["New Zealand","England","India","Pakistan"]
    good_batting_performance=0
    good_bowling_performance=0
    both=0
    for index, row in db.iterrows():
        for i, r in averages.iterrows():
            if (row['updated_venue'] in r['updated_venue'])&(row['team_A'] in wc_countries)&(row['team_A']==row['winner']):  #change this line (individual team vs final four vs all 12 teams)
                if((row['team_A']==row['toss_winner'])&(row['toss_decision']=='bat')) | ((row['team_A']!=row['toss_winner'])&(row['toss_decision']=='field')):
                    if (row['Total_Score_A']>r['avg_score']):
                        both+=1   
                    else:
                        good_bowling_performance+=1
                else:
                    if (row['Total_Score_A']<r['avg_score']):
                        both+=1
                    elif (row['Total_Score_A']>r['avg_score']):
                        good_batting_performance+=1     
            else:
                continue
    batting = np.array([good_batting_performance,good_bowling_performance,both])
    labels=["good batting","good bowling","both"]
    plt.pie(batting,labels=labels,autopct='%1.1f%%')
    plt.title("Composition of Wins")
    plt.show()

if __name__ == "__main__":
    BASE_PATH = os.getcwd()
    database = pd.read_csv('../DataProcessing/result_post_step_2.csv')
    averages=ground_averages(database)
    performance(database,averages)
    win_composition(database,averages)
    