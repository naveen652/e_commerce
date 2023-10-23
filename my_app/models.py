from django.db import models

class userProfiles(models.Model):
    userId=models.IntegerField(default=0)
    userName=models.CharField(max_length=15)
    phoneNumber=models.CharField(max_length=10)
    email=models.CharField(max_length=20)
    def __str__(self):
        return f"{self.userId}"

class categories(models.Model):
    categoryId=models.IntegerField(default=0)
    categoryName=models.CharField(max_length=15)
    def __str__(self):
        return f"{self.categoryName}"

class products(models.Model):
    categoryId = models.ForeignKey(categories, on_delete=models.CASCADE)
    productId=models.IntegerField(default=0)
    productName=models.CharField(max_length=15)
    price=models.IntegerField()
    def __str__(self):
        return f"{self.productName}"

class orders(models.Model):
    userId = models.ForeignKey(userProfiles, on_delete=models.CASCADE)
    productName = models.CharField(max_length=15)
    orderId=models.IntegerField()
    total=models.IntegerField(default=0)
