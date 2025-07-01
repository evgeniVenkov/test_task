import csv
from typing import Any
OPERATIONS = {
        "avg": lambda vals: sum(vals) / len(vals) if vals else 0,
        "min": min,
        "max": max,
        # Можно легко добавить новые операции здесь:
    }

def read_csv(filepath: str) -> list[dict[str, Any]]:
    """
    Читает CSV-файл, возвращает список dict.

    :param filepath: путь к CSV-файлу
    :return: list[dict[str, Any]]
    """
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    return rows


def check_is_str(value: str) -> str | float | int:
    '''
    Преобразует строку в число, если возможно, иначе возвращает саму строку.
    :param value:
    :return: str | float | int
    '''
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def check_columns(row: dict[str, Any], colum: str):
    '''
    Проверяет есть ли колонка в словаре
    :param row: словарь
    :param colum: наименование колонки
    '''
    check = row.get(colum)
    if check is None:
        raise KeyError("Колонка не найдена")


def get_col_val_op(where: str) -> tuple[Any, Any, str]:
    """
        Парсит условие фильтра (например, 'price>=200') и возвращает
        кортеж: (колонка, значение, оператор).

        Выбрасывает ValueError при неправильном формате или лишних операторах.
        """
    for op in ['>=', '<=', '>', '<', '=']:
        if op in where:
            column, value = where.split(op, 1)
            column, value = column.strip(), value.strip()
            if any(o in value for o in ['>=', '<=', '>', '<', '=']):
                raise ValueError("Неверный формат: множественные операторы")
            break
    else:
        raise ValueError("Неверный формат")
    return column, value, op


def where_dict(rows: list[dict[str, Any]], where: str) -> list[dict[str, Any]]:
    """
       Фильтрует список словарей по условию вида 'column operator value'.
       Возвращает строки, удовлетворяющие условию.
    """
    column, value, op = get_col_val_op(where)

    value = check_is_str(value)

    def filter_row(row: dict[str, Any]) -> bool:
        check_columns(row, column)
        cell = check_is_str(row[column])
        match op:
            case '=':
                return cell == value
            case '>':
                return cell > value
            case '<':
                return cell < value
            case '>=':
                return cell >= value
            case '<=':
                return cell <= value
            case _:
                return False

    return [row for row in rows if filter_row(row)]


def aggregate(rows: list[dict[str, Any]], agg: str) -> list[dict[str, Any]] | None:
    """
       Выполняет агрегацию по указанной колонке и операции.

       Парсит строку агрегации формата "column=operation".
       Проверяет, что колонка числовая.
       Вычисляет агрегацию с помощью словаря OPERATIONS.

       :param rows: список словарей
       :param agg: строка агрегации, например "price=avg"
       :return: список с одним словарём {operation: результат}, или None если нет данных

    """
    try:
        colum, op = agg.split('=', 1)
        op, colum = op.strip(), colum.strip()
    except ValueError:
        raise ValueError("Не верно передана агрегация!\nПример: колонка=операция")

    values = []
    for row in rows:
        check_columns(row, colum)
        val = check_is_str(row[colum])
        if not isinstance(val, (int, float)):
            raise ValueError(f"Колонка {colum} не числовая")
        values.append(val)

    if not values:
        return None

    if op not in OPERATIONS:
        raise ValueError(f"Неизвестная операция агрегации: {op}")

    result = OPERATIONS[op](values)

    return [{op: result}]
