import numpy as np
import pandas as pd
import bar_chart_race as bcr
from moviepy.editor import VideoFileClip, clips_array


# Call and store inflation data into a dataframe.
from matplotlib import pyplot as plt

inflationDF = pd.read_excel('https://github.com/ObamaBinModdin/CS445-Final_Project/raw/main/inflation.xlsx')

print('got here')

# Replace all ".." values to "nan".
inflationDF = inflationDF.replace('..', np.nan)

# Change all year columns to type float.
inflationDF.iloc[:, 4:] = inflationDF.iloc[:, 4:].astype(float)

# Replace all "nan" values to the column mean ignoring outliers.
for col in inflationDF.iloc[:, 4:].columns:
    Q1 = inflationDF[col].quantile(0.25)
    Q3 = inflationDF[col].quantile(0.75)
    IQR = Q3 - Q1
    df_filtered = inflationDF[(inflationDF[col] >= Q1 - 1.5 * IQR) & (inflationDF[col] <= Q3 + 1.5 * IQR)]
    mean_col = df_filtered[col].mean()
    inflationDF[col] = inflationDF[col].fillna(mean_col)

inflationDF.drop(['Country Code', 'Series Code', 'Country Code', 'Series Name'], inplace=True, axis=1)

inflationDF.set_index('Country Name', inplace=True)

inflationDF.index.name = None

inflationDF = inflationDF.T.reset_index().set_index('index')

inflationDF.index.name = 'Year'


# Call and store inflation data into a dataframe.
unemploymentDF = pd.read_excel('https://github.com/ObamaBinModdin/CS445-Final_Project/raw/main/unemployment_rate.xlsx')

# Replace all ".." values to "nan".
unemploymentDF = unemploymentDF.replace('..', np.nan)

# Change all year columns to type float.
unemploymentDF.iloc[:, 4:] = unemploymentDF.iloc[:, 4:].astype(float)

# Replace all "nan" values to the column mean ignoring outliers.
for col in unemploymentDF.iloc[:, 4:].columns:
    Q1 = unemploymentDF[col].quantile(0.25)
    Q3 = unemploymentDF[col].quantile(0.75)
    IQR = Q3 - Q1
    df_filtered = unemploymentDF[(unemploymentDF[col] >= Q1 - 1.5 * IQR) & (unemploymentDF[col] <= Q3 + 1.5 * IQR)]
    mean_col = df_filtered[col].mean()
    unemploymentDF[col] = unemploymentDF[col].fillna(mean_col)

unemploymentDF.drop(['Country Code', 'Series Code', 'Country Code', 'Series Name'], inplace=True, axis=1)

unemploymentDF.set_index('Country Name', inplace=True)

unemploymentDF.index.name = None

unemploymentDF = unemploymentDF.T.reset_index().set_index('index')

unemploymentDF.index.name = 'Year'


fig1 = bcr.bar_chart_race(df=inflationDF, title='My first bar chart race', steps_per_period=10,
                                period_length=500, n_bars=10, interpolate_period=False,
                                period_label={'x': .95, 'y': .5, 'ha': 'right', 'va': 'center'},
                                period_fmt='Race 1: {x}', filename='test1.mp4')

# Create the second bar chart race
fig2 = bcr.bar_chart_race(df=unemploymentDF, n_bars=10, title='My second bar chart race', steps_per_period=10,
                                period_length=500, interpolate_period=False,
                                period_label={'x': .05, 'y': .5, 'ha': 'left', 'va': 'center'},
                                period_fmt='Race 2: {x}', filename='test2.mp4')

print('got here 2.0')

clip1 = VideoFileClip('test1.mp4')
clip2 = VideoFileClip('test2.mp4')

# Resize the videos to the same height
clip1 = clip1.resize(height=360)
clip2 = clip2.resize(height=360)

# Combine the videos side by side
final_clip = clips_array([[clip1, clip2]])

# Write the final clip to a new file
final_clip.write_videofile('combined.mp4')
