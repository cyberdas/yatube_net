from django.contrib.auth.forms import UserCreationForm # готовый класс UserCreationForm 
# на основе которого создаётся форма регистрации нового пользователя в forms.py
from django.contrib.auth import get_user_model


User = get_user_model()


# создадим собственный класс для формы регистрации
# сделаем его наследником предустановленного класса UserCreationForm
class CreationForm(UserCreationForm):
        class Meta(UserCreationForm.Meta):
                # модель уже существует, сошлёмся на неё
                model = User
                # укажем, какие поля должны быть видны в форме и в каком порядке
                fields = ("first_name", "last_name", "username", "email")
# создаем модель - в forms.py создается класс формы,
# добавляем view класс в views.py, Createview - шаблон для отрисовки форм
# форма передается в шаблон и к полям можно обращаться через .
