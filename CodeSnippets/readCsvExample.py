import pandas
import datetime

data = pandas.read_csv("./../boundary_crossings_caracteristics_BS.csv", sep=';')

dates = data["Date (year/month/day)"]
times = data["Time (HH:MM)"]

# convert from string to datetime

