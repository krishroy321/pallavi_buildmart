def read_inventory(filename):
    inventory = []

    file = open(filename, "r")

    for line in file:
        line = line.strip()

        if line != "":
            parts = line.split(",")

            product = {
                "name": parts[0].strip(),
                "brand": parts[1].strip(),
                "stock": float(parts[2].strip()),
                "unit": parts[3].strip(),
                "rate": float(parts[4].strip())
            }

            inventory.append(product)

    file.close()

    return inventory