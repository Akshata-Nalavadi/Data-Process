import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from plotnine import (
    ggplot, aes,
    geom_point, geom_violin, geom_smooth, geom_boxplot, geom_line, 
    geom_rect, geom_histogram, geom_density,
    labs, facet_wrap, theme_dark, theme, element_rect, theme_gray, theme_seaborn
)

# Load the data
cmidat = pd.read_excel("data/cmi_inspections.xlsx")

# Display first 25 rows of data
st.header("Data First Look")
st.subheader("First 25 Rows")
st.write(cmidat.head(25))

# Display data description
st.subheader("Data Description")
st.write(cmidat.describe())

# Value counts of 'Event' column
st.subheader("Number of different events (* is no event)")
st.write(cmidat['Event'].value_counts())

# Value counts of 'Ident' column
st.subheader("Number of measurement points per machine")
st.write(cmidat['Ident'].value_counts())

# Histograms of selected time variables
st.header("Histograms")
st.subheader("Time Variables")
time_vars = ['Date', 'WorkingAge', 'DayBRdg', 'Life']
cmidat_sel = cmidat[["Ident"] + time_vars]
cmidat_long = pd.melt(cmidat_sel, id_vars='Ident', value_vars=time_vars, value_name='value')
histogram = (
    ggplot(cmidat_long, aes(x='value', y="..density.."))
    + geom_histogram(bins = 30)+ geom_density(fill = "lightgreen", alpha=0.4)
    + facet_wrap('variable', scales="free", ncol = 2)
    + theme_gray() + theme(plot_background=element_rect(fill='black', alpha=.3))
    )
st.pyplot(ggplot.draw(histogram))

# Histograms of specific columns
prefix_list = ["M1H", "M2A", "M2H", "P1H", "P1V", "P2H"]
for prefix in prefix_list:
    #baseplot = ggplot(cmidat)
    columns = [col for col in cmidat.columns if prefix in col]
    cmidat_sel = cmidat[["Ident"] + columns]
    cmidat_long = pd.melt(cmidat_sel, id_vars='Ident', value_vars=columns, value_name='value')
    histogram = (
        ggplot(cmidat_long, aes(x='value', y="..density.."))
        + geom_histogram(bins = 30)+ geom_density(fill = "lightgreen", alpha=0.4)
        + facet_wrap('variable', scales="free", ncol = 2)
        + theme_gray() + theme(plot_background=element_rect(fill='black', alpha=.3))
        )
    st.subheader("Measurements for " + prefix + " variables")
    st.pyplot(ggplot.draw(histogram))

# Time series plots including events
st.subheader("Time series plot for each machine with recorded events")
times = cmidat[['Ident', 'WorkingAge', 'Life', 'Event']]
filtered_times = times[(times['Event'] != "*") & (times['Event'] != "B")]
events = pd.DataFrame(filtered_times)
machines = list(cmidat.Ident.unique())

plot1 = (
    ggplot(cmidat[cmidat.Ident.isin(machines[:9])], aes(x='WorkingAge', y='M1H_Overall'))
    + geom_line(color="DarkGreen")
    + facet_wrap('Ident', ncol=3)
    + labs(x='Time', y='Value')
    + geom_line(aes(x='WorkingAge', y='M2A_Overall'), color="Blue")
    + geom_line(aes(x='WorkingAge', y='M2H_Overall'), color="Orange")
    + geom_line(aes(x='WorkingAge', y='M2V_Overall'), color="Red")
    + geom_rect(events[events.Ident.isin(machines[:9])], aes(y=0, xmin="WorkingAge", xmax="WorkingAge", ymin=0, ymax=0.3, color="Event", fill="Event"), size=1)
    + theme_gray() + theme(plot_background=element_rect(fill='black', alpha=.3))
)
st.pyplot(ggplot.draw(plot1))


plot2 = (
    ggplot(cmidat[cmidat.Ident.isin(machines[9:])], aes(x='WorkingAge', y='M1H_Overall'))
    + geom_line(color="DarkGreen")
    + facet_wrap('Ident', ncol=3)
    + labs(x='Time', y='Value')
    + geom_line(aes(x='WorkingAge', y='M2A_Overall'), color="Blue")
    + geom_line(aes(x='WorkingAge', y='M2H_Overall'), color="Orange")
    + geom_line(aes(x='WorkingAge', y='M2V_Overall'), color="Red")
    + geom_rect(events[events.Ident.isin(machines[9:])], aes(y=0, xmin="WorkingAge", xmax="WorkingAge", ymin=0, ymax=0.3, color="Event", fill="Event"), size=1)
    + theme_gray() + theme(plot_background=element_rect(fill='black', alpha=.3))
)
st.pyplot(ggplot.draw(plot2))
# Correlation matrix
st.subheader("Correlation Matrix Heatmap")
all_feat = [col for prefix in prefix_list for col in cmidat.columns if prefix in col]
corr_matrix = cmidat[all_feat].corr()
plt.matshow(corr_matrix)
st.pyplot(plt)