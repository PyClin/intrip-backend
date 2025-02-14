import json
import traceback

import requests
from django.conf import settings
from rest_framework.status import is_success


class GGConstants:
    EMPLOYER = "EMPLOYER"
    STAFF = "STAFF"
    EMPLOYEE = "EMPLOYEE"
    PUBLIC = "PUBLIC"

    @staticmethod
    def get_gg_constant(user_type):
        if user_type == "employer":
            return GGConstants.EMPLOYER
        if user_type == "employee":
            return GGConstants.EMPLOYEE
        if user_type == "staff":
            return GGConstants.STAFF
        return GGConstants.PUBLIC


class GGHelper:
    def create_wallet(self, wallet_id, user_type):
        user_type = GGConstants.get_gg_constant(user_type)
        data = {
            "wallet_id": wallet_id,
            "type": user_type
        }
        url = f"{settings.GG_CONF['url']}/api/wallet"
        headers = {
            "Content-Type": "application/json"
        }
        for i in range(5):
            try:
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=15)
                if is_success(response.status_code):
                    print(f"Response from gg: {response.content}")
                    break
                print(f"Call to GG failed. Trying again")
            except Exception:
                print(traceback.format_exc())

    def deposit(self, wallet_id, amount):
        url = f"{settings.GG_CONF['url']}/api/wallet/deposit"
        data = {
            "wallet_id": wallet_id,
            "amount": amount
        }
        headers = {
            "Content-Type": "application/json"
        }
        for i in range(5):
            try:
                print(f"data={data}")
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=15)
                if is_success(response.status_code):
                    print(f"Response from gg: {response.content}")
                    break
                print(f"Call to GG failed. Trying again")
            except Exception:
                print(traceback.format_exc())


    def wallet_balance(self, wallet_id):
        url = f"{settings.GG_CONF['url']}/api/wallet/balance?wallet_id={str(wallet_id)}"

        for i in range(5):
            try:
                response = requests.get(url, timeout=15)
                if is_success(response.status_code):
                    print(f"Response from gg: {response.content}")
                    content = response.json()
                    return content["balance"]
                print(f"Call to GG failed. Trying again")
            except Exception:
                print(traceback.format_exc())

    def create_transaction(self, from_wallet_id, to_wallet_id, amount, memo, employer_wallet_id=None):
        url = f"{settings.GG_CONF['url']}/api/transaction"
        data = {
            "from_wallet_id": int(from_wallet_id),
            "to_wallet_id": int(to_wallet_id),
            "amount": str(amount),
            "memo": memo,
        }
        if employer_wallet_id:
            data["employer"] = int(employer_wallet_id)

        headers = {
            "Content-Type": "application/json"
        }

        for i in range(5):
            try:
                print(f"data={data}")
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=15)
                if is_success(response.status_code):
                    print(f"Response from gg: {response.content}")
                    content = response.json()
                    txn_hash = content["txn_hash"]
                    return txn_hash
                print(f"Call to GG failed. Trying again")
            except Exception:
                print(traceback.format_exc())
            return ""


    def employee_claim(self, wallet_id, hashes):
        url = f"{settings.GG_CONF['url']}/api/wallet/claim"
        data = {
            "wallet_id": int(wallet_id),
            "txn_hashs": hashes
        }

        headers = {
            "Content-Type": "application/json"
        }

        for i in range(5):
            try:
                print(f"data={data}")
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=15)
                if is_success(response.status_code):
                    print(f"Response from gg: {response.content}")
                    content = response.json()
                    amount = content["amount"]
                    return amount
                print(f"Call to GG failed. Trying again")
            except Exception:
                print(traceback.format_exc())
            return ""