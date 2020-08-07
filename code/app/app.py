from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from classes import *
import matching 
from flask_login import current_user, login_user, login_required, logout_user
from flask import render_template, flash, redirect, url_for
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from werkzeug import secure_filename
import os
from flask import request
import json
import psycopg2
import datetime
import time
from tensorflow.keras.models import Model
from tensorflow.keras import backend
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.preprocessing import image

# import sys, os
# sys.path.insert(0, '%s'%os.environ['PROJECT_PATH'])


application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)
db.create_all()
db.session.commit()
bootstrap = Bootstrap(application)

# login_manager needs to be initiated before running the app
login_manager = LoginManager()
login_manager.init_app(application)

# Added at the bottom to avoid circular dependencies.
# (Altough it violates PEP8 standards)


base_model = InceptionV3(weights='imagenet')
model = Model(inputs=base_model.input,
              outputs=base_model.get_layer('avg_pool').output)
model._make_predict_function()



@application.route('/index', methods=['GET', 'POST'])
@application.route('/', methods=['GET', 'POST'])
def index():
    """upload a file from a client machine."""
    file = UploadFileForm()  # file : UploadFileForm class instance
    if file.validate_on_submit():
        f = file.file_selector.data  # f : Data of FileField
        filename = secure_filename(f.filename)
        # filename : filename of FileField
        # secure_filename secures a filename
        # before storing it directly on the filesystem.

        file_dir_path = os.path.join(application.instance_path, 'files')
        file_path = os.path.join(file_dir_path, filename)

        # if current_user.is_authenticated:
        #     user_id = str(current_user.get_id())
        #     username = current_user.username
        #     ts = time.time()
        #     timestamp = datetime.datetime.\
        #         fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        #     myConnection = psycopg2.connect(
        #                                     host=db_hostname,
        #                                     user=db_username,
        #                                     password=db_password,
        #                                     dbname=db_database)
        #     cur = myConnection.cursor()
        #     cur.execute("create table if not exists puppy.user_upload\
        #                 (user_id varchar(255), username varchar(255),\
        #                 file_path varchar(255), upload_time timestamp);")

        #     cur.execute("INSERT into puppy.user_upload \
        #                 (user_id, username, file_path, upload_time\
        #                 ) values ('%s','%s','%s','%s');"
        #                 % (user_id, username, file_path, timestamp))
        #     cur.close()
        #     myConnection.commit()
        #     myConnection.close()

        if os.path.exists(file_dir_path):
            # Save file to file_path (instance/ + 'files’ + filename)
            f.save(file_path)
        else:
            try:
                os.makedirs(file_dir_path)
                f.save(file_path)
            except OSError:
                print("Creation of the directory %s failed" % file_dir_path)
                return redirect(url_for('index'))
        return redirect(url_for('result', filename=filename))
    return render_template('index.html', form=file,
                           authenticated_user=current_user.is_authenticated)


@application.route('/register', methods=['GET', 'POST'])
def register():
    """Registers a new user"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = classes.User(username=form.username.data,
                            email=form.email.data, password=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # myConnection = psycopg2.connect(
        #                                 host=db_hostname, user=db_username,
        #                                 password=db_password,
        #                                 dbname=db_database)
        # cur = myConnection.cursor()
        # cur.execute(
        #             "create table if not exists puppy.users\
        #             (username varchar(255), email varchar(255),\
        #             password varchar(255));")
        # username = str(form.username.data)
        # email = str(form.email.data)
        # password = str(form.password.data)

        # cur.execute("INSERT into puppy.users (username, email,\
        #             password) values ('%s', '%s', '%s');"
        #             % (username, email, password))
        # # cur.execute("select * from puppy.users;")
        # myConnection.commit()
        # myConnection.close()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@application.route('/login', methods=['GET', 'POST'])
def login():
    """Logs in a user"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = classes.User.query.\
            filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@application.route('/logout')
@login_required
def logout():
    """Logs out a user"""
    before_logout = '<h1> Before logout - is_autheticated : ' \
                    + str(current_user.is_authenticated) + '</h1>'

    logout_user()

    after_logout = '<h1> After logout - is_autheticated : ' \
                   + str(current_user.is_authenticated) + '</h1>'
    # pause for .2 seconds before redirect to index.
    time.sleep(.2)
    return redirect(url_for('index'))


