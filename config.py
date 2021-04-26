from random import choice, randint, sample
from string import ascii_letters

a = [choice(ascii_letters) for _ in range(15)] + [str(randint(0, 9)) for _ in range(15)]
SECRET_KEY = ''.join(sample(a, len(a)))

LOGO_IMG = 'https://cdn.worldvectorlogo.com/logos/minecraft-1.svg'

BOOTSTRAP_CSS = 'https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css'

ERROR_TEMPLATE = 'Попробуйте позже. Если ошибка не исправиться, то обратитесь к администратору сайта. Контакты: ' \
                 'cornet.dmitry28@yandex.ru '
