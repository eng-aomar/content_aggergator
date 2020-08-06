import pandas as pd
import geopandas as gpd

data = pd.read_html('https://www.worldometers.info/coronavirus/')

for data_cases in data:
    print(data_cases)

