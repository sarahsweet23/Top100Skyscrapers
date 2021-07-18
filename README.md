import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import csv
import pydeck as pdk
from PIL import Image

def scatterplot():
    skyscrapers_data = pd.read_csv("Skyscrapers2021.csv")
    completion_year_List = []
    meters_List = []
    for row in skyscrapers_data:
        # st.write(row)
        completion_year = pd.to_numeric(skyscrapers_data.COMPLETION)
        # print(completion_year)
        completion_year_List.append(completion_year)
        meters = skyscrapers_data.Meters.str.replace(r'\s+m', '').astype(float)
        meters_List.append(meters)

        plt.xlabel("Completion Year",fontsize=10)
        plt.ylabel("Meters",fontsize=10)
        plt.title("Height & Numbers along with completion year",fontsize=13)
        plt.scatter(completion_year_List, meters_List, alpha=0.3, marker=".", color="cornflowerblue")
        plt.show()
        #return plt

#这个就是你之前的rank_map函数 我改名字为whole_mao(),为了和下面的rank_map()区分
def whole_map():
    skyscrapers_data = pd.read_csv("Skyscrapers2021.csv")
    sky_df = pd.DataFrame(skyscrapers_data, columns=["RANK", "Latitude", "Longitude"])
    sky_df.rename(columns={"Latitude": "lat", "Longitude": "lon"},inplace=True)
    st.map(sky_df)

#新rank_map()函数,显示按照rank选择出来的大楼
def rank_map(select_rank):
    skyscrapers_data = pd.read_csv("Skyscrapers2021.csv")
    sky_df = pd.DataFrame(skyscrapers_data, columns=["RANK", "CITY", "Latitude", "Longitude"])
    sky_df.rename(columns={"Latitude": "lat", "Longitude": "lon"}, inplace=True)
    select_rank_max = select_rank + 19
    rank_df = sky_df[(sky_df['RANK'] >= select_rank) & (sky_df['RANK'] <= select_rank_max)]
    #在sidebar展示数据表格
    rank_df_show = pd.DataFrame(rank_df, columns=['CITY', 'lon', 'lat'])
    st.sidebar.table(rank_df_show)
    #画出地图
    st.pydeck_chart(pdk.Deck(
        map_style = 'mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=rank_df['lat'].mean(),
            longitude=rank_df['lon'].mean(),
            zoom=1,
            pitch=0
        ),
        layers = [
            pdk.Layer(
                'HexagonLayer',
                data=rank_df,
                get_position = '[lon, lat]',
                radius = 200000,
                elevation_scale = 10000,
                elevation_range = [400,1000],
                pickable = True,
                extruded = True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=rank_df,
                get_position='[lon, lat]',
                get_color = '[200, 30, 0, 160]',
                get_radius = 200000,
            ),
        ],
    ))

#按照选择年份画出平均高度的折线图
def average_height_line_chart(select_year):
    average_height_df =pd.DataFrame(columns=['Year', 'AverageHeight'])
    skyscrapers_data = pd.read_csv("Skyscrapers2021.csv")
    year_df = pd.DataFrame(skyscrapers_data, columns=["COMPLETION", "Meters"])
    year_df.COMPLETION = pd.to_numeric(year_df.COMPLETION)
    year_df.Meters = year_df.Meters.str.replace(r'\s+m', '').astype(float)
    year_df = year_df[year_df['COMPLETION']<= select_year]
    year_df.sort_values(by = ['COMPLETION'], ascending = True, inplace= True)
    for year in range(1931, select_year):#之前你这写的是1931~1991，估计这是为什么只显示到1991吧
        mean_height = (year_df[['Meters']][year_df['COMPLETION'] <= year]).mean()
        a = {'Year': year, 'AverageHeight': mean_height}
        average_height_df = average_height_df.append(a, ignore_index=True)
    plt.xlabel("Completion Year",fontsize=10)
    plt.ylabel("Average Height",fontsize=10)
    plt.title("Average Height along with completion year",fontsize=13)
    plt.plot(average_height_df.Year, average_height_df.AverageHeight)
    plt.show()

