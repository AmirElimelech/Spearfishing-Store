from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200 , null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name
    
    @property #this method should prevent django from crashing if no image was found for the product 
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url







class Order(models.Model):
    customer = models.ForeignKey(Customer ,on_delete=models.SET_NULL , null=True , blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete  = models.BooleanField(default=False)
    transacion_id =models.CharField(max_length=100 , null=True)
    

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        total = 0
        orderitems = self.orderitem_set.all() #to get all order items that belong to the specific cart
        for item in orderitems: # with this loop i add to the total each item price and count them so i can get a sum for all items in the cart 
            total += item.get_total
        return total
    
    @property
    def get_cart_items(self):
        total = 0
        orderitems = self.orderitem_set.all() #to get all order items that belong to the specific cart
        for item in orderitems: # with this loop i add to the total each item and count them so i can get a sum for all items
            total += item.quantity
        return total
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product , on_delete=models.SET_NULL , null=True)
    order = models.ForeignKey(Order , on_delete=models.SET_NULL ,null=True)
    quantity = models.IntegerField(default=0 , null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    

    
class SippingAddress(models.Model):
    customer = models.ForeignKey(Customer , on_delete= models.SET_NULL,null=True)
    order = models.ForeignKey(Order , on_delete=models.SET_NULL , null=True)
    address = models.CharField(max_length=200 , null=True)
    city = models.CharField(max_length=200 , null=True)
    zipcode = models.CharField(max_length=200 , null=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.address


'''
Customer model:
user: One-to-one relationship with the built-in User model provided by Django. 
One Customer can have at most one associated User, and each User can be associated
 with at most one Customer.


Product model:
No relationships with other models.

Order model:
customer: Many-to-one relationship with the Customer model. Each Order can be 
associated with at most one Customer, but a Customer can be associated with many orders.
orderitem_set: Related manager to access the related OrderItem objects. Many-to-one 
relationship with the Order model. Each OrderItem can be associated with at most one 
Order, but an Order can have many OrderItems.

OrderItem model:
product: Many-to-one relationship with the Product model. Each OrderItem can be 
associated with at most one Product, but a Product can be associated with many OrderItems.
order: Many-to-one relationship with the Order model. Each OrderItem can be associated with
 at most one Order, but an Order can have many OrderItems.

ShippingAddress model:
customer: Many-to-one relationship with the Customer model. Each ShippingAddress can 
be associated with at most one Customer, but a Customer can be associated with many
ShippingAddresses.
order: Many-to-one relationship with the Order model. Each ShippingAddress can be 
associated with at most one Order, but an Order can have many ShippingAddresses.
'''