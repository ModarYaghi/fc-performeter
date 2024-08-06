import pandas as pd
from transliterate import translit
import arabic_reshaper
from bidi.algorithm import get_display

# Simple transliteration dictionary
transliteration_dict = {
    'ا': 'a', 'ب': 'b', 'ت': 't', 'ث': 'th', 'ج': 'j', 'ح': 'h', 'خ': 'kh',
    'د': 'd', 'ذ': 'dh', 'ر': 'r', 'ز': 'z', 'س': 's', 'ش': 'sh', 'ص': 's',
    'ض': 'd', 'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'q',
    'ك': 'k', 'ل': 'l', 'م': 'm', 'ن': 'n', 'ه': 'h', 'و': 'w', 'ي': 'y',
    'ء': "'", 'آ': 'a', 'أ': 'a', 'ؤ': 'u', 'ئ': 'i', 'ى': 'a', 'ة': 'h'
}


data = {
    'First Name': [
        "فاطمة", "علي", "محمد"
    ],
    'Last Name': [
        "عبدالله", " حسين", "أحمد"
    ]
}

df = pd.DataFrame(data)


def transliterate_arabic(name):
    # reshaped_text = arabic_reshaper.reshape(name)
    # bidi_text = get_display(reshaped_text)
    # transliterated_text = ''.join(transliteration_dict.get(char, char) for char in bidi_text)
    # return transliterated_text
    return ''.join(transliteration_dict.get(char, char) for char in name)

first_name = df['First Name (Latin)'] = df['First Name'].apply(transliterate_arabic)

last_name = df['Last Name (Latin)'] = df['Last Name'].apply(transliterate_arabic)

print(df)