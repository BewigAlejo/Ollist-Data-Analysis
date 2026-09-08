# Olist E-commerce Data Analysis

## About the Project

This project is an end-to-end data analytics case study based on the **Olist Brazilian E-Commerce Public Dataset**.

Olist is a Brazilian e-commerce marketplace that connects small businesses with customers across Brazil. The dataset contains information about orders, customers, sellers, products, payments, reviews and deliveries.

The objective of this project is to work through a complete analytics workflow:

**Data acquisition → Data quality assessment → Data cleaning → SQL/Pandas analysis → Dashboard → Business insights → Recommendations**

The main business problem explored in this project is:

> **What factors are associated with late deliveries and poor customer reviews, and where should the business prioritize improvements?**

The project focuses not only on building visualizations, but on understanding the data, identifying quality issues, answering business questions and translating the findings into actionable recommendations.

### Technologies

- Python
- pandas
- SQL
- Power BI
- Power Query
- DAX
- Git / GitHub

---

## Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist**, available on Kaggle.

Dataset:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

The dataset contains multiple CSV files representing different parts of the e-commerce operation, including:

- Orders
- Customers
- Order items
- Products
- Sellers
- Payments
- Customer reviews
- Geolocation
- Product category translations

Because the dataset is relational, the different tables can be connected through identifiers such as `order_id`, `customer_id`, `product_id` and `seller_id`.

---

## Getting the Data

The raw dataset is **not stored directly in this repository**.

Instead, it can be downloaded directly from Kaggle using the `kagglehub` Python library. This makes the project easier to reproduce without uploading the original dataset to GitHub.

### 1. Install the required libraries

```bash
pip install kagglehub pandas
```

### 2. Authenticate with Kaggle

If Kaggle authentication is required in your environment:

```python
import kagglehub

kagglehub.login()
```

You can create your Kaggle API credentials from your Kaggle account settings.

> Never upload your Kaggle API token, `kaggle.json` or `.env` file to GitHub.

---

### 3. Download the dataset

```python
import kagglehub

path = kagglehub.dataset_download(
    "olistbr/brazilian-ecommerce"
)

print("Dataset path:", path)
```

`kagglehub` stores the dataset in its local cache and returns the directory containing the downloaded files.

There is no need to manually move the original CSV files into the repository.

---

### 4. Inspect the downloaded files

```python
import os

files = os.listdir(path)

for file in files:
    print(file)
```

You should find files similar to:

```text
olist_orders_dataset.csv
olist_customers_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
olist_geolocation_dataset.csv
product_category_name_translation.csv
```

---

### 5. Load a table with pandas

For example, the orders table can be loaded with:

```python
import pandas as pd
import os

orders = pd.read_csv(
    os.path.join(path, "olist_orders_dataset.csv")
)

orders.head()
```

From this point, the dataset is ready for the **data profiling and quality assessment stage**.

---

## Project Workflow

The project will follow these stages:

1. Data acquisition
2. Dataset and table understanding
3. Data profiling
4. Null and duplicate analysis
5. Primary and foreign key validation
6. Data cleaning and transformation
7. Exploratory Data Analysis with pandas
8. SQL analysis
9. KPI definition
10. Power BI dashboard
11. Business insights
12. Business recommendations
13. Documentation and case study