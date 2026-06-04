# Патч интернационализации (i18n) для Sivilio ATS

## Структура патча

```
i18n_patch/
├── hr_project/
│   └── settings.py                  # исправлен импорт gettext_lazy
├── apps/
│   ├── people/
│   │   ├── models.py                # исправлен PersonStatus, добавлены _()
│   │   └── views.py                 # переводимые messages + action-строки
│   └── vacancies/
│       ├── models.py                # gettext_lazy + VacancyStatus
│       ├── views.py                 # переводимые messages
│       └── forms.py                 # переводимые labels и placeholders
├── templates/
│   ├── base/
│   │   └── base.html                # исправлены "System", "Dashboard", aria-labels
│   └── people/
│       └── index.html               # все строки через {% trans %} / {% blocktrans %}
└── locale/
    ├── ru/LC_MESSAGES/django.po     # Русский
    ├── be/LC_MESSAGES/django.po     # Беларуская
    ├── de/LC_MESSAGES/django.po     # Deutsch
    ├── pl/LC_MESSAGES/django.po     # Polski
    └── uk/LC_MESSAGES/django.po     # Українська
```

---

## Применение патча

### 1. Скопируйте файлы

Замените соответствующие файлы в вашем проекте файлами из этого патча,
сохраняя структуру директорий.

### 2. Создайте директорию locale (если нет)

```bash
mkdir -p locale
```

Скопируйте папки `ru`, `be`, `de`, `pl`, `uk` внутрь `locale/`.

### 3. Скомпилируйте переводы

```bash
python manage.py compilemessages
унутры докера:
docker compose exec web python manage.py compilemessages
```

Требуется утилита `msgfmt` (пакет `gettext`):
```bash
# Ubuntu/Debian
sudo apt install gettext

# macOS
brew install gettext
```

### 4. Проверьте работу

```bash
python manage.py runserver
```

Откройте приложение и переключите язык в выпадающем списке в шапке.

---

## Добавление переводов для остальных приложений

После каждого изменения запускайте:
```bash
python manage.py makemessages -l ru -l be -l de -l pl -l uk
# редактируете .po файлы, добавляете переводы
python manage.py compilemessages
```
унутры докера:
# 1. Извлечь все строки из кода и шаблонов в .po файлы
docker compose exec web python manage.py makemessages -l ru -l be -l de -l pl -l uk

# 2. Открыть .po файлы, найти новые строки (msgstr "")
# и вписать переводы вручную

# 3. Скомпилировать
docker compose exec web python manage.py compilemessages

---

## Важные замечания

### f-строки несовместимы с gettext_lazy
```python
# НЕПРАВИЛЬНО — перевод не сработает
messages.success(request, f'Сохранено: {obj.name}')

# ПРАВИЛЬНО — % форматирование
messages.success(request, _('Saved: %(name)s') % {'name': obj.name})

# ТОЖЕ ПРАВИЛЬНО — для немедленного перевода (не lazy)
from django.utils.translation import gettext as _   # без lazy
messages.success(request, _(f'Saved: {obj.name}'))  # только если не в module scope
```

### TextChoices: ключи БД не переводятся
```python
# НЕПРАВИЛЬНО — сломает миграции
class MyStatus(models.TextChoices):
    ACTIVE = _('active'), _('Active')  # ← _() на ключе!

# ПРАВИЛЬНО
class MyStatus(models.TextChoices):
    ACTIVE = 'active', _('Active')     # ← ключ = обычная строка
```

### pluralize несовместим с русским/украинским/белорусским
```django
{# НЕПРАВИЛЬНО для ru/uk/be — только 2 формы #}
{{ count }} record{{ count|pluralize }}

{# ПРАВИЛЬНО — blocktrans с count даёт 3 формы для славянских языков #}
{% blocktrans count counter=count %}
  {{ counter }} record
{% plural %}
  {{ counter }} records
{% endblocktrans %}
```
В .po файлах для ru/uk/be используются `msgstr[0]`, `msgstr[1]`, `msgstr[2]`.
