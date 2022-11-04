import json


class Transaction:
    def __init__(self, transaction_data: dict):
        self.transaction_data: dict = transaction_data
        self.sender_signature: bytes = None

    def toJson(self):
        json_obj = json.dumps(
            {
                "transaction_data": self.transaction_data,
                "sender_signature": self.sender_signature.hex(),
            }
        )
        return json_obj