def statisticchart(selection):
    if selection == "By Function":
        fp = open('Skyscrapers2021.csv', 'r')
        reader = csv.reader(fp)
        count = 0
        d = {'office': 0, 'hotel': 0, 'residential': 0, 'hotel / office': 0, 'residential / office': 0,
             'multifunction': 0}
        for row in reader:
            if count > 0:
                label = row[12]
                if label == 'office':
                    d['office'] += 1
                elif label == 'hotel':
                    d['hotel'] += 1
                elif label == 'residential':
                    d['residential'] += 1
                elif label == 'hotel / office':
                    d['hotel / office'] += 1
                elif label == 'residential / office':
                    d['residential / office'] += 1
                else:
                    d['multifunction'] += 1
            count += 1

        label = []
        values = []
        for key in d:
            label.append(key)
            values.append(d[key])
        EXPLODE_VALUE = 0.1
        max_percentage = max(d.values())
        max_percentage_index = values.index(max_percentage)
        explode_values = [0] * len(label)
        explode_values[max_percentage_index] = EXPLODE_VALUE
        colors = ["skyblue", "cadetblue", "cornflowerblue","powderblue","steelblue","lightslategray"]
        plt.pie(values, labels=label, colors=colors,explode=explode_values, autopct='%1.1f%%', startangle=90,
                textprops={'fontsize': 10})
        plt.show()

        plt.rcParams.update({"font.size": 7})
        plt.legend(loc="lower right", bbox_to_anchor=(1.5, 0))
        plt.show()
    else:
        skyscrapers_data = pd.read_csv("Skyscrapers2021.csv")
        material_description = {}
        for i in skyscrapers_data["MATERIAL"]:
            if i in material_description:
                material_description[i] += 1
            else:
                material_description[i] = 1
        material_Percentage_Value = material_description.values()
        labels = material_description.keys()
        mfunction = [x for x in material_Percentage_Value]
        st.set_option('deprecation.showPyplotGlobalUse', False)

        EXPLODE_VALUE = 0.1
        max_percentage = max(material_Percentage_Value)
        max_percentage_index = mfunction.index(max_percentage)
        explode_values = [0] * len(labels)
        explode_values[max_percentage_index] = EXPLODE_VALUE
        colors = ["tan", "peru", "orange", "gold"]

        plt.pie(mfunction, labels=labels, colors=colors, explode=explode_values, autopct='%1.1f%%', startangle=90,
                textprops={'fontsize': 10})
        plt.legend(loc="lower right", bbox_to_anchor=(1.5, 0))
        plt.show()

    return plt

def main():
    skyscrapers_data = pd.read_csv("Skyscrapers2021.csv")
    img = Image.open("photo.jpg")
    st.image(img, width=700)
    st.title("Top 100 Skyscrapers around the world!")
    if st.checkbox("Show DataFrame"):
        st.dataframe(skyscrapers_data, width=700, height=300)
    if st.checkbox("Show all 100 Skyscrapers in the map"):
        whole_map()

    # sidebar选择rank
    rank = st.sidebar.selectbox('Select rank:', ('1~20', '21~40', '41~60', '61~80', '81~100'))
    rank_list = {'1~20': 1, '21~40': 21, '41~60': 41, '61~80': 61, '81~100': 81}
    select_rank = rank_list[rank]
    # 用选好的年份画map
    st.write('Skyscrapers Rank ' + str(select_rank) + ' ~ ' + str(select_rank+19))
    rank_map(select_rank)

    #去除一个不重要的警告信息
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(scatterplot())

    # 插入pivot table
    skyscrapers_data = pd.read_csv("Skyscrapers2021.csv")
    skyscrapers_data.Meters = skyscrapers_data.Meters.str.replace(r'\s+m', '').astype(float)
    tt = pd.pivot_table(skyscrapers_data, index=['CITY', 'COMPLETION', 'MATERIAL'],values=['Meters','Latitude','Longitude'])
    st.dataframe(tt)

    # sidebar选择年份
    select_year = st.sidebar.slider("Select years", 1931, 2020)
    # 用选好的年份画折线图
    st.pyplot(average_height_line_chart(select_year))

    selection = st.sidebar.selectbox("Select an option: ",("By Function", "By Material"))
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(statisticchart(selection))

main()
