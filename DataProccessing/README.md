# Current Progress  
1. Currently able to read in the files and return necessary data into Result.csv
2. ToDo
    - Inquire about the number of matches missing the city data field
    - Manually update the csv file after running `main.py` to account for the changes in the stadium and/or city names

# Commit history
### 2022-11-22
1. Added 2 new columns to split the `id` column into `innings_number` and `match_id`
2. Added code line to update venue names, thereby accounting for step 1 in our de-duplication process for stadium and city names

Useful resource link on [pandas](https://pandas.pydata.org/pandas-docs/stable/reference/index.html)
