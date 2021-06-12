import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import folium
import requests
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import streamlit as st
from streamlit_folium import folium_static
import streamlit.components.v1 as components


from bs4 import BeautifulSoup

import regex

with st.echo(code_location='below'):
    # st.set_page_config(layout="wide")
    st.write('Цель данного проекта - рассмотрение статистики по правонарушениям и преступлениям (англ. - offenses) '
             'в США в течение последних десяти лет.')

    # #BLOCK1
    # entrypoint = "https://api.usa.gov/crime/fbi/sapi/api/agencies"
    # query = {'api_key': 'e8vEnIM7V1Msff37SGU86c4r27dVzZOUow7LFCiM'}
    # r = requests.get(entrypoint, params=query)
    # data = r.json()
    # columns_all = ['ori', 'agency_name', 'agency_type_name', 'state_name', 'state_abbr', 'division_name', 'region_name',
    #                'region_desc', 'county_name', 'nibrs', 'latitude', 'longitude', 'nibrs_start_date']
    # summ_all = pd.DataFrame(columns=columns_all)
    # for i in data:
    #     for j in data[i]:
    #         a = (data[i][j])
    #         new = []
    #         for k in a:
    #             new += [a[k]]
    #         summ_all.loc[len(summ_all)] = new
    # print(summ_all)
    summ_all = pd.read_csv("summ_all.csv")

    # BLOCK2
    summ_all = (summ_all).dropna()
    st.write(
        'На данной карте представлены все агентства, подключенные к системе NIBRS (Национальная система отчетности об инцидентах) '
        'Можно заметить, что данной системой активно пользуются в восточной части страны, а западной части сотаются '
        'целые штаты, в которых ни одно агентство не используют NIBRS. '
        'Например, в Пенсильвании находится более 1500 агентств, однако системой пользуют только 25 агентств. ')
    m = folium.Map([41.75215, -97.61819], zoom_start=4)
    for ind, row in summ_all.iterrows():
        folium.Circle([row.latitude, row.longitude],
                      radius=10).add_to(m)
    folium_static(m)
    # ct = summ_all[(summ_all['state_abbr'] == "KS")].reset_index().dropna()
    # ct["Cases"] = np.nan
    # for ori in ct['ori']:
    # entrypoint = "https://api.usa.gov/crime/fbi/sapi/api/data/arrest/agencies/offense/" + ori + "/all/2019/2019"
    # query = {'api_key': 'e8vEnIM7V1Msff37SGU86c4r27dVzZOUow7LFCiM'}
    # data2 = requests.get(entrypoint, params=query).json()
    # for h in data2:
    #     if type(data2[h]) == list and data2[h] != []:
    #         data2[h][0].pop("data_year")
    #         data2[h][0].pop("csv_header")
    #         values = data2[h][0].values()
    #         ct["Cases"][ct['ori'] == ori] = sum(values)

    ct = pd.read_csv("ct.csv")

    # BLOCK3
    st.write(
        'Давайте более подробно изучим статистики в одном из штатов. На карте расположены все агнетства штата Канзас. '
        'Размер точек зависит от количества зарегистрированных правонарушений или преступлений в 2019 году. ')
    st.write("Число агентств в Казасе:")
    st.write(pd.value_counts(summ_all['state_abbr'])["KS"])

    ct = ct.dropna()
    ct = ct.sort_values(by="Cases")
    fig = go.Figure()
    ct['text'] = "Number of registered offenses in " + ct['agency_name'] + " is " + (ct["Cases"]).astype(str)
    limits = [(0, 10), (10, 100), (100, 1000), (1000, 3000), (3000, 15000)]
    colors = ["royalblue", "crimson", "lightseagreen", "orange", "lightgrey"]
    cities = []
    scale = 5
    fig = go.Figure()
    # print(sum(ct["Cases"]))

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = ct[(ct["Cases"] >= lim[0]) & (ct["Cases"] < lim[1])]
        fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            lon=df_sub['longitude'],
            lat=df_sub['latitude'],
            text=df_sub['text'],
            marker=dict(
                size=df_sub['Cases'] / scale,
                color=colors[i],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area'
            ),
            name='{0} - {1}'.format(lim[0], lim[1])))

    fig.update_layout(width=800, height=400,
                      geo=dict(
                          scope='north america',
                          showland=True,
                          landcolor="rgb(212, 212, 212)",
                          subunitcolor="rgb(255, 255, 255)",
                          center_lon=-98.0,
                          center_lat=38.45,
                          resolution=50,
                          coastlinecolor="white",
                          lonaxis=dict(
                              range=[-102.0, -93.0]
                          ),
                          lataxis=dict(
                              range=[36.8, 40.2]
                          ),
                          domain=dict(x=[0, 1], y=[0, 1])),
                      title='Agencies by offenses, Kansas, 2019',
                      )
    st.plotly_chart(fig)

    # #BLOCK4
    # # state_data=((summ_all['state_abbr'].unique()))
    # state_data = ['HI', 'DE', 'PR', 'TX', 'MA', 'MD', 'ME', 'IA', 'ID', 'MI', 'UT', 'MN', 'MO', 'IL',
    #               'IN', 'MS', 'MT', 'AK', 'VA', 'AL', 'AR', 'VI', 'NC', 'ND', 'RI', 'NE', 'AZ', 'NH',
    #               'NJ', 'VT', 'NM', 'FL', 'NV', 'WA', 'NY', 'SC', 'SD', 'WI', 'OH', 'GA', 'OK', 'CA',
    #               'WV', 'WY', 'OR', 'GM', 'KS', 'CO', 'KY', 'PA', 'CT', 'LA', 'TN', 'DC']
    # # EXCLUDE "PR"
    # offenses = ["aggravated-assault", "burglary", "larceny", "motor-vehicle-theft", "homicide", "rape", "robbery",
    #             "arson",
    #             "violent-crime", "property-crime"]
    # col_det = ["ori", "data_year", "offense", "state_abbr", "cleared", "actual"]
    # years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
    # summ_off = pd.DataFrame()
    # for abbr in state_data:
    #     state_alloff = pd.DataFrame()
    #     for off in offenses:
    #         state_off = pd.DataFrame(np.nan, index=[abbr], columns=years)
    #         entrypoint1 = "https://api.usa.gov/crime/fbi/sapi/api/nibrs/" + off + "/victim/states/" + abbr + "/count"
    #         print(entrypoint1)
    #         query = {'api_key': 'e8vEnIM7V1Msff37SGU86c4r27dVzZOUow7LFCiM'}
    #         r1 = requests.get(entrypoint1, params=query)
    #         data1 = r1.json()
    #         for i in data1:
    #             if type(data1[i]) == list and data1[i] != ['Count'] and data1[i] != []:
    #                 for j in data1[i]:
    #                     if years.count(str(j['data_year'])) == 1:
    #                         state_off[str(j['data_year'])] = j['value']
    #                         state_off["Offense"] = off
    #
    #         state_alloff = state_alloff.append(state_off)
    #     summ_off = summ_off.append(state_alloff)

    summ_off = pd.read_csv("summ_off.csv")
    # print(summ_off)

    # BLOCK5

    state_data = ['HI', 'DE', 'PR', 'TX', 'MA', 'MD', 'ME', 'IA', 'ID', 'MI', 'UT', 'MN', 'MO', 'IL',
                  'IN', 'MS', 'MT', 'AK', 'VA', 'AL', 'AR', 'VI', 'NC', 'ND', 'RI', 'NE', 'AZ', 'NH',
                  'NJ', 'VT', 'NM', 'FL', 'NV', 'WA', 'NY', 'SC', 'SD', 'WI', 'OH', 'GA', 'OK', 'CA',
                  'WV', 'WY', 'OR', 'GM', 'KS', 'CO', 'KY', 'PA', 'CT', 'LA', 'TN', 'DC']
    columns_all = summ_off.columns
    agr_off = pd.DataFrame()
    agr_off = pd.DataFrame(columns=columns_all)
    for i in range(len(state_data)):
        agr_off.loc[len(agr_off)] = summ_off.iloc[range(i, i + 10), :].sum(numeric_only=True)

    agr_off["Offense"] = state_data
    agr_off = (agr_off.set_index("Offense"))
    sort = agr_off.sort_values(by="2019", ascending=False).head(10)
    # sort.to_csv("sorted_by_state.csv")

    # BLOCK6

    name = "https://datausa.io/profile/geo/kansas"
    r = requests.get(name)
    soup = BeautifulSoup(r.text)
    ans = soup.find("head")
    cont = ((soup.find("head")).find_all("meta", {"name": "description"}))[0]['content']
    st.write('Возьмём информацию о населении Канзаса с сайта datausa.io: ')
    st.write(cont)
    pop = (regex.findall(r"(?<=[^\Wm])\s[\d]+\W+[\d]+\w[M]", cont))
    st.write("С помощью регулярных выражений найдем население Канзаса в 2018 году - ")
    st.write(pop)

    # BLOCK7
    st.write('Далее рассмотрим правонарушения или преступления, совершенные с 2010 года, вычислив общее количество '
             'преступлений в каждый год. Можно заметить, что суммарное число правонарушений или преступлений в год '
             'снижается. На основе этих данных построим предсказание на 2020 год. ')
    ind_list = range(460, 470)
    ks_off = (summ_off.iloc[ind_list, :])
    ks_total = ks_off.sum(numeric_only=True)
    usa_total = summ_off.sum(numeric_only=True)
    regr = LinearRegression()
    X = np.array([2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]).reshape((-1, 1))
    y = [0]
    y[0] = ks_total
    regr.fit(X, y[0])
    figpr = plt.figure()
    plt.plot(X, y[0])
    plt.title("Offenses in Kansas, 2010-2019")
    plt.plot(X, regr.predict(X), color='C1')
    st.pyplot(figpr)
    #
    # z=[0]
    # A=X
    #
    # z[0]=usa_total
    # figall = plt.figure()
    # plt.plot(A, z[0])
    # plt.plot(A, regr.predict(A), color='C1')
    # st.pyplot(figall)
    st.write('Predicition for 2020')
    st.write(regr.predict(np.array([[2020]])))

    # BLOCK8
    st.write('Рассчитаем корреляцию между уровенем безработицы, ВВП на душу населения'
             'и числом правонарушений.')
    unemp = np.array((pd.read_csv("KSURN.csv"))["KSURN"])
    gdp_h = np.array((pd.read_csv("MEHOINUSKSA672N.csv"))["MEHOINUSKSA672N"])
    u, u_sd = (np.around(np.mean(unemp), decimals=3), np.around(np.std(unemp), decimals=3))
    g, g_sd = (np.around(np.mean(gdp_h / 1000), decimals=3), np.around(np.std(gdp_h / 1000), decimals=3))
    st.write('Безработица и ВВП на душу населния в Канзасе, 2009-2019:')
    st.write(pd.read_csv("KSURN.csv"))
    st.write('ВВП на душу населения в Канзасе, 2009-2019:')
    st.write(pd.read_csv("MEHOINUSKSA672N.csv"))
    st.write("Коэффициент корреляции между безработицей и ВВП на душу населения:")
    st.write(np.corrcoef(unemp, gdp_h)[0, 1])
    st.write("Коэффициент корреляции между безработицей и числом правонарушений:")
    st.write(np.corrcoef(unemp[1:], np.array(ks_total))[0, 1])
    st.write("Коэффициент корреляции между ВВП на душу населения и числом правонарушений:")
    st.write(np.corrcoef(gdp_h[1:], np.array(ks_total))[0, 1])

    # BLOCK9

    import networkx as nx

    df = pd.read_csv("results.csv")
    df = df[~df['to'].str.contains('(page does not exist)')]
    a = (df['from'].value_counts())
    st.write("С помощью scrapy зайдем на страницу List of law enforcement agencies in Kansas в Википедии. "
             "Большинство ссылок недействительны, так как для многих учреждений ещё не созданы страницы. "
             "Ниже на графе представлены те страницы, страницы для которых на данный момент сущестувуют. "
             "Цифрами обозначены количество страниц, на которые с них можно перейти. ")
    list1 = ["List of law enforcement agencies in Kansas"] * (len(a) - 1)
    list2 = ["Kansas Department of Wildlife, Parks and Tourism", "Fort Hays State University",
             "Overland\nPark\nPolice\nDepartment", "Wichita\nPolice\nDepartment"]

    fign, ax = plt.subplots(figsize=(15, 8))
    edges = zip(list1, list2)
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, width=1, edge_color="blue", linewidths=1, node_size=500, node_color='skyblue',
            labels={node: node for node in G.nodes()})
    nx.draw_networkx_edge_labels(G, pos, edge_labels=
    {('List of law enforcement agencies in Kansas', 'Kansas Department of Wildlife, Parks and Tourism'): str(a[1]),
     ('List of law enforcement agencies in Kansas', 'Fort Hays State University'): str(a[2]),
     ('List of law enforcement agencies in Kansas', 'Overland\nPark\nPolice\nDepartment'): str(a[3]),
     ('List of law enforcement agencies in Kansas', 'Wichita\nPolice\nDepartment'): str(a[4])}, font_color='red')
    # Проблемы с выводом nx решаются (согласно советам из интернета) с помощью установки более ранней версии
    # matplotlib, однако для моец версии python установка matplotlib 2.2.3 уже невозможна. К счастью, в Jupyter
    # Notebook у меня всё построилось. Прилагаю граф, построенный Jupyter.

    st.image("graph.png")
    # BLOCK10
    # BLOCK11
    st.header("The analysis of offenses in Kansas in 2020")
    HtmlFile = open("r_code.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    st.markdown(source_code, unsafe_allow_html=True)

