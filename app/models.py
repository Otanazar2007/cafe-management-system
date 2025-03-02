import json

from django.db import models
from django.http import JsonResponse


# Create your models here.
class Order(models.Model):
    ORDER_COICE = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено')
    ]
    table_number = models.IntegerField(verbose_name='Номер стола')
    items = models.TextField(verbose_name='Список блюд')
    total_price = models.DecimalField(verbose_name='Общая стоимость', max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(verbose_name='Статус', max_length=10, choices=ORDER_COICE, default='pending')

    def save(self, *args, **kwargs):
        if isinstance(self.items, list):
            self.items = json.dumps(self.items, ensure_ascii=False)
        super().save(*args, **kwargs)

    def get_items_list(self):
        return json.loads(self.items)

    def __str__(self):
        return f'{self.table_number} стол, статус {self.status}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'