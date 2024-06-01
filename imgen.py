import requests
import time
import base64
from PIL import Image
from io import BytesIO
import os
import json

if 'logger.json' not in os.listdir('.'):
    raise Exception('Нет данных для аутентификации в YandexAPI.')

with open('logger.json', 'r', encoding='utf-8') as file:
    log = json.load(file)

catalogue_id = log['catalogue_id']
apikey = log['apikey']

class ImageGenerator():
    def __init__(self):
        pass

    def generate(self, text):
        prompt = {
            "modelUri": f"art://{catalogue_id}/yandex-art/latest",
            "generationOptions": {
                "seed": 17
            },
            "messages": [
                {
                    "weight": 1,
                    "text": text
                }
            ]
        }

        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"

        headers = {
            'Content-Type': "application/json",
            "Authorization": f"Api-Key {apikey}"
        }

        response = requests.post(
            url, headers=headers, json=prompt
        ).json()

        return response

    def get_answ(self, response, wait = 2):
        headers = {
            'Content-Type': "application/json",
            "Authorization": "Api-Key AQVN3acGoWLlgL9AXnn7xD_1mja1itYM8Xo8LbTX"
        }

        req = requests.get(
            url=f'https://llm.api.cloud.yandex.net:443/operations/{response["id"]}', headers=headers
        ).json()['done']

        total = 15
        f_sym = '█'
        l_sym = '▒'
        sleep_counter = 0
        while req != True:
            sleep_counter += 1

            print(f"( {f_sym * sleep_counter}{(total - sleep_counter) * l_sym} ) --> {sleep_counter}/{total} | ({sleep_counter * 2} сек.)")
            time.sleep(wait)
            req = requests.get(
                url=f'https://llm.api.cloud.yandex.net:443/operations/{response["id"]}', headers=headers
            ).json()['done']

        req = requests.get(
            url=f'https://llm.api.cloud.yandex.net:443/operations/{response["id"]}', headers=headers
        ).json()

        return req

    def get_image(self, req, filename):
        base64_string = req["response"]["image"]
        decoded_bytes = base64.b64decode(base64_string)

        image_buffer = BytesIO(decoded_bytes)

        image = Image.open(image_buffer)

        image.save(filename)

        return image

    def assembly(self, text, filename):
        gen = self.generate(text)
        req = self.get_answ(gen, wait=2)
        image = self.get_image(req, filename)

        return image


