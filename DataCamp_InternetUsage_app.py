import streamlit as st
import plotly.express as px
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

import plotly.graph_objects as go
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"

# -----------------------------------------------------------------------------------------------------------------
## PAGE CONFIGURATION

st.set_page_config(page_title = ":bar_chart: Global Internet Trend Analysis",
                   # page_icon=":bar_chart:",               # Check https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/  to get the desired icon
                   layout="wide"
                   )

with open(BASE_DIR / "style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------------------------------

###############################################################################################
###########################          LOAD DATA         ########################################
###############################################################################################

df2 = pd.read_csv(DATA_DIR / "data_longF.csv", encoding="ISO-8859-1")


df2.rename(columns={"gdp_ppp_of_most_current_available_year": "gdp_2023",
                    "continent": "Continent",
                    "year": "Year",
                    "population": "Population"}, inplace=True)
#
# df_bvi = pd.read_csv(DATA_DIR / "British_Virgin_Islands_Population.csv", encoding="ISO-8859-1")
# df_nauru = pd.read_csv(DATA_DIR / "Nauru_Population.csv", encoding="ISO-8859-1")
#
# df2 = pd.concat([df2, df_bvi, df_nauru])
# df2.reset_index(drop=True, inplace=True)
# st.dataframe(df2)
# df2 = df2.drop(df2.index[4944:])
# df2.to_csv("data_longF.csv", index=False)



###############################################################################################
#########################            FUNCTIONS              ###################################
###############################################################################################

def display_per_continent_trend(df2):
    continent_df = df2.groupby(by=['Year', 'Continent'],
                               as_index=False)['Internet_Usage'].mean()

    # Define custom colors for each continent
    custom_colors = {
        "Africa": "#EC4223",
        "Europe": "#1cc88a",
        "Asia": "rgba(54,185,204,0.3)",  # Muted transparent blue
        "North America": "rgba(132,157,233,0.3)",  # Muted transparent light blue
        "Oceania": "rgba(220,35,217,0.3)",  # Muted transparent purple
        "South America": "#ECDF98"  # Muted transparent light blue
    }

    # Line Plot
    fig2 = px.line(continent_df,
                   x="Year",
                   y="Internet_Usage",
                   color="Continent",
                   title = "Global Trend by Continent in the period [2000-2023]",
                   labels={'Year': 'Year',                                                      # X-axis Label
                           'Internet_Usage': '% Internet Usage'},  # Y-axis Label
                   color_discrete_map = custom_colors,  # Use the custom color map
                   # markers=True
                   )

    # Customize the line thickness
    for trace in fig2.data:
        if trace.name == "Europe":
            trace.update(line=dict(width=4))  # Thicker line for Europe
        elif trace.name == "Africa":
            trace.update(line=dict(width=4))  # Thicker line for Africa
        else:
            trace.update(line=dict(width=2))  # Default line thickness for other continents

    # Customize the appearance
    fig2.update_layout(xaxis=dict(showgrid=True,
                                  tickmode='linear',
                                  tick0=2000,
                                  dtick=2,       # X-axis ticks
                                  range=[2000, 2023]  # Limit the x-axis range to 2000-2023
                                  ),
                       yaxis=dict(showgrid=True),
                       font=dict(size=14),                                                      # Font size for labels
                       )

    fig2.update_layout(title_font_family = "Open Sans",
                       title_font_color = "#174C4F",
                       title_font_size = 20,
                       font_size = 16,
                       margin=dict(l=80, r=80, t=100, b=80, pad=0),  # Margins
                       height=500,
                       )
    # Show the figure
    st.plotly_chart(fig2, use_container_width=True)

def display_country_line(df2,selected_countries):
    # Define the threshold values:
    thresholds = [50, 70, 80]
    threshold_colors = ['#EC4223', '#EAAD6E', '#1cc88a']  # Colors for each threshold


    # # Streamlit country filter
    # countries = df2['Country'].unique().tolist()
    # selected_countries = st.multiselect('Select countries to display:',
    #                                     countries,
    #                                     default=countries[:3],
    #                                     max_selections=6
    #                                     )

    # Filter the data based on the selection
    df_countries = df2[df2['Country'].isin(selected_countries)]

    custom_colors = {}
    colors = ['#5CB85C',
              '#93AAEB',
              '#D08497',
              '#F2EC98',
              '#94A392',
              '#8AD8E3']  # Define colors for up to 6 countries

    # colors = ['rgba(99,110,250,0.6)',  # Transparent Blue
    #           'rgba(239,84,59,0.6)',  # Transparent Red
    #           'rgba(0,204,150,0.6)',  # Transparent Green
    #           'rgba(171,99,250,0.6)',  # Transparent Purple
    #           'rgba(255,255,0,0.6)',  # Transparent Yellow
    #           'rgba(25,211,243,0.6)'  # Transparent Cyan
    #           ]  # Define transparent colors for up to 6 countries

    for i, country in enumerate(selected_countries):
        custom_colors[country] = colors[i]  # Assign a color to each selected country

    # Create the line chart
    fig_line = px.line(df_countries,
                       x='Year',
                       y='Internet_Usage',
                       color='Country',
                       color_discrete_map=custom_colors,
                       markers=True,
                       title='% Internet Usage Across Selected Countries (2000–2023)',
                       labels={'Internet_Usage': '% Internet Usage', 'Year': 'Year'}
                      )

    # Update layout for better visualization
    fig_line.update_layout(legend_title='Country',
                           xaxis_title='Year',
                           yaxis_title='% Internet Usage',
                           template='plotly_white',
                           title_font_family="Open Sans",
                           title_font_color="#174C4F",
                           title_font_size=20,
                           height=500
                          )

    # Add horizontal lines for thresholds
    for value, color in zip(thresholds, threshold_colors):
        fig_line.add_shape(type='line',
                      x0=df_countries['Year'].min(),  # Start of the line on X-axis
                      x1=df_countries['Year'].max(),  # End of the line on X-axis
                      y0=value,  # Y position of the line
                      y1=value,  # Y position of the line
                      line=dict(color=color, width=1)  # Line style
                      )

        if value == 50:
            texto = f"{value}: Low Internet"
        elif value == 70:
            texto = f"{value}: Moderate Internet"
        else:
            texto = f"{value}: High Internet"

        # Add annotations for each threshold
        fig_line.add_annotation(
            x=df_countries['Year'].min() + 0.5,
            # Shift the annotation to the left by subtracting 1 (or adjust the value as needed)
            y=value + 4,
            text=texto,  # Annotation text
            showarrow=False,
            font=dict(color=color, size=12),  # Text style
            align='right',  # Align the text
            xanchor='left',  # Anchor the text to the left of the specified x-coordinate
            yanchor='middle'  # Anchor the text to the middle of the line
        )

        # Add a vertical line at the year 2016
        fig_line.add_shape(
            type='line',
            x0=2016,  # Start of the vertical line on X-axis
            x1=2016,  # End of the vertical line on X-axis
            y0=0,  # Start of the vertical line on Y-axis
            y1=df_countries['Internet_Usage'].max() + 8,  # End of the vertical line on Y-axis
            line=dict(color="#BABBBB", width=2, dash="dash")  # Style of the vertical line
        )

        # Add annotation for the vertical line
        fig_line.add_annotation(
            x=2016 - 1.5,
            y=df_countries['Internet_Usage'].min() - 5,  # Adjust the Y-coordinate for annotation placement
            text="2016",
            showarrow=True,
            arrowhead=2,
            ax=40,  # Horizontal offset for arrow
            ay=0,  # Vertical offset for arrow
            font=dict(color="#BABBBB", size=12),
            arrowcolor="white"
        )

    # Make the lines thicker and adjust transparency
    fig_line.update_traces(line=dict(width=3), opacity=0.6)  # Set line width to make them thicker

    st.plotly_chart(fig_line, use_container_width=True)


def display_yoybarchat(df2, selected_countries_yoy):
    # Filtered data
    df_filtered = df2.copy()

    # Calculate Year-over-Year Change (in %)
    df_filtered['YoY_Change'] = df_filtered.groupby('Country')['Internet_Usage'].pct_change() * 100

    # Filter for years 2018 onward
    df_filtered = df_filtered[df_filtered['Year'] >= 2018]

    # Filter data for selected countries
    df_filtered = df_filtered[df_filtered['Country'].isin(selected_countries_yoy)]

    # List 1: Unique Years as categorical type
    years = df_filtered['Year'].astype('category').cat.categories.tolist()

    # Initialize empty lists for min, max, and corresponding countries
    yoy_min = []
    yoy_max = []
    countries_min = []
    countries_max = []

    # Iterate through each unique year to calculate the required values
    for year in years:
        year_data = df_filtered[df_filtered['Year'] == year]  # Filter data for the year
        min_value = year_data['YoY_Change'].min()
        max_value = year_data['YoY_Change'].max()

        yoy_min.append(min_value)
        yoy_max.append(max_value)

        country_min = year_data[year_data['YoY_Change'] == min_value]['Country'].iloc[0]
        country_max = year_data[year_data['YoY_Change'] == max_value]['Country'].iloc[0]

        countries_min.append(country_min)
        countries_max.append(country_max)

    # Creating the bar plot
    fig = go.Figure(data=[go.Bar(name='max',
                                 x = years,
                                 y = yoy_max,
                                 marker=dict(color='#4E73DF'),  # Custom color for max bars
                                 text=[f"{val:.2f}%" for val in yoy_max],  # Display YoY value on the bar
                                 hovertext=[f"{country}" for country in countries_max],  # Display country name
                                 hoverinfo="text+name"  # Show hovertext and series name
                                 ),
                          go.Bar(name='min',
                                 x = years,
                                 y = yoy_min,
                                 marker=dict(color='rgba(54,185,204,0.3)'),  # Custom color for min bars (red)
                                 text=[f"{val:.2f}%" for val in yoy_min],  # Display YoY value on the bar
                                 hovertext=[f"{country}" for country in countries_min],  # Display country name
                                 hoverinfo="text+name"  # Show hovertext and series name
                                 )]
                    )

    fig.update_layout(title='Year-over-Year Internet Usage % Change Across Selected Countries (2018–2023)',
                      xaxis_title='Year',
                      yaxis_title='YoY % Change',
                      barmode='group',
                      height=500,
                      template='plotly_white',
                      title_font_family="Open Sans",
                      title_font_color="#174C4F",
                      title_font_size=18,
                      yaxis=dict(range=[-4,None])
                     )

    st.plotly_chart(fig, theme='streamlit', use_container_width=True)


def display_yoy_peryear(df2):
    # Filtered data
    df_filtered = df2.copy()

    # Calculate Year-over-Year Change (in %)
    df_filtered['YoY_Change'] = df_filtered.groupby('Country')['Internet_Usage'].pct_change() * 100

    # Filter for years 2018 onward
    df_filtered = df_filtered[df_filtered['Year'] >= 2016]

    # List 1: Unique Years as categorical type
    years = df_filtered['Year'].astype('category').cat.categories.tolist()

    # Initialize empty lists for min, max, and corresponding countries
    yoy_min = []
    yoy_max = []
    countries_min = []
    countries_max = []

    for year in years:
        # df_yoy_top = df_filtered[df_filtered['Year'] == year].sort_values(by='YoY_Change', ascending=False)
        # df_yoy_top.head(10)[["Country", "YoY_Change"]]
        # df_yoy_top.reset_index(drop=True, inplace=True)

        year_data = df_filtered[df_filtered['Year'] == year]  # Filter data for the year
        min_value = year_data['YoY_Change'].min()
        max_value = year_data['YoY_Change'].max()

        yoy_min.append(min_value)
        yoy_max.append(max_value)

        country_min = year_data[year_data['YoY_Change'] == min_value]['Country'].iloc[0]
        country_max = year_data[year_data['YoY_Change'] == max_value]['Country'].iloc[0]

        countries_min.append(country_min)
        countries_max.append(country_max)

    # Creating the bar plot
    fig = go.Figure(data=[go.Bar(name='max',
                                 x=years,
                                 y=yoy_max,
                                 marker=dict(color='#4E73DF'),  # Custom color for max bars
                                 text=[f"{val:.1f}%" for val in yoy_max],  # Display YoY value on the bar
                                 textposition='inside',
                                 hovertext=[f"{country}" for country in countries_max],  # Display country name
                                 hoverinfo="text+name",  # Show hovertext and series name
                                 ),
                          go.Bar(name='min',
                                 x=years,
                                 y=yoy_min,
                                 marker=dict(color='rgba(54,185,204,0.3)'),  # Custom color for min bars (red)
                                 text=[f"{val:.1f}%" for val in yoy_min],  # Display YoY value on the bar
                                 textposition='inside',
                                 hovertext=[f"{country}" for country in countries_min],  # Display country name
                                 hoverinfo="text+name",  # Show hovertext and series name
                                 )]
                    )

    # Adding country labels as annotations
    for i, year in enumerate(years):
        # Add annotation for max bar
        fig.add_annotation(
            x=year,
            y=yoy_max[i],
            text=countries_max[i],  # Country name for max
            showarrow=False,
            font=dict(size=14, color="#4E73DF"),
            yshift=15,  # Offset above the bar
            xshift = -18  # Shift to the left
        )
        # Add annotation for min bar
        fig.add_annotation(
            x=year,
            y=yoy_min[i],
            text=countries_min[i],  # Country name for min
            showarrow=False,
            font=dict(size=13, color="#2FA9BB"),
            yshift=-15,  # Offset above the bar
            xshift = 18  # Shift to the right
        )

    fig.update_layout(title='Year-over-Year Internet Usage % Change (2016–2023): Max and Min per year',
                      xaxis_title='Year',
                      yaxis_title='YoY % Change',
                      barmode='group',
                      height=600,
                      template='plotly_white',
                      title_font_family="Open Sans",
                      title_font_color="#174C4F",
                      title_font_size=18,
                      yaxis=dict(range=[-50, None])
                      )

    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

def display_gdp_Internet(df2):
    # Filtered data
    df_filtered = df2.copy()


    # Function to classify income levels (According to https://blogs.worldbank.org/en/opendata/new-world-bank-group-country-classifications-income-level-fy24)
    def classify_income_level(gdp_per_capita):
        if gdp_per_capita <= 3400:
            return "Low-income"
        elif 3401 <= gdp_per_capita <= 6465:
            return "Lower middle-income"
        elif 6466 <= gdp_per_capita <= 15845:
            return "Upper middle-income"
        elif 15846 <= gdp_per_capita:
            return "High-income"

    # Apply the function to create a new column
    df_filtered['Income_Level'] = df_filtered['gdp_2023'].apply(classify_income_level)
    df_filtered = df_filtered[df_filtered['Year'] == 2023]


    # "#487FA7" verde
    # "#1cc88a" teal
    # "#E2DA11" amarillo
    # "#EC4223" rojo

    # Define custom colors for each continent
    custom_colors = {
        "Low-income": "#E2DA11",
        "Lower middle-income": "#EC4223",
        "Upper middle-income": "#1cc88a",
        "High-income": "#337BFF"
    }

    fig = px.scatter(df_filtered,
                     x= 'gdp_2023',
                     y= 'Internet_Usage',
                     # text = 'Country',
                     size="Population",
                     color='Income_Level',
                     title="Internet Usage vs. GDP per Capita in 2023",
                     hover_data=['Country'],
                     size_max=40,  # Adjust the maximum marker size
                     color_discrete_map=custom_colors  # Use the custom color map
                     )

    fig.update_traces(marker=dict(line=dict(width=1, color='white')),
                      opacity=0.6)

    # Update the x-axis to use log scale
    fig.update_layout(xaxis=dict(type='log',
                                 title = 'GDP in 2023 (Log Scale)'),
                      # plot_bgcolor="#F8F8F8",  # Plot area color
                      margin=dict(l=60, r=60, t=80, b=60, pad=0),  # Margins
                      title_font_family="Open Sans",
                      title_font_color="#174C4F",
                      title_font_size=20,
                      font_size=16,
                      height=500  # Chart height
                      )

    st.plotly_chart(fig, use_container_width=True)


def display_bottom_contries(df2,selected_year):
    # Sorting by Internet Usage in ascending order to identify countries with low usage
    df_year_bottom = df2[df2['Year'] == selected_year].sort_values(by='Internet_Usage', ascending=True)
    df_year_bottom = df_year_bottom.head(10)[["Country", "Internet_Usage", "Population"]]
    df_year_bottom.reset_index(drop=True, inplace=True)
    df_year_bottom["Rank"] = df_year_bottom.index + 1

    # Streamlit app layout
    st.markdown(f"<h3 style='text-align: center; font-size: 19px; color: #174C4F;'>Top Countries Impacted by Lack of Internet in {selected_year}</h3>",
        unsafe_allow_html=True)

    # Create the table without progress bars
    for index, row in df_year_bottom.iterrows():
        st.markdown(
            f"""
                <div style="display: flex; align-items: center; justify-content: space-between; 
                            background-color: white; padding: 10px; margin-bottom: 5px; 
                            border-radius: 8px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);">
                    <div style="flex: 1; text-align: center; font-weight: bold; color: #EC4223;">
                        {row['Rank']:02d}
                    </div>
                    <div style="flex: 3; text-align: left; padding-left: 10px;">
                        {row['Country']}
                    </div>
                    <div style="flex: 2; text-align: center; color: #EC4223; font-weight: bold;">
                        {round(row['Internet_Usage'], 2)}%
                    </div>
                </div>
                """,
            unsafe_allow_html=True,
        )


def display_top_contries(df2, selected_year):
    # Sorting by Internet Usage in descending order
    df_year_top = df2[df2['Year'] == selected_year].sort_values(by='Internet_Usage', ascending=False)
    df_year_top = df_year_top.head(10)[["Country", "Internet_Usage", "Population"]]
    df_year_top.reset_index(drop=True, inplace=True)
    df_year_top["Rank"] = df_year_top.index + 1

    # Streamlit app layout
    st.markdown(f"<h3 style='text-align: center; font-size: 19px; color: #174C4F;'>Top Countries with High Internet Penetration in {selected_year}</h3>",
        unsafe_allow_html=True)

    # Create the table without progress bars
    for index, row in df_year_top.iterrows():
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: space-between; 
                        background-color: white; padding: 10px; margin-bottom: 5px; 
                        border-radius: 8px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);">
                <div style="flex: 1; text-align: center; font-weight: bold; color: #1cc88a;">
                    {row['Rank']:02d}
                </div>
                <div style="flex: 3; text-align: left; padding-left: 10px;">
                    {row['Country']}
                </div>
                <div style="flex: 2; text-align: center; color: #1cc88a; font-weight: bold;">
                    {round(row['Internet_Usage'], 2)}%
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def compute_number_threshold(df2):
    #     Grouping by country
    country_group = df2.groupby('Country')

    # Initialize counters for each category
    below_50 = 0
    between_50_70 = 0
    between_70_80 = 0
    above_80 = 0

    # Analyzing each country
    for country, group in country_group:

        usage_values = group['Internet_Usage']

        # Check the conditions
        if (usage_values < 50).all():  # All values below 50%
            below_50 += 1
        elif (usage_values > 50).any() and (usage_values <= 70).all():  # Between 50% and 70%
            between_50_70 += 1
        elif (usage_values > 70).any() and (usage_values <= 80).all():  # Between 70% and 80%
            between_70_80 += 1
        elif (usage_values > 80).any():  # Above 80%
            above_80 += 1

    return below_50, between_50_70, between_70_80, above_80


