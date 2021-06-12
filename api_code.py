import requests
import pandas as pd
import numpy as np

# BLOCK1
entrypoint = "https://api.usa.gov/crime/fbi/sapi/api/agencies"
query = {'api_key': 'e8vEnIM7V1Msff37SGU86c4r27dVzZOUow7LFCiM'}
r = requests.get(entrypoint, params=query)
data = r.json()
columns_all = ['ori', 'agency_name', 'agency_type_name', 'state_name', 'state_abbr', 'division_name', 'region_name',
               'region_desc', 'county_name', 'nibrs', 'latitude', 'longitude', 'nibrs_start_date']
summ_all = pd.DataFrame(columns=columns_all)
for i in data:
    for j in data[i]:
        a = (data[i][j])
        new = []
        for k in a:
            new += [a[k]]
        summ_all.loc[len(summ_all)] = new
print(summ_all)

summ_all.to_csv(r"summ_all.csv")

summ_all = pd.read_csv("summ_all.csv")

# BLOCK2
summ_all = (summ_all).dropna()
ct = summ_all[(summ_all['state_abbr'] == "KS")].reset_index().dropna()
ct["Cases"] = np.nan

ct = summ_all[(summ_all['state_abbr'] == "KS")].reset_index().dropna()
ct["Cases"] = np.nan
for ori in ct['ori']:
    entrypoint = "https://api.usa.gov/crime/fbi/sapi/api/data/arrest/agencies/offense/" + ori + "/all/2019/2019"
    query = {'api_key': 'e8vEnIM7V1Msff37SGU86c4r27dVzZOUow7LFCiM'}
    data2 = requests.get(entrypoint, params=query).json()
    for h in data2:
        if type(data2[h]) == list and data2[h] != []:
            data2[h][0].pop("data_year")
            data2[h][0].pop("csv_header")
            values = data2[h][0].values()
            ct["Cases"][ct['ori'] == ori] = sum(values)

ct.to_csv(r"ct.csv")
ct = pd.read_csv("ct.csv")

# BLOCK4
# state_data=((summ_all['state_abbr'].unique()))
state_data = ['HI', 'DE', 'PR', 'TX', 'MA', 'MD', 'ME', 'IA', 'ID', 'MI', 'UT', 'MN', 'MO', 'IL',
              'IN', 'MS', 'MT', 'AK', 'VA', 'AL', 'AR', 'VI', 'NC', 'ND', 'RI', 'NE', 'AZ', 'NH',
              'NJ', 'VT', 'NM', 'FL', 'NV', 'WA', 'NY', 'SC', 'SD', 'WI', 'OH', 'GA', 'OK', 'CA',
              'WV', 'WY', 'OR', 'GM', 'KS', 'CO', 'KY', 'PA', 'CT', 'LA', 'TN', 'DC']
# EXCLUDE "PR"
offenses = ["aggravated-assault", "burglary", "larceny", "motor-vehicle-theft", "homicide", "rape", "robbery",
            "arson",
            "violent-crime", "property-crime"]
col_det = ["ori", "data_year", "offense", "state_abbr", "cleared", "actual"]
years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
summ_off = pd.DataFrame()
for abbr in state_data:
    state_alloff = pd.DataFrame()
    for off in offenses:
        state_off = pd.DataFrame(np.nan, index=[abbr], columns=years)
        entrypoint1 = "https://api.usa.gov/crime/fbi/sapi/api/nibrs/" + off + "/victim/states/" + abbr + "/count"
        print(entrypoint1)
        query = {'api_key': 'e8vEnIM7V1Msff37SGU86c4r27dVzZOUow7LFCiM'}
        r1 = requests.get(entrypoint1, params=query)
        data1 = r1.json()
        for i in data1:
            if type(data1[i]) == list and data1[i] != ['Count'] and data1[i] != []:
                for j in data1[i]:
                    if years.count(str(j['data_year'])) == 1:
                        state_off[str(j['data_year'])] = j['value']
                        state_off["Offense"] = off

        state_alloff = state_alloff.append(state_off)
    summ_off = summ_off.append(state_alloff)

summ_off.to_csv(r"summ_off.csv")
summ_off = pd.read_csv("summ_off.csv")

