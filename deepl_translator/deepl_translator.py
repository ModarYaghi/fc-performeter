# import pandas as pd
import requests

# Load DeepL API key form an environment variable or directly
DEEPL_API_KEY = "c250f7db-210a-4cb9-8a98-68f980a23ca0:fx"

# DeepL API endpoint
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_text(text, target_lang="EN-US"):
    """
    Translate text using DeepL API.
    :parm text: Text to be translated
    :parm target_lang: Target language (default is English 'EN')
    :return: Translate text
    """
    params = {"auth_key": DEEPL_API_KEY, "text": text, "target_lang": target_lang}
    response = requests.post(DEEPL_API_URL, data=params)
    if response.status_code == 200:
        return response.json()["translations"][0]["text"]
    else:
        print(f"Error translating '{text}': {response.status_code} - {response.text}")
        return None


# Path to Excel file
# excel_file = ""
# Step 1: Read the Excel file
# df = pd.read_excel("phrases.xlsx")

# step 2: Translate each phrase
# df["English"] = df["Arabic"].apply(translate_text)

# Step 3: Save the updated DataFrame back to the Excel file
# df.to_excel("translated_phrases.xlsx", index=False)

# print(
# "Translation complete. Translated phrases have been saved to 'translated_phrases.xlsx'."
# )


def translate_dataframe_column(df, col_to_translate, new_col_name, translate_function):
    """
    Translates a specified column in a DataFrame and inserts the translated values as a new column.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    col_to_translate (str): The name of the column to be translated.
    new_col_name (str): The name of the new column to store the translated values.
    translate_function (callable): The function used for translation. Should accept a single value and return the translated value.

    Returns:
    pd.DataFrame: A DataFrame with the translated column added.
    """
    # Ensure the column to translate exists
    if col_to_translate not in df.columns:
        raise ValueError(f"Column '{col_to_translate}' not found in DataFrame.")

    # Apply the translation function to the specified column
    translated_column = df[col_to_translate].apply(translate_function)

    # Insert the new column right after the original column
    col_position = df.columns.get_loc(col_to_translate) + 1
    df.insert(col_position, new_col_name, translated_column)

    return df
