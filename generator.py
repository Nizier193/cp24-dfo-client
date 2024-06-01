import requests
import time
import os
import json

if 'logger.json' not in os.listdir('.'):
    raise Exception('Нет данных для аутентификации в YandexAPI.')

with open('logger.json', 'r', encoding='utf-8') as file:
    log = json.load(file)

catalogue_id = log['catalogue_id']
apikey = log['apikey']

class ProcessText():

    thesis_prompt = ("Выдели основной тезис в этом тексте для плаката. \n"
                     "Выведи только тезис, он должен быть из 7 слов и одного предложения. Не добавляй своих комментариев, выведи только тезис. \n")

    header_prompt = ("Выдели ОДИН заголовок текста для плаката. Выведи только его, ничего не поясняй и не добавляй комментариев.")

    content_prompt = ("Проанализируй текст, напиши промпт для генерации картинки, подходящей к этому тексту."
                      "Опиши что будет на картинке, немного деталей, которые просты для генерации нейросетью. "
                      "Цвет выбери один из этих: синий, красный, жёлтый, серый. "
                      "Выведи в виде единого ответа не более 20 слов, обязательно укажи цветовую палитру. Не употребляй цензурные слова и события. Нельзя упоминать флаги.\n\n")


    background_prompt = ("Картинка, которая будет сгенерирована по этому описанию будет на плакате. Предложи один вариант фона, на котором будет расположена картинка. Бери неяркие цвета, не чёрные."
                         "К примеру: 'Бежевый холст, градиент в голубой' или 'Бежевый холст, градиент в оранжевый'. Подбери подходящие цвета. Выведи только описание ОДНОГО фона, не предлагай несколько. \n\n")


    motivate_prompt = ("Напиши одну мотивирующую фразу к тексту из трёх слов. При ответе не добавляй своих комментариев. Ответ только одним предложением.")

    def __init__(self):
        pass

    def _basic_request(self, text):
        prompt = {
            "modelUri": f"gpt://{catalogue_id}/yandexgpt-lite/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.5,
                "maxTokens": "100",
            },
            "messages": [
                {"role": "system", "text": f"{text}"}
            ]
        }

        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

        headers = {
            'Content-Type': "application/json",
            "Authorization": f"Api-Key {apikey}"
        }

        response = requests.post(
            url, headers=headers, json=prompt
        )
        # print(response.json())

        return response.json()

    def process(self, text, num_words = 8):
        content = self._basic_request(self.content_prompt + f"Текст: {text}")
        time.sleep(1)
        thesis = self._basic_request(self.thesis_prompt + f"Текст: {text}")
        time.sleep(1)
        header = self._basic_request(self.header_prompt + f"Текст: {text}")
        time.sleep(1)
        background = self._basic_request(self.background_prompt + f"Текст: {content['result']['alternatives'][0]['message']['text']}")
        time.sleep(1)
        motivation = self._basic_request(self.motivate_prompt + f"Текст: {text}")

        return {
            'content': content,
            'thesis': thesis,
            'header': header,
            'backgr': background,
            'motivation': motivation,
        }

text = """
Психологи называют мотивацией сложный психофизиологический процесс, который влияет на способность человека достигать поставленных целей и удовлетворять свои потребности. Если проще, то мотивация — это эмоциональная и психическая готовность сделать что-то, несмотря на трудности на пути. Способность и готовность прилагать усилия, чтобы получать желаемое."""