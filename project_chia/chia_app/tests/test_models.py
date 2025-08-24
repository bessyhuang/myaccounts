import pytest
from chia_app.models import Category, Record
from datetime import date


# 告訴 pytest 這個測試需要操作資料庫
pytestmark = pytest.mark.django_db


def test_category_str():
    """測試 Category 的 __str__ 方法"""
    cat = Category.objects.create(category="食物")
    assert str(cat) == "食物"

def test_record_str_and_fields():
    """測試 Record 的 __str__ 方法與欄位關聯"""
    cat = Category.objects.create(category="娛樂")
    
    rec = Record.objects.create(
        date=date(2025, 8, 24),
        description="電影票",
        category=cat,
        cash=300,
        balance_type="支出"
    )

    # __str__ 方法
    assert str(rec) == "收支描述：電影票"
    
    # 欄位值測試
    assert rec.category == cat
    assert rec.cash == 300
    assert rec.balance_type == "支出"
    assert rec.date == date(2025, 8, 24)

def test_record_category_nullable():
    """測試 category 可為空"""
    rec = Record.objects.create(
        date=date.today(),
        description="其他費用",
        category=None,
        cash=100,
        balance_type="支出"
    )
    assert rec.category is None

'''
測試範例：

@pytest.mark.django_db
def test_model_str():
    obj = Record.objects.create(...)  # 填寫必要欄位
    assert str(obj) == "你預期的名稱"
'''
