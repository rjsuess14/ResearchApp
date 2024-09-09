import os
import pandas as pd
import numpy as np


def clean_fd_df(df):
    # Drop unused columns
    df.drop(columns=['ticker','calendar_date','period'], inplace=True)

    # Set date as index and sort
    df.set_index('report_period', inplace=True)
    df.sort_index(inplace=True)

    # Remove duplicate entries
    df = df[~df.index.duplicated(keep='first')]

    # Convert numeric columns to float
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].astype(float)

    # Handle missing values (you might want to adjust this based on your specific needs)
    df.fillna(0, inplace=True)

    # Transpose the DataFrame
    df = df.transpose()  # This flips the DataFrame
    return df


def clean_fmp_df(df):
    # Drop unused columns
    df.drop(columns=['symbol','reportedCurrency','cik', 'fillingDate', 'acceptedDate', 'period'], inplace=True)

    # Set date as index and sort
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)

    # Remove duplicate entries
    df = df[~df.index.duplicated(keep='first')]

    # Convert numeric columns to float
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].astype(float)

    # Handle missing values (you might want to adjust this based on your specific needs)
    df.fillna(0, inplace=True)

    # Transpose the DataFrame
    df = df.transpose()  # This flips the DataFrame
    return df