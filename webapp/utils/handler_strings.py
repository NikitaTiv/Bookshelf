def split_row_book_delete(row: str) -> tuple[str, str]:
    """Функция, которая делит получаемую строку."""
    return row.split('/')[0].strip(), row.split('/')[1].strip()
