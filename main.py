import numpy as np
import pandas as pd
import bar_chart_race as bcr
from moviepy.editor import VideoFileClip, clips_array

# Call and store inflation data into a dataframe.
inflationDF = pd.read_excel('https://github.com/ObamaBinModdin/CS445-Final_Project/raw/main/inflation.xlsx')
# Call and store unemployment data into a dataframe.
unemploymentDF = pd.read_excel('https://github.com/ObamaBinModdin/CS445-Final_Project/raw/main/unemployment_rate.xlsx')


def cleanData(df):
    # Replace all ".." values to "nan".
    df = df.replace('..', np.nan)

    # Change all year columns to type float.
    df.iloc[:, 4:] = df.iloc[:, 4:].astype(float)

    # Replace all "nan" values to the column mean ignoring outliers.
    for col in df.iloc[:, 4:].columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df_filtered = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]
        mean_col = df_filtered[col].mean()
        df[col] = df[col].fillna(mean_col)

    # Dropping useless columns.
    df.drop(['Country Code', 'Series Code', 'Country Code', 'Series Name'], inplace=True, axis=1)

    # Setting column 'Country Name' to index.
    df.set_index('Country Name', inplace=True)

    # Removing name for index column.
    df.index.name = None

    # Transposing, resetting index, and setting index to 'index'.
    df = df.T.reset_index().set_index('index')

    # Rename index to year.
    df.index.name = 'Year'

    return df


# Cleaning data for both datasets.
inflationDF = cleanData(inflationDF)
unemploymentDF = cleanData(unemploymentDF)

# Selecting specific countries.
inflationDF = inflationDF[
    ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'India', 'France', 'Italy', 'Canada',
     'Korea, Rep.']]
unemploymentDF = unemploymentDF[
    ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'India', 'France', 'Italy', 'Canada',
     'Korea, Rep.']]

# Create the first bar chart race.
fig1 = bcr.bar_chart_race(df=inflationDF.iloc[8:, :], title='Inflation, consumer prices (annual %)', dpi=300,
                          steps_per_period=250, sort='desc', label_bars=True,
                          period_length=2500, interpolate_period=True, cmap='dark12',
                          filter_column_colors=True,
                          period_label={'x': .95, 'y': .5, 'ha': 'right', 'va': 'center'},
                          period_fmt='{x:.0f}', filename='inflation_bcr.mp4', bar_kwargs={'alpha': 1})

# Create the second bar chart race.
fig2 = bcr.bar_chart_race(df=unemploymentDF.iloc[8:, :], title='Unemployment (annual %)', dpi=300,
                          steps_per_period=250, sort='desc', label_bars=True,
                          period_length=2500, interpolate_period=True, cmap='dark12', filter_column_colors=True,
                          period_label={'x': .95, 'y': .5, 'ha': 'right', 'va': 'center'},
                          period_fmt='{x:.0f}', filename='unemployment_bcr.mp4', bar_kwargs={'alpha': 1})

# mp4s of the bar chart races.
clip1 = VideoFileClip('inflation_bcr.mp4')
clip2 = VideoFileClip('unemployment_bcr.mp4')

# Resize the videos to the same height
clip1 = clip1.resize(height=360)
clip2 = clip2.resize(height=360)

# Combine the videos side by side
final_clip = clips_array([[clip1, clip2]])

# Write the final clip to a new file
final_clip.write_videofile('inflation_unemployment_bcr.mp4')
