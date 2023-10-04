import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from plotnine import (
    ggplot, aes,
    geom_point, geom_violin, geom_smooth, geom_boxplot, geom_line, 
    geom_rect, geom_histogram, geom_density,
    labs, facet_wrap, theme_dark, theme, element_rect, theme_gray, theme_seaborn, element_text
)


# Load the data
cmidat = pd.read_excel("data/cmi_inspections.xlsx")
cmi_cols = list(cmidat.columns)
energy_cols = [col for col in cmi_cols if "_Gs" in col]
overall_cols = [col for col in cmi_cols if "_Over" in col]
st.set_page_config(layout="wide")

prefix_list = ["M1H", "M2H", "M2A", "M2V", "P1H", "P2H", "P1V", "P2V"]
time_vars = ['WorkingAge', 'DayBRdg', 'Life']
machines = list(cmidat.Ident.unique())

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


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview","Histograms", "TimeSeries", "Correlations", "Machine 32-4180"])
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

with tab2:
    # Histograms of selected time variables
    st.header("Histograms")
    def hist_vars(varlist, nc, h):
        cmidat_sel = cmidat[["Ident"] + varlist]
        cmidat_long = pd.melt(cmidat_sel, id_vars='Ident', value_vars=varlist, value_name='value')
        histogram = (
            ggplot(cmidat_long, aes(x='value', y="..density.."))
            + geom_histogram(bins = 30)+ geom_density(fill = "lightgreen", alpha=0.4)
            + facet_wrap('variable', scales="free", ncol = nc)
            + theme_gray() + theme(plot_background=element_rect(fill='black', alpha=.3), text=element_text(size=5))
            )
        fig = ggplot.draw(histogram)
        fig.set_figheight(h)
        return fig
    
    st.subheader("Time Variables")
    st.pyplot(hist_vars(time_vars, 3, 1.5))

    st.subheader("Acceleration Energy Variables")
    st.pyplot(hist_vars(energy_cols, 2, 4))

    st.subheader("Average Velocity Variables")
    st.pyplot(hist_vars(overall_cols, 2, 4))

with tab3:
    # Time series plots including events
    st.header("Time series plots for each machine with recorded events")
    times = cmidat[['Ident', 'WorkingAge', 'Life', 'Event']]
    filtered_times = times[(times['Event'] != "*") & (times['Event'] != "B")]
    events = pd.DataFrame(filtered_times)

    #@st.cache(hash_funcs={ggplot.draw: lambda _: None})
    def eventplot(varlist, mlist, nc, h):
        cmidat_sel = cmidat[["Ident", "WorkingAge"] + varlist]
        cmidat_long = pd.melt(cmidat_sel, id_vars=['Ident','WorkingAge'], value_vars=varlist, value_name='value')
        cmidat_m =  cmidat_long[ cmidat_long.Ident.isin(mlist)]
        maxy=max(cmidat_long.value)
        plot = (
            ggplot(cmidat_m, aes(x='WorkingAge', y='value', fill="variable", color="variable", group='variable'))
            + geom_line()
            + facet_wrap('Ident', ncol=nc)
            + labs(x='Time', y='Value')
            + geom_rect(events[events.Ident.isin(mlist)], aes(y=0, group=1, xmin="WorkingAge", xmax="WorkingAge", ymin=0, ymax=maxy, color="Event", fill="Event"), size=1)
            + theme_gray() + theme(plot_background=element_rect(fill='black', alpha=.3), text=element_text(size=5))
        )
        
        fig = ggplot.draw(plot)
        fig.set_figheight(h)
        return fig
    
    st.subheader("Acceleration Energy Variables")
    st.pyplot(eventplot(energy_cols, machines, 2, 7))

    st.subheader("Average Velocity Variables")
    st.pyplot(eventplot(overall_cols, machines, 2, 7))


with tab4:   
    # Correlation matrix
    st.subheader("Correlation Matrix Heatmap")
    all_feat = [col for prefix in prefix_list for col in cmidat.columns if prefix in col]
    corr_matrix = cmidat[all_feat].corr()
    plt.matshow(corr_matrix)
    st.pyplot(plt)

with tab5:
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



