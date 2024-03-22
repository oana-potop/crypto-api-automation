import os
from time import time
from time import sleep
from pullFunction import *
import seaborn as sns
import matplotlib.pyplot as plt


for i in range(30):
    single_df = api_runner()

    if(i == 0):
        df = pd.DataFrame(columns = list(single_df.columns))

    # Adding to a dataframe after each pull
    df = pd.concat([df, single_df])

    # Creating a CSV file with the data we pulled
    if not os.path.isfile(f"{os.curdir}/all_data.csv"):
        df.to_csv(f"{os.curdir}/all_data.csv", header='column_names')
    else:
        df.to_csv(f"{os.curdir}/all_data.csv", mode='a', header=False)

    #Grouping the data based on the quote USD % change over different timeframes and creating a separate CSV file for that
    df_group = df.groupby('name', sort=False)[['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d']].mean()
    df_stack = df_group.stack()
    
    df1 = df_stack.to_frame(name='values')
    # x = df1['values'].value_counts()
    # print(len(x))
    # index = pd.Index(range(len(x)))
    df_pivot = df1.reset_index()
    df_pivot = df_pivot.rename(columns={'level_1': 'percent_change'})
    df_pivot['percent_change'] = df_pivot['percent_change'].replace(['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d'], ['1h', '24h', '7d', '30d', '60d', '90d'])

    if not os.path.isfile(f"{os.curdir}/percent_changes.csv"):
        df_pivot.to_csv(f"{os.curdir}/percent_changes.csv", header='column_names')
    else:
        df_pivot.to_csv(f"{os.curdir}/percent_changes.csv", mode='a', header=False)

    #Plotting the results
    sns.catplot(x='percent_change', y='values', hue='name', data=df_pivot, kind='point')
    plt.show()

    print('API Runner completed successfully')
    sleep(60) #sleep for 1 min


