from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Account
from .serializers import LoginSerializer, AccountSerializer


class LoginAPI(generics.GenericAPIView):
    def get_queryset(self):
        return Account.objects.all()

    def get_serializer_class(self):
        return LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        pas = request.data['password']
        print(username)
        print(pas)
        true_phone = '+'
        for i in str(username):
            if i.isalnum():
                true_phone = true_phone + i
        user = Account.objects.filter(username=username, password=pas).first()
        if not user:
            return Response({'message': 'Bunaqa user yogu nima qilamiza endi'}, status=status.HTTP_404_NOT_FOUND)
        if user.check_password(pas):
            return Response({'message': 'Parolingni tori kiritgin'}, status=400)
        token = Token.objects.get_or_create(user=user)
        data = dict()
        data['token'] = str(token)
        data['success'] = True
        data['role'] = user.role
        return Response(data, status=status.HTTP_200_OK)


class WorkersList(generics.ListAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = Account.objects.filter(is_staff=True)
        return queryset
