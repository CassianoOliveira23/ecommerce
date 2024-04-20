import mercadopago

public_key = "TEST-418a35be-e516-4ea1-a56d-898c515ac927"
token = "TEST-2385292061141152-041620-7bce21da5f979d0a97e02a9bf7a34016-150619048"

def create_payment(order_items, link):

    # Add Credentials
    sdk = mercadopago.SDK(token)

    items = []
    for item in order_items:
        quantity = int(item.quantity)
        product_name = item.stok_item.product.name
        unit_price = float(item.stok_item.product.price)
        items.append({
            "title":  product_name,
            "quantity": quantity,
            "unit_price": unit_price,
        })
        
    #items, total
    preference_data = {
        "items": items,
    
        "back_urls": {
            "success": link,
            "pending": link,
            "failure": link,
        }
    }
    
    response = sdk.preference().create(preference_data)
    link_payment = response["response"]["init_point"]
    id_payment = response["response"]["id"]
    return link_payment, id_payment
