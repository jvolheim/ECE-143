import os
import pandas as pd

def ground_averages_reference(df):
    '''
    : *Reference only for ground averages
    '''
    x=df['updated_venue']
    separated=[]
    for i in x.items():
        for l in i:
            if i[0]!=l:
                category=l.split(', ')
                separated.append(category)
    separatedseries=pd.Series(separated)
    separatedseries=separatedseries.explode()
    counts=separatedseries.value_counts(ascending=True)
    final=pd.DataFrame(counts,columns=['count'])

    updated=[]
    for i in final['count'].items():
        if i[1]>=20:
            updated.append(i[0])
        else:
            continue
    averages={}

    for index, row in df.iterrows():
        if row['updated_venue'] in updated:
            if ((row['team_A']==row['toss_winner'])&(row['toss_decision']=='bat')) | ((row['team_A']!=row['toss_winner'])&(row['toss_decision']=='field')):
                if row['updated_venue'] in averages.keys():
                    averages[row['updated_venue']].append(row['Total_Score_A'])
                else:
                    averages[row['updated_venue']]=[(row['Total_Score_A'])]
    for keys,values in averages.items():               
        averages[keys]=int(sum(values)/len(values))

    print(sorted(averages.values()))

if __name__ == "__main__":
    BASE_PATH = os.getcwd()
    database = pd.read_csv('../DataProcessing/result_post_step_2.csv')
    ground_averages_reference(database)