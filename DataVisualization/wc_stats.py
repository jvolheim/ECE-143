import pandas as pd
import os
import seaborn as sns

import matplotlib.pyplot as plt

def seperate_wc(df:pd.DataFrame):
    wc_df = df[(df['event'] == "ICC Men's T20 World Cup") & (df['year'] == 2022) & (df['id'] >= '1298147A')].reset_index()
    return wc_df

def average_inng_total(df, innings_number='A'):
    innings_scores = df[df['innings_number'] == innings_number]
    innings_scores = innings_scores[['team_A', 'Total_Score_A']]
    avg_inn_score = innings_scores.groupby('team_A').mean().reset_index()
    avg_inn_score.rename(columns={"team_A": "Team Name"}, inplace=True)
    avg_inn_score = avg_inn_score.sort_values(by="Total_Score_A", axis=0, ascending=False)
    if innings_number == "A":
        avg_inn_score['innings_number'] = "First"
    else:
        avg_inn_score['innings_number'] = "Second"
    return avg_inn_score


def plot_avg_scores(avg_inn_score):
    plt.subplots(figsize=(12, 6))

    sns.set_color_codes("pastel")
    sns.barplot(x="Total_Score_A", y=f"Team Name", data=avg_inn_score, hue='innings_number')
    plt.xlabel("Average Score")
    plt.title("Average First and Second Innings scores by different teams during WC")
    SAVE_PATH = os.path.join(os.getcwd(), 'DataVisualization', 'plots', 'avg_wc_scores.png')
    # plt.show()
    plt.savefig(SAVE_PATH)
    return


def win_loss_compare(wc_df):
    wc_df['teamA_winner'] = (wc_df['team_A'] == wc_df['winner'])
    wins = wc_df[['team_A', 'teamA_winner']].groupby('team_A').sum().reset_index()
    total = wc_df[['team_A', 'teamA_winner']].groupby('team_A').count().reset_index()
    merged_df = pd.merge(left=wins, right=total, how='inner', on='team_A')
    merged_df = merged_df.sort_values(by="teamA_winner_x", axis=0, ascending=False, ignore_index=True)
    merged_df['win_percent'] = merged_df['teamA_winner_x'] / merged_df['teamA_winner_y']

    f, ax = plt.subplots(figsize=(12, 6))
    sns.set_color_codes("pastel")
    sns.barplot(x="teamA_winner_y", y="team_A", data=merged_df, color='r', label="Loss")
    sns.barplot(x="teamA_winner_x", y="team_A", data=merged_df, color='g', label="wins")
    # for adding the win percent text
    for i in range(12):
        win_percent = 100 * merged_df['win_percent'][i] 
        p = ax.patches[i+12]
        width = p.get_width()
        ax.text(width+0.15, p.get_y() + p.get_height()/ 2, f'{win_percent:.2f}%', ha='left', va='center', fontsize=12)
    ax.set(ylabel="Country",xlabel="Number of matches played")
    ax.legend(ncol=2, loc="lower right", frameon=True)
    plt.title('Country wise Win-Loss Record for WC')
    SAVE_PATH = os.path.join(os.getcwd(), 'DataVisualization', 'plots', 'wc_win_loss.png')
    # plt.show()
    plt.savefig(SAVE_PATH)

if __name__ == "__main__":
    df = pd.read_csv("DataProcessing/result_post_step.csv")
    wc_df = seperate_wc(df)
    avg_inn1_score = average_inng_total(wc_df, 'A')
    avg_inn2_score = average_inng_total(wc_df, 'B')
    avg_inn_score = pd.concat([avg_inn1_score, avg_inn2_score], ignore_index=True)
    plot_avg_scores(avg_inn_score)
    win_loss_compare(wc_df)
    plt.show()