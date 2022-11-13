# Detailed data descriptions 

We pull the following fields from the <match_id>.csv file for each match:
Please note that match ID contains the suffix A or B wherein A bats first in the match but that doesn't imply that the particular team won the toss as well
  1. "match_id" -> Match X (id)
  2. year from "start_date" -> Year  -> Static
  3. "venue" -> Stadium for Table 2 and Table 1 -> Static
  4. "batting_team" -> Team A 
  5. "bowling_team" -> Team B
  
Three phases defined in each inning ->
  Powerplay -> First 6 overs: [ 0.1 , 6.1 )
  Middle overs -> Middle 10 overs: [ 6.1, 16.1)
  Death overs -> Last 4 overs: [16.1, 19.-] (Wherever the value under "innings" shifts from 1 to 2)

  6. Sum of values under columns "runs_off_bat" and "extras" for the rows defined under powerplay -> Runs in Powerplay
  7. Number of cells with some value under column "wicket_type" for rows defined under powerplay -> Wickets in Powerplay 
  8. Sum of values under columns "runs_off_bat" and "extras" for the rows defined under middle overs -> Runs in Middle overs
  9. Number of cells with some value under column "wicket_type" for rows defined under middle overs -> Wickets in Middle overs
  10. Sum of values under columns "runs_off_bat" and "extras" for the rows defined under Death overs -> Runs in Death overs
  11. Number of cells with some value under column "wicket_type" for rows defined under Death overs -> Wickets in Death overs
  12. Sum of "Score in Powerplay", "Score in Middle overs", and "Score in Death overs" -> Total score
  13. Sum of "Wickets in Powerplay", "Wickets in Middle overs", and "Wickets in Death overs" -> Total wickets

We pull the following fields from the <match_id>__info.csv file for each match:
  1. "venue" -> Stadium -> Static
  2. "city" -> City -> Static
  3. "toss_winner" -> Toss winner -> Static
  4. "Toss_decision" -> Toss decision -> Static 
  5. "winner" -> Result (could be abandoned for rain washed out matches) -> Static
