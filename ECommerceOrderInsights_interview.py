from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import pandas as pd

# Create sample data
data = {
    'customer_id': [1, 1, 2, 2, 3, 3, 4],
    'order_date': ['2023-01-01', '2023-01-15', '2023-01-02', '2023-01-10', '2023-01-03', '2023-01-20', '2023-01-05'],
    'order_id': [1, 2, 3, 4, 5, 6, 7],
    'product_id': [101, 102, 103, 104, 105, 106, 107],
    'quantity': [2, 1, 3, 2, 1, 2, 1],
    'amount': [100, 150, 200, 180, 120, 220, 90],
    'category': ['hobby&toys', 'electronics', 'books', 'hobby&toys', 'clothing', 'electronics', 'books']
}
df = pd.DataFrame(data)

console = Console()

# Function definitions (as before)
def first_order_hobby_toys(df):
    first_orders = df.sort_values('order_date').groupby('customer_id').first().reset_index()
    customers_with_multiple_orders = df.groupby('customer_id').size()[df.groupby('customer_id').size() >= 2].index
    result = first_orders[
        (first_orders['customer_id'].isin(customers_with_multiple_orders)) &
        (first_orders['category'] == 'hobby&toys')
    ]['customer_id']
    return 1 if not result.empty else 0

def above_average_basket(df):
    customer_avg_basket = df.groupby('customer_id')['amount'].mean()
    overall_avg_basket = customer_avg_basket.mean()
    above_average_customers = customer_avg_basket[customer_avg_basket > overall_avg_basket]
    customer_labels = (customer_avg_basket > overall_avg_basket).astype(int)
    return 1 if not above_average_customers.empty else 0, overall_avg_basket, customer_labels

# Create and display data structure table
table = Table(title="Data Structure")
table.add_column("Column Name", style="cyan")
table.add_column("Description", style="magenta")

columns = [
    ("customer_id", "Unique identifier for each customer"),
    ("order_date", "Date of the order"),
    ("order_id", "Unique identifier for each order"),
    ("product_id", "Unique identifier for each product"),
    ("quantity", "Number of items ordered"),
    ("amount", "Total amount of the order"),
    ("category", "Product category")
]

for col, desc in columns:
    table.add_row(col, desc)

console.print(table)

# Display questions and results
console.print(Panel.fit(
    "[bold green]Question 1:[/bold green] Create a customer label for customers who have placed at least 2 different orders and made a purchase in the hobby&toys category in their first order. The label should be 1 if the condition is met, 0 if not.",
    title="Question 1"
))

result_q1 = first_order_hobby_toys(df)
console.print(f"[bold blue]Result:[/bold blue] {result_q1}")

console.print(Panel.fit(
    "[bold green]Question 2:[/bold green] Create a customer label for customers whose basket average is above the arithmetic mean of all customers' basket averages. The label should be 1 if the condition is met, 0 if not. (basket = average order amount)",
    title="Question 2"
))

result_q2, avg_basket, customer_labels = above_average_basket(df)
console.print(f"[bold blue]Result:[/bold blue] {result_q2}")
console.print(f"[bold blue]Overall average basket amount:[/bold blue] {avg_basket:.2f} TL")

# Create and display customer results table
customer_table = Table(title="Customer Results")
customer_table.add_column("Customer ID", style="cyan", justify="right")
customer_table.add_column("Average Basket", style="magenta", justify="right")
customer_table.add_column("Label", style="green", justify="center")

for customer, label in customer_labels.items():
    avg_amount = df[df['customer_id'] == customer]['amount'].mean()
    label_text = "1 (Above average)" if label == 1 else "0 (Below average)"
    label_color = "green" if label == 1 else "red"
    customer_table.add_row(
        str(customer),
        f"{avg_amount:.2f} TL",
        Text(label_text, style=label_color)
    )

console.print(customer_table)