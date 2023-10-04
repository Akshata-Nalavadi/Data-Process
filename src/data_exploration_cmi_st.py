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
cmi_cols = list(cmidat.columns)
energy_cols = [col for col in cmi_cols if "_Gs" in col]

prefix_list = ["M1H", "M2H", "M2A", "M2V", "P1H", "P2H", "P1V", "P2V"]
time_vars = ['Date', 'WorkingAge', 'DayBRdg', 'Life']

var_dict = {"Prefix": prefix_list,
            "Explanation":["Motor, position 1, Horisontal position",
                           "Motor, position 2, Horisontal position",
                           "Motor, position 2, Axial position",
                           "Motor, position 2, Vertical position",
                           "Pump, position 1, Horisontal position",
                           "Pump, position 2, Horisontal position",
                           "Pump, position 1, Vertical position",
                           "Pump, position 2, Vertical position"]
}
vardf = pd.DataFrame(var_dict)


tab1, tab2, tab3 = st.tabs(["Overview", "Machine 32-4180", "Machine2"])
with tab1:
    st.title("Con Mon vibration on pumps")

    st.header("Introduction")
    st.markdown("Longitudinal routine vibration condition monitoring data on 18 identical centrifugal pump systems over years of operation. Data includes multiple points on the motor and pump, notification of failures and suspensions, overall vibration values and frequency band information.")
    st.markdown("Vibration data collected using a handheld meter and processed using vendor's propriatary software. Raw data is unavailable and meter vendor is not known.")
    st.markdown("Required data set citation is https://prognosticsdl.systemhealthlab.com/ and the date you accessed the data.")
    st.markdown("Required paper citation if using the data is: Sundin, P.O., Eng, P., Montgomery, N. & Jardine, A.K.S., (2007) 'Pulp mill on-site implementation of CBM decision support software' in Proceedings of ICOMS Asset Management Conference 2007, Melbourne Australia, Paper 68.")

    st.table(vardf)

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

    #@st.cache(hash_funcs={ggplot.draw: lambda _: None})
    def eventplot(mlist):
        plot = (
            ggplot(cmidat[cmidat.Ident.isin(mlist)], aes(x='WorkingAge', y='M1H_Overall'))
            + geom_line(color="DarkGreen")
            + facet_wrap('Ident', ncol=3)
            + labs(x='Time', y='Value')
            + geom_line(aes(x='WorkingAge', y='M2A_Overall'), color="Blue")
            + geom_line(aes(x='WorkingAge', y='M2H_Overall'), color="Orange")
            + geom_line(aes(x='WorkingAge', y='M2V_Overall'), color="Red")
            + geom_rect(events[events.Ident.isin(mlist)], aes(y=0, xmin="WorkingAge", xmax="WorkingAge", ymin=0, ymax=0.3, color="Event", fill="Event"), size=1)
            + theme_gray() + theme(plot_background=element_rect(fill='black', alpha=.3))
        )
        return plot
    st.pyplot(ggplot.draw(eventplot(machines[:9])))

    st.pyplot(ggplot.draw(eventplot(machines[9:])))
    # Correlation matrix
    st.subheader("Correlation Matrix Heatmap")
    all_feat = [col for prefix in prefix_list for col in cmidat.columns if prefix in col]
    corr_matrix = cmidat[all_feat].corr()
    plt.matshow(corr_matrix)
    st.pyplot(plt)

with tab2:
    prefix = "M1H"
    m = machines[2]
    columns = [col for col in cmidat.columns if prefix in col]
    mdat = cmidat[cmidat.Ident==m]
    mdat_long = pd.melt(mdat, id_vars='WorkingAge', value_vars=columns, value_name='value')
    evdat = events[events.Ident==m]

    plot1 = (
        ggplot(mdat_long, aes(x='WorkingAge', y='value', color="variable", group='variable'))
        + geom_line()
        #+ facet_wrap('Ident', ncol=3)
        + labs(x='Time', y='Value')
        #+ geom_rect(evdat, aes(y=0, xmin="WorkingAge", xmax="WorkingAge", ymin=0, ymax=0.3, color="Event", fill="Event"), size=1)
        + theme_gray() + theme(plot_background=element_rect(fill='black', alpha=.3))
    )
    st.pyplot(ggplot.draw(plot1))    
