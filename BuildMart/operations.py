from datetime import datetime
from write_data import write_invoice_header


WEIGHT_DISCOUNT_LIMIT = 50
QUANTITY_DISCOUNT_LIMIT = 100
DISCOUNT_RATE = 0.05


def display_inventory(inventory):
    print()
    print("=" * 80)
    print("BUILD MART HARDWARE STORE - INVENTORY")
    print("=" * 80)

    print(f"{'No.':<5}{'Product':<22}{'Brand':<20}{'Stock':<12}{'Unit':<12}{'Rate':<10}")
    print("-" * 80)

    number = 1

    for product in inventory:
        stock = product["stock"]

        if product["unit"] == "quantity":
            stock = int(stock)

        print(
            f"{number:<5}"
            f"{product['name']:<22}"
            f"{product['brand']:<20}"
            f"{stock:<12}"
            f"{product['unit']:<12}"
            f"Rs. {product['rate']:<10.2f}"
        )

        number += 1

    print("=" * 80)


def find_product(inventory, product_name):
    for product in inventory:
        if product["name"].lower() == product_name.lower():
            return product

    return None


def calculate_discount(product, amount):
    discount = 0

    if product["unit"].lower() == "kg":
        if amount >= WEIGHT_DISCOUNT_LIMIT:
            discount = amount * product["rate"] * DISCOUNT_RATE

    elif product["unit"].lower() == "quantity":
        if amount >= QUANTITY_DISCOUNT_LIMIT:
            discount = amount * product["rate"] * DISCOUNT_RATE

    return discount


def update_inventory_file(filename, inventory):
    file = open(filename, "w")

    for product in inventory:
        line = (
            product["name"] + ", " +
            product["brand"] + ", " +
            str(product["stock"]) + ", " +
            product["unit"] + ", " +
            str(product["rate"]) + "\n"
        )

        file.write(line)

    file.close()


def create_sales_invoice(customer_name, purchased_items):
    now = datetime.now()

    filename = "sales_invoice_" + now.strftime("%Y%m%d_%H%M%S") + ".txt"

    file = open(filename, "w")

    write_invoice_header(file, "BUILD MART HARDWARE STORE")
    file.write("VAT / SALES INVOICE\n\n")

    file.write("Customer Name: " + customer_name + "\n")
    file.write("Date: " + now.strftime("%d-%m-%Y %H:%M:%S") + "\n")
    file.write("\n")

    total_amount = 0
    total_discount = 0

    for item in purchased_items:
        file.write("-" * 60 + "\n")
        file.write("Product: " + item["name"] + "\n")
        file.write("Brand: " + item["brand"] + "\n")
        file.write("Unit: " + item["unit"] + "\n")
        file.write("Quantity Sold: " + str(item["quantity"]) + "\n")
        file.write("Rate: Rs. " + format(item["rate"], ".2f") + "\n")
        file.write("Subtotal: Rs. " + format(item["subtotal"], ".2f") + "\n")
        file.write("Discount: Rs. " + format(item["discount"], ".2f") + "\n")
        file.write("Item Total: Rs. " + format(item["total"], ".2f") + "\n")

        total_amount += item["total"]
        total_discount += item["discount"]

    file.write("\n")
    file.write("=" * 60 + "\n")
    file.write("Total Discount: Rs. " + format(total_discount, ".2f") + "\n")
    file.write("TOTAL AMOUNT: Rs. " + format(total_amount, ".2f") + "\n")
    file.write("=" * 60 + "\n")

    file.close()

    return filename


def sell_products(inventory, filename):
    customer_name = input("Enter customer name: ")

    purchased_items = []

    while True:
        product_name = input("\nEnter product name to sell: ")

        product = find_product(inventory, product_name)

        if product is None:
            print("Product not found.")
            continue

        print("Available stock:", product["stock"], product["unit"])
        print("Rate: Rs.", product["rate"])

        try:
            quantity = float(input("Enter quantity to sell: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if quantity <= 0:
            print("Quantity must be greater than 0.")
            continue

        if quantity > product["stock"]:
            print("Not enough stock available.")
            continue

        subtotal = quantity * product["rate"]

        discount = calculate_discount(product, quantity)

        total = subtotal - discount

        product["stock"] = product["stock"] - quantity

        item = {
            "name": product["name"],
            "brand": product["brand"],
            "unit": product["unit"],
            "quantity": quantity,
            "rate": product["rate"],
            "subtotal": subtotal,
            "discount": discount,
            "total": total
        }

        purchased_items.append(item)

        print("\nProduct added to sale.")
        print("Subtotal: Rs.", subtotal)
        print("Discount: Rs.", discount)
        print("Total: Rs.", total)

        choice = input("\nDo you want to buy another product? (yes/no): ")

        if choice.lower() != "yes":
            break

    update_inventory_file(filename, inventory)

    invoice = create_sales_invoice(customer_name, purchased_items)

    print("\nSale completed successfully.")
    print("Invoice generated:", invoice)


def create_restock_invoice(supplier_name, restocked_items):
    now = datetime.now()

    filename = "restock_invoice_" + now.strftime("%Y%m%d_%H%M%S") + ".txt"

    file = open(filename, "w")

    write_invoice_header(file, "BUILD MART HARDWARE STORE")
    file.write("RESTOCK / PURCHASE INVOICE\n\n")

    file.write("Supplier Name: " + supplier_name + "\n")
    file.write("Date: " + now.strftime("%d-%m-%Y %H:%M:%S") + "\n")
    file.write("\n")

    grand_total = 0

    for item in restocked_items:
        file.write("-" * 60 + "\n")
        file.write("Product: " + item["name"] + "\n")
        file.write("Brand: " + item["brand"] + "\n")
        file.write("Unit: " + item["unit"] + "\n")
        file.write("Quantity Bought: " + str(item["quantity"]) + "\n")
        file.write("Rate: Rs. " + format(item["rate"], ".2f") + "\n")
        file.write("Total: Rs. " + format(item["total"], ".2f") + "\n")

        grand_total += item["total"]

    file.write("\n")
    file.write("=" * 60 + "\n")
    file.write("GRAND TOTAL: Rs. " + format(grand_total, ".2f") + "\n")
    file.write("=" * 60 + "\n")

    file.close()

    return filename


def restock_products(inventory, filename):
    supplier_name = input("Enter supplier/vendor name: ")

    restocked_items = []

    while True:
        product_name = input("\nEnter product name to restock: ")

        product = find_product(inventory, product_name)

        if product is None:
            print("Product not found.")
            continue

        print("Current stock:", product["stock"], product["unit"])
        print("Rate: Rs.", product["rate"])

        try:
            quantity = float(input("Enter quantity to restock: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if quantity <= 0:
            print("Quantity must be greater than 0.")
            continue

        total = quantity * product["rate"]

        product["stock"] = product["stock"] + quantity

        item = {
            "name": product["name"],
            "brand": product["brand"],
            "unit": product["unit"],
            "quantity": quantity,
            "rate": product["rate"],
            "total": total
        }

        restocked_items.append(item)

        print("\nProduct restocked successfully.")
        print("Added:", quantity, product["unit"])
        print("Cost: Rs.", total)

        choice = input("\nDo you want to restock another product? (yes/no): ")

        if choice.lower() != "yes":
            break

    update_inventory_file(filename, inventory)

    invoice = create_restock_invoice(supplier_name, restocked_items)

    print("\nRestock completed successfully.")
    print("Invoice generated:", invoice)