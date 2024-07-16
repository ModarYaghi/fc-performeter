# from src.all_in_one import *
import pandas as pd


scr = pd.read_csv("data/processed/0624/00_psscr_0624.csv")
scr['sc_s1'] = pd.to_datetime(scr['sc_s1'])
scr['sc_s1'] = scr['sc_s1'].dt.year


annual_registration_counts = scr.groupby('sc_s1').size().reset_index(name='count')
total_registrations = annual_registration_counts['count'].sum()

annual_registration_counts['percentage'] = (annual_registration_counts['count'] / total_registrations) * 100


print(annual_registration_counts)
