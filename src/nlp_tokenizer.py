import re

import pandas as pd

df = pd.read_csv("data/eng_to_bang_data.csv")
data = df.iloc[:, 0]
bangle_sentences = []
count = 1


for df in data:
    sentences = re.split(r'\s', df)
    if len(sentences) > 1:
        print(sentences)
        count += 1

    for sen in sentences:
        bangle_sentences.append(sen)


print(f"Dataset Size : {len(data)}")
print(f"Total Number of Tokens: {len(bangle_sentences)}")
