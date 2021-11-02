import pandas
import matplotlib.pyplot as plot


df = pandas.read_csv('basket.csv', sep=',')

# question A
rs = df[['Item']].drop_duplicates().count()
print(rs)

# question B
rs = df.groupby(['Item']).size().sort_values()
products = list(rs.keys())
product_counts = list(rs.values)
plot.bar(products, product_counts)
plot.show()

