from flask import render_template, url_for, flash, redirect,request,  send_from_directory,send_file
from flaskblog import app,db
from flaskblog.forms import RegistrationForm, LoginForm,PaymentForm,Search,Delete
from flaskblog.models import User, Payment
from flask_login import login_user, current_user, logout_user, login_required
import datetime
import xlsxwriter

posts = [
    {
        'author': 'Complex Society',
        'title': 'Kalyani Complex Payment Site',
        'content': 'A Higher Quality of Living',
        'date_posted': 'January 05, 2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(Username=form.username.data, Address=form.address.data, PhoneNumber=form.phonenumber.data,PlotNumber=form.plotnumber.data
                    ,FlatNumber=form.flatnumber.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Role='admin').first()
        if user.Username == 'sadmin' and form.password.data == 'su':
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
'''
    if form.username.data == 'su' and form.password.data == 'su':
            user = form.username.data
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
'''

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/payment",methods=['GET', 'POST'])
@login_required
def payment():
    totamt=0
    form = PaymentForm()
    if form.validate_on_submit():
        paymnetinfo = Payment.query.filter_by(PhoneNumber=form.phonenumber.data).first()
        if paymnetinfo:
            amt = form.amount.data
            totamt = int(amt) + int(paymnetinfo.Amount)
            #now = datetime.datetime.now()
            #datetm = now.strftime("%Y-%m-%d %H:%M:%S")
            totmonth = 1 + paymnetinfo.TotalMonth
            paymnetinfo.ReceiptNo = form.receiptNo.data
            paymnetinfo.Amount  = str(totamt)
            paymnetinfo.EndDate = datetime.datetime.today()
            paymnetinfo.TotalMonth = totmonth
            db.session.add(paymnetinfo)
        else:
            userinfo = User.query.filter_by(PhoneNumber=form.phonenumber.data).first()
            if  userinfo:
                 totamt = form.amount.data
                 puser = Payment(PhoneNumber=form.phonenumber.data,ReceiptNo=form.receiptNo.data,Amount= form.amount.data,TotalMonth=1
                            ,Donation=form.donation.data,user_id = userinfo.id)
                 db.session.add(puser)
            else:
                flash(f'User Not yet registeed with the Phone no {form.phonenumber.data} Please Register First!', 'success')
                return redirect(url_for('home'))

        db.session.commit()
        flash(f'Upadte the amount to {totamt}!', 'success')
        return redirect(url_for('home'))
    return render_template('payment.html', title='Payment', form=form)

@app.route("/search",methods=['GET', 'POST'])
@login_required
def search():
    form = Search()

    if form.validate_on_submit():
        UserDetails = User.query.join(Payment, User.id == Payment.user_id).add_columns(User.Username,
                                                                                    User.PhoneNumber,
                                                                                    User.PlotNumber,
                                                                                    User.Date_created,
                                                                                    Payment.ReceiptNo,
                                                                                    Payment.Amount,
                                                                                    Payment.StartDate,
                                                                                    Payment.EndDate,
                                                                                    Payment.TotalMonth,
                                                                                    Payment.Donation).filter(User.PhoneNumber == form.phonenumber.data)
        phnocheck = Payment.query.filter_by(PhoneNumber=form.phonenumber.data).first()
        if phnocheck:
            return render_template('viewdetails.html', title='Search person',UserDetails=UserDetails,legend='Search Person')
        else:
            flash(f'Payment is Not yet Done. Please do the payment !', 'success')
            return redirect(url_for('home'))

    return render_template('search.html', title='Search', form=form)


@app.route("/viewall",methods=['GET'])
@login_required
def viewall():


    UserDetails = db.session.query(User,Payment).add_columns(User.Username,
                                                             User.PhoneNumber,
                                                             User.PlotNumber,
                                                             User.Date_created,
                                                             Payment.ReceiptNo,
                                                             Payment.Amount,
                                                             Payment.StartDate,
                                                             Payment.EndDate,
                                                             Payment.TotalMonth,
                                                             Payment.Donation).outerjoin(Payment,User.id ==Payment.user_id)
    ucheck = User.query.first()
    if ucheck:
            return render_template('viewdetails.html', title='Search person',UserDetails=UserDetails,legend='View Details')
    else:
        flash(f'No Record found in the table to Dispaly!', 'success')
        return redirect(url_for('home'))

@app.route("/delete",methods=['GET', 'POST'])
@login_required
def delete():
    form = Delete()

    if form.validate_on_submit():
        phnocheck = Payment.query.filter_by(PhoneNumber=form.phonenumber.data).first()
        user = User.query.filter_by(PhoneNumber=form.phonenumber.data).first()
        #flag = False
        if phnocheck:
            db.session.delete(phnocheck)
            db.session.commit()
            #flag=True

        if user:
            db.session.delete(user)
            db.session.commit()


        flash(f'Record is deleted having phone no {form.phonenumber.data} !', 'success')
        return redirect(url_for('home'))

    return render_template('delete.html', title='Delete Record', form=form)


@app.route("/download",methods=['GET'])
@login_required
def download():
    UserDetails = db.session.query(User,Payment).add_columns(User.Username,
                                                             User.PhoneNumber,
                                                             User.PlotNumber,
                                                             User.Date_created,
                                                             Payment.ReceiptNo,
                                                             Payment.Amount,
                                                             Payment.StartDate,
                                                             Payment.EndDate,
                                                             Payment.TotalMonth,
                                                             Payment.Donation).outerjoin(Payment,User.id ==Payment.user_id)

    ucheck = User.query.first()
    if ucheck:
            #preparedexcl(UserDetails)
            #return send_file(attachment_filename='Expenses.xlsx', as_attachment=True)
            return redirect(url_for('home'))

           # return redirect(url_for('home'))
    else:
        flash(f'No Record found to download!', 'success')
        return redirect(url_for('home'))

def preparedexcl(obj):
    workbook = xlsxwriter.Workbook('flaskblog/Expenses.xlsx')
    worksheet = workbook.add_worksheet('UserDetails')

    row=0
    col=0
    worksheet.write(row, col, "UserName")
    worksheet.write(row, col + 1, "PhoneNumber")
    worksheet.write(row, col + 2, "PlotNumber")
    worksheet.write(row, col + 2, "Registration")
    worksheet.write(row, col + 2, "ReceiptNumber")
    worksheet.write(row, col + 2, "Amount")
    worksheet.write(row, col + 2, "AmountStartDate")
    worksheet.write(row, col + 2, "AmountEndDate")
    worksheet.write(row, col + 2, "TotalMonth")
    worksheet.write(row, col + 2, "Donation")

    row =1
    for value in obj:
        if 'sadmin' not in value.Username:
            worksheet.write(row, col, value.Username)
            worksheet.write(row, col + 1, value.PhoneNumber)
            worksheet.write(row, col + 2, value.PlotNumber)
            if value.Date_created:
                regi=(str(value.Date_created))[0:11]
            else:
                regi=''
            worksheet.write(row, col+3, regi)
            if value.ReceiptNo:
                rcno=value.ReceiptNo
            else:
                rcno=''
            worksheet.write(row, col + 4, rcno)
            if value.Amount:
                amt= value.Amount
            else:
                amt='0'

            worksheet.write(row, col + 5, amt)

            if value.StartDate:
                stdt=(str(value.StartDate))[0:11]
            else:
                stdt=''

            worksheet.write(row, col + 6, stdt)

            if value.EndDate:
                eddt=(str(value.EndDate))[0:11]
            else:
                eddt=''

            worksheet.write(row, col + 7, eddt)

            if value.TotalMonth:
                totamt=value.TotalMonth
            else:
                totamt='0'

            worksheet.write(row, col + 8, totamt)

            if value.Donation:
                dod=value.Donation
            else:
                dod='0'

            worksheet.write(row, col + 9, dod)

            row += 1

    workbook.close()
