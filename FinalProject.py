"""
Name: Ruby Ren
CS230: Section N2
Data: Skyscrapers2021.csv
URL: Link to your web application online (see extra credit)
Description:
This program imports file as a dataframe, displays the 100 Skyscrapers around the world, allows users to explore every 20
skyscrapers each time by narrowing down the selection range,shows the skyscrapers Height & Numbers along with the year,
users can also check the average meters until a specific year as well as the function & material percentage both by
interaction.


"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import csv
import pydeck as pdk
from PIL import Image


# draw a scatter plot to show the skyscrapers Height & Numbers along with the year
def scatterplot():
    skyscrapers_data = pd.read_csv("Skyscrapers2021.csv")
    completion_year_List = []
    meters_List = []
    for row in skyscrapers_data:
        # st.write(row)
        completion_year = pd.to_numeric(skyscrapers_data.COMPLETION)
        # print(completion_year)
        completion_year_List.append(completion_year)
        meters = skyscrapers_data.Meters.str.replace(r"\s+m", "").astype(float)  # ger rid of the space and "m"
        meters_List.append(meters)

        plt.xlabel("Completion Year", fontsize=10)
        plt.ylabel("Meters", fontsize=10)
        plt.title("Height & Numbers along with completion year", fontsize=13)
        plt.scatter(completion_year_List, meters_List, alpha=0.3, marker=".", color="cornflowerblue")
        plt.show()
        # return plt


# show all the top 100 Skyscrapers around the world
def whole_map():
    skyscrapers_data = pd.read_csv("Skyscrapers2021.csv")
    sky_df = pd.DataFrame(skyscrapers_data, columns=["RANK", "Latitude", "Longitude"])
    sky_df.rename(columns={"Latitude": "lat", "Longitude": "lon"}, inplace=True)
    st.map(sky_df)


# show every 20 Skyscrapers around the world(narrow down)
@st.cache
def rank_map(select_rank):
    skyscrapers_data = pd.read_csv("Skyscrapers2021.csv")
    sky_df = pd.DataFrame(skyscrapers_data, columns=["RANK", "CITY", "Latitude", "Longitude"])
    sky_df.rename(columns={"Latitude": "lat", "Longitude": "lon"}, inplace=True)


    select_rank_max = select_rank + 19  # 5 select rank  is 1, 21,,41,61,81, the max will be 20, 40, 60, 80, 100
    rank_df = sky_df[(sky_df["RANK"] >= select_rank) & (sky_df["RANK"] <= select_rank_max)]  # pick 20 buildings

    rank_df_show = pd.DataFrame(rank_df, columns=["CITY", "lon", "lat"])  # display corresponding info on the side
    st.sidebar.table(rank_df_show)

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=rank_df["lat"].mean(),
            longitude=rank_df["lon"].mean(),
            zoom=1,
            pitch=0
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=rank_df,
                get_position="[lon, lat]",
                radius=200000,
                elevation_scale=10000,
                elevation_range=[500, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=rank_df,
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200000,
            ),
        ],
    ))


# line chart to show the average meters until a specific year,eg: if choose year 2000,year 2000 will display the
# average height  that all the skyscrapers achieved until 2000 not just in 2000---the single year
def average_height_line_chart(select_year):
    average_height_df = pd.DataFrame(columns=["Year", "AverageHeight"])
    skyscrapers_data = pd.read_csv("Skyscrapers2021.csv")
    year_df = pd.DataFrame(skyscrapers_data, columns=["COMPLETION", "Meters"])
    year_df.COMPLETION = pd.to_numeric(year_df.COMPLETION)
    year_df.Meters = year_df.Meters.str.replace(r"\s+m", "").astype(float)
    year_df = year_df[year_df["COMPLETION"] <= select_year]
    year_df.sort_values(by=["COMPLETION"], ascending=True, inplace=True)
    for year in range(1931, select_year):
        mean_height = (year_df[["Meters"]][year_df["COMPLETION"] <= year]).mean()
        a = {"Year": year, "AverageHeight": mean_height}
        average_height_df = average_height_df.append(a, ignore_index=True)
    plt.xlabel("Completion Year", fontsize=10)
    plt.ylabel("Average Height", fontsize=10)
    plt.title("Average Height along with completion year", fontsize=13)
    plt.plot(average_height_df.Year, average_height_df.AverageHeight)
    plt.show()


# pie chart to display the percentage of skyscrapers' function and material among 100 skyscrapers
def statisticchart(selection):
    if selection == "By Function":
        fp = open("Skyscrapers2021.csv", "r")
        reader = csv.reader(fp)
        count = 0
        d = {"office": 0, "hotel": 0, "residential": 0, "hotel / office": 0, "residential / office": 0,
             "multifunction": 0}
        for row in reader:
            if count > 0:
                label = row[12]
                if label == "office":
                    d["office"] += 1
                elif label == "hotel":
                    d["hotel"] += 1
                elif label == "residential":
                    d["residential"] += 1
                elif label == "hotel / office":
                    d["hotel / office"] += 1
                elif label == "residential / office":
                    d["residential / office"] += 1
                else:
                    d["multifunction"] += 1
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
        colors = ["skyblue", "cadetblue", "cornflowerblue", "powderblue", "steelblue", "lightslategray"]
        plt.pie(values, labels=label, colors=colors, explode=explode_values, autopct="%1.1f%%", startangle=90,
                textprops={"fontsize": 10})
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
        material = [x for x in material_Percentage_Value]
        st.set_option("deprecation.showPyplotGlobalUse", False)

        EXPLODE_VALUE = 0.1
        max_percentage = max(material_Percentage_Value)
        max_percentage_index = material.index(max_percentage)
        explode_values = [0] * len(labels)
        explode_values[max_percentage_index] = EXPLODE_VALUE
        colors = ["tan", "peru", "orange", "gold"]

        plt.pie(material, labels=labels, colors=colors, explode=explode_values, autopct='%1.1f%%', startangle=90,
                textprops={"fontsize": 10})
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

    # use sidebar to choose specific rank range
    rank = st.sidebar.selectbox("Select rank:", ("1~20", "21~40", "41~60", "61~80", "81~100"))
    rank_list = {"1~20": 1, "21~40": 21, "41~60": 41, "61~80": 61, "81~100": 81}
    select_rank = rank_list[rank]

    st.write("Skyscrapers Rank " + str(select_rank) + " ~ " + str(select_rank + 19))
    rank_map(select_rank)

    st.set_option("deprecation.showPyplotGlobalUse", False)
    st.pyplot(scatterplot())

    # insert pivot table, using 'CITY', 'COMPLETION', 'MATERIAL' as index, drive focus on meters
    skyscrapers_data = pd.read_csv("Skyscrapers2021.csv")
    skyscrapers_data.Meters = skyscrapers_data.Meters.str.replace(r'\s+m', '').astype(float)
    tt = pd.pivot_table(skyscrapers_data, index=["CITY", "COMPLETION", "MATERIAL"], values=["NAME","Meters"])
    st.dataframe(tt)

    # user inputs city,calculate total numbers and average height&floors in one specific city
    city_list = skyscrapers_data["CITY"].unique()
    select_city = st.selectbox(
        "Which city would you like to choose?",
        city_list)
    select_city_df = skyscrapers_data[skyscrapers_data["CITY"] == select_city]
    skyscraper_amount = select_city_df.shape[0]
    average_height_of_city = select_city_df["Meters"].mean()
    average_floor_of_city = select_city_df["FLOORS"].mean()

    st.write(f"{select_city} has {skyscraper_amount} skyscrapers. ")
    st.write(f"Average Height is {average_height_of_city:0.2f}m.")
    st.write(f"Average floor is {int(average_floor_of_city)}.")

    select_year = st.sidebar.slider("Select years", 1931, 2020)

    st.pyplot(average_height_line_chart(select_year))

    selection = st.sidebar.selectbox("Select an option: ", ("By Function", "By Material"))
    st.set_option("deprecation.showPyplotGlobalUse", False)
    st.pyplot(statisticchart(selection))


main()
