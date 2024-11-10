import streamlit as st
import pandas as pd
import csv

# Product Class
class Product:
    def __init__(self, name='', category='', price=0.0, rating=0.0):
        self.name = name
        self.category = category
        self.price = price
        self.rating = rating

    def __str__(self):
        return f"-----------------------\nName: {self.name}\nPrice: ${self.price}\nRating: {self.rating} stars\nCategory: {self.category}"

# Load the product data
# @st.cache
def read_from_csv(filename):
    products = []
    try:
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                name, category, price, rating = row
                products.append(Product(name, category, float(price), float(rating)))
    except FileNotFoundError:
        st.write("Error opening file for reading!")
    return products

# Function to display products
def display_products(products):
    data = []
    for product in products:
        data.append([product.name, product.category, f"${product.price}", f"{product.rating} stars"])
    df = pd.DataFrame(data, columns=["Name", "Category", "Price", "Rating"])
    st.dataframe(df, use_container_width=True)

# Search Products by Name
def search_products_by_name(products, search_term):
    search_term = search_term.lower()
    result = []
    for product in products:
        if search_term in product.name.lower():
            result.append(product)
    return result

# Search Products by Category
def search_products_by_category(products, category):
    category = category.lower()
    result = []
    for product in products:
        if category in product.category.lower():
            result.append(product)
    return result


# Heapify function for heap sort in Python
def heapify(products, n, i, sortByPrice):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Compare based on either price or rating
    if sortByPrice:
        if left < n and products[left].price > products[largest].price:
            largest = left
        if right < n and products[right].price > products[largest].price:
            largest = right
    else:
        if left < n and products[left].rating > products[largest].rating:
            largest = left
        if right < n and products[right].rating > products[largest].rating:
            largest = right

    # If largest is not root
    if largest != i:
        products[i], products[largest] = products[largest], products[i]
        # Recursively heapify the affected subtree
        heapify(products, n, largest, sortByPrice)

# Heap sort function
def heapSort(products, sortByPrice=True):
    n = len(products)

    # Build a max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(products, n, i, sortByPrice)

    # Extract elements from the heap one by one
    for i in range(n - 1, 0, -1):
        products[0], products[i] = products[i], products[0]  # Swap
        heapify(products, i, 0, sortByPrice)

# Streamlit UI
st.title('Product Catalog')

# Load the product data
filename = 'catalogue.csv'
products = read_from_csv(filename)

# Display all products in a table
st.subheader("All Products")
display_products(products)

# Centered Search Bar
search_query = st.text_input('Search for a product', '')

if search_query:
    # Search for matching products
    found_products = search_products_by_name(products, search_query)

    if not found_products:
        st.write(f"No products found for '{search_query}'. Trying by category...")
        found_products = search_products_by_category(products, search_query)

    # Display Found Products
    st.subheader(f"Results for '{search_query}'")
    display_products(found_products)

    # Sorting Options
    sort_by_price = st.radio("Sort by:", ("Price", "Rating")) == "Price"

    if sort_by_price:
        heapSort(found_products, sortByPrice= True)
    else:
         # Perform Heap Sort based on selected option
        heapSort(found_products, sortByPrice=False)
    

    # Display Sorted Products
    st.subheader(f"Sort by {('Price' if sort_by_price else 'Rating')}")
    display_products(found_products)

    min_price = min(product.price for product in found_products)
    max_price = max(product.price for product in found_products)
    price_range = st.slider("Select Price Range", min_value=min_price, max_value=max_price, value=(min_price, max_price))

    filtered_by_price = []
    for product in found_products:
        if price_range[0] <= product.price <= price_range[1]:
            filtered_by_price.append(product)

    st.subheader(f"Filtered by Price: ${price_range[0]} - ${price_range[1]}")
    display_products(filtered_by_price)

    # Rating Filter
    rating_filter = st.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.1)

    filtered_by_rating = []
    for product in filtered_by_price:
        if product.rating >= rating_filter:
            filtered_by_rating.append(product)

    st.subheader(f"Filtered by Rating: ≥ {rating_filter} stars")
    display_products(filtered_by_rating)


else:
    st.write("Search for a product to view results.")

