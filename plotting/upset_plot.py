from src.all_in_one import *
from src.basic_variables import *

from upsetplot import UpSet
from upsetplot import from_indicators
import matplotlib.pyplot as plt

int_file = path_manager.get_data_file(Category.PS, PSFile.PSNT)
intake = get_df(int_file.path, int_file.sheet)
intake_dataset = Dataset(config_file, int_file.sheet)
filtered_intake = filter_dataframe_on_date(
    intake, intake_dataset.dvars, START, END, FilterType.IN
)

new_intake = filter_dataframe_on_date(intake, "nt_s2", START, END)

# convert the DataFrame to a UpSet-friendly format
data = from_indicators(new_intake, indicators=new_intake.columns)

upset = UpSet(data, subset_size="count", show_counts="%d")

upset.plot()
plt.show()
