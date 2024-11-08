# %%
import pandas as pd
from irm_final_eval_sources import excel_file_path, open_questions_rename_mapping

from deepl_translator import translate_text, translate_dataframe_column

# %%
open_questions = pd.read_excel(excel_file_path, sheet_name='open_questions')
open_questions.rename(columns=open_questions_rename_mapping, inplace=True)

# %%
open_questions.head(1)
# %%
gossip_exclusion_exp_index = open_questions.columns.get_loc('gossip_exclusion_exp')
open_questions.insert(
    gossip_exclusion_exp_index + 1,
    'gossip_exc_exp_en',
    open_questions['gossip_exclusion_exp'].apply(
        translate_text
    )
    )

# %%
translate_dataframe_column(open_questions, 'gossip_exclusion_exp', 'gossip_exc_exp_en', translate_text)
# %%
open_questions.head(1)
# %%
translate_dataframe_column(open_questions, 'exp_1', 'exp_en_1', translate_text)