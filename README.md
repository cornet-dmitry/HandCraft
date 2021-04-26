# HandCraft
Основой для написание сайта стал микрофреймворк для языка программирования Python - Flask
Также была использована База данных SQLite. Взаиможействует при помощи библиотеки SQLAlchemy. Называется: shop.db, в ней находятся таблицы: item - товары на сайте, users - пользователи сайта.
Классы Item и Users нужны для реализации добавления товаров и регистрации пользователей.
Функция main запускает работу сервера. В ней определяются взаимодействия между html-страницами, лежащими в папке templates, и самим сервером, чтобы получить сайт, по которому можно свободно перемещаться.
В папке static/images сохраняются изображения товаров, а также хранятся статичные изображения сайта, такие как лого или about.
Из папки forms наследуются классы, ответственные за построение регистрации и входа.
Для реализации некоторых функций используются внешние классы и библиотеки. Например, модуль change.resize приводит все изображения товаров к размеру 180*180.
