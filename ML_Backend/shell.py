from banner_assembler import Banner_Assembly
import time
import shutil
import os

print('Давайте создадим баннер для вашего текста!')
text = input("<< Пожалуйста, скопируйте текст, который вы хотите обработать и вставьте его сюда. >> \n"
             "Если ваш текст находится в файле text.txt, напишите 'Нет' >> \n>> ")
if text in ['Нет', 'НЕТ', 'нет']:
    text = open('text.txt', 'r', encoding='utf-8').read()

print()
print('-------------------')
print('Шаг 1. Генерация текстовой информации.')
assembly = Banner_Assembly()
result = assembly.make_text_content(text)

def length():
    return

print()
print('Из текста получилось выделить следующее.')
l = len(result["inplace"].split())
print(f'    Мотивационная фраза: {result["inplace"]} \n{'    Длина: ' + str(l) if l < 5 else ("    >> !!! Рекомендуется перегенерировать!")}\n')

l = len(result["header"].split())
print(f'    Заголовок: {result["header"]} \n{'    Длина: ' + str(l) if l < 5 else ("    >> !!! Рекомендуется перегенерировать!")}\n')

l = len(result["thesis"].split())
print(f'    Основная мысль: {result["thesis"]} \n{'    Длина: ' + str(l) if l < 10 else ("    >> !!! Рекомендуется перегенерировать!")}\n')

print()
ans = input("Вас устраивает текстовое содержание баннера? \n1 - Да \n2 - Нет \n>> ")
while ans not in ['ДА', 'Да', 'да', '1']:
    custom = input("Напишите, что можно было бы добавить или передать нейросети? \n>> ")
    result = assembly.make_text_content(f'{custom} \n {text}')

    print('Из текста получилось выделить следующее.')

    l = len(result["inplace"].split())
    print(
        f'    Мотивационная фраза: {result["inplace"]} \n{'    Длина: ' + str(l) if l < 5 else ("    >> !!! Рекомендуется перегенерировать!")}\n')

    l = len(result["header"].split())
    print(f'    Заголовок: {result["header"]} \n{'    Длина: ' + str(l) if l < 5 else ("     >> !!! Рекомендуется перегенерировать!")}\n')

    l = len(result["thesis"].split())
    print(
        f'    Основная мысль: {result["thesis"]} \n{'    Длина: ' + str(l) if l < 12 else ("     >> !!! Рекомендуется перегенерировать!")}\n')

    ans = input("Вас устраивает текстовое содержание баннера? \n1 - Да \n2 - Нет (перегенерировать)\n>> ")

print()
print('-------------------')
print('Шаг 2. Генерация графической части. >> (Фон и основная картинка.)')
images = assembly.make_content()
images[0].show()
images[1].show()
print('Генерация успешна! Ознакомьтесь с результатами.')
ans = input('Вас устраивает графическое содержание баннера? \n1 - Да \n2 - Нет \n>> ')
while ans not in ['ДА', 'Да', 'да', '1']:
    images[0].show()
    images[1].show()
    print('Генерация успешна! Ознакомьтесь с результатами.')
    ans = input('Вас устраивает графическое содержание баннера? \n1 - Да \n2 - Нет \n>> ')

print('-------------------')
print('Шаг 3. Сборка баннера.')
print('На этом этапе вам необходимо указать, какие элементы следует добавить на баннер.')

FILEFORMATS = ['png', 'jpg', 'jpeg']

QR = input('  Хотите добавить QR-код? (Да/Нет)  >> ')
q_flag = False
if QR in ['ДА', 'Да', 'да', '1']: print('\n< Важно!!! Поскольку вы хотите добавить QR-код, добавьте его в папку Project/dist с именем QR.png. >\n'); q_flag = True
assembly.stack_banner(
    thesis=True if input('  Хотите добавить тезис в две-три строки ниже заголовка? (Да/Нет) >> ') in ['ДА', 'Да', 'да', '1'] else False,
    inplace=True if input('  Хотите добавить мотивационную табличка "врез" сверху от заголовка? (Да/Нет) >> ') in ['ДА', 'Да', 'да', '1'] else False,
    button=True if input('  Хотите добавить кнопку "Узнать больше" ниже тезиса? (Да/Нет) >> ') in ['ДА', 'Да', 'да', '1'] else False,
    QR= 'QR.png' if q_flag else None,
)

print('Сборка успешна! Ознакомьтесь с полученным баннером.\nФормат - 1920x1080.\n\nСпасибо вам!')

time.sleep(5)
