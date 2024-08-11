import stripe
from rest_framework import viewsets, generics, views, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Subscription, Payment
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModerator, IsOwner
from .paginators import CustomPagination
from .services import create_stripe_product, create_stripe_price, create_stripe_checkout_session
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class SubscriptionView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message})


class SubscriptionListView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        # Создание продукта в Stripe
        product_id = create_stripe_product(course.title, course.description)

        # Создание цены в Stripe (цена умножается на 100, т.к. Stripe работает с ценами в центах)
        price_id = create_stripe_price(product_id, int(course.price * 100))

        # Создание сессии оплаты в Stripe
        success_url = request.build_absolute_uri('/payment-success/')
        cancel_url = request.build_absolute_uri('/payment-cancel/')
        session_id, session_url = create_stripe_checkout_session(price_id, success_url, cancel_url)

        # Сохранение информации о платеже в базе данных
        payment = Payment.objects.create(
            user=user,
            course=course,
            stripe_product_id=product_id,
            stripe_price_id=price_id,
            stripe_checkout_session_id=session_id,
            paid=False
        )

        return Response({"session_url": session_url}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        """ Обработка успешной оплаты """
        session_id = request.query_params.get('session_id')
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == 'paid':
            payment = get_object_or_404(Payment, stripe_checkout_session_id=session_id)
            payment.paid = True
            payment.save()

            return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Payment not successful"}, status=status.HTTP_400_BAD_REQUEST)


class PaymentSuccessView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Payment was successful!"}, status=status.HTTP_200_OK)


class PaymentCancelView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Payment was cancelled."}, status=status.HTTP_200_OK)
