from django_filters import rest_framework as filters
from rest_framework import generics, permissions, parsers
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class PaymentFilter(filters.FilterSet):
    course = filters.NumberFilter(field_name="course__id")
    lesson = filters.NumberFilter(field_name="lesson__id")
    payment_method = filters.ChoiceFilter(choices=Payment.PAYMENT_METHODS)
    order_by = filters.OrderingFilter(fields=('date',))

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method']


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PaymentFilter
    permission_classes = [IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
