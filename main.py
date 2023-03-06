import numpy as np
import pandas as pd

# Call and store inflation data into a dataframe.
inflationDF = pd.read_excel('https://github.com/ObamaBinModdin/CS445-Final_Project/raw/main/inflation.xlsx')

# Replace all ".." values to "nan".
inflationDF = inflationDF.replace('..', np.nan)

# Change all year columns to type float.
inflationDF.iloc[:, 4:] = inflationDF.iloc[:, 4:].astype(float)

# Replace all "nan" values to the column mean ignoring outliers.
for col in inflationDF.iloc[:, 4:].columns:
    Q1 = inflationDF[col].quantile(0.25)
    Q3 = inflationDF[col].quantile(0.75)
    IQR = Q3 - Q1
    df_filtered = inflationDF[(inflationDF[col] >= Q1 - 1.5*IQR) & (inflationDF[col] <= Q3 + 1.5*IQR)]
    mean_col = df_filtered[col].mean()
    inflationDF[col] = inflationDF[col].fillna(mean_col)
