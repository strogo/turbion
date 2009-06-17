= Установка turbion

В данном файле описаны этапы интеграции turbion в уже существующий или вновь созданный
джанговский проект.

== Установка пакета `turbion` в системе

=== Использование easy_install

=== Использование virtualenv + pip

== Создание и/или настройка проекта

=== Полуавтоматическая

Данный тип установки подходит для ситуаций, когда вы хотите создать новый проект
с блогом `turbion`.

Для облегчения первичной установки существует скрипт `turbion-admin.py`.

Используя команду `startblogproject` можно создать джанговский проект
с базовыми настройками `turbion`:

    # turbion-admin.py startblogprject my_blog_project --name="My Super Blog"

=== Ручная

Для тех кто хочет сам установить `turbion` в новый проект или интегрировать уже
в имеющийся необходимо выполнить следующие шаги:

 * Добавить `turbion` в `INSTALLED_APPS`

 * Добавить `turbion.core.blogs.context_processors.blog_globals` в `CONTEXT_PROCESSORS`

 * Если вы хотите исольвазовать модель `Profile` в качестве замены стандартной `User`,
 не обходимо:

   * заменить в стандарный `django.contrib.auth.middleware.AuthenticationMiddleware`
   на `turbion.core.profiles.middleware.AuthenticationMiddleware` в `MIDDLEWARE_CLASSES`

   * [опционально] для того чтобы только пользователя помеченные как `active=True`
   могли логиниться, необходимо добавить в `AUTHENTICATION_BACKENDS`

Должен быть contrib.admin для работы dashboard


= Установка дополнительных приложений

Все приложения требует подключенного основного `turbion` приложения.

== turbion.contrib.aliases

== turbion.contrib.feedback

== turbion.contrib.openid
