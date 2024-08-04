import pandas as pd
import locale
from datetime import datetime


def translate_activity(activity_type):
    if activity_type == "Laufen":
        activity_type = "Running"
    return activity_type


def create_date_obj(date_str):
    # Setting locale to German
    locale.setlocale(locale.LC_TIME, 'deu_deu')
    # Converting the string to a datetime object
    date_obj = datetime.strptime(date_str, "%a, %b %d, %Y %H:%M")
    return date_obj


def remove_text_from_speed(speed_str):
    speed_in_minutes_per_kilometer = speed_str.split()[0]
    return speed_in_minutes_per_kilometer

# Importing the csv
df = pd.read_csv('activities.csv')

numeric_cols = df.select_dtypes(include='number').columns
object_cols = df.select_dtypes(include='object').columns

df[numeric_cols] = df[numeric_cols].fillna(0)
df[object_cols] = df[object_cols].fillna('N/A')

for column in df.columns:
    print(column)

# Applying the functions whereever needed
df["Activity Type"] = df["Activity Type"].apply(translate_activity)
df["Begin Timestamp"] = df["Begin Timestamp"].apply(create_date_obj)
df["End Timestamp"] = df["End Timestamp"].apply(create_date_obj)
df["Average Speed"] = df["Average Speed"].apply(remove_text_from_speed)

# Selecting the required columns ignoring the the columns that are repeated

# column_of_interest_user = ["user_id", "name", "age", "gender", "height", "weight"]

column_of_interest_activity = ["Activity ID", "Activity Type", "Begin Timestamp", "End Timestamp", "Max. Elevation (Raw)",
                               "Min. Elevation (Raw)", "Elevation Gain (Raw)", "Elevation Loss (Raw)",
                               "Average Heart Rate (bpm)", "Max. Heart Rate (bpm).1", "Average Moving Speed",
                               "Average Speed", "Max. Speed", "Distance (Raw)", "Duration (h:m:s)",
                               "Moving Duration (h:m:s)"]

column_of_interest_geo = ["Begin Latitude (Decimal Degrees Raw)", "Begin Longitude (Decimal Degrees Raw)",
                          "End Latitude (Decimal Degrees Raw)", "End Longitude (Decimal Degrees Raw)",
                          "Temperature (Raw)", "Wind Speed (Raw)", "Wind Direction", "Humidity (Raw)", "Condition",
                          "Rainfall"]

# Creating separate DataFrames for each set of columns
df_activity = df[column_of_interest_activity]
df_geo = df[column_of_interest_geo]

# Concatenating the DataFrames vertically
df_combined = pd.concat([df_activity, df_geo], axis=1)

# Saving the combined DataFrame to a single CSV file
df_combined.to_csv('activities_cleaned.csv', index=False)
