import stripe
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from payments.models import Payment
from payments.serializers import PaymentSerializer
from payments.services import create_stripe_session, get_payment_data

from education.models import Course


# Create your views here.
class PaymentListApiView(generics.ListAPIView):
    """
    Retrieve a list of payments.

    This view allows users to retrieve a list of payments. It supports ordering and filtering by course and payment method.
    - Admin users can view all payments.
    - Authenticated users can view their own payments.
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date', ]
    filterset_fields = ['course', 'payment_method']

    def get_permissions(self):
        if self.request.user.is_staff:
            permission_classes = [IsAuthenticated]
        elif self.request.user.is_authenticated:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment_create(request, course_id):
    """
       Create a new payment session for the specified course.

       This view allows authenticated users to create a new payment session for a specific course. It generates a payment session
       with a Stripe link and returns the session ID and payment link.
       """

    course = Course.objects.get(pk=course_id)

    session = create_stripe_session(course)

    request.session['course_id'] = course_id

    return Response({'session_id': session.id, 'payment_link': session.url})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_payment_status(request, session_id):
    """
        Check the payment status for a given session.

        This view allows authenticated users to check the payment status for a specific session. It retrieves the payment data from Stripe
        using the session ID, and if the payment is successful, it records the payment in the database.
        """

    course = Course.objects.get(pk=request.session.get('course_id'))

    if course is None:
        return Response({'detail': 'Идентификатор курса отсутствует в сессии'}, status=400)

    try:
        payment_data = get_payment_data(session_id)

        if payment_data.status == 'succeeded':
            new_payment = Payment.objects.create(
                user=request.user,
                course=course,
                amount=payment_data.amount / 100,
                payment_method='transfer',
            )
            return Response({'detail': 'Платеж прошел успешно'})

        return Response({'detail': 'Ошибка платежа'})

    except stripe.error.StripeError as e:
        return Response({'detail': f'Ошибка Stripe: {str(e)}'})
