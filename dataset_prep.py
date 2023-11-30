import pandas as pd
import string
import re
from collections import Counter, defaultdict
import json
import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def remove_emoji(s):
    emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                u"\U0001f926-\U0001f937"
                u'\U00010000-\U0010ffff'
                u"\u200d"
                u"\u2640-\u2642"
                u"\u2600-\u2B55"
                u"\u23cf"
                u"\u23e9"
                u"\u231a"
                u"\u3030"
                u"\ufe0f"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', s)

def clean(s):
    return re.sub(r'\s+', ' ', remove_emoji(s.split(".")[0]).translate(str.maketrans('', '', string.punctuation))).lower().strip().split()

def sliding_window(all_sentences, window_size):
    words_that_follow_x = defaultdict(list)
    for words in all_sentences:
        prev_words = ["."] * window_size
        for i in range(len(words)):
            words_that_follow_x[" ".join(prev_words)].append(words[i])
            prev_words = prev_words[1:] + [words[i]] 
        words_that_follow_x[" ".join(prev_words)].append(".")
    for x in words_that_follow_x:
        words_that_follow_x[x] = sorted(list(Counter(words_that_follow_x[x]).items()), reverse=True, key=lambda x: x[1])
    return words_that_follow_x

def prep_dataset(all_sentences):
    max_sentence_length = all_sentences.apply(len).max()
    most_common_at_position = [Counter([item[i] if len(item) > i else "." for item in all_sentences]).most_common(1)[0][0] for i in range(max_sentence_length)]
    return {
        'number_of_sentences': len(all_sentences),
        'all_sentences': all_sentences.tolist(),
        'avg_sentence_length': round(all_sentences.apply(len).mean()),
        'max_sentence_length': max_sentence_length,
        'most_common_word': Counter([item for sublist in all_sentences for item in sublist]).most_common(1)[0][0],
        'most_common_word_at_position': most_common_at_position[:most_common_at_position.index('.')],
        'sliding_window': [sliding_window(all_sentences, i) for i in range(1, 6)]
    }


review_data = pd.read_csv("reviews.txt")

five_star_data = prep_dataset(review_data[review_data['review_stars'] == 5].sample(n=500, random_state=42)['review_text'].apply(clean))

one_star_data = prep_dataset(review_data[review_data['review_stars'] == 1].sample(n=500, random_state=42)['review_text'].apply(clean))

with open("subtitles.txt", 'r', encoding='utf-8') as file:
    subtitle_data = prep_dataset(pd.DataFrame({'sentences': file.readlines()}).sample(n=500, random_state=42)['sentences'].apply(clean))


output_string = """
const fiveStarData = """+json.dumps(five_star_data, cls=NpEncoder)+""";
const oneStarData = """+json.dumps(one_star_data, cls=NpEncoder)+""";
const subtitleData = """+json.dumps(subtitle_data, cls=NpEncoder)+""";
export {fiveStarData, oneStarData, subtitleData};
"""

with open("src/datasets.js", 'w', encoding='utf-8') as file:
    file.write(output_string)