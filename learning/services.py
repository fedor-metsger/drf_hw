
import requests

from learning.models import Course, Product, Price, Link, Intent

STRIPE_USERNAME="sk_test_4eC39HqLyjWDarjtT1zdp7dc"

def get_or_create_product(course_id):

    if Product.objects.filter(course_id=course_id).exists():
        prod = Product.objects.filter(course_id=course_id).get()
        return prod.pk, prod.prod_id

    course = Course.objects.filter(pk=course_id).get()
    session = requests.Session()
    session.auth = (STRIPE_USERNAME, "")
    response = session.post(
        "https://api.stripe.com/v1/products",
        headers={"Authorization": "Basic c2tfdGVzdF80ZUMzOUhxTHlqV0Rhcmp0VDF6ZHA3ZGM6"},
        data={"name": f'Course "{course.title}"'}
    )
    if response.status_code == 200:
        prod_id = response.json()["id"]
        prod = Product(course_id=course_id, prod_id=prod_id)
        prod.save()
        return prod.pk, prod.prod_id
    else:
        return None, response.status_code


def get_or_create_price(product_id, amount):

    if Price.objects.filter(product_id=product_id).exists():
        price = Price.objects.filter(product_id=product_id).get()
        return price.pk, price.price_id

    product = Product.objects.filter(pk=product_id).get()
    session = requests.Session()
    session.auth = (STRIPE_USERNAME, "")
    response = session.post(
        "https://api.stripe.com/v1/prices",
        headers={"Authorization": "Basic c2tfdGVzdF80ZUMzOUhxTHlqV0Rhcmp0VDF6ZHA3ZGM6"},
        data={
            "unit_amount": amount,
            "currency": "rub",
            "product": product.prod_id
        }
    )
    if response.status_code == 200:
        price_id = response.json()["id"]
        price = Price(product_id=product_id, price_id=price_id, amount=amount)
        price.save()
        return price.pk, price.price_id

    return None, response.status_code

def get_or_create_payment_link(price_id, user_id):

    if Link.objects.filter(price_id=price_id, user_id=user_id).exists():
        link = Link.objects.filter(price_id=price_id, user_id=user_id).get()
        return link.pk, link.link_id, link.url

    price = Price.objects.filter(pk=price_id).get()
    session = requests.Session()
    session.auth = (STRIPE_USERNAME, "")
    response = session.post(
        "https://api.stripe.com/v1/payment_links",
        headers={"Authorization": "Basic c2tfdGVzdF80ZUMzOUhxTHlqV0Rhcmp0VDF6ZHA3ZGM6"},
        data={
            "line_items[0][price]": price.price_id,
            "line_items[0][quantity]": 1
        }
    )
    if response.status_code == 200:
        link = Link(price_id=price_id,
                    user_id=user_id,
                    link_id=response.json()["id"],
                    url=response.json()["url"])
        link.save()
        return link.pk, link.link_id, link.url

    return None, response.status_code, None

def get_or_create_pi(course_id, user_id, amount):

    if Intent.objects.filter(course_id=course_id, user_id=user_id).exists():
        pi = Intent.objects.filter(course_id=course_id, user_id=user_id).get()
        return pi.pk, pi.pi_id

    session = requests.Session()
    session.auth = (STRIPE_USERNAME, "")
    response = session.post(
        "https://api.stripe.com/v1/payment_intents",
        headers={"Authorization": "Basic c2tfdGVzdF80ZUMzOUhxTHlqV0Rhcmp0VDF6ZHA3ZGM6"},
        data={
            "amount": amount,
            "currency": "rub",
            "payment_method_types[]": "card"
        }
    )
    if response.status_code == 200:
        pi_id = response.json()["id"]
        secret = response.json()["client_secret"]
        pi = Intent(
            course_id=course_id,
            user_id=user_id,
            pi_id=pi_id,
            secret=secret,
            amount=amount
        )
        pi.save()
        return pi.pk, pi.pi_id
    else:
        return None, response.status_code

def retrieve_pi(pi_id):

    session = requests.Session()
    session.auth = (STRIPE_USERNAME, "")
    response = session.post(
        f'https://api.stripe.com/v1/payment_intents/{pi_id}',
        headers={"Authorization": "Basic c2tfdGVzdF80ZUMzOUhxTHlqV0Rhcmp0VDF6ZHA3ZGM6"},
    )
    if response.status_code == 200:
        pi_id = response.json()["id"]
        pi_status = response.json()["status"]
        return pi_id, pi_status
    else:
        return None, response.status_code