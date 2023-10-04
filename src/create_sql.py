from sqlalchemy import create_engine
import pandas as pd

host="localhost"
user="root"
password="Tinfish582<3"
database="cmi"

engine = create_engine('mysql+mysqlconnector://' + user + ':' + password + '@' + host + '/' + database)

cmidat = pd.read_excel("data/cmi_inspections.xlsx")
cmidat.to_sql(name='pump_vibration', con=engine, if_exists='replace', index=False)