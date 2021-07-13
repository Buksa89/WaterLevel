#!/usr/bin/env python3
import pandas as pd
import sqlalchemy
from db_data import *

engine = sqlalchemy.create_engine(f'{dbtype}://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}')


# Import hydro data from api and create DataFrame
url = "https://danepubliczne.imgw.pl/api/data/hydro/"

df = pd.read_json(url)
df = df[["id_stacji", "stan_wody", "stan_wody_data_pomiaru"]]
df.columns = ['station_id',  'value', 'datetime']
df["datetime"] = pd.to_datetime(df["datetime"], format='%Y-%m-%d %H:%M:%S', errors='ignore')
df.dropna(inplace=True)

# Save hydro data to database if not exist
for index, row in df.iterrows():
    with engine.connect() as connection:

        result = connection.execute(f"""SELECT
            COUNT(*)
        FROM {hdtable}
        WHERE station_id = {row["station_id"]} AND
        value = {row["value"]} AND 
        datetime = '{row["datetime"]}'
        """)
        for res in result:
            if res[0]:
                pass
            else:
                row = row.to_frame().T
                row.to_sql(hdtable, engine, if_exists='append', index=False)
                print(row)

# Import weather data from api and create DataFrame
url = "https://danepubliczne.imgw.pl/api/data/synop/"

df = pd.read_json(url)
df = df[["id_stacji","data_pomiaru","godzina_pomiaru","suma_opadu"]]
df["datetime"] = pd.to_datetime(df["data_pomiaru"], format='%Y-%m-%d', errors='ignore') + df["godzina_pomiaru"].apply(lambda hour: timedelta(hours=hour))
df.drop(columns=["data_pomiaru","godzina_pomiaru"], inplace=True)
df.columns = ['station_id',  'value', 'datetime']
df.dropna(inplace=True)

# Save weather data to database if not exist
for index, row in df.iterrows():
    with engine.connect() as connection:

        result = connection.execute(f"""SELECT
            COUNT(*)
        FROM {wdtable}
        WHERE station_id = {row["station_id"]} AND
        value = {row["value"]} AND 
        datetime = '{row["datetime"]}'
        """)
        for res in result:
            if res[0]:
                pass
            else:
                row = row.to_frame().T
                row.to_sql(wdtable, engine, if_exists='append', index=False)
                print(row)