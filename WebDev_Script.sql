show databases;
USE mydb;
show tables;
SELECT * From courier;
SELECT * From customer;
SELECT * From parcel;

INSERT INTO Customer (Account_ID, Name, Email, Contact_No) VALUES
(1, 'John Doe', 'john.doe@example.com', 1234567890),
(2, 'Jane Smith', 'jane.smith@example.com', 2345678901),
(3, 'Alice Johnson', 'alice.johnson@example.com', 3456789012),
(4, 'Bob Brown', 'bob.brown@example.com', 4567890123),
(5, 'Charlie Davis', 'charlie.davis@example.com', 5678901234),
(6, 'Diana Evans', 'diana.evans@example.com', 6789012345),
(7, 'Frank Green', 'frank.green@example.com', 7890123456),
(8, 'Grace Hall', 'grace.hall@example.com', 8901234567),
(9, 'Henry White', 'henry.white@example.com', 9012345678),
(10, 'Ivy King', 'ivy.king@example.com', 1234567891);

INSERT INTO Parcel (Parcel_ID, Item_Type, Item_Name) VALUES
(50000001, 'Electronics', 'Smartphone'),
(50000002, 'Books', 'Fiction novel'),
(50000003, 'Clothing', 'Men’s winter jacket'),
(50000004, 'Toys', 'Lego building set'),
(50000005, 'Groceries', 'Organic vegetables and fruits');

INSERT INTO courier (customer_account_id, parcel_parcel_id, Delivery_Status, Sender_Name, Sender_Address, Receiver_Address, Receiver_Name) VALUES
(3, 50000001, 'Delivered', 'Alice Johnson', '123 Maple Street, Springfield, IL', '456 Elm Street, Springfield, IL', 'Bob Brown'),
(1, 50000002, 'In Transit', 'John Doe', '789 Oak Street, Springfield, IL', '101 Pine Street, Springfield, IL', 'Jane Smith'),
(5, 50000003, 'Pending', 'Charlie Davis', '202 Birch Street, Springfield, IL', '303 Cedar Street, Springfield, IL', 'Frank Green'),
(6, 50000004, 'Delivered', 'Diana Evans', '404 Walnut Street, Springfield, IL', '505 Ash Street, Springfield, IL', 'Grace Hall'),
(9, 50000005, 'In Transit', 'Henry White', '606 Beech Street, Springfield, IL', '707 Chestnut Street, Springfield, IL', 'Ivy King');
