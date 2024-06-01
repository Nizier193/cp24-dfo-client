from SETTINGS import *
from PIL import Image, ImageDraw, ImageFont
from generator import *
from imgen import ImageGenerator


class Banner_Assembly():
    def __init__(self):
        pass

    def make_text_content(self, text):
        processor = ProcessText()
        processed = processor.process(text)

        self.thesis = processed['thesis']['result']['alternatives'][0]['message']['text'].replace('*', '')
        self.header = processed['header']['result']['alternatives'][0]['message']['text'].replace('*', '')
        self.content = processed['content']['result']['alternatives'][0]['message']['text'].replace('*', '')
        self.background = processed['backgr']['result']['alternatives'][0]['message']['text']
        self.motivation = processed['motivation']['result']['alternatives'][0]['message']['text']

        self.dct = {
            'thesis': self.thesis,
            'header': self.header,
            'inplace': self.motivation,
        }

        return self.dct

    def make_content(self):
        processor = ImageGenerator()
        image = processor.assembly(self.content, 'images/banner_image.png')
        background = processor.assembly("Минимализм. \n" + self.background, 'images/background.png')

        return image, background

    def resize(self, image, width):

        base_width = width
        wpercent = (base_width / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = image.resize((base_width, hsize), Image.Resampling.LANCZOS)

        return image

    def split_sentence(self, sentence, num_of_char):
        split_sentence = []
        sentence_word = sentence.split(' ')
        current_line = ""
        for word in sentence_word:
            if len(current_line) + len(word) <= num_of_char:
                current_line += word + " "
            else:
                split_sentence.append(current_line)
                current_line = word + " "
        split_sentence.append(current_line)
        return split_sentence

    def stack_banner(self,
        inplace = True,
        button = True,
        thesis = True,
        QR = None):

        # QR-коды

        elements = []
        elements.append('inplace' if inplace else None)
        elements.append('header')
        elements.append('thesis' if thesis else None)
        elements.append('button' if button else None)

        positions = [2, 7, 12, 21]

        canvas = Image.new('RGB', (1920, 1080), color=(255, 255, 255))
        draw = ImageDraw.Draw(canvas)

        image = Image.open('images/banner_image.png')
        image = self.resize(image, 700)

        background = Image.open('images/background.png')
        background = self.resize(background, 1920)
        canvas.paste(background)

        for elem, pos_y in zip(elements, positions):
            if elem in ['button']:
                attrs = banners_inplace['pos'][elem]

                font = ImageFont.truetype('arial.ttf', attrs['font'])

                spl_text = ''
                for txt in self.split_sentence(text, 50):
                    spl_text += txt + '\n'

                draw.rounded_rectangle(((2 * 40, pos_y * 40), (500, (pos_y * 40) + 100)), 20, fill=(200, 200, 200))
                draw.text((2.25 * 40, (pos_y * 40) + 20), "Узнать подробнее", (0, 0, 0), font=font)

            if elem in ['inplace']:
                attrs = banners_inplace['pos'][elem]

                font = ImageFont.truetype('arial.ttf', attrs['font'])
                text = self.dct[elem]

                spl_text = ''
                for txt in self.split_sentence(text, 50):
                    spl_text += txt + '\n'

                draw.rounded_rectangle(((2 * 40, pos_y * 40), (1000, (pos_y * 40) + 100)), 20, fill=(200, 200, 200))
                draw.text((2.25 * 40, (pos_y * 40) + 10), spl_text, (0, 0, 0), font=font)

            if elem in ['header', 'thesis']:
                attrs = banners_inplace['pos'][elem]

                font = ImageFont.truetype('arial.ttf', attrs['font'])
                text = self.dct[elem]

                spl_text = ''
                for txt in self.split_sentence(text, 20):
                    spl_text += txt + '\n'

                draw.text((2.25 * 40, pos_y * 40), spl_text, (0, 0, 0), font=font)

        impos = banners_inplace['pos']['image']['pos']

        image = Image.open('images/banner_image.png')
        image = self.resize(image, 700 if not QR else 500)

        canvas.paste(image, (
            ((1920 - 100 - 300 - 550) if QR else (1920 - 100 - 700)),
            ((1080 - 100 - 500) if QR else (1080 - 100 - 700)))
        )

        if QR:
            qr = Image.open(QR)
            qr = self.resize(qr, 300)
            canvas.paste(qr, (1920 - 300 - 100, 1080 - 300 - 100))

        canvas.save('banner.png')
