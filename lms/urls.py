from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    LessonListCreateAPIView,
    LessonRetrieveUpdateDestroyAPIView,
    SubscriptionView,
    LessonViewSet,
    PaymentView,  # Новый импорт для обработки платежей
    PaymentSuccessView,  # Для успешной оплаты
    PaymentCancelView,  # Для отмененной оплаты
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),
    path('subscriptions/', SubscriptionView.as_view(), name='subscriptions'),
    path('payment/', PaymentView.as_view(), name='payment'),  # Новый маршрут для обработки платежей
    path('payment-success/', PaymentSuccessView.as_view(), name='payment-success'),  # Маршрут для успешной оплаты
    path('payment-cancel/', PaymentCancelView.as_view(), name='payment-cancel'),  # Маршрут для отмененной оплаты
]
