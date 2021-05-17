import pandas as pd
import matplotlib.pyplot as plt


def openamazondata(orders, refunds):
    # open the csv files and fill in all NaN values with 0, and store the data in two variables for later use.
    df_orders = pd.read_csv(orders).fillna(0)
    df_refunds = pd.read_csv(refunds).fillna(0)
    df_joined = pd.concat([df_orders, df_refunds])
    df = df_joined[["Order Date", "Total Charged", "Tax Charged", "Refund Amount"]].copy()
    del df_refunds, df_joined, df_orders

    return df


def spendingstats(orders, refunds):
    # Open and store the csv files by calling our openamazondata function
    df = openamazondata(orders, refunds)
    # format the columns to be float type and strip the $
    charged = df["Total Charged"].str.replace('$', '', regex=True).astype(float)
    refunded = df["Refund Amount"].str.replace('$', '', regex=True).astype(float)
    theft = df["Tax Charged"].str.replace('$', '', regex=True).astype(float)

    # start calculations on order data
    total_charged = charged.sum().round(2)
    total_refund = refunded.sum().round(2)
    total_spent = (total_charged - total_refund).round(2)

    average_cost = round(charged.mean(), 2)
    max_cost = charged.max()
    min_cost = min(i for i in charged if i > 0)
    total_theft = theft.sum().round(2)
    theft_rate = (total_theft / total_charged * 100).round(2)

    stats = f"""
    Your Amazon Spending Stats:
    
    Total Amount Charged: ${total_charged}
    Total Amount Refunded: ${total_refund}
    Total Spent After Refunds: ${total_spent}
    Total Stolen by The State: ${total_theft}
    State Theft Rate: {theft_rate}%
    Average Purchase Cost: ${average_cost}
    Largest Single Purchase: ${max_cost}
    Smallest Single Purchase: ${min_cost}
    """
    return stats


def spendingtrend(orders, refunds):
    # Open and store the csv files by calling our openamazondata function
    df = openamazondata(orders, refunds)
    df["Total Charged"] = df["Total Charged"].str.replace('$', '', regex=True).astype(float).fillna(0)
    df["Refund Amount"] = df["Refund Amount"].str.replace('$', '', regex=True).astype(float).fillna(0) * -1
    df["Order Date"] = pd.to_datetime(df['Order Date'])

    spending = df.groupby(df['Order Date'].dt.to_period('M')).sum()[["Refund Amount", "Total Charged"]]
    spending.plot.bar(figsize=(20, 10), stacked=True, color=['red', 'blue'])
    plt.title("Monthly Amazon Shopping Trends")
    plt.xlabel("Months (Year-Month)")
    plt.ylabel("Amount Spent in USD ($)")
    #plt.figtext(1,1,spendingstats(orders, refunds))
    plt.subplots_adjust(right=.8)
    plt.text(0.8, 0.5, spendingstats(orders, refunds), fontsize=14, transform=plt.gcf().transFigure)
    plt.show()


# openamazondata('/home/glencross/PythonProjects/AmazonShopping/orders_and_shipments.csv',
# '/home/glencross/PythonProjects/AmazonShopping/refunds.csv')
#spendingstats('/home/glencross/PythonProjects/AmazonShopping/orders_Abel.csv',
#              '/home/glencross/PythonProjects/AmazonShopping/refunds_Abel.csv')
spendingtrend('/home/glencross/PythonProjects/AmazonShopping/orders_AJG.csv',
              '/home/glencross/PythonProjects/AmazonShopping/refunds_AJG.csv')
