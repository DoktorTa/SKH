class HexPresentor:

    def __init__(self):
        pass

    def presentor(self, data: bytes) -> list:
        hex_list = []
        hex_row = []
        
        data = data.hex()
        for inc in data:
            hex_row.append()
            hex_list.append(hex_row)

        return hex_list

    def row_creator(self, len_row: int):
        self.row = self.row + len_row
        return f'{self.row:08d}'
