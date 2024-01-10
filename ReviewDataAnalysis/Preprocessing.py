## Function to clean the text data

import string
import contractions
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def clean_text_df(df, col_name):
    """
    This function cleans the text data i.e., converts the text to lover case, removes punctuations, numbers,
    extra spaces, emojis, emoticons

    Parameters:
    - df (DataFrame): The input DataFrame.
    - col_name (str): the name of the column containing the text that has to be cleaned.

    Returnes:
    - DataFrame: the DataFrame with cleaned text.
    """
    df[col_name] = df[col_name].apply(lambda x: clean_text(x) if x is not None else None)
    return df


def clean_text(text):
    """
    Convert the input text to lower case, remove contractions, punctuations, numbers, extra spaces, emojis
    and emoticons
    """

    # convert text to lower case
    text = text.lower()

    # Remove contractions: There are many words like don't, can't, it's and so on. That would be fixed in this step
    text = contractions.fix(text)

    # Remove punctuations
    text = ''.join(char for char in text if char not in string.punctuation)

    # Remove numbers
    text = ''.join(char for char in text if not char.isdigit())

    # Remove extra spaces
    text = ' '.join(text.split())

    # Remove emojis
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F700-\U0001F77F"  # alchemical symbols
        u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251"
        "]+"
    )

    text = emoji_pattern.sub('', text)

    # Remove emoticons

    emoticons = {
        u":‑)": "Happy face or smiley",
        u":)": "Happy face or smiley",
        u":-]": "Happy face or smiley",
        u":]": "Happy face or smiley",
        u":-3": "Happy face smiley",
        u":3": "Happy face smiley",
        u":->": "Happy face smiley",
        u":>": "Happy face smiley",
        u"8-)": "Happy face smiley",
        u":o)": "Happy face smiley",
        u":-}": "Happy face smiley",
        u":}": "Happy face smiley",
        u":-)": "Happy face smiley",
        u":c)": "Happy face smiley",
        u":^)": "Happy face smiley",
        u"=]": "Happy face smiley",
    }

    emoticon_pattern = re.compile("|".join(re.escape(emoticon) for emoticon in emoticons.keys()))
    text = emoticon_pattern.sub('', text)

    # Replace "media could not be loaded with ''"
    text = text.replace('the media could not be loaded', '')

    # Remove stop words
    text = ' '.join(word for word in word_tokenize(text) if word not in stopwords.words('english'))

    return text


