from django.contrib import admin
from .models import Course, Lesson, Subscription, Payment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'description')
    search_fields = ('title', 'description')
    list_filter = ('owner',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'owner')
    search_fields = ('title', 'description')
    list_filter = ('course', 'owner')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
    list_filter = ('user', 'course')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'paid', 'created_at')
    list_filter = ('paid', 'created_at')
