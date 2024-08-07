"""定義 database schema"""

from django.db import models
from django.db.models import CharField, DateField, ForeignKey, IntegerField

# Create your models here.
BALANCE_TYPE = (('收入', '收入'), ('支出', '支出'))	#元組 tuple：可以視為不可改變的串列 ((key,value),(key,value))

class Category(models.Model):
    """定義收支類別"""
    category = CharField(max_length=20)

    def __str__(self):
        return F'{self.category}'

class Record(models.Model):
    """定義收支記錄的欄位"""
    date = DateField()
    description = CharField(max_length=300)
    # 外來鍵是一個(或數個)指向另外一個表格主鍵的欄位。
    category = ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    cash = IntegerField()
    # 收/支 choices 只有兩種，已定義在上方的 BALANCE_TYPE
    balance_type = CharField(max_length=2, choices=BALANCE_TYPE)

    def __str__(self):
        return F'收支描述：{self.description}'
