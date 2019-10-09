import boto3
import datetime
from project import db
from project.models import Applicant, Resume, Job, Application
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, redirect, request, Blueprint, session


users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('users.login'))


@users_blueprint.route('/register', methods=['GET','POST'])
def register():
    session.clear()
    if request.method == 'POST':
        email = request.form.get('email', None)
        name = request.form.get('name', None)
        password = request.form.get('password', None)
        gender = request.form.get('gridRadios', None)
        repeat_password = request.form.get('repeat_password', None)
        dob = request.form.get('date_of_birth', None)
        resume = request.files.get('resume', None)
        resume_name = resume.filename.replace(' ', '')

        if email is None or email == '':
            return render_template('register.html', warning='Email cannot be Empty')

        if password is None or password == '':
            return render_template('register.html', warning='Password cannot be Empty')

        if repeat_password is None or repeat_password == '':
            return render_template('register.html', warning='Confirm Password cannot be Empty')

        if name is None or name == '':
            return render_template('register.html', warning='Name cannot be Empty')

        if gender is None:
            return render_template('register.html', warning='Gender cannot be Empty')

        if dob is None or dob == '':
            return render_template('register.html', warning='Date of Birth cannot be Empty')

        if resume is None or resume.filename == '':
            return render_template('register.html', warning='Resume cannot be Empty')

        if not (password == repeat_password):
            return render_template('register.html', warning='Both passwords should be same.')

        user = Applicant.query.filter_by(email=email).first()

        if user == None:
            new_user_obj = Applicant(name=name,
                                     email=email,
                                     gender=gender,
                                     birth_date=datetime.datetime.strptime(dob, '%m/%d/%Y'),
                                     hashed_password=generate_password_hash(password))
            db.session.add(new_user_obj)
            db.session.commit()

            user = Applicant.query.filter_by(email=email).first()
            public_resume_link = file_upload_to_s3(resume, resume_name)
            new_resume_obj = Resume(app_id=user.id,
                                    resume=public_resume_link)
            db.session.add(new_resume_obj)
            db.session.commit()
            return redirect(url_for('users.login'))
        else:
            return render_template('register.html', warning='Email already exists. Please Login')
    return render_template('register.html')


@users_blueprint.route('/login', methods=['GET','POST'])
def login():
    session.clear()
    if request.method == 'POST':
        email = request.form.get('email', 'None')
        password = request.form.get('password', 'None')
        user = Applicant.query.filter_by(email=email).first()

        if user == None:
            return render_template('login.html', warning='Email Does not exist!!!')
        elif check_password_hash(user.hashed_password, password) and user is not None:
            login_user(user)
            session['user_email'] = user.email
            print("user is logged in!!!", current_user.is_authenticated)
            return redirect(url_for('users.applicant_view'))
        else:
            return render_template('login.html', warning='Password is incorrect')
    return render_template('login.html')


@users_blueprint.route('/applicant-view', methods=['GET', 'POST'])
@login_required
def applicant_view():
    user_email = session['user_email']
    page = request.args.get('page', 1, type=int)
    total_jobs = Job.query.paginate(page=page, per_page=5)
    total_job_count = (total_jobs.__dict__)['total']
    user_obj = Applicant.query.filter_by(email=user_email).first()
    applicant_obj = Application.query.filter_by(app_id=user_obj.id).all()
    job_id_list = [x.job_id for x in applicant_obj]


    if request.method == 'POST':
        apply_job_id = request.form.get('apply_job', None)
        new_application_obj = Application(appl_date=datetime.datetime.utcnow(),
                                          app_id=user_obj.id,
                                          job_id=apply_job_id)
        db.session.add(new_application_obj)
        db.session.commit()
        return redirect(url_for('users.applicant_view'))


    return render_template('applicant-view.html',
                           total_jobs=total_jobs,
                           user_name=user_obj.name,
                           job_id_list=job_id_list,
                           total_job_count=total_job_count)


########################################################################################################################
########################################################################################################################
########################################################################################################################
def file_upload_to_s3(file, object_name):
    bucket = 'putbox-darshan'
    s3 = boto3.client(
        's3',
        aws_access_key_id='AKIA5SX2735H2JOS3RN2',
        aws_secret_access_key='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'
    )
    s3.upload_fileobj(file, bucket, object_name, ExtraArgs={"ACL": "public-read"})
    public_url = f"https://putbox-darshan.s3-us-west-1.amazonaws.com/{object_name}"
    return public_url