from read_data import read_inventory
from operations import display_inventory
from operations import sell_products
from operations import restock_products


INVENTORY_FILE = "buildmart.txt"


def main():
    inventory = read_inventory(INVENTORY_FILE)

    while True:
        print()
        print("=" * 50)
        print("BUILD MART HARDWARE STORE")
        print("=" * 50)

        print("1. Display Inventory")
        print("2. Sell Products")
        print("3. Restock Products")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            display_inventory(inventory)

        elif choice == "2":
            sell_products(inventory, INVENTORY_FILE)

        elif choice == "3":
            restock_products(inventory, INVENTORY_FILE)

        elif choice == "4":
            print("\nThank you for using Build Mart Hardware Store.")
            break

        else:
            print("\nInvalid choice. Please try again.")


main()