import csv
from typing import List, Any


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
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def check_columns(row: dict[str, Any], colum):
    check = row.get(colum)
    if check is None:
        raise KeyError("Колонка не найдена")


def where_dict(rows: list[dict[str, Any]], where: str) -> list[dict[str, Any]]:
    for op in ['>=', '<=', '>', '<', '=']:
        if op in where:
            column, value = where.split(op, 1)
            column, value = column.strip(), value.strip()
            break
    else:
        raise ValueError("Неверный формат")

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
    try:
        colum, op = agg.split('=', 1)
        op, colum = op.strip(), colum.strip()
    except ValueError:
        raise ValueError("Не верно передана агрегация!\nПример: операция=колонка")

    values = []
    for row in rows:
        check_columns(row, colum)
        val = check_is_str(row[colum])
        if not isinstance(val, (int, float)):
            raise ValueError(f"Колонка {colum} не числовая")
        values.append(val)

    if not values:
        return None
    match op:
        case "avg":
            result = sum(values) / len(values)
        case "min":
            result = min(values)
        case "max":
            result = max(values)
        case _:
            raise ValueError("неизвестная операция")

    return [{op: result}]
