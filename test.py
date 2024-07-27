import unittest
import pandas as pd
from io import StringIO
import json

# Importing functions from task.py
from task import (
    preprocess_data, 
    compute_monthly_revenue, 
    compute_product_revenue, 
    compute_customer_revenue, 
    compute_top_customers, 
    generate_output
)

# Sample CSV data for testing
sample_data = """order_id,customer_id,order_date,product_id,product_name,product_price,quantity
ORD1000,CUST1000,2024-01-01,PROD100,Product 0,50.00,2
ORD1001,CUST1001,2024-02-01,PROD101,Product 1,20.00,1
ORD1002,CUST1002,2024-03-01,PROD102,Product 2,30.00,3
ORD1003,CUST1003,2024-01-15,PROD103,Product 3,40.00,1
ORD1004,CUST1004,2024-02-20,PROD104,Product 4,60.00,5
ORD1005,CUST1005,2024-03-10,PROD105,Product 5,10.00,4
ORD1006,CUST1006,2024-01-25,PROD106,Product 6,70.00,2
ORD1007,CUST1007,2024-02-15,PROD107,Product 7,80.00,1
ORD1008,CUST1008,2024-03-20,PROD108,Product 8,90.00,3
ORD1009,CUST1009,2024-01-30,PROD109,Product 9,100.00,1
"""

class TestRevenueCalculations(unittest.TestCase):
    
    def setUp(self):
        self.df = pd.read_csv(StringIO(sample_data))
        self.df = preprocess_data(self.df)

    def test_compute_monthly_revenue(self):
        monthly_revenue_json = compute_monthly_revenue(self.df)
        monthly_revenue = json.loads(monthly_revenue_json)
        self.assertEqual(len(monthly_revenue), 3)
        self.assertTrue(any(rev['month'] == '2024-01' and rev['revenue'] == 380.0 for rev in monthly_revenue))

    def test_compute_product_revenue(self):
        product_revenue_json = compute_product_revenue(self.df)
        product_revenue = json.loads(product_revenue_json)
        self.assertEqual(len(product_revenue), 10)
        self.assertTrue(any(rev['product_name'] == 'Product 0' and rev['revenue'] == 100.0 for rev in product_revenue))

    def test_compute_customer_revenue(self):
        customer_revenue_json = compute_customer_revenue(self.df)
        customer_revenue = json.loads(customer_revenue_json)
        self.assertEqual(len(customer_revenue), 10)
        self.assertTrue(any(rev['customer_id'] == 'CUST1004' and rev['revenue'] == 300.0 for rev in customer_revenue))

    def test_compute_top_customers(self):
        top_customers_json = compute_top_customers(self.df)
        top_customers = json.loads(top_customers_json)
        self.assertEqual(len(top_customers), 10)
        self.assertEqual(top_customers[0]['customer_id'], 'CUST1004')

    def test_generate_output(self):
        output = generate_output(self.df)
        self.assertEqual(len(output), 4)
        self.assertEqual(output[0]['question'], 1)
        self.assertEqual(output[1]['question'], 2)
        self.assertEqual(output[2]['question'], 3)
        self.assertEqual(output[3]['question'], 4)

if __name__ == '__main__':
    unittest.main()
