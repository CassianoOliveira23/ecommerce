import mercadopago

public_key = "TEST-418a35be-e516-4ea1-a56d-898c515ac927"
token = "TEST-2385292061141152-041620-7bce21da5f979d0a97e02a9bf7a34016-150619048"

# Add Credentials
sdk = mercadopago.SDK(token)

#items, total
preference_data = {
    "items": [
        {
            "title": "My Item",
            "quantity": 1,
            "unit_price": 75.76
        }
    ],
    "back_urls": {
        "success": ,
        "pending": ,
        "failure": ,
    }
}
       


response = sdk.preference().create(preference_data)
link = response["response"]["init_point"]
id_payment = response["response"]["id"]
print(link)
