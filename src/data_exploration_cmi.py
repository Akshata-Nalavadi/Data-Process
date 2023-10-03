#### Initial Data Exploration ####
import pandas as pd
import matplotlib.pyplot as plt
#import polars as pl
#import seaborn as sn
#import seaborn_polars as snl
#import plotly.express as px
#import pyarrow as pw
import os
from datetime import datetime
from plotnine import (
    ggplot, aes,
    geom_point, geom_violin, geom_smooth, geom_boxplot, geom_line, geom_rect,
    labs, facet_wrap, theme
)


cmidat = pd.read_excel("data/cmi_inspections.xlsx")
cmidat.info()
cmidat.head(25)
cmidat.describe()
cmidat['Event'].value_counts()
cmidat['Ident'].value_counts()

columns = cmidat.columns



cmi_timevars = cmidat[['Date', 'WorkingAge', 'DayBRdg', 'Life']]
histogram = cmi_timevars.hist()
plt.show()

times = cmidat[['Ident', 'WorkingAge', 'Life','Event']]
start = times.groupby(by="Ident").agg()
times.head(20)
[times.Life == 0]*1

#events = times.groupby(by=["Ident", "Event"],as_index=False)['Life'].agg(["min", "max"])
events = times[times['Event'] != "*"]
events = events[events['Event'] !="B"]

hdat_m_df = pd.DataFrame(hdat_m)
shade = data.frame(x1=c(1918,1930), x2=c(1921,1932), y1=c(-3,-3), y2=c(4,4))

prefixlist = ["M1H", "M2A", "M2H", "P1H", "P1V", "P2H"]

m1h = columns[["M1H" in c for c in columns]]
cmidat[m1h].hist()
plt.show()

m2a = columns[["M2A" in c for c in columns]]
cmidat[m2a].hist()
plt.show()

m2h = columns[["M2H" in c for c in columns]]
cmidat[m2h].hist()
plt.show()

m2v = columns[["M2V" in c for c in columns]]
cmidat[m2v].hist()
plt.show()

p1h = columns[["P1H" in c for c in columns]]
cmidat[p1h].hist()
plt.show()

p1v = columns[["P1H" in c for c in columns]]
cmidat[p1v].hist()
plt.show()

p2h = columns[["P2H" in c for c in columns]]
cmidat[p2h].hist()
plt.show()

p2v = columns[["P2V" in c for c in columns]]
cmidat[p2v].hist()
plt.show()

all_feat = list(m1h) + list(m2a) + list(m2h) + list(m2v) + list(p1h) + list(p1v) + list(p2h) + list(p2v)
plt.matshow(cmidat[all_feat].corr())
plt.show()


(
    ggplot(cmidat, aes(x='WorkingAge', y='M1H_Overall'))
    + geom_line(color="DarkGreen")
    + facet_wrap('Ident', ncol=3)
    + labs(x='Time', y='blabla')
    + geom_line(aes(x='WorkingAge', y='M2A_Overall'), color="DarkBlue")
    + geom_line(aes(x='WorkingAge', y='M2H_Overall'), color="Orange")
    + geom_line(aes(x='WorkingAge', y='M2V_Overall'), color="Red")
    + geom_rect(events, aes(y=0, xmin="WorkingAge", xmax="WorkingAge", ymin=0, ymax=0.3, color="Event", fill="Event"), size=2)
)




(
    ggplot(hdat_m_df, aes(x=str('Monthnm'), y='Global_active_power'))
    + geom_boxplot(fill="LightGreen") + geom_point(color="Grey")
    + labs(x='Month', y='Active Power') +  facet_wrap("Year")
)



(
    ggplot(hdat_m, aes(x='Month', y='Global_active_power'))
    + geom_smooth(se=False, color="DarkGreen", method = 'loess', span=.001)
    + facet_wrap('Year', scales='free_x', ncol=1)
    + labs(x='Time', y='Active Power')
)


lp = px.line(hdat.to_pandas(),x='DateTime', y='Global_active_power', line_group='Year',
             facet_col='Year', facet_col_wrap=3)
lp.update_xaxes(matches=None)
lp.show()