import stripe
from config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(course):
    """
       Create a Stripe payment session for the specified course.
       """

    product = stripe.Product.create(
        name=course.title
    )

    price = stripe.Price.create(
        unit_amount=int(course.price * 100),
        currency="rub",
        product=product.id
    )

    session = stripe.checkout.Session.create(
        success_url=f"http://127.0.0.1:8000/courses/{course.id}",
        line_items=[
            {
                "price": price.id,
                "quantity": 2,
            },
        ],
        mode="payment",
    )

    return session


def get_payment_data(session_id):
    """
        Retrieve payment data for a Stripe session.
        """

    session = stripe.checkout.Session.retrieve(
        session_id,
    )

    payment_id = session.payment_intent

    payment_data = stripe.PaymentIntent.retrieve(
             payment_id
        )

    return payment_data


