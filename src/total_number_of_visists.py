from src.all_in_one import *
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime


def count_and_plot_total_sessions(data_files_path, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    count = []

    for file_name in os.listdir(data_files_path):
        file_path = os.path.join(data_files_path, file_name)
        df = pd.read_csv(file_path)