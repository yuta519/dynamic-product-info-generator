import ast
from openai import OpenAI

from config import get_settings


settings = get_settings()
client = OpenAI(api_key=settings.openai_key)


def generate_manufacture(manufacture_name: str):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Find the address, phone, email for the following manufacture: {manufacture_name}. The response should be a list of address, phone, email.",
                },
                {
                    "role": "system",
                    "content": "Output will be a only dictionary with keys: address, phone, email, which are easy to parse with Python. Any other texts are not allowed. Python annotation is not required.",
                },  # TODO: Use function call to parse the output
            ],
        )
        result: dict[str, str] = (
            ast.literal_eval(completion.choices[0].message.content) or {}
        )
        return result
    except Exception:
        return {}


def generate_product_information(product_info: dict):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"This is the information for the product: {product_info}. Please complete and provide the product name, description, category, price, rating, reviews, spec. If any information is missing, please assume and provide the product information. price and rating must be a float. spec must be a dictionary, which includes the product's specifications like height, width, weight and so on.",
                },
                {
                    "role": "system",
                    "content": "Output will be a only dictionary with keys, which are easy to parse with Python. Any other texts are not allowed. Python annotation is not required.",
                },  # TODO: Use function call to parse the output
            ],
        )
        result: dict[str, str] = (
            ast.literal_eval(completion.choices[0].message.content) or {}
        )
        return result
    except Exception:
        return None
