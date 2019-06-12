import pandas as pd
import matplotlib.pyplot as plt


def clean_data(df):
    df = df['Place of Publication'].apply(
        lambda x: 'London' if 'London' in x else x.replace('-', ' ')
    )
    return df



file = 'Books.csv'

df = pd.read_csv(file)
#print(df)
#print(df['Place of Publication'])
df_placeOfpublic = clean_data(df)
print(df_placeOfpublic)
df_p_count = df_placeOfpublic.value_counts()
print(df_p_count)

df_p_count.plot.pie(subplots=True)
plt.show()

