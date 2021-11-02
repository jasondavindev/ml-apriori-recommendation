import pandas
import matplotlib.pyplot as plot


df = pandas.read_csv('basket.csv', sep=',')

# question A
rs = df[['Item']].drop_duplicates().count()
print(rs)


def insert_values():
    return [plot.text(x=index, y=data, s=str(data))
            for index, data in enumerate(product_counts)]


def filter_by_period_day(df, period):
    return df[df['period_day'] == period].groupby('Item').size().sort_values()


# question B
rs = df.groupby('Item').size().sort_values().tail(10)
products = list(rs.keys())
product_counts = list(rs.values)
plot.bar(products, product_counts)
insert_values()
plot.show()

# question C
rs = filter_by_period_day(df, 'morning').tail(10)
products = list(rs.keys())
product_counts = list(rs.values)
plot.bar(products, product_counts)
insert_values()
plot.show()

# question D
rs = filter_by_period_day(df, 'afternoon').tail(10)
products = list(rs.keys())
product_counts = list(rs.values)
plot.bar(products, product_counts)
insert_values()
plot.show()

# question E
rs = filter_by_period_day(df, 'evening').tail(10)
products = list(rs.keys())
product_counts = list(rs.values)
plot.bar(products, product_counts)
insert_values()
plot.show()
