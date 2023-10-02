#### Initial Data Exploration ####
import pandas as pd
import polars as pl
import seaborn as sn
import seaborn_polars as snl
import plotly.express as px
import pyarrow as pw
import os
from datetime import datetime


from plotnine import (
    ggplot,
    aes,
    geom_point,
    geom_smooth,
    labs,
    facet_wrap
)


hdat = pl.read_csv("data/household_power_consumption.csv",separator=";", 
                   infer_schema_length=0, dtypes=[pl.Utf8, pl.Utf8] + [pl.Float32]*7,
                    null_values=["?"] )
hdat.__len__
hdat = hdat.with_columns(hdat.select(pl.concat_str(['Date', 'Time'],separator = "T").alias('DateTime')))
hdat = hdat.with_columns(pl.col("DateTime").str.to_datetime("%d/%m/%YT%H:%M:%S"))
hdat = hdat.with_columns(pl.col("DateTime").dt.year().alias("Year"))
hdat = hdat.with_columns(pl.col("DateTime").dt.month().alias("Month"))
hdat = hdat.with_columns(pl.col("DateTime").dt.weekday().alias("Day"))
hdat.__len__
hdat.columns

(
    ggplot(hdat, aes(x='DateTime', y='Global_active_power'))
    #+ geom_point() 
    + geom_smooth(se=False, color="DarkGreen", method = 'loess', span=.001)
    + facet_wrap('Year', scales='free_x', ncol=1)
    + labs(x='Time', y='Active Power')
)

hdat_m = hdat.group_by(by=["Year", "Month"]).mean()

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