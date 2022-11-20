import os
import json
from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect, secure_filename

from data import db_session
from data.users import User
from data.products import Product
from data.vectors import Vector

from forms.user import RegistrationForm, EnterForm

UPLOAD_FOLDER = 'json_files/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'as;dlkfjsa333'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db_session.global_init('database.db')


@app.route('/')
def start_page():
    return render_template('start_page.html', file='css/start_page.css',
                           title='Вход')


@app.route('/registration', methods=['GET', 'POST'])
def registration_page():
    form, message = RegistrationForm(), ''

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        check_user = db_sess.query(User).filter(
            User.phone == form.phone.data).first()
        if check_user:
            message = 'Номер используется!'
        else:
            user = User()
            user.name = form.name.data
            user.surname = form.surname.data
            user.phone = form.phone.data
            db_sess.add(user)
            db_sess.commit()
            user_id = db_sess.query(User).filter(
                User.phone == form.phone.data).first().id
            return redirect(f'/main/{user_id}')

    return render_template('registration_page.html', file='css/registration_page.css',
                           title='Регистрация', message=message, form=form)


@app.route('/enter', methods=['GET', 'POST'])
def enter_page():
    form, message = EnterForm(), ''

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        check_user = db_sess.query(User).filter(
            User.phone == form.phone.data).first()
        if check_user:
            return redirect(f'/main/{check_user.id}')
        else:
            message = 'Телефон не найден!'

    return render_template('enter_page.html', file='css/enter_page.css',
                           title='Вход', message=message, form=form)


@app.route('/main/<int:id>', methods=['GET', 'POST'])
def facecam_page(id):
    current_user_id = id
    message = ''

    if request.method == 'POST':
        if request.files['file']:
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(f"{app.config['UPLOAD_FOLDER']}{filename}", "r") as json_file:
                data_order = json.load(json_file)

            db_sess = db_session.create_session()
            check_user = db_sess.query(Product).filter(
                Product.user_id == current_user_id).first()

            if check_user:
                with open(check_user.json_file, 'r') as json_file:
                    user_data = json.load(json_file)
                for key in data_order:
                    user_data[key] = user_data.get(key, []) + data_order[key]

                with open(check_user.json_file, 'w') as json_file:
                    json.dump(user_data, json_file)

            else:
                with open(f'json_files/users_files/{current_user_id}.json', 'w') as json_file:
                    json.dump(data_order, json_file)
                product = Product()
                product.user_id = current_user_id
                product.json_file = f'json_files/users_files/{current_user_id}.json'
                db_sess.add(product)
                db_sess.commit()

            os.remove(f"{app.config['UPLOAD_FOLDER']}{filename}")
            return redirect(f'/recomendation/{current_user_id}')

        else:
            message = 'Выберите файл!'

    return render_template('main_page.html', file='css/main_page.css',
                           title='Добавление продуктов', message=message)


@app.route('/recomendation/<int:id>', methods=['GET', 'POST'])
def recomendation_page(id):
    current_user_id = id
    often_shopping, rec_shopping_first, rec_shopping = [], [], []

    with open(f'json_files/users_files/{id}.json', 'r') as json_file:
        data = json.load(json_file)

    for category in data:
        count_data = {}
        for p in data[category]:
            count_data[p[0]] = count_data.get(p[0], 0) + p[1]
        sorted_data = sorted(count_data.items(),
                             key=lambda x: x[1], reverse=True)
        often_shopping += sorted_data
        rec_shopping_first.append(list(count_data)[0])

    often_shopping.sort(key=lambda x: x[1], reverse=True)
    often_shopping = [el[0] for el in often_shopping]
    often_shopping = often_shopping[:3] if len(
        often_shopping) >= 3 else often_shopping

    rec_shopping = [
        el for el in rec_shopping_first if el not in often_shopping]
    rec_shopping = rec_shopping[:3] if len(rec_shopping) >= 3 else rec_shopping

    return render_template('recomendation_page.html', file='css/recomendation.css',
                           title='Рекомендации', often=often_shopping, rec=rec_shopping)


@app.route('/admin', methods=['POST', 'GET'])
def admin_page():
    db_sess = db_session.create_session()
    products = db_sess.query(Product)
    data_id = [i.user_id for i in products]
    dict_all_types = {}

    for user_id in data_id:
        with open(f'json_files/users_files/{user_id}.json', 'r') as file:
            data_json = json.load(file)

        for type_prod in data_json:
            if type_prod in dict_all_types:
                pass
            else:
                dict_all_types[type_prod] = {}
                for data_list_prod in data_json[type_prod]:
                    if data_list_prod[0] in dict_all_types[type_prod]:
                        dict_all_types[type_prod][data_list_prod[0]
                                                  ] += data_list_prod[1]
                    else:
                        dict_all_types[type_prod][data_list_prod[0]
                                                  ] = data_list_prod[1]

    return render_template('admin_page.html', title='Панель администратора',
                           file='css/admin.css', dict_all_types=dict_all_types)


app.run()
