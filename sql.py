import sqlite3

# connect to sqlite
connection = sqlite3.connect("client.db")

# cursor
cursor = connection.cursor()

#create table
table_info="""

CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    Price DECIMAL(10, 2),
    StockQuantity INT,
    SalesLastMonth INT,
    Description TEXT
);


"""

#cursor.execute(table_info)
insert_info = """

    INSERT INTO Products (ProductID, ProductName, Category, Price, StockQuantity, SalesLastMonth, Description)
VALUES(1, 'Wireless Bluetooth Headphones', 'Electronics', 59.99, 120, 45, 'Over-ear wireless headphones with noise cancellation.'),
(2, 'Organic Cotton T-Shirt', 'Apparel', 19.99, 300, 150, 'Soft organic cotton T-shirt available in various colors.'),
(3, '4K Ultra HD Smart TV', 'Electronics', 799.99, 50, 25, '55-inch 4K UHD Smart TV with streaming apps.'),
(4, 'Running Shoes', 'Footwear', 89.99, 200, 65, 'Lightweight running shoes with breathable material.'),
(5, 'Stainless Steel Water Bottle', 'Accessories', 14.99, 500, 100, 'Insulated stainless steel bottle, keeps drinks cold for 24 hours.'),
(6, 'Smartphone - 128GB', 'Electronics', 699.99, 75, 30, 'Latest model smartphone with 128GB storage and 5G capability.'),
(7, 'Yoga Mat', 'Fitness', 24.99, 150, 80, 'Eco-friendly yoga mat with non-slip surface, available in multiple colors.'),
(8, 'Laptop Backpack', 'Accessories', 49.99, 220, 90, 'Water-resistant laptop backpack with multiple compartments.'),
(9, 'Gaming Mouse', 'Electronics', 29.99, 140, 60, 'Ergonomic gaming mouse with customizable RGB lighting.'),
(10, 'Coffee Maker', 'Home Appliances', 89.99, 80, 40, '12-cup programmable coffee maker with reusable filter.');


"""
cursor.execute(insert_info)

# display the info

print("The Inserted Records are: ")
data = cursor.execute("Select * from Products")

for row in data:
    print(row)

# close the connection
connection.commit()
connection.close()
