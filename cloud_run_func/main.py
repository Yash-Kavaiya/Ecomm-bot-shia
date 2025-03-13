import functions_framework
from flask import jsonify
import google.cloud.bigquery as bigquery
import random

@functions_framework.http
def handle_webhook(request):
    """HTTP Cloud Function."""
    print("Received webhook request.")
    request_json = request.get_json()
    print(f"Request JSON: {request_json}")

    if request_json and "fulfillmentInfo" in request_json and "tag" in request_json["fulfillmentInfo"]:
        tag = request_json["fulfillmentInfo"]["tag"]
        print(f"Extracted tag: {tag}")

        if tag == "get_order_details":
            print("Handling get_order_details request.")
            response = get_order_details(request_json)
            print(f"Response from get_order_details: {response}")
            return response
        elif tag == "generate_offer":
            print("Handling generate_offer request.")
            response = generate_offer(request_json)
            print(f"Response from generate_offer: {response}")
            return response
        else:
            print(f"Unknown tag: {tag}")
            response = jsonify({
                "fulfillmentResponse": {
                    "messages": [{
                        "text": {
                            "text": ["I'm not sure how to handle that request."]
                        }
                    }]
                }
            })
            print(f"Response: {response}")
            return response
    else:
        print("Invalid request format.")
        response = jsonify({
            "fulfillmentResponse": {
                "messages": [{
                    "text": {
                        "text": ["Invalid request."]
                    }
                }]
            }
        })
        print(f"Response: {response}")
        return response

def get_order_details(request_json):
    """Retrieves order details from BigQuery based on order_id."""
    print("Entering get_order_details function.")

    if "sessionInfo" not in request_json or "parameters" not in request_json["sessionInfo"] or "order_id" not in request_json["sessionInfo"]["parameters"]:
        print("Missing sessionInfo, parameters, or order_id.")
        response = jsonify({
            "fulfillmentResponse": {
                "messages": [{
                    "text": {
                        "text": ["Please provide an order ID."]
                    }
                }]
            }
        })
        print(f"Response: {response}")
        return response

    order_id = request_json["sessionInfo"]["parameters"]["order_id"]
    print(f"Extracted order_id: {order_id}")

    client = bigquery.Client()
    query = f"""
        SELECT
            order_id,
            customer_id,
            order_date,
            status,
            tracking_number,
            shipping_address
        FROM
            `innate-lacing-450600-r5.E_commerce.sample_orders`
        WHERE
            order_id = '{order_id}'
    """
    print(f"BigQuery query: {query}")

    try:
        query_job = client.query(query)
        results = list(query_job.result())
        print(f"BigQuery query results: {results}")

        if not results:
            print(f"Order {order_id} not found in BigQuery.")
            response = jsonify({
                "fulfillmentResponse": {
                    "messages": [{
                        "text": {
                            "text": [f"Order {order_id} not found."]
                        }
                    }]
                }
            })
            print(f"Response: {response}")
            return response

        order = results[0]  # Assuming only one order per ID
        order_date = order["order_date"].strftime("%Y-%m-%d") if order["order_date"] else "N/A"
        tracking_number = order["tracking_number"] if order["tracking_number"] else "N/A"

        response_text = f"Order ID: {order['order_id']}\n"
        response_text += f"Customer ID: {order['customer_id']}\n"
        response_text += f"Order Date: {order_date}\n"
        response_text += f"Status: {order['status']}\n"
        response_text += f"Tracking Number: {tracking_number}\n"
        response_text += f"Shipping Address: {order['shipping_address']}"

        response = jsonify({
            "fulfillmentResponse": {
                "messages": [{
                    "text": {
                        "text": [response_text]
                    }
                }]
            },
            "sessionInfo": {
                "parameters": {
                    "order_status": order["status"],
                    "order_date": order_date,
                    "tracking_number": tracking_number,
                    "shipping_address": order["shipping_address"]
                }
            }
        })
        print(f"Response: {response}")
        return response

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        response = jsonify({
            "fulfillmentResponse": {
                "messages": [{
                    "text": {
                        "text": [f"An error occurred: {str(e)}"]
                    }
                }]
            }
        })
        print(f"Response: {response}")
        return response

def generate_offer(request_json):
    """Generates an offer based on a user-provided number."""
    print("Entering generate_offer function.")

    if "sessionInfo" not in request_json or "parameters" not in request_json["sessionInfo"] or "user_number" not in request_json["sessionInfo"]["parameters"]:
        print("Missing sessionInfo, parameters, or user_number.")
        response = jsonify({
            "fulfillmentResponse": {
                "messages": [{
                    "text": {
                        "text": ["Please enter a number between 1 and 9."]
                    }
                }]
            }
        })
        print(f"Response: {response}")
        return response

    user_number_data = request_json["sessionInfo"]["parameters"]["user_number"]

    try:
        # Access the 'original' value from the user_number dictionary
        user_number = int(user_number_data['original'])

        if not 1 <= user_number <= 9:
            print(f"Invalid user number: {user_number}")
            response = jsonify({
                "fulfillmentResponse": {
                    "messages": [{
                        "text": {
                            "text": ["Please enter a number between 1 and 9."]
                        }
                    }]
                }
            })
            print(f"Response: {response}")
            return response

        offers = {
    1: "Get 10% off your next purchase! Use code TRR10 at checkout. [Shop now at The RealReal](https://couponfollow.com/site/therealreal.com).",
    2: "Free shipping on orders over $50! Use code FREESHIP50 at checkout. [Shop now at The RealReal](https://www.retailmenot.com/view/therealreal.com).",
    3: "Buy one, get one 50% off on selected items! Use code BOGO50 at checkout. [Shop now at The RealReal](https://www.couponcabin.com/coupons/the-realreal/).",
    4: "Exclusive access to our new product launch! Use code NEWLAUNCH at checkout. [Shop now at The RealReal](https://simplycodes.com/store/therealreal.com).",
    5: "Earn double reward points on your next order! Use code DOUBLEPOINTS at checkout. [Shop now at The RealReal](https://www.groupon.com/coupons).",
    6: "Get a free gift with your purchase! Use code FREEGIFT at checkout. [Shop now at The RealReal](https://www.dontpayfull.com/at/therealreal.com).",
    7: "Enjoy a complimentary upgrade on your subscription! Use code UPGRADESUB at checkout. [Shop now at The RealReal](https://www.goodsearch.com/coupons/therealreal.com).",
    8: "Receive a personalized styling session! Use code STYLESESSION at checkout. [Shop now at The RealReal](https://www.offers.com/stores/realreal/).",
    9: "Unlock a secret discount code for a limited time! Use code SECRETDISCOUNT at checkout. [Shop now at The RealReal](https://www.groupon.com/coupons/amazon)."
}


        offer_message = offers[user_number]
        print(f"Generated offer: {offer_message}")

        response = jsonify({
            "fulfillmentResponse": {
                "messages": [{
                    "text": {
                        "text": [offer_message]
                    }
                }]
            }
        })
        print(f"Response: {response}")
        return response

    except (ValueError, KeyError, TypeError) as e:
        print(f"Invalid user number format or missing data: {e}")
        response = jsonify({
            "fulfillmentResponse": {
                "messages": [{
                    "text": ["Please enter a valid number."]
                }]
            }
        })
        print(f"Response: {response}")
        return response
