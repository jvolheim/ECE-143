import pandas as pd
import os


# for over
# runs, wickets def over(df):

def id_info_csv(path):
    '''
    Function takes and processes the data for the info.csv format data
    :param path: should be valid path to file
    :return: toss_winner, toss_decision, city, winner
    '''
    assert isinstance(path, str)  # check for valid type input
    # initialize return variable
    result = []

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

        # pull data based on index values
        for i in a:
            result.append(s.at[i][2])

        # delete dataframe
        del field
        # check for full return values
        if len(result) != 4:
            raise Exception("Result length != 4")

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
    result = []

    return result


if __name__ == '__main__':

    your_path = './Sample Data'
    files = os.listdir(your_path)

    for file in files:
        if file[-8:-4] == 'info':  # csv_info
            toss_winner, toss_decision, city, winner = id_info_csv(your_path + '/' + file)
            print(toss_winner)
        else:  # csv regular
            fields = id_csv(your_path + '/' + file)
            print(fields)

        # create row of main dataframe here

        #
