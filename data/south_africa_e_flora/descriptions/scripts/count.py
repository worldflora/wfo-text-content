import pandas as pd

df = pd.read_csv(r"data\south_africa_e_flora\descriptions\raw\dwca-flora_descriptions-v1.42\vernacularname.txt", sep="\t", dtype=str)
df.columns = df.columns.str.strip()
pd.set_option("display.max_rows", None)
print(df["language"].value_counts())
