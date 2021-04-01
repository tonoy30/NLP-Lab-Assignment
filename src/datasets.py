import pandas as pd

data = pd.read_csv("data/ben.txt", sep="\t", header=None,
                   names=["English", "Bangla", "Attribution"])

data = data.drop("Attribution", axis=1)
print(f"Modified Dataset: { data.head()}")

data.to_csv("data/eng_to_bang_data.csv", index=False)

print(f"Prepared Dataset: {data.head()}")
print(f"Number of Data: {data.count().sum()} and {data.count()}")
print(f"Null Data: {data.isna().sum()}")
print(f"Description of Dataset: {data.describe()}")
print(f"Info about Dataset: {data.info}")
