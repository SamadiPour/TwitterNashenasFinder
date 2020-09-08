from datetime import datetime

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.database import DatabaseHelper

if __name__ == '__main__':
    # load database!
    tweets_date = list(
        map(
            lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S'),
            DatabaseHelper().get_all_dates()
        )
    )

    # values
    start_date = datetime.combine(tweets_date[0], datetime.min.time())
    end_date = datetime.combine(tweets_date[-1], datetime.max.time())
    max_freq = 0

    # initiate index and values
    dates = pd.date_range(start=start_date, end=end_date, freq='1h')
    freq = [0 for x in range(len(dates))]

    # fill frequents
    for date in tweets_date:
        index = int((date - start_date).total_seconds() / 3600)
        freq[index] += 1

    # create dataframe with datetime as index and aggregated (frequency) values
    df = pd.DataFrame({"freq": freq}, index=dates)

    # add a column hours and days
    df["hours"] = df.index.hour.map(lambda x: f"{x:02d}")
    df["days"] = df.index.map(lambda x: x.strftime('%b %d'))

    # create pivot table, days will be columns, hours will be rows
    piv = pd.pivot_table(df, values="freq", index=["hours"], columns=["days"], fill_value=0)

    # plot pivot table as heatmap using seaborn
    pal = sns.light_palette("navy", as_cmap=True)
    ax = sns.heatmap(piv, square=True, cmap="Purples", vmin=0)  # vmax
    ax.set_title("Nashenas Heat Map")
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
    plt.tight_layout()

    # save and show plot
    plt.savefig('../heatmap.svg', format='svg', dpi=600)
    plt.savefig('../heatmap.png', format='png', dpi=600)
    plt.show()
