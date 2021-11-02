import pandas
import matplotlib.pyplot as plot


df = pandas.read_csv('basket.csv', sep=',')

# question A
rs = df[['Item']].drop_duplicates().count()
print(rs)


def insert_values():
    return [plot.text(x=index, y=data, s=str(data))
            for index, data in enumerate(product_counts)]


# question B
# rs = df.groupby(['Item']).size().sort_values()
rs = df.groupby('Item').size().sort_values().tail(10)
products = list(rs.keys())
product_counts = list(rs.values)
plot.bar(products, product_counts)
insert_values()
plot.show()

# question C
rs = df[df['period_day'] == 'morning'].groupby(
    'Item').size().sort_values().tail(10)
products = list(rs.keys())
product_counts = list(rs.values)
plot.bar(products, product_counts)
insert_values()
plot.show()

# question D
rs = df[df['period_day'] == 'afternoon'].groupby(
    'Item').size().sort_values().tail(10)
products = list(rs.keys())
product_counts = list(rs.values)
plot.bar(products, product_counts)
insert_values()
plot.show()

# question E
rs = df[df['period_day'] == 'evening'].groupby(
    'Item').size().sort_values().tail(10)
products = list(rs.keys())
product_counts = list(rs.values)
plot.bar(products, product_counts)
insert_values()
plot.show()