def display_metrics(df2, Quantity, title_color, threshold, main_icon, explanation):
    total_countries = len(df2['Country'].unique())
    percentage = (Quantity * 100) / total_countries

    wch_colour_font_hex = "#000000"  # Black color for the font
    fontsize = 20
    border_color = "#C2CCD8"
    title_color = title_color  # Color of the title of the card
    progress_color = title_color

    # Importing the font-awesome icons as a stylesheet
    lnk = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">'

    # Create the HTML structure for the card
    htmlstr = f"""
    <div style='background-color: white;
                color: {wch_colour_font_hex};
                font-size: {fontsize + 4}px;
                border-radius: 7px;
                border-left: 5px solid {border_color};
                padding: 15px;
                line-height:25px;
                box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);
                font-family: Arial, sans-serif;
                margin-bottom: 15px;'>
        <div style='color: {title_color}; font-size: 12px; font-weight: bold;'>
            {f"{threshold}".upper()}
            <span style='font-size: 12px; 
                         color: gray; 
                         margin-left: 5px;' 
                         title="{explanation}">
                <i class="fas fa-question-circle"></i> <!-- Tooltip icon -->
            </span>
        </div>
        <BR>
        <div style='font-size: 24px; font-weight: bold; color: #333;'>
            {percentage:,.0f}%
        </div>
        <div style='display: flex; align-items: center; justify-content: space-between; margin-top: 10px;'>
            <!-- Progress bar -->
            <div style='flex: 1; background-color: #f0f0f0; border-radius: 7px; height: 10px; margin-right: 10px;'>
                <div style='width: {percentage}%; background-color: {progress_color}; height: 100%; border-radius: 7px;'></div>
            </div>
            <!-- Icon -->
            <div style='font-size: 24px; color: {progress_color};'>
                {main_icon}
            </div>
        </div>
    </div>
    """

    # Render the card in Streamlit
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)


