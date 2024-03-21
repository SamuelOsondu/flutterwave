import uuid

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import generate_referral_code
from fondstack import settings


@api_view(['GET'])
def list_banks(request):
    url = "https://api.paystack.co/bank"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SEC_KEY}"
    }

    params = {
        "country": "nigeria",
        "use_cursor": True,
        "perPage": 100,
    }

    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        return Response(response_data)

    except requests.exceptions.RequestException as err:
        return Response({"error": str(err)}, status=500)


@api_view(['GET'])
def resolve_account(request):
    url = "https://api.paystack.co/bank/resolve"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SEC_KEY}"
    }

    account_number = request.query_params.get("account_number")
    bank_code = request.query_params.get("bank_code")

    params = {
        "bank_code": bank_code,
        "account_number": account_number,
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response_data = response.json()
        return Response(response_data)

    except requests.exceptions.RequestException as err:
        return Response({"error": str(err)}, status=500)


@api_view(['POST'])
def create_recipient(request):
    url = "https://api.paystack.co/transferrecipient"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SEC_KEY}"
    }

    name = request.data.get("name")
    account_number = request.data.get("account_number")
    bank_code = request.data.get("bank_code")

    data = {
        "type": "nuban",
        "name": name,
        "account_number": account_number,
        "bank_code": bank_code,
        "currency": "NGN"
            }

    try:
        response = requests.post(url, data=data, headers=headers)
        response_data = response.json()
        return Response(response_data)

    except requests.exceptions.RequestException as err:
        return Response({"error": str(err)}, status=500)

@api_view(['POST'])
def initiate_withdrawal(request):
    url = "https://api.paystack.co/transfer"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SEC_KEY}"
    }

    amount = request.data.get("amount")
    recipient = request.data.get("recipient")

    # I need to first verify if the user has the enough amount he is planning to withdraw

    data = {
        "amount": str(amount),
        "source": "balance",
        "reference": generate_referral_code(length=9),
        "reason": "Withdrawal",
        "recipient": recipient,
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        return Response(response_data)

    except requests.exceptions.RequestException as err:
        return Response({"error": str(err)}, status=500)
