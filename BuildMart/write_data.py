def write_header(title):
    print()
    print("=" * 60)
    print(title.center(60))
    print("=" * 60)


def write_invoice_header(file, title):
    file.write("=" * 60 + "\n")
    file.write(title.center(60) + "\n")
    file.write("=" * 60 + "\n")