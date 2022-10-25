class StubUserReview:
    def __init__(self, stub_payload):
        self.stub_payload = stub_payload

    def dict(self):
        return self.stub_payload


payload_foreign_none = stub_payload_missing_data = {
    "personal": {"tax_residences": None}
}

payload_foreign_missing_value = {
    "personal": {"tax_residences": {"anything": "anything"}}
}

payload_foreign_missing_contry = {
    "personal": {
        "nationality": {"value": 1, "source": "by_test"},
        "tax_residences": {
            "source": "google",
            "value": [{"country": "BRA"}, {"teste": "teste"}],
        },
    },
    "marital": {"spouse": None},
}

user_review_stub_missing_params = StubUserReview(
    stub_payload=payload_foreign_missing_value
)
user_review_stub_missing_country = StubUserReview(
    stub_payload=payload_foreign_missing_contry
)
