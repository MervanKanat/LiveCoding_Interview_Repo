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

def first_order_hobby_toys(df):
    customer_order_counts = df.groupby('customer_id').size()
    customers_with_multiple_orders = customer_order_counts[customer_order_counts >= 2].index
    first_orders = df.sort_values('order_date').groupby('customer_id').first().reset_index()
    result = first_orders[
        (first_orders['customer_id'].isin(customers_with_multiple_orders)) &
        (first_orders['category'] == 'hobby&toys')
    ]
    return result, customers_with_multiple_orders

def above_average_basket(df):
    customer_avg_basket = df.groupby('customer_id')['amount'].mean()
    overall_avg_basket = customer_avg_basket.mean()
    customer_labels = (customer_avg_basket > overall_avg_basket).astype(int)
    return overall_avg_basket, customer_labels

# Display the data
data_table = Table(title="Sample Data")
for column in df.columns:
    data_table.add_column(column, style="cyan")

for _, row in df.iterrows():
    data_table.add_row(*[str(value) for value in row])

console.print(data_table)

# Display questions and results
console.print(Panel.fit(
    "[bold green]Question 1:[/bold green] Create a customer label for customers who have placed at least 2 different orders and made a purchase in the hobby&toys category in their first order. The label should be 1 if the condition is met, 0 if not.",
    title="Question 1"
))

result_q1, multiple_orders = first_order_hobby_toys(df)
q1_table = Table(title="Question 1 Detailed Results")
q1_table.add_column("Customer ID", style="cyan")
q1_table.add_column("Multiple Orders", style="magenta")
q1_table.add_column("First Order Category", style="yellow")
q1_table.add_column("Condition Met", style="green")

for customer_id in df['customer_id'].unique():
    has_multiple_orders = "Yes" if customer_id in multiple_orders else "No"
    first_order = df[df['customer_id'] == customer_id].sort_values('order_date').iloc[0]
    first_category = first_order['category']
    condition_met = "Yes" if customer_id in result_q1['customer_id'].values else "No"
    
    row_style = "bold green" if condition_met == "Yes" else "dim red"
    q1_table.add_row(
        str(customer_id),
        has_multiple_orders,
        first_category,
        condition_met,
        style=row_style
    )

console.print(q1_table)

console.print(Panel.fit(
    "[bold green]Question 2:[/bold green] Create a customer label for customers whose basket average is above the arithmetic mean of all customers' basket averages. The label should be 1 if the condition is met, 0 if not. (basket = average order amount)",
    title="Question 2"
))

avg_basket, customer_labels = above_average_basket(df)
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
