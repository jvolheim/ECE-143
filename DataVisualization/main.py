import pandas as pd


if __name__ == '__main__':

   database = pd.read_csv('../DataProcessing/Result.csv')
   print(database.head())