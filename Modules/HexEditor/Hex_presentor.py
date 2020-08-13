class HexPresentor:

    def __init__(self):
        pass

    def hex_presentor(self, data: bytes, step: int) -> list:
        hex_list = []
        hex_row = []

        data = data.hex()
        for i in range(len(data) // 2):
            hex_row.append(data[i * 2:i * 2 + 2])

        for i in range(len(data) // step):
            hex_list.append(hex_row[i * step: i * step + step])

        return hex_list

    def ascii_creator(self):
        pass

    def row_creator(self, len_row: int, step: int, pos: int) -> list:
        rows = []
        row = pos * step - step
        for inc in range(len_row):
            row = row + step
            rows.append(f'{row:08d}')
        return rows
