from django_filters import rest_framework as filters
from rest_framework import generics
from .models import Payment
from .serializers import PaymentSerializer


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
