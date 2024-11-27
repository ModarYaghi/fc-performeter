# %%
"""Importing necessary libraries and source code"""
import pandas as pd
from irm_final_eval_sources import excel_file_path, open_questions_rename_mapping

from deepl_translator import translate_text, translate_dataframe_column

# %%
open_questions = pd.read_excel(excel_file_path, sheet_name="open_questions")
open_questions.rename(columns=open_questions_rename_mapping, inplace=True)

# %%
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "gossip_exclusion_exp", "gossip_exc_exp_en", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "exp_1", "exp_en_1", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "exp_2", "exp_en_2", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "exp_3", "exp_en_3", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "exp_4", "exp_en_4", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "participation_challenges", "part_chal_en", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "exp_5", "exp_en_5", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "feedback_on_team", "fdbk_on_t_en", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "safety_suggestions", "sfty_sug_en", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "physical_wellbeing_exp", "phy_wb_exp_en", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "mental_wellbeing_exp", "mtl_wb_exp_en", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "financial_wellbeing_exp", "fin_wb_exp_en", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "family_wellbeing_exp", "fmly_wb_exp_en", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "recognition_exp", "recgn_exp_en", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "sense_of_justice_exp", "sns_jus_exp_en", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "dignity_exp", "dig_exp_en", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "most_significant_impact", "mst_signf_mpct_en", translate_text
)
open_questions.head(1)
# %%
open_questions = translate_dataframe_column(
    open_questions, "additional_participation_info", "mst_signf_mpct_en", translate_text
)
open_questions.head(1)
# %%
open_questions.columns
# %%
open_questions.to_clipboard()