from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import Order
from rest_framework import authentication, permissions
from payment.payme import client, client_receipt


class CardCreate(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        number = self.request.data.get('number')
        expire = self.request.data.get('expire')
        save = True
        res = client.cards_create(number=number, expire=expire, save=save)
        print(res)
        try:
            token = res['result']['card']['token']
        except:
            return Response({'message': 'Invalid information'}, status=status.HTTP_400_BAD_REQUEST)
        resp = client.card_get_verify_code(token)
        print(resp)
        return Response({'message': 'Verification code has sent', 'token': token}, status=status.HTTP_200_OK)


class CardVerify(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        verify_code = self.request.data.get('verify_code')
        token = self.request.data.get('token')
        res = client.cards_verify(verify_code, token)
        print(res)
        try:
            token = res['result']['card']['token']
        except:
            return Response({'message': 'Invalid information'}, status=status.HTTP_404_NOT_FOUND)
        check = client.cards_check(token)
        return Response(str(check), status=status.HTTP_200_OK)


class ReceiptCreate(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        amount = self.request.data.get('amount')
        order = Order.objects.create(
            client_id=self.request.user.id,
            amount=amount
        )
        order.save()
        if not order:
            return Response({'message': 'Invalid Order'})
        token = self.request.data.get('token')
        phone = self.request.user.phone
        res = client_receipt._receipts_create(123, amount, f'{order.id}', title='Gaz prom',
                                              code='21331213',
                                              package_code='123456', price=amount)
        print(res)
        try:
            invoice_id = res['result']['receipt']['_id']
            print("invoice" + invoice_id)
        except:
            return Response({'message': 'Invalid information'}, status=status.HTTP_404_NOT_FOUND)
        try:
            pay = client_receipt._receipts_pay(123, invoice_id, token, phone)
            print(pay)
            order.is_paid = True
            order.save()
        except:
            return Response({'message': 'Invalid information'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

