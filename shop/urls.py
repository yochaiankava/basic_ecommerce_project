from django.urls import path
from shop import views


urlpatterns = [
   path('', views.products, name='all_products'),
   path('update_products_stock/', views.update_products_stock, name='update_products_stock'),
   path('view_purchase_cart/', views.view_purchase_cart, name='view_purchase_cart'),
   path('add/<int:product_id>', views.add_to_cart, name='add_to_cart'),
   # path('<int:product_id>', views.single_product, name='single_product'),
   path("login/", views.login_page, name="login_page"),
   path("login_user/", views.login_user, name="login_user"),
   path('logout/', views.logout_user, name='logout'),
   path("register/", views.user_register, name="user_register"),
   path("create_cart/", views.create_purchase_card, name="create_purchase_card"),
   path('delete_product/<int:product_id>/', views.delete_product_from_cart, name='delete_product_from_cart'),
   path("get_purchases_cart_history/>", views.get_purchases_cart_history, name="get_purchases_cart_history"),
   path('view_cart_details/<int:cart_id>/', views.view_cart_details, name='view_cart_details'),
   
  ]

