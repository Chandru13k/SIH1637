from django.urls import path
from .views import *
from .transaction import TransactionView, OrderView, PaymentView


urlpatterns = [
    
  
    path("produces/", ProduceListView.as_view(), name="produce-list"),
    path("produces/<str:pk>/", ProduceView.as_view(), name="produce-detail"),

  
    path("marketprices/", MarketPriceListView.as_view(), name="market-price-list"),
    path("marketprices/<str:pk>/", MarketPriceView.as_view(), name="market-price"),
   
    path("locations/", LocationListView.as_view(), name="market-locations"),

 
    path("listings/", ListingListView.as_view(), name="all-listings"),  # All listings
    path("listings/<uuid:listing_id>/", ListingView.as_view(), name="listing-detail"),  # Retrieve individual listing
    # path("listings/<uuid:listing_id>/update/", ListingUpdateView.as_view(), name="listing-update"),  # Update a listing
    # path("listings/<uuid:listing_id>/delete/", ListingDeleteView.as_view(), name="listing-delete"),  # Delete a listing

  
    path("listings/mylistings/<str:pk>/",MyListingView.as_view(), name="seller-listings"),
    path("listings/mylistings/",MyListingView.as_view(), name="seller-listings"),

    path("upload", upload.as_view(), name="user-listings"),

    # Transactions
    path("transactions/", TransactionView.as_view(), name="transaction-list"),
    path("transactions/<int:transaction_id>/", TransactionView.as_view(), name="transaction-detail"),

    # Orders
    path("orders/", OrderView.as_view(), name="order-list"),
    path("orders/<int:order_id>/", OrderView.as_view(), name="order-detail"),
    
    # Payments
    path("payments/", PaymentView.as_view(), name="payment-list"),
    path("payments/<int:payment_id>/", PaymentView.as_view(), name="payment-detail"),




]