@application.route('/upload', methods=['GET', 'POST'])
def upload():
    """upload a file from a client machine."""
    file = UploadFileForm()  # file : UploadFileForm class instance
    if file.validate_on_submit():
        f = file.file_selector.data  # f : Data of FileField
        filename = secure_filename(f.filename)
        # filename : filename of FileField
        # secure_filename secures a filename
        # before storing it directly on the filesystem.

        file_dir_path = os.path.join(application.instance_path, 'files')
        file_path = os.path.join(file_dir_path, filename)

        if current_user.is_authenticated:
            user_id = str(current_user.get_id())
            username = current_user.username
            # ts = time.time()
            # timestamp = datetime.datetime.\
            #     fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            # myConnection = psycopg2.connect(host=db_hostname,
            #                                 user=db_username,
            #                                 password=db_password,
            #                                 dbname=db_database)
            # cur = myConnection.cursor()
            # cur.execute("create table if not exists\
            #             puppy.user_upload (user_id varchar(255),\
            #             username varchar(255),\
            #             file_path varchar(255),\
            #             upload_time timestamp);")

            # cur.execute("INSERT into puppy.user_upload\
            #             (user_id, username, file_path,\
            #             upload_time) values\
            #             ('%s','%s','%s','%s');"
            #             % (user_id, username,
            #                file_path, timestamp))
            # cur.close()
            # myConnection.commit()
            # myConnection.close()

        if os.path.exists(file_dir_path):
            # Save file to file_path (instance/ + 'files' + filename)
            f.save(file_path)
        else:
            try:
                os.makedirs(file_dir_path)
                f.save(file_path)
            except OSError:
                print("Creation of the directory %s failed" % file_dir_path)
                return redirect(url_for('index'))
        # flash('Please wait, we are getting your results')
        return redirect(url_for('result', filename=filename))
    return render_template('upload.html', form=file)


@application.route('/result', methods=['GET', 'POST'])
def result():
    """show matching result to user."""
    file_name = request.args.get('filename')
    file_path = os.path.join(application.instance_path, 'files', file_name)

    # here change to local folder 
    # PATH = os.path.join(os.sep, "e", "ec2-user",
    #                     "product-analytics-group-project-puppylover",
    #                     "data")

    # the path for metadata.
    merged_path = "../../data/final.csv"
    # os.environ["LOCAL_TABLE_PATH"]
    # the path for embedding results.
    embedding_path = "../../data/embeddings.out"
    # os.environ["LOCAL_EMBED_PATH"]

    dogs = matching.matching_dog(model, file_path,
                                 embedding_path, merged_path)
    file = UploadFileForm()  # file : UploadFileForm class instance
    return render_template('result_new.html',
                           form=file, title='Photos', dogs=dogs)





if __name__ == '__main__':
    application.run(debug=True,host='0.0.0.0')

# @application.route('/record')
# @login_required
# def record():
#     """Show a user's past search results"""
#     user_id = current_user.get_id()
#     myConnection = psycopg2.connect(host=db_hostname,
#                                     user=db_username,
#                                     password=db_password,
#                                     dbname=db_database)
#     cur = myConnection.cursor()
#     cur.execute("select * from puppy.user_upload where\
#                 upload_time in (select max(upload_time)\
#                 from puppy.user_upload\
#                 where user_id = '%s');" % str(user_id))
#     result = cur.fetchall()
#     try:
#         user_name = result[0][1]
#         latest_upload_path = result[0][2]

#         PATH = os.path.join(os.sep, "home", "ec2-user",
#                             "product-analytics-group-project-puppylover",
#                             "data")
#         embedding_path = os.path.join(PATH, "embedding_clean.out")
#         merged_path = os.path.join(PATH, "final.csv")
#         dogs = matching.matching_dog(model,
#                                      latest_upload_path,
#                                      embedding_path,
#                                      merged_path)

#         return render_template('record.html', user_name=user_name, dogs=dogs)
#     except RuntimeError:
#         return render_template('no_record.html')

# Citation: some code is adapted from
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
