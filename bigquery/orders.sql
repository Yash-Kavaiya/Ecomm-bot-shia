-- Create a table with the generated data (if you haven't already)
CREATE OR REPLACE TABLE `innate-lacing-450600-r5.E_commerce.sample_orders` AS
SELECT
  LPAD(CAST(FLOOR(RAND() * 100000000) AS STRING), 8, '0') AS order_id, -- Generate 8-digit order IDs
  CONCAT('CUST', CAST(FLOOR(RAND() * 1000) AS STRING)) AS customer_id,
  DATE_SUB(CURRENT_DATE(), INTERVAL CAST(FLOOR(RAND() * 30) AS INT64) DAY) AS order_date,
  CASE
    WHEN RAND() < 0.3 THEN 'Pending'
    WHEN RAND() < 0.6 THEN 'Shipped'
    WHEN RAND() < 0.9 THEN 'Delivered'
    ELSE 'Cancelled'
  END AS status,
  CASE
    WHEN RAND() < 0.7 THEN CONCAT('TRACK', CAST(FLOOR(RAND() * 1000000) AS STRING))
    ELSE NULL
  END AS tracking_number,
  CONCAT(
    FLOOR(RAND() * 1000),
    ' ',
    CASE
      WHEN RAND() < 0.3 THEN 'Main St'
      WHEN RAND() < 0.6 THEN 'Oak Ave'
      ELSE 'Pine Ln'
    END,
    ', ',
    CASE
      WHEN RAND() < 0.3 THEN 'Anytown'
      WHEN RAND() < 0.6 THEN 'Springfield'
      ELSE 'Riverside'
    END,
    ', ',
    CASE
      WHEN RAND() < 0.5 THEN 'CA'
      ELSE 'NY'
    END
  ) AS shipping_address,
  CASE
    WHEN RAND() < 0.2 THEN 'Electronics'
    WHEN RAND() < 0.5 THEN 'Clothing'
    WHEN RAND() < 0.8 THEN 'Books'
    ELSE 'Home Goods'
  END AS product_category,
  CASE
    WHEN RAND() < 0.3 THEN CONCAT('Product', CAST(FLOOR(RAND() * 100) AS STRING))
    WHEN RAND() < 0.6 THEN CONCAT('Item', CAST(FLOOR(RAND() * 150) AS STRING))
    ELSE CONCAT('Widget', CAST(FLOOR(RAND() * 200) AS STRING))
  END AS product_name,
  CAST(FLOOR(RAND() * 100 + 10) AS INT64) AS quantity,
  CAST(RAND() * 1000 AS NUMERIC) AS total_price,
  CASE
    WHEN RAND() < 0.2 THEN 'Credit Card'
    WHEN RAND() < 0.5 THEN 'PayPal'
    WHEN RAND() < 0.8 THEN 'Bank Transfer'
    ELSE 'Cash on Delivery'
  END AS payment_method,
  CASE
    WHEN RAND() < 0.2 THEN 'Standard'
    WHEN RAND() < 0.5 THEN 'Express'
    WHEN RAND() < 0.8 THEN 'Same Day'
    ELSE 'International'
  END AS shipping_method
FROM
  UNNEST(GENERATE_ARRAY(1, 15));

-- Example Queries:

-- 1. Select all data from the table
SELECT * FROM `innate-lacing-450600-r5.E_commerce.sample_orders`;

-- 2. Select specific columns and filter by order status
SELECT order_id, customer_id, order_date, status
FROM `innate-lacing-450600-r5.E_commerce.sample_orders`
WHERE status = 'Shipped';

-- 3. Count orders by status
SELECT status, COUNT(*) AS order_count
FROM `innate-lacing-450600-r5.E_commerce.sample_orders`
GROUP BY status;

-- 4. Find orders placed within a specific date range
SELECT *
FROM `innate-lacing-450600-r5.E_commerce.sample_orders`
WHERE order_date BETWEEN '2023-10-15' AND '2023-10-25';

-- 5. Calculate the average total price
SELECT AVG(total_price) AS average_total_price
FROM `innate-lacing-450600-r5.E_commerce.sample_orders`;

-- 6. Find orders with a specific tracking number (if exists)
SELECT *
FROM `innate-lacing-450600-r5.E_commerce.sample_orders`
WHERE tracking_number = 'TRACK123456'; -- Replace with an actual tracking number

-- 7. Orders shipped to a specific state.
SELECT *
FROM `innate-lacing-450600-r5.E_commerce.sample_orders`
WHERE shipping_address LIKE '%CA%';

-- 8. Find orders from a specific customer.
SELECT *
FROM `innate-lacing-450600-r5.E_commerce.sample_orders`
WHERE customer_id = 'CUST123'; -- Replace with a real customer ID.

-- 9. Find the latest order date.
SELECT MAX(order_date) from `innate-lacing-450600-r5.E_commerce.sample_orders`;

-- 10. Find the orders with the highest total price.
SELECT * FROM `innate-lacing-450600-r5.E_commerce.sample_orders` ORDER BY total_price DESC LIMIT 5;
