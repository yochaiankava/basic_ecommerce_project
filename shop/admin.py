# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from .models import MyUser
from .models import Product
from .models import Category
from .models import PurchaseCard
from .models import PurchaseLine

admin.site.register(MyUser)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(PurchaseCard)
admin.site.register(PurchaseLine)
