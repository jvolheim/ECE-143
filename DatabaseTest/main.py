import pandas as pd
import os


def run_wickets(df, over):
    field = df['ball']
    if over == 1:
        A = field[field >= 6.1].index.tolist()
        field = field.drop(index=A)
    if over == 2:
        A = field[field >= 16.1].index.tolist()
        field = field.drop(index=A)
        A = field[field < 6.1].index.tolist()
        field = field.drop(index=A)
    if over == 3:
        A = field[field < 16.1].index.tolist()
        field = field.drop(index=A)

    A = field[field > 0].index.tolist()
    wick = df['wicket_type']
    run = df['runs_off_bat']
    ex = df['extras']

    wick = wick.drop(index=A).astype(str)
    wick = wick.apply(lambda x: len(x) > 3) * 1

    run = run.drop(index=A)

    ex = ex.drop(index=A)

    w = wick.sum()
    r = run.sum()
    e = ex.sum()

    return [[r + e], [w]]


def inning(dataf, over):
    field = dataf["innings"]
    A = field[field == over].index.tolist()
    df = dataf.drop(index=A)
    df = df.reset_index()
    r = {}

    r['team_A'] = [df["batting_team"][0]]
    r['team_B'] = [df["bowling_team"][0]]
    r['RiP'], r['WliP'] = run_wickets(df, 1)
    r['RiM'], r['WliM'] = run_wickets(df, 2)
    r['RiD'], r['WliD'] = run_wickets(df, 3)

    r['Winning Score'] = int(r['RiP'][0]) + int(r['WliP'][0]) + \
                         int(r['RiM'][0]) + int(r['WliM'][0]) + \
                         int(r['RiD'][0]) + int(r['WliD'][0])

    return r


def id_info_csv(path):
    '''
    Function takes and processes the data for the info.csv format data
    :param path: should be valid path to file
    :return: toss_winner, toss_decision, city, winner
    '''
    assert isinstance(path, str)  # check for valid type input
    # initialize return variable
    result = {}

    try:
        # read data as Length x 1 each row being stored as string in 1 column
        dataframe = pd.read_csv(path, delimiter='\r')
        # split loaded dataframe by comma into list
        s = dataframe.squeeze().str.split(',')
        # Shrink Series to column of fields
        field = s.apply(lambda x: x[1])

        # pull required data index's
        a = field[field == 'toss_winner'].index.tolist()
        a += field[field == 'toss_decision'].index.tolist()
        a += field[field == 'city'].index.tolist()
        a += field[field == 'winner'].index.tolist()

        # check for full return values
        if len(a) != 4:
            raise Exception("Result length != 4")

        # pull data based on index values
        result['toss_winner'] = [s.at[a[0]][2]]
        result['toss_decision'] = [s.at[a[1]][2]]
        result['city'] = [s.at[a[2]][2]]
        result['winner'] = [s.at[a[3]][2]]

        # delete dataframe
        del field

        # return field results
        return result
    except:
        print('Error Occurred with path: ' + path)
        print(result)


def id_csv(path):
    '''
    Extract data from id_csv
    :param path: should be valid path to file
    :return:
    '''
    r1 = {}
    # try:
    dataframe = pd.read_csv(path, usecols=["match_id", "start_date", "venue", "innings",
                                           "ball", "batting_team", "bowling_team", "runs_off_bat",
                                           "extras", "wicket_type"])

    r1['id'] = str(dataframe["match_id"][0])
    r1['year'] = [int(dataframe['start_date'][0].split('-')[0])]
    r1['venue'] = [dataframe["venue"][0]]
    r2 = r1.copy()

    r1['id'] = [r1['id'] + 'A']
    r2['id'] = [r2['id'] + 'B']

    inn_1 = inning(dataframe, 1)
    inn_2 = inning(dataframe, 2)

    r1.update(inn_1)
    r2.update(inn_2)

    del dataframe
    return r1, r2
    # except:
    # print('Error Occurred with path: ' + path)


if __name__ == '__main__':

    your_path = './Sample Data'
    files = os.listdir(your_path)
    frame = pd.DataFrame()
    for file in files:
        if file[-8:-4] != 'info':  # id.csv

            fieldA, fieldB = id_csv(your_path + '/' + file)

            info = id_info_csv(your_path + '/' + file[:-4] + '_info.csv')

            fieldA.update(info)
            fieldB.update(info)

            frame = pd.concat([frame, pd.DataFrame(fieldA)])
            frame = pd.concat([frame, pd.DataFrame(fieldB)])

    print(frame)
    frame.to_csv('Result.csv')
