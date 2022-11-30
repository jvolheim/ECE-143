# ECE-143
## Data Analysis Project Objective
### Top level objectives:
- Analysing team performance in T20Is upto the tournament (from the 2016 WC till the start of the 2022 WC) -> Performance in all locations (with focus on Australia)
   - Overall metrics - all matches -> Try to understand how a team plays
   
         1. Win/Loss ratio - divided by batting first and batting second; histogram point for each year (2016-2022) - further segregated by location later 
         2. (Average first innings score and wickets conceded) versus win loss ratio in that versus various oppositions (Super 12) - by location (ground, country) 
            - Phase progression across powerplay, middle overs, and death overs (for all years separately or averaged out across all years) divided by win and loss 
         3. (Average second innings score and wickets conceded) versus win loss ratio in that versus various oppositions (Super 12) - by location (ground, country) 
            - Phase progression across powerplay, middle overs, and death overs (for all years separately or averaged out across all years) divided by win and loss 
         4. Optional : Star player of each team versus each opposition - Batting: Max runs scored against that opposition; Bowling: Max. wickets taken 
      
   - What led to the win/loss - batting or bowling? - 12 competing teams - Try to judge the nature of matchups  
   
         5. If batting score > min(opposition score, 1st innings ground average) -> Good batting performance   
         6. If bowling restricted score < min(team score, 1st innings ground average) -> Good bowling performance 
         7. Try to plot wins/losses based on these two metrics - divide by oppositions 
         
   - Performance in T20 WC (TBD) 
   
         8. Have to do for each match of Super 12s and Knockouts 
      

## Data sources    

### Building database from Cricsheet:  
   Source:  https://cricsheet.org/

TABLE 1 -> 1,2,3  

      Match X (id) - Team A - Team B - Year - Runs in Powerplay - Wickets lost in Powerplay - Runs in middle overs -  Wickets lost in middle overs - Runs in Death overs - Wickets lost in death overs - Total Score A - Wickets lost A - Win/Loss A - City - Stadium - Toss winner - Toss decision  


TABLE 2 -> 5,6,7  

      Stadium - City - 1st innings ground average  
    
## Tasks and Roles 

1. Parse the data 
2. Build the tables
3. Plot the visualisations
4. Formatting the graphs (in the slides)