###############################################################################################
##########################           APP LAYOUT            ####################################
###############################################################################################
#################### My LinkedIn Profile ###################
linkedin_url = "https://www.linkedin.com/in/lissette-valdes"

st.markdown(
    """
    <style>
        .top-right-text {
            position: absolute;
            top: 10px;
            right: 20px;
            font-size: 14px;
            font-weight: bold;
            color: #9F9F9F;
            background-color: rgba(255, 255, 255, 0.8);
            padding: 5px 10px;
            border-radius: 10px;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
        }
    </style>
    <div class="top-right-text">
        Created by Lissette Valdés Valdés
    </div>
    """,
    unsafe_allow_html=True
)
st.write(' ')
st.write(' ')
st.markdown(
    f"""
    <style>
        .linkedin-container {{
            position: absolute;
            top: 10px;
            right: 20px;
            z-index: 100;
        }}
        .linkedin-container a {{
            text-decoration: none;
            font-size: 16px;
            font-weight: bold;
            color: #0A66C2;
        }}
        .linkedin-container img {{
            width: 25px;
            vertical-align: middle;
        }}
    </style>
    <div class="linkedin-container">
        <a href="{linkedin_url}" target="_blank"> 
            Contact me
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

################
APP_TITLE = ('🌐 Global Internet Usage Dashboard')
APP_SUB_TITLE = "Source: DataCamp Competition"

# st.title(APP_TITLE)
st.markdown("""
    <h1 style='color: #174C4F;'><i class="fa-solid fa-globe"></i> Global Internet Usage Dashboard</h1>
    """, unsafe_allow_html=True)
st.caption(APP_SUB_TITLE)

# st.divider()  # Adds a horizontal line

# Customized with CSS horizontal line
st.markdown("""
    <hr style="border: 2px solid #174C4F; margin: 20px 0;">
""", unsafe_allow_html=True)

## Main Page
below_50, between_50_70, between_70_80, above_80 = compute_number_threshold(df2)
cols1, cols2, cols3, cols4, = st.columns([2, 2, 2, 2])
with cols1:
    display_metrics(df2, below_50, "#EC4223", "Low Internet Penetration", '<i class="fa-solid fa-arrow-down-wide-short"></i>',
                    'Proportion of countries with low internet penetration (<50%) during (2020-2023)')
with cols2:
    display_metrics(df2, between_50_70, "#EAAD6E", "Moderate Internet", '<i class="fas fa-arrows-alt-h"></i>',
                    'Proportion of countries with moderate internet penetration [50%-70%) in 2023')
with cols3:
    display_metrics(df2, between_70_80, "#8AB85C", "High Internet, but not universal", '<i class="fas fa-arrows-alt-h"></i>',
                    'Proportion of countries with high but still not universal internet penetration (70%-80) in 2023')
with cols4:
    display_metrics(df2, above_80, "#1cc88a", "Good Internet Penetration", '<i class="fa-solid fa-arrow-up-wide-short"></i>',
                    'Proportion of countries with good internet penetration (>80%) in 2023')
st.write(' ')

col1, _, col2= st.columns([4.6,0.1,4.4])
with col1:
    display_per_continent_trend(df2)


with col2:
    # Slider to filter the years in the data
    selected_year = st.slider("Select a year",
                              min_value=2000,
                              max_value=2023,
                              value=2023,
                              step=1
                              )
    left, right = st.columns([2, 2])
    with left:
        display_bottom_contries(df2, selected_year)
    with right:
        display_top_contries(df2, selected_year)

display_gdp_Internet(df2)

# Streamlit country filter
countries = df2['Country'].unique().tolist()


col1, _, col2= st.columns([4.7,0.1,4.5])
with col1:
    selected_countries1 = st.multiselect('Select countries to display for the plot:',
                                        countries,
                                        default=countries[:3],
                                        max_selections=6
                                        )
    display_country_line(df2,selected_countries1)
with col2:
    # selected_countries2 = st.multiselect('Select countries to display for the comparison:',
    #                                     countries,
    #                                     default=countries[:3],
    #                                     max_selections=6
    #                                     )
    # display_yoybarchat(df2, selected_countries2)
    display_yoy_peryear(df2)


