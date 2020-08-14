class HexPresentor:

    def __init__(self):
        pass

    def present(self, data: bytes, step: int, pos: int) -> (list, list, list):
        hex_rows = self._hex_creator(data, step)
        ascii_rows = self._ascii_creator(data, step)
        rows = self._row_creator(len(hex_rows), step, pos)
        return rows, hex_rows, ascii_rows

    @staticmethod
    def _hex_creator(data: bytes, step: int) -> list:
        hex_list = []
        hex_row = []

        data = data.hex()
        for i in range(len(data) // 2):
            hex_row.append(data[i * 2:i * 2 + 2])
            if len(hex_row) == step:
                hex_list.append(hex_row)
                hex_row = []
        else:
            residue = len(data) % (step * 2)
            if residue != 0:
                for j in range(step - residue):
                    hex_row.append('00')
                hex_list.append(hex_row)

        return hex_list

    @staticmethod
    def _ascii_creator(data: bytes, step: int) -> list:
        hex_list = []
        ascii_row = []

        for i in range(len(data)):
            symbol = data[i:i + 1]
            try:
                ascii_row.append(symbol.decode('ascii'))
            except UnicodeDecodeError:
                ascii_row.append('.')
            if len(ascii_row) == step:
                hex_list.append(ascii_row)
                ascii_row = []
        else:
            residue = len(data) % step
            if residue != 0:
                for j in range(step - residue):
                    ascii_row.append('.')
                hex_list.append(ascii_row)

        return hex_list

    @staticmethod
    def _row_creator(len_row: int, step: int, pos: int) -> list:
        rows = []
        row = pos * step - step
        for inc in range(len_row):
            row = row + step
            rows.append(f'{row:08d}')
        return rows
