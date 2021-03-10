import uuid

from django.db import models
from django.utils import timezone

# Create your models here.
class Item(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=10)
    status = models.CharField(default='', max_length=20)
    note = models.CharField(default='', max_length=100)
    created_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
            self.code = uuid.uuid4().hex[:6].upper()
        return super(Item, self).save(*args, **kwargs)

    def get_category(self):
        return ItemCategory.objects.get(item=self).category

    def get_active():
        return Item.objects.filter(status='active')


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=10)
    created_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
            self.code = uuid.uuid4().hex[:6].upper()
        return super(Category, self).save(*args, **kwargs)

    def get_items(self, status='active', search_param=None):
        item_categoies = ItemCategory.objects.filter(category=self, item__status=status)
        items = None
        for ic in item_categoies:
            items.append(ic.item)
        return Item.objects.filter(item__in=items)


class ItemCategory(models.Model):
    item = models.ForeignKey('app_inventory.Item', on_delete=models.CASCADE)
    category = models.ForeignKey('app_inventory.Category', on_delete=models.CASCADE)
    created_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
            self.code = uuid.uuid4().hex[:6].upper()
        return super(ItemCategory, self).save(*args, **kwargs)


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=10)
    created_date = models.DateTimeField()
    estimated_arrival_date = models.DateTimeField(blank=True, default=None)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
            self.code = uuid.uuid4().hex[:6].upper()
        return super(Order, self).save(*args, **kwargs)

    def get_items(self):
        return ItemOrder.objects.filter(order=self)

    def get_statuses(self):
        return OrderStatusUpdate.objects.filter(order=self)
    
    def get_status(self, status='current'):
        if status == 'current':
            return OrderStatusUpdate.objects.filter(order=self).order_by('-created_date')[0]
        else:
            return OrderStatusUpdate.objects.get(order=self, status=status)
        return None


class OrderStatusUpdate(models.Model):
    order = models.ForeignKey('app_inventory.Order', on_delete=models.CASCADE)
    status = models.CharField(default='', max_length=20)
    note = models.CharField(max_length=100)
    created_date = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
            self.code = uuid.uuid4().hex[:6].upper()
        return super(OrderStatusUpdate, self).save(*args, **kwargs)


class ItemOrder(models.Model):
    item = models.ForeignKey('app_inventory.Item', on_delete=models.CASCADE)
    order = models.ForeignKey('app_inventory.Order', on_delete=models.CASCADE)
    created_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
            self.code = uuid.uuid4().hex[:6].upper()
        return super(ItemOrder, self).save(*args, **kwargs)


class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
    status = models.CharField(default='', max_length=20)
    customer = models.ForeignKey('app_inventory.Customer', on_delete=models.CASCADE)
    payment_method = models.ForeignKey('app_inventory.PaymentMethod', on_delete=models.CASCADE)
    delivery_method = models.CharField(max_length=100)
    created_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
            self.code = uuid.uuid4().hex[:6].upper()
        return super(Transaction, self).save(*args, **kwargs)

    def get_items(self):
        return 


class PaymentMethod(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
            self.code = uuid.uuid4().hex[:6].upper()
        return super(PaymentMethod, self).save(*args, **kwargs)


class ItemTransaction(models.Model):
    item = models.ForeignKey('app_inventory.Item', on_delete=models.CASCADE)
    Transaction = models.ForeignKey('app_inventory.Transaction', on_delete=models.CASCADE)
    created_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
            self.code = uuid.uuid4().hex[:6].upper()
        return super(ItemOrder, self).save(*args, **kwargs)


class Customer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=10)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(null=True)
    contact_number = models.CharField(max_length=12)
    created_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
            self.code = uuid.uuid4().hex[:6].upper()
        return super(Customer, self).save(*args, **kwargs)
