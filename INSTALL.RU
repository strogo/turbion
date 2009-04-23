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

Все приложения требует подключеного основного `turbion` приложения.

Приложения имеющие админки могут как "прицеплятся" к выделенной админке (dashboard)
turbion, так и к глобальной. Это регулуриется параметром настроеки
`TURBION_CONTRIB_USE_GLOBAL_ADMIN`, который по умолчанию `False`

== turbion.contrib.aliases

== turbion.contrib.feedback

== turbion.contrib.dbtemplates

Приложение позволяет держать шаблоны в базе данных.

Для установки необходимо:
 * добавить `turbion.contrib.dbtemplates` в `INSTALLED_APPS`
 * добавить `turbion.dbtemplates.loader.load_template_source` в `TEMPLATE_LOADERS`

В зависимости от порядка в котором перечислены лоадеры,можно управлять логикой
поиска шаблонов джанги. Т.е. если поствить этот лоадер первым, то он будет иметь
преоритет перед шаблона в файловой системе, что дас возможно подменять их и редактировать
через административный интерфейс.

== turbion.contrib.openid
