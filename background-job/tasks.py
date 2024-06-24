import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
import requests
from tabulate import tabulate
from broker import rabbitmq_broker

# # Ensure the broker is set up in this file
# rabbitmq_broker = RabbitmqBroker(url="amqp://guest:guest@rabbitmq:5672/")
# dramatiq.set_broker(rabbitmq_broker)

API_URL = "http://192.168.144.143:30002/api/students/?query="

@dramatiq.actor
def print_message(message):
    print(f"Received message: {message}")

@dramatiq.actor
def add_numbers(a, b):
    result = a + b
    print(f"The result of {a} + {b} is {result}")

@dramatiq.actor
def call_api():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            headers = ["Id", "Fullname", "Gender", "School", "Email"]  # Adjust headers based on your API response structure
            table_data = [[item["id"], item["full_name"], item["gender"], item["school"], item["email"]] for item in data]
            table = tabulate(table_data, headers=headers, tablefmt="pretty")
            print("API Response:")
            print(table)
        else:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while calling the API: {str(e)}")
