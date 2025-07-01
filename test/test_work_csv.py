import pytest
from process import work_csv

TEST_ROWS = [
    {'name': 'iphone 15 pro', 'brand': 'apple', 'price': '999', 'rating': '4.9'},
    {'name': 'galaxy s23 ultra', 'brand': 'samsung', 'price': '1199', 'rating': '4.8'},
    {'name': 'redmi note 12', 'brand': 'xiaomi', 'price': '199', 'rating': '4.6'},
    {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '299', 'rating': '4.4'},
]


def test_read_csv():
    assert work_csv.read_csv('../process/data.csv') == TEST_ROWS


def test_check_is_str():
    assert work_csv.check_is_str('test') == 'test'
    assert work_csv.check_is_str('123.34') == 123.34
    assert work_csv.check_is_str('56') == 56

def test_check_columns():
    for row in TEST_ROWS:
        work_csv.check_columns(row,"brand")

    with pytest.raises(KeyError):
        work_csv.check_columns(TEST_ROWS[0], "column")

def test_where_dict():
    filtered = work_csv.where_dict(TEST_ROWS, 'price>200')
    assert len(filtered) == 3
    assert all(int(row['price']) > 200 for row in filtered)
    filtered = work_csv.where_dict(TEST_ROWS, 'brand=samsung')
    assert len(filtered) == 1
    filtered = work_csv.where_dict(TEST_ROWS, 'rating<=4.8')
    assert len(filtered) == 3
    assert all(float(row['rating']) <= 4.8 for row in filtered)
def test_aggregate():
    result = work_csv.aggregate(TEST_ROWS, 'price=avg')
    val = [float(row["price"]) for row in TEST_ROWS]

    assert len(result) == 1
    assert result[0]['avg'] == sum(val)/len(val)

    result = work_csv.aggregate(TEST_ROWS, 'price=min')
    assert len(result) == 1
    assert result[0]['min'] == min(val)

    result = work_csv.aggregate(TEST_ROWS, 'price=max')
    assert len(result) == 1
    assert result[0]['max'] == max(val)

def test_aggregate_invalid_column():
    with pytest.raises(KeyError):
        work_csv.aggregate(TEST_ROWS, 'avg=nonexistent')

def test_where_dict_invalid_format():
    with pytest.raises(ValueError):
        work_csv.where_dict(TEST_ROWS, 'price>>100')