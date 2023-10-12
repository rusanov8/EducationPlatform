from django.urls import path
from payments.apps import PaymentsConfig
from payments.views import PaymentListApiView, payment_create, check_payment_status

app_name = PaymentsConfig.name


urlpatterns = [
    path('payments/', PaymentListApiView.as_view(), name='payment-list'),
    path('courses/<int:pk>/payment', payment_create, name='payment'),
    path('payments/check_payment_status/<str:session_id>/', check_payment_status, name='payment-status')

]

