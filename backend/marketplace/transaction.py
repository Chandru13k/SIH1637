from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.authentication import JWTAuthentication
from database.models import Transaction, Listings,Order,Payment
from .serializers import TransactionSerializer,OrderSerializer,PaymentSerializer
from django.utils.timezone import now

class TransactionView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, transaction_id=None):
        """Retrieve a single transaction or list all transactions for the logged-in user."""
        if transaction_id:
            transaction = get_object_or_404(Transaction, id=transaction_id, buyer=request.user)
            serializer = TransactionSerializer(transaction)
        else:
            transactions = Transaction.objects.filter(buyer=request.user)
            serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        """Create a new transaction."""
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            listing_id = request.data.get("listing")
            listing = get_object_or_404(Listings, id=listing_id)

            if listing.seller == request.user:
                raise PermissionDenied("You cannot purchase your own listing.")

            transaction = serializer.save(buyer=request.user, seller=listing.seller, listing=listing, status="Pending")
            return JsonResponse({"message": "Transaction created successfully", "transaction_id": transaction.id}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, transaction_id):
        """Update a transaction status (only by the seller)."""
        transaction = get_object_or_404(Transaction, id=transaction_id, seller=request.user)
        serializer = TransactionSerializer(transaction, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Transaction updated successfully", "data": serializer.data}, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, order_id=None):
        """Retrieve a single order or list all orders for the logged-in user."""
        if order_id:
            order = get_object_or_404(Order, id=order_id, user=request.user)
            serializer = OrderSerializer(order)
        else:
            orders = Order.objects.filter(user=request.user)
            serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        """Create a new order."""
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(user=request.user, status="Pending")
            return JsonResponse({"message": "Order created successfully", "order_id": order.id}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, order_id):
        """Update an order (only by the user who placed it)."""
        order = get_object_or_404(Order, id=order_id, user=request.user)
        serializer = OrderSerializer(order, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Order updated successfully", "data": serializer.data}, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        """Cancel an order (only if it's still pending)."""
        order = get_object_or_404(Order, id=order_id, user=request.user, status="Pending")
        order.status = "Cancelled"
        order.save()
        return JsonResponse({"message": "Order cancelled successfully", "order_id": order.id}, status=HTTP_200_OK)



class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, payment_id=None):
        """Retrieve a single payment or list all payments made by the user."""
        if payment_id:
            payment = get_object_or_404(Payment, id=payment_id, user=request.user)
            serializer = PaymentSerializer(payment)
        else:
            payments = Payment.objects.filter(user=request.user)
            serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        """Process a new payment for a transaction."""
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            transaction_id = request.data.get("transaction")
            transaction = get_object_or_404(Transaction, id=transaction_id)

            if transaction.buyer != request.user:
                raise PermissionDenied("You can only make payments for your own transactions.")
            if transaction.status == "Paid":
                return JsonResponse({"message": "Transaction is already paid."}, status=HTTP_400_BAD_REQUEST)

            payment = serializer.save(user=request.user, transaction=transaction, status="Completed", timestamp=now())
            transaction.status = "Paid"
            transaction.save()

            order = Order.objects.filter(transaction=transaction).first()
            if order:
                order.status = "Paid"
                order.save()

            return JsonResponse({"message": "Payment processed successfully", "payment_id": payment.id}, status=HTTP_201_CREATED)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)






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