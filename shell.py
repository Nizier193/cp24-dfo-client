from banner_assembler import Banner_Assembly
import time

print('Давайте создадим баннер для вашего текста!')
text = input("<< Пожалуйста, скопируйте текст, который вы хотите обработать и вставьте его сюда. >> \n>> ")

print('----------------')
print('Шаг 1. Генерация текстовой информации.')
assembly = Banner_Assembly()
result = assembly.make_text_content(text)

print()
print('Из текста получилось выделить следующее.')
print(f'    Мотивационная фраза: {result["inplace"]}')
print(f'    Заголовок: {result["header"]}')
print(f'    Основная мысль: {result["thesis"]}')

print()
ans = input("Вас устраивает текстовое содержание баннера? \n1 - Да \n2 - Нет \n>> ")
while ans not in ['1', 'Да']:
    custom = input("Напишите, что можно было бы добавить или передать нейросети? \n>> ")

    result = assembly.make_text_content(f'{custom} \n {text}')
    print(f'    Мотивационная фраза: {result["inplace"]}')
    print(f'    Заголовок: {result["header"]}')
    print(f'    Основная мысль: {result["thesis"]}')
    ans = input("Вас устраивает текстовое содержание баннера? \n1 - Да \n2 - Нет \n>> ")

print()
print('Шаг 2. Генерация графической части. >> (Фон и основная картинка.)')
images = assembly.make_content()
images[0].show()
images[1].show()
print('Генерация успешна! Ознакомьтесь с результатами.')
ans = input('Вас устраивает графическое содержание баннера? \n1 - Да \n2 - Нет \n>> ')
while ans not in ['1', 'Да']:
    images[0].show()
    images[1].show()
    print('Генерация успешна! Ознакомьтесь с результатами.')
    ans = input('Вас устраивает графическое содержание баннера? \n1 - Да \n2 - Нет \n>> ')

print('-------------------')
print('Шаг 3. Сборка баннера.')
print('На этом этапе вам необходимо указать, какие элементы следует добавить на баннер.')

FILEFORMATS = ['png', 'jpg', 'jpeg']

QR = input('   QR-код, если имеется. введите название файла, если есть {Название файла}.png и "Нет", если нет QR кода.  >> ')
assembly.stack_banner(
    thesis=True if input('  Хотите добавить тезис в две-три строки ниже заголовка? (Да/Нет) >> ') == 'Да' else False,
    inplace=True if input('  Хотите добавить мотивационную табличка "врез" сверху от заголовка? (Да/Нет) >> ') == 'Да' else False,
    button=True if input('  Хотите добавить кнопку "Узнать больше" ниже тезиса? (Да/Нет) >> ') == 'Да' else False,
    QR=QR if QR.split('.')[-1].split()[0] in FILEFORMATS else None,
)

print('Сборка успешна! Ознакомьтесь с полученным баннером.\nФормат - 1920x1080.\n\nСпасибо вам!')

time.sleep(5)
