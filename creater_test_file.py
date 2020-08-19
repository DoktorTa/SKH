with open(r'A:\Programming languages\In developing\Python\SKH\TestModules\HexEditor\num.txt', r"w") as file:
    for i in range(5):
        row = 0
        for inc in range(999):
            row = row + 1
            file.write(f'.{row:03d}')
