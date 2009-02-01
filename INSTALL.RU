

= Установка turbion

 1. Добавить `turbion` в `INSTALLED_APPS`

 2. Если вы хотите исольвазовать модель `Profile` в качестве замены стандартной `User`,
 не обходимо:

   1. заменить в стандарный `django.contrib.auth.middleware.AuthenticationMiddleware`
   на `turbion.core.profiles.middleware.AuthenticationMiddleware` в `MIDDLEWARE_CLASSES`

   3. [опционально] для того чтобы только пользователя помеченные как `active=True`
   могли логиниться, необходимо добавить в `AUTHENTICATION_BACKENDS`

Должен быть contrib.admin для работы dashboard


= Установка дополнительных приложений

Все приложения требует подключеного основного `turbion` приложения.

== turbion.contrib.aliases

== turbion.contrib.feedback

== turbion.contrib.dbtemplates

Приложение позволяет держать шаблоны в базе данных.

Для установки необходимо:
 1. добавить `turbion.contrib.dbtemplates` в `INSTALLED_APPS`
 2. добавить `turbion.dbtemplates.loader.load_template_source` в `TEMPLATE_LOADERS`

В зависимости от порядка в котором перечислены лоадеры,можно управлять логикой
поиска шаблонов джанги. Т.е. если поствить этот лоадер первым, то он будет иметь
преоритет перед шаблона в файловой системе, что дас возможно подменять их и редактировать
через административный интерфейс.

== turbion.contrib.pingback

== turbion.contrib.openid

== turbion.contrib.gears

== turbion.contrib.registration
