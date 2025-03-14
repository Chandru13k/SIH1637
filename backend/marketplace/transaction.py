from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from .models import Transaction,Order,Payment
from .serializers import TransactionSerializer,OrderSerializer,PaymentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from database.models import Transaction, Listings, Order, Payment
from .serializers import TransactionSerializer, OrderSerializer, PaymentSerializer
from django.core.exceptions import PermissionDenied
from django.utils.timezone import now

class TransactionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(buyer=self.request.user)  # Show transactions for the logged-in user


class TransactionCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        listing_id = self.request.data.get("listing")
        listing = get_object_or_404(Listings, id=listing_id)
        if listing.seller == self.request.user:
            raise PermissionDenied("You cannot purchase your own listing.")
        transaction = serializer.save(buyer=self.request.user, seller=listing.seller, listing=listing, status="Pending")
        return JsonResponse({"message": "Transaction created successfully", "transaction_id": transaction.id})


class TransactionDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(buyer=self.request.user)  # Ensure user can only see their transactions


class TransactionUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_queryset(self):
        return Transaction.objects.filter(seller=self.request.user)  # Seller can update the transaction status

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return JsonResponse({"message": "Transaction updated successfully", "data": response.data})


# Order Views
class OrderListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)  # Show orders for the logged-in user


class OrderCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user, status="Pending")
        return JsonResponse({"message": "Order created successfully", "order_id": order.id})


class OrderDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)  # Ensure user can only see their orders


class OrderUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)  # User can update their order status

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return JsonResponse({"message": "Order updated successfully", "data": response.data})


class OrderCancelView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status="Pending")

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        order.status = "Cancelled"
        order.save()
        return JsonResponse({"message": "Order cancelled successfully", "order_id": order.id})


# Payment Views
class PaymentCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        transaction_id = self.request.data.get("transaction")
        transaction = get_object_or_404(Transaction, id=transaction_id)
        if transaction.buyer != self.request.user:
            raise PermissionDenied("You can only make payments for your own transactions.")
        if transaction.status == "Paid":
            return JsonResponse({"message": "Transaction is already paid."}, status=400)
        
        payment = serializer.save(user=self.request.user, transaction=transaction, status="Completed", timestamp=now())
        transaction.status = "Paid"
        transaction.save()
        
        order = Order.objects.filter(transaction=transaction).first()
        if order:
            order.status = "Paid"
            order.save()
        
        return JsonResponse({"message": "Payment processed successfully", "payment_id": payment.id})


class PaymentDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)





#class TransactionView(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
#    # permission_classes = [IsAuthenticated]
#    # authentication_classes = [JWTAuthentication]
#    queryset = Transaction.objects.all()
#    serializer_class = TransactionSerializer
#
#    def post(self, request, *args, **kwargs):
#        return self.create(request, *args, **kwargs)
# #   
#    def get(self, request, *args, **kwargs):
 #       return self.retrieve(request, *args, **kwargs)
    
#    def put(self, request, *args, **kwargs):
#        return self.update(request, *args, **kwargs)
#    
#    def delete(self, request, *args, **kwargs):
 #       return self.destroy(request, *args, **kwargs)
 #   
#    def get_queryset(self):
 #       return Transaction.objects.filter(user=self.request.user)
    

#class OrderView(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
#    queryset = Order.objects.all()
#    serializer_class = OrderSerializer
#
#    def post(self, request, *args, **kwargs):
 #       return self.create(request, *args, **kwargs)
    
 #   def get(self, request, *args, **kwargs):
  #      return self.retrieve(request, *args, **kwargs)
    
  #  def put(self, request, *args, **kwargs):
  #      return self.update(request, *args, **kwargs)
 #   
  #  def delete(self, request, *args, **kwargs):
 #       return self.destroy(request, *args, **kwargs)

#class PaymentView(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
 #   # permission_classes = [IsAuthenticated]
#    # authentication_classes = [JWTAuthentication]
 #   queryset = Payment.objects.all()
 #   serializer_class = PaymentSerializer

 #   def post(self, request, *args, **kwargs):
  #      return self.create(request, *args, **kwargs)
    
 #   def get(self, request, *args, **kwargs):
 #       return self.retrieve(request, *args, **kwargs)
#    
 #   def put(self, request, *args, **kwargs):
 #       return self.update(request, *args, **kwargs)
    
 #   def delete(self, request, *args, **kwargs):
  #      return self.destroy(request, *args, **kwargs)*/