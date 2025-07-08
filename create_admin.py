from getpass import getpass
import sys

from app import create_app
from app.user.models import User, db

app = create_app()

with app.app_context():
    email = input('Введите email: ')

    if User.query.filter(User.email.ilike(email)).count():
        print('Этот Email уже используется')
        sys.exit(0)

    username = input('Введите имя: ')
    if User.query.filter(User.username.ilike(username)).count():
        print('Имя занято')
        sys.exit(0)
    password1 = getpass('Введите пароль')
    password2 = getpass('Введите пароль')

    if not password1 == password2:
        print('Пароли не совпадают')
        sys.exit(0)

    new_user = User(email=email, username=username, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print(f'Добавлен новый пользователь с id={new_user.id}')

