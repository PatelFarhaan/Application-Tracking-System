from flask_login import UserMixin
from project import db, login_manager


########################################################################################################################
###############################################* LOGIN MANAGER *########################################################
########################################################################################################################
@login_manager.user_loader
def user_load(user_id):
    return Applicant.query.get(user_id)
########################################################################################################################


########################################################################################################################
###############################################* LOGIN MANAGER *########################################################
########################################################################################################################
@login_manager.user_loader
def user_load(user_id):
    return Employee.query.get(user_id)
########################################################################################################################


########################################################################################################################
#################################################* DEPARTMENT *#########################################################
########################################################################################################################
class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64))
########################################################################################################################


########################################################################################################################
#################################################* APPLICANT *##########################################################
########################################################################################################################
class Applicant(db.Model, UserMixin):
    __tablename__ = 'applicant'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    status = db.Column(db.String(64), default="Active")
    birth_date = db.Column(db.DateTime)
    hashed_password = db.Column(db.String(256))
    email = db.Column(db.String(128), unique=True, index=True)
########################################################################################################################


########################################################################################################################
#################################################* RESUME *#############################################################
########################################################################################################################
class Resume(db.Model):
    __tablename__ = 'resume'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    resume = db.Column(db.String(256))
    app_id = db.Column(db.Integer, db.ForeignKey('applicant.id'), nullable=False)
########################################################################################################################


########################################################################################################################
#################################################* EMPLOYEE *###########################################################
########################################################################################################################
class Employee(db.Model, UserMixin):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    salary = db.Column(db.Float)
    hire_date = db.Column(db.DateTime)
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
########################################################################################################################


########################################################################################################################
#################################################* USERS *##############################################################
########################################################################################################################
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    type = db.Column(db.String(64), nullable=False)
    hashed_password = db.Column(db.String(256), nullable=False)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
########################################################################################################################


########################################################################################################################
###################################################* JOB *##############################################################
########################################################################################################################
class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(64))
    min_salary = db.Column(db.Float)
    max_salary = db.Column(db.Float)
    open_date = db.Column(db.DateTime)
    location = db.Column(db.String(64))
    description = db.Column(db.Text)
    status = db.Column(db.String(64), nullable=False)
    visibility = db.Column(db.Boolean, default=False, nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
########################################################################################################################


########################################################################################################################
#################################################* APPLICATION *########################################################
########################################################################################################################
class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    appl_date = db.Column(db.DateTime)
    status = db.Column(db.String(64), nullable=False, default='Applied')
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    app_id = db.Column(db.Integer, db.ForeignKey('applicant.id'), nullable=False)
########################################################################################################################


########################################################################################################################
#################################################* INTERVIEW *##########################################################
########################################################################################################################
class Interview(db.Model):
    __tablename__ = 'interview'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    int_date = db.Column(db.DateTime)
    comments = db.Column(db.Text)
    status = db.Column(db.String(64), nullable=False)
    app_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
########################################################################################################################


########################################################################################################################
####################################################* OFFER *###########################################################
########################################################################################################################
class Offer(db.Model):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    salary = db.Column(db.Float)
    ofr_date = db.Column(db.DateTime)
    start_date = db.Column(db.DateTime)
    status = db.Column(db.String(64), nullable=False)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    int_id = db.Column(db.Integer, db.ForeignKey('interview.id'), nullable=False)
########################################################################################################################