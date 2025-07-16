import pandas as pd
import os

# ✅ Read lyrics file
df = pd.read_excel("data/raw_lyrics_ovh.xlsx")
df.columns = df.columns.str.lower().str.strip()  # Normalize column names

# ✅ Word lists
male_words = ['he', 'him', 'his', 'man', 'boy']
female_words = ['she', 'her', 'hers', 'woman', 'girl']

# ✅ Count function
def count_words(text, word_list):
    text = str(text).lower()
    return sum(text.count(word) for word in word_list)

# ✅ Apply counts
df['male_words'] = df['lyrics'].apply(lambda x: count_words(x, male_words))
df['female_words'] = df['lyrics'].apply(lambda x: count_words(x, female_words))
df['bias_score'] = df['male_words'] - df['female_words']

df['love_count'] = df['lyrics'].apply(lambda x: str(x).lower().count('love'))
df['hate_count'] = df['lyrics'].apply(lambda x: str(x).lower().count('hate'))
df['sentiment'] = df['love_count'] - df['hate_count']

# ✅ Save cleaned data
os.makedirs("data", exist_ok=True)
df.to_excel("data/cleaned_lyrics.xlsx", index=False)

print("🎉 Analysis complete → data/cleaned_lyrics.xlsx")
