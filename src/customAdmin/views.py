from datetime import datetime
from datetime import date
import calendar
import inflect
from xml.sax.xmlreader import AttributesNSImpl
from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from django.db.models import Sum
from random import randint, randrange


from customAdmin.forms import AccountAuthenticationForm, DepartmentForm, DesignationForm, EmergencyContactForm, EmployeeForm, EmployeeSalaryForm, AccountOfficerForm
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from django.http import HttpResponse

from django.views.generic import TemplateView

# Create your views here.


class attendance_screen_view(LoginRequiredMixin, View):
    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        user = request.user
        if user.role == "admin":
            emp = Employee.objects.all()
            sked = EmployeeSchedule.objects.filter(id=1)
            sched = EmployeeSchedule.objects.filter(status="ACTIVE")

            for schdule in sched:
                timein = schdule.timein
                # officialTimein = timein.strftime("%H:%M:%S")

            context = {
                'empl': emp,
                'officialTimein': timein,
                'sched': sched,
            }

            return render(request, 'take_attendance_template.html', context)
        else:
            print("not admin!")
            return render(request, 'restrict-content.html', {})

    def post(self, request):
        form = EmployeeAttendance(request.POST)
        if request.method == 'POST':
            if 'TimeLogin' in request.POST:
                empId = request.POST.get("employeeID")
                InOut = request.POST.get("LoginOptions")

                currentDateAndTime = datetime.now()
                currentTime = currentDateAndTime.strftime("%H:%M:%S")

                currentEndTime = request.POST.get("timeout")

                officialTimeIn = request.POST.get("timein")
                official_start_time = datetime.strptime(
                    officialTimeIn, "%H:%M:%S")

                inout = datetime.now()

                start_time = datetime.strptime(currentTime, "%H:%M:%S")
                end_time = datetime.strptime(currentEndTime, "%H:%M:%S")

                if InOut == '1':

                    # if EmployeeAttendance.objects.filter(todaydate=datetime.today()).filter(employee_id_id=empId).exists():
                    #     if EmployeeAttendance.objects.filter(timeout__isnull=False).filter(todaydate=datetime.today()):
                    #         messages.success(request, 'Already Timed In!')
                    #         return redirect('attendance')
                    #     else:
                    #         messages.success(request, 'Already Timed In!')
                    #         return redirect('attendance')
                    # else:

                    if EmployeeAttendance.objects.filter(timein__isnull=False).filter(todaydate=datetime.today()).filter(employee_id_id=empId).exists():
                        if EmployeeAttendance.objects.filter(timein__isnull=False).filter(todaydate=datetime.today()):
                            print(start_time)
                            print(official_start_time)
                            messages.success(request, 'Already Timed In!')
                            return redirect('attendance')
                        else:
                            print(start_time)
                            print(official_start_time)
                            messages.success(request, 'Already Timed In!')
                            return redirect('attendance')
                    else:

                        if start_time > official_start_time:

                            # LATE CALCULATIONS
                            EmpofficialTimeIn = datetime.strptime(
                                officialTimeIn, "%H:%M:%S")

                            delta = start_time - EmpofficialTimeIn

                            LateSec = delta.total_seconds()
                            LateMin = LateSec / 60
                            LateHours = LateSec / (60 * 60)

                            totalSec = int(LateSec)

                            TimeIntotalMin = int(LateMin)
                            if EmployeeAttendance.objects.filter(todaydate=datetime.today()).filter(employee_id_id=empId).exists():
                                if EmployeeAttendance.objects.filter(timein__isnull=True).filter(todaydate=datetime.today()):
                                    EmployeeAttendance.objects.filter(todaydate=datetime.today()).filter(
                                        employee_id_id=empId).update(
                                        timein=inout, employee_id_id=empId, status="LATE", remarks="TIMED IN", lateMin=TimeIntotalMin)

                        else:
                            if EmployeeAttendance.objects.filter(todaydate=datetime.today()).filter(employee_id_id=empId).exists():
                                if EmployeeAttendance.objects.filter(timein__isnull=True).filter(todaydate=datetime.today()):
                                    EmployeeAttendance.objects.filter(todaydate=datetime.today()).filter(
                                        employee_id_id=empId).update(
                                        timein=inout, employee_id_id=empId, status="TIME IN", remarks="TIMED IN", lateMin=0)

                    messages.success(request, 'Timed In Successfully!')
                    return redirect('attendance')

                else:
                    if EmployeeAttendance.objects.filter(todaydate=datetime.today()).filter(employee_id_id=empId).exists():
                        if EmployeeAttendance.objects.filter(timeout__isnull=True).filter(todaydate=datetime.today()):

                            getTimeIn = EmployeeAttendance.objects.filter(todaydate=datetime.today()).filter(
                                employee_id_id=empId).values_list('timein', flat=True)

                            # TOTAL HOURS CALCULATIONS
                            for a in getTimeIn:

                                SubtotalTime = a.strftime(
                                    "%H:%M:%S")
                                totalTime = datetime.strptime(
                                    SubtotalTime, "%H:%M:%S")

                                totaldelta = start_time - totalTime

                                sec = totaldelta.total_seconds()
                                min = sec / 60
                                hours = sec / (60 * 60)

                                TimeOuttotalHour = int(hours)

                                if EmployeeAttendance.objects.filter(timeout__isnull=False):
                                    EmployeeAttendance.objects.filter(todaydate=datetime.today()).filter(
                                        employee_id_id=empId).update(timeout=inout, employee_id_id=empId, status="TIMED OUT", remarks="ABSENT", hours=TimeOuttotalHour)
                                else:
                                    EmployeeAttendance.objects.filter(todaydate=datetime.today()).filter(
                                        employee_id_id=empId).update(timeout=inout, employee_id_id=empId, status="TIMED OUT", remarks="PRESENT", hours=TimeOuttotalHour)

                                print("Total Min: " + str(min))

                            messages.success(
                                request, 'Timed Out Successfully!')

                            return redirect('attendance')
                        else:
                            messages.success(request, 'Already Timed Out!')
                            return redirect('attendance')
                    else:
                        messages.success(request, 'You did not Time In!')
                        return redirect('attendance')


class admin_screen_view(LoginRequiredMixin, View):
    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        user = request.user
        if user.role == "admin":
            employee = Employee.objects.all()
            totalEmp = Employee.objects.count()
            totalDept = Department.objects.count()
            totalDesg = Designation.objects.count()
            totalPresent = EmployeeAttendance.objects.filter(todaydate=datetime.today()).filter(
                timein__isnull=False, timeout__isnull=False).count()
            todayAbsent = EmployeeAttendance.objects.filter(todaydate=datetime.today()).filter(
                remarks="ABSENT").count()
            schedule = EmployeeSchedule.objects.all()
            context = {
                'empl': employee,
                'totalEmp': totalEmp,
                'totalDept': totalDept,
                'totalDesg': totalDesg,
                'totalPresent': totalPresent,
                'todayAbsent': todayAbsent,
                'sched': schedule
            }
            return render(request, 'admin/index.html', context)
        else:
            print("not admin!")
            return render(request, 'restrict-content.html', {})


def logout_screen_view(request):
    logout(request)
    return redirect('admin-login')


def choose_screen_view(request):
    return render(request, 'admin/choose.html')


class register_screen_view(View):
    def get(self, request):
        accoff = AccountOfficer.objects.all()
        context = {
            'accoff': accoff
        }
        return render(request, 'admin/register.html', context)

    def post(self, request):
        form = AccountOfficerForm(request.POST)
        email = request.POST.get("email")
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        password = request.POST.get("password")
        form = AccountOfficer(email=email, username=username,
                              firstname=firstname, password=password)
        form.save()

        return redirect('account-officer')


# def accoff_login_screen_view(request):
#     if (request.method == 'GET'):
#         return render(request, 'admin/accofficerlogin.html')
#     else:

#         email = request.POST['email']
#         password = request.POST['password']
#         intakes = AccountOfficer.objects.all().filter(email=email, password=password)

#         for intake in intakes:

#             if intake.email == email and intake.password == password:
#                 return render(request, "admin/employee/attendance-employee.html")
#             else:
#                 return render(request, "admin/register.html")

def accoff_login_screen_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('employee-schedule')

    if request.method == 'POST':
        form = AccountOfficerForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('employee-schedule')
        else:
            messages.info(request, 'Email or Password do not match!')
            return redirect('account-officer')
    else:
        form = AccountOfficerForm()

    context['form'] = form
    return render(request, 'admin/accofficerlogin.html', context)

# AUTHENTICATION


def login_screen_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('admin-dashboard')

    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user is not None:

                if user.role == "admin":
                    login(request, user)
                    return redirect('admin-dashboard')
                else:
                    login(request, user)
                    return redirect('employee-schedule')
        else:
            messages.info(request, 'Email or Password do not match!')
            return redirect('admin-login')
    else:
        form = AccountAuthenticationForm()

    context['form'] = form
    return render(request, 'admin/login.html', context)


# END AUTHENTICATION

# EMPLOYEE


class all_employee_screen_view(LoginRequiredMixin, View):

    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        if 'SearchEmp' in request.GET:
            q1 = request.GET['q1']
            q2 = request.GET['q2']
            q3 = request.GET['q3']
            # multiQ = Q(Q(employee_id__icontains=q) & Q(firstname__icontains=q) )

            if q1 and q2 != '':
                employee = Employee.objects.filter(employee_id=q1).filter(
                    Q(firstname=q2) | Q(lastname=q2))
                department = Department.objects.all()
                designation = Designation.objects.all()

            elif q1 and q3 != '':
                employee = Employee.objects.filter(
                    employee_id=q1).filter(designation_name=q3)
                department = Department.objects.all()
                designation = Designation.objects.all()

            elif q2 and q3 != '':
                employee = Employee.objects.filter(Q(Q(firstname=q2) | Q(
                    lastname=q2))).filter(designation_name=q3)
                department = Department.objects.all()
                designation = Designation.objects.all()

            else:
                if q3 == '':
                    employee = Employee.objects.filter(Q(Q(
                        firstname=q2) | Q(lastname=q2))) or Employee.objects.filter(Q(employee_id=q1))
                else:
                    employee = Employee.objects.filter(designation_name=q3)
                department = Department.objects.all()
                designation = Designation.objects.all()
            # print(employee)
            # department = Department.objects.all()
            # designation = Designation.objects.all()
        else:
            department = Department.objects.all()
            designation = Designation.objects.all()
            employee = Employee.objects.all()

        context = {
            'dept': department,
            'desig': designation,
            'empl': employee,
        }

        return render(request, 'admin/employee/employees.html', context)

    def post(self, request):
        form = EmployeeForm(request.POST)
        formEme = PrimaryEmergencyContacts(request.POST)
        SalaryForm = EmployeeSalaryForm(request.POST)

        if request.method == 'POST':
            if 'btnSubmitEmployee' in request.POST:
                default_schedStart = datetime.now().replace(
                    hour=8, minute=0, second=0, microsecond=0)
                default_schedEnd = datetime.now().replace(
                    hour=17, minute=0, second=0, microsecond=0)
                empid = request.POST['employee_id']
                # finalemp = "EMP" + str(empid)
                firstName = request.POST['firstname_text']
                lastName = request.POST['lastname_text']
                userName = request.POST['username_text']
                emailPost = request.POST['email_text']
                gender = request.POST['gender_text']
                address = "Edit your Address"
                phonePost = request.POST['phone_text']
                designationPost = request.POST['designation_text']
                EmeName = "Edit Emergency Contact"
                EmeRela = "Edit Emergency Contact"
                EmePhone = "Edit Emergency Contact"

                form = Employee(employee_id=empid, firstname=firstName, lastname=lastName, username=userName, email=emailPost,
                                phone=phonePost, designation_name_id=designationPost, gender=gender, address=address, sched_start=default_schedStart, sched_end=default_schedEnd)
                form.save()

                formEme = PrimaryEmergencyContacts(
                    employee_id_id=empid, name=EmeName, relationship=EmeRela, phone=EmePhone)
                formEme.save()

                SalaryForm = EmployeeSalary(base_salary=0,
                                            daily_rate=0, gross_salary=0, employee_id_id=empid, pag_ibig=0, philhealth=0, sss=0, net_salary=0)
                SalaryForm.save()

                messages.success(request, "Employee successfully Added!")
                return redirect('all-employee')

            if 'btnUpdateEmp' in request.POST:
                eid = request.POST.get("emplID")
                fname = request.POST.get("firstname_update")
                lname = request.POST.get("lastname_update")
                uname = request.POST.get("username_update")
                emailUp = request.POST.get("email_update")
                phoneUp = request.POST.get("phone_update")
                # departmentUp = request.POST.get("department_name")
                designationUp = request.POST.get("designation_name")
                # idemp = request.POST.get("empid_update")

                Employee.objects.filter(employee_id=eid).update(firstname=fname, lastname=lname,
                                                                username=uname, email=emailUp, phone=phoneUp, designation_name_id=designationUp)
                messages.success(request, "Employee " +
                                 eid + " successfully Updated!")
                return redirect('all-employee')

    @staticmethod
    def deleteEmp(request, id):
        emp = Employee.objects.get(employee_id=id)
        emp.delete()
        messages.success(request, "Employee successfully Deleted!")
        return redirect('all-employee')


class employee_list_screen_view(LoginRequiredMixin, View):
    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        if 'SearchEmp' in request.GET:
            q1 = request.GET['q1']
            q2 = request.GET['q2']
            q3 = request.GET['q3']
            print(q3)
            # multiQ = Q(Q(employee_id__icontains=q) & Q(firstname__icontains=q) )
            if q1 and q2 != '':
                employee = Employee.objects.filter(employee_id=q1).filter(
                    Q(firstname=q2) | Q(lastname=q2))
                department = Department.objects.all()
                designation = Designation.objects.all()

            elif q1 and q3 != '':
                employee = Employee.objects.filter(
                    employee_id=q1).filter(designation_name=q3)
                department = Department.objects.all()
                designation = Designation.objects.all()

            elif q2 and q3 != '':
                employee = Employee.objects.filter(Q(Q(firstname=q2) | Q(
                    lastname=q2))).filter(designation_name=q3)
                department = Department.objects.all()
                designation = Designation.objects.all()

            else:
                if q3 == '':
                    employee = Employee.objects.filter(Q(Q(
                        firstname=q2) | Q(lastname=q2))) or Employee.objects.filter(Q(employee_id=q1))
                else:
                    employee = Employee.objects.filter(designation_name=q3)
                department = Department.objects.all()
                designation = Designation.objects.all()
            # print(employee)
            # department = Department.objects.all()
            # designation = Designation.objects.all()
        else:
            department = Department.objects.all()
            designation = Designation.objects.all()
            employee = Employee.objects.all()

        context = {
            'dept': department,
            'desig': designation,
            'empl': employee,
        }
        return render(request, 'admin/employee/employees-list.html', context)

    def post(self, request):
        form = EmployeeForm(request.POST)
        if request.method == 'POST':
            if 'btnSubmitEmployee' in request.POST:
                default_schedStart = datetime.now().replace(
                    hour=8, minute=0, second=0, microsecond=0)
                default_schedEnd = datetime.now().replace(
                    hour=17, minute=0, second=0, microsecond=0)
                empid = request.POST['employee_id']
                #finalemp = "EMP" + str(empid)
                firstName = request.POST['firstname_text']
                lastName = request.POST['lastname_text']
                userName = request.POST['username_text']
                emailPost = request.POST['email_text']
                # passwordPost = request.POST['password_text']
                # password2 = request.POST['password2_text']
                gender = request.POST['gender_text']
                address = "Edit your Address here"
                phonePost = request.POST['phone_text']
                designationPost = request.POST['designation_text']
                # departmentPost = request.POST['department_text']
                # hashed_pw = make_password(password2)
                form = Employee(employee_id=empid, firstname=firstName, lastname=lastName, username=userName, email=emailPost,
                                phone=phonePost, designation_name_id=designationPost, gender=gender, address=address, sched_start=default_schedStart, sched_end=default_schedEnd)
                form.save()
                messages.success(request, "Employee successfully Added!")
                return redirect('employee-list')

            if 'btnUpdateEmp' in request.POST:
                eid = request.POST.get("emplID")
                fname = request.POST.get("firstname_update")
                lname = request.POST.get("lastname_update")
                uname = request.POST.get("username_update")
                emailUp = request.POST.get("email_update")
                phoneUp = request.POST.get("phone_update")
                # departmentUp = request.POST.get("department_name")
                designationUp = request.POST.get("designation_name")
                # idemp = request.POST.get("empid_update")

                Employee.objects.filter(employee_id=eid).update(firstname=fname, lastname=lname,
                                                                username=uname, email=emailUp, phone=phoneUp, designation_name_id=designationUp)
                messages.success(request, "Employee " +
                                 eid + " successfully Updated!")
                return redirect('employee-list')


class profile_screen_view(LoginRequiredMixin, View):

    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        employee = Employee.objects.all()
        department = Department.objects.all()
        designation = Designation.objects.all()
        emergency = PrimaryEmergencyContacts.objects.all()
        attendanceFilter = EmployeeAttendance.objects.filter(
            employee_id_id=id)

        today = date.today().month

        salaryList = EmployeeSalary.objects.filter(employee_id_id=id)

        for sal in salaryList:
            baseSalary = sal.base_salary
            dailyRate = sal.daily_rate
            grossSalary = sal.gross_salary
            pagibig = sal.pag_ibig
            philhealth = sal.philhealth
            sss = sal.sss
            netSalary = sal.net_salary

        print(baseSalary)
        print(dailyRate)
        print(grossSalary)

        # employeeFilter = Employee.objects.filter(
        #     employee_id=id)

        # CALCULATE No. Working Days
        weekday_count = 0
        cal = calendar.Calendar()

        current_year = date.today().year
        current_month = date.today().month

        today_month = calendar.month_name[current_month]

        absent = EmployeeAttendance.objects.filter(employee_id_id=id).filter(
            status="NONE").filter(todaydate__month__lte=today).filter(remarks="ABSENT").count()

        for week in cal.monthdayscalendar(current_year, current_month):
            for i, day in enumerate(week):
                # not this month's day or a weekend
                if day == 0 or i >= 6:
                    continue
                # or some other control if desired..
                weekday_count += 1

        if 'btnAttendanceSearch' in request.GET:
            searchDate = request.GET['selectDate']
            searchYear = request.GET['searchYear']
            searchMonth = request.GET['searchMonth']
            employee = Employee.objects.all()
            if searchDate != '':
                #date = EmployeeAttendance.objects.filter(todaydate=searchDate)
                attendanceFilter = EmployeeAttendance.objects.filter(
                    employee_id_id=id, todaydate=searchDate)

                absent = EmployeeAttendance.objects.filter(employee_id_id=id).filter(
                    status="NONE").filter(todaydate=searchDate).filter(remarks="ABSENT").count()

            elif searchYear != '':
                # date = EmployeeAttendance.objects.filter(
                # todaydate__year__gte=searchYear, todaydate__year__lte=searchYear)
                attendanceFilter = EmployeeAttendance.objects.filter(
                    employee_id_id=id, todaydate__year__gte=searchYear, todaydate__year__lte=searchYear)

                absent = EmployeeAttendance.objects.filter(employee_id_id=id).filter(
                    status="NONE").filter(todaydate__year__gte=searchYear, todaydate__year__lte=searchYear).filter(remarks="ABSENT").count()

            elif searchMonth != '':
                # date = EmployeeAttendance.objects.filter(
                #     todaydate__month__gte=searchMonth, todaydate__month__lte=searchMonth)
                attendanceFilter = EmployeeAttendance.objects.filter(
                    employee_id_id=id, todaydate__month__gte=searchMonth, todaydate__month__lte=searchMonth)

                absent = EmployeeAttendance.objects.filter(employee_id_id=id).filter(
                    status="NONE").filter(todaydate__month__gte=searchMonth, todaydate__month__lte=searchMonth).filter(remarks="ABSENT").count()

            elif searchYear and searchMonth != '':
                # date = EmployeeAttendance.objects.filter(
                #     todaydate__year__gte=searchYear, todaydate__month__gte=searchMonth, todaydate__year__lte=searchYear, todaydate__month__lte=searchMonth)
                attendanceFilter = EmployeeAttendance.objects.filter(
                    employee_id_id=id, todaydate__year__gte=searchYear, todaydate__month__gte=searchMonth, todaydate__year__lte=searchYear, todaydate__month__lte=searchMonth)

                absent = EmployeeAttendance.objects.filter(employee_id_id=id).filter(
                    status="NONE").filter(todaydate__year__gte=searchYear, todaydate__month__gte=searchMonth, todaydate__year__lte=searchYear, todaydate__month__lte=searchMonth).filter(remarks="ABSENT").count()

        else:

            employee = Employee.objects.all()
            #empatt = EmployeeAttendance.objects.all()
            today = datetime.today().month
            # totalMin = EmployeeAttendance.objects.values('timein')

            # FILTER FOR KINSENAS
            if 'kinsenas1' in request.GET:
                attendanceFilter = EmployeeAttendance.objects.filter(employee_id_id=id, todaydate__range=[
                                                                     datetime.now().replace(day=1), datetime.now().replace(day=15)])

                absent = EmployeeAttendance.objects.filter(employee_id_id=id).filter(
                    status="NONE").filter(todaydate__range=[datetime.now().replace(day=1), datetime.now().replace(day=15)]).filter(remarks="ABSENT").count()

            elif 'kinsenas2' in request.GET:
                attendanceFilter = EmployeeAttendance.objects.filter(employee_id_id=id, todaydate__range=[
                                                                     datetime.now().replace(day=16), datetime.now().replace(day=31)])
                absent = EmployeeAttendance.objects.filter(employee_id_id=id).filter(
                    status="NONE").filter(todaydate__range=[
                        datetime.now().replace(day=16), datetime.now().replace(day=31)]).filter(remarks="ABSENT").count()

            else:
                attendanceFilter = EmployeeAttendance.objects.filter(
                    employee_id_id=id, todaydate__month__gte=today, todaydate__month__lte=today)

            # END FILTER FOR KINSENAS

        context = {
            'id': id,
            'dept': department,
            'desig': designation,
            'empl': employee,
            'eme': emergency,
            # 'empatt': date,
            'attid': attendanceFilter,
            # 'empfil': employeeFilter,
            'workingDays': weekday_count,
            'todayMonth': today_month,
            'salary': salaryList,
            'baseSal': baseSalary,
            'dailyRat': dailyRate,
            'grossSal': grossSalary,
            'pagibig': pagibig,
            'philhealth': philhealth,
            'sss': sss,
            'netSalary': netSalary,
            'absent': absent,
        }

        return render(request, 'admin/employee/profile.html', context)

    def post(self, request, id):

        form = EmergencyContactForm(request.POST)
        SalaryForm = EmployeeSalaryForm(request.POST)

        if request.method == 'POST':

            if 'btnSaveSalary' in request.POST:
                salary = request.POST.get("salary_input")
                daily = request.POST.get("daily_input")
                gross = request.POST.get("gross_input")
                pagibig = request.POST.get("pagibig_input")
                philhealth = request.POST.get("philhealth_input")
                sss = request.POST.get("sss_input")
                netSal = request.POST.get("net_input")

                EmployeeSalary.objects.filter(employee_id_id=id).update(
                    base_salary=salary, daily_rate=daily, gross_salary=gross, pag_ibig=pagibig, philhealth=philhealth, sss=sss, net_salary=netSal)

                messages.success(request, "Salary successfully Updated!")

                return redirect('profile', id)

            if 'btnEditProfile' in request.POST:
                fname = request.POST.get("firstname_profile")
                lname = request.POST.get("lastname_profile")
                # uname = request.POST.get("username_profile")
                # emailProf = request.POST.get("email_update")
                phoneProf = request.POST.get("phone_profile")
                # departmentProf = request.POST.get("depart_name")
                designationProf = request.POST.get("desig_name")
                # idempProf = request.POST.get("empid_update")
                gender = request.POST.get("gender")
                birthD = request.POST.get("BirthDate")
                address = request.POST.get("address")
                state = request.POST.get("state")
                country = request.POST.get("country")

                Employee.objects.filter(employee_id=id).update(firstname=fname, lastname=lname, phone=phoneProf,
                                                               designation_name_id=designationProf, gender=gender, address=address, state=state, country=country, birthDate=birthD)
                messages.success(request, "Profile successfully Updated!")
                return redirect('profile', id)

            if 'btnEditPersonal' in request.POST:
                passNum = request.POST.get("passportNo")
                passExpiry = request.POST['passExpiryDate']
                Nationality = request.POST.get("nationality")
                Religion = request.POST.get("religion")
                MStatus = request.POST.get("MaritalStatus")
                child = request.POST.get("Children")

                Employee.objects.filter(employee_id=id).update(passNo=passNum, passExp=passExpiry,
                                                               nationality=Nationality, religion=Religion, maritalStatus=MStatus, children=child)
                messages.success(
                    request, "Personal Information successfully Updated!")
                return redirect('profile', id)

            if 'btnEditEmergency' in request.POST:
                Name = request.POST.get("Name")
                relation = request.POST.get("Relationship")
                Phone = request.POST.get("Phone")

                if PrimaryEmergencyContacts.objects.filter(employee_id_id=id).exists():
                    PrimaryEmergencyContacts.objects.filter(employee_id_id=id).update(
                        name=Name, relationship=relation, phone=Phone)
                    messages.success(
                        request, "Personal Information successfully Updated!")
                    return redirect('profile', id)
                else:
                    form = PrimaryEmergencyContacts(
                        employee_id_id=id, name=Name, relationship=relation, phone=Phone)
                    form.save()
                    messages.success(
                        request, "Personal Information successfully Updated!")
                    return redirect('profile', id)


def holidays_screen_view(request):
    return render(request, 'admin/employee/holidays.html')


def leaves_admin_screen_view(request):
    return render(request, 'admin/employee/leaves-admin.html')


def leaves_employee_screen_view(request):
    return render(request, 'admin/employee/leaves-employee.html')


def leaves_settings_screen_view(request):
    return render(request, 'admin/employee/leaves-settings.html')


def attendance_admin_screen_view(request):
    return render(request, 'admin/employee/attendance-admin.html')

# INITIAL ATTENDANCE - ACCESS THIS PAGE FOR PARTIAL ATTENDANCE OF THE EMPLOYEE


class initial_attendance_view(LoginRequiredMixin, View):
    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        emp = Employee.objects.all()
        att = EmployeeAttendance.objects.all()

        for employee in emp:
            print("SAVE")
            form = EmployeeAttendance(
                employee_id_id=employee.employee_id, status="NONE", remarks="ABSENT", hours=0, lateMin=0)
            form.save()

        context = {
            'emp': emp,
        }

        # return render(request, 'admin/employee/initial-attendance.html', context)
        return redirect('admin-dashboard')

    @staticmethod
    def initalTimein(request, id):
        empid = Employee.objects.get(employee_id=id)

        form = EmployeeAttendance(
            employee_id_id=empid.employee_id, status="NONE")

        form.save()

        messages.success(request, "Employee Timed in!")
        return redirect('initial-attendance')


class attendance_employee_screen_view(LoginRequiredMixin, View):
    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        if 'btnAttendanceSearch' in request.GET:
            searchDate = request.GET['selectDate']
            searchYear = request.GET['searchYear']
            searchMonth = request.GET['searchMonth']
            emp = Employee.objects.all()
            if searchDate != '':
                date = EmployeeAttendance.objects.filter(todaydate=searchDate)

            elif searchYear != '':
                date = EmployeeAttendance.objects.filter(
                    todaydate__year__gte=searchYear, todaydate__year__lte=searchYear)

            elif searchMonth != '':
                date = EmployeeAttendance.objects.filter(
                    todaydate__month__gte=searchMonth, todaydate__month__lte=searchMonth)

            elif searchYear and searchMonth != '':
                date = EmployeeAttendance.objects.filter(
                    todaydate__year__gte=searchYear, todaydate__month__gte=searchMonth, todaydate__year__lte=searchYear, todaydate__month__lte=searchMonth)

            else:
                today = datetime.today()
                date = EmployeeAttendance.objects.filter(todaydate=today)

        else:
            emp = Employee.objects.all()
            # empatt = EmployeeAttendance.objects.all()
            today = datetime.today()
            date = EmployeeAttendance.objects.filter(todaydate=today)
            # totalMin = EmployeeAttendance.objects.values('timein')

        context = {
            'emp': emp,
            'empatt': date,


        }
        return render(request, 'admin/employee/attendance-employee.html', context)


class departments_screen_view(LoginRequiredMixin, View):
    login_url = 'admin-login'
    login_url = 'account-officer'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        dept = Department.objects.all()
        context = {
            'dept': dept
        }

        return render(request, 'admin/employee/departments.html', context)

    def post(self, request):
        form = DepartmentForm(request.POST)
        if request.method == 'POST':
            if 'btnSubmitDepartment' in request.POST:
                department = request.POST['department_text']
                form = Department(department_name=department)
                form.save()
                messages.success(request, "Deparment successfully Added!")
                return redirect('departments')

            if 'btnDepartUpdate' in request.POST:
                departID = request.POST.get("deptID")
                departName = request.POST.get("depart_name")

                Department.objects.filter(id=departID).update(
                    department_name=departName)
                messages.success(request, "Deparment successfully Updated!")
                return redirect('departments')

    @staticmethod
    def deleteDepartment(request, id):
        depart = Department.objects.get(id=id)
        depart.delete()
        messages.success(request, "Deparment successfully Deleted!")
        return redirect('departments')


class designations_screen_view(LoginRequiredMixin, View):
    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        designation = Designation.objects.all()
        department = Department.objects.all()
        context = {
            'desig': designation,
            'dept': department
        }
        return render(request, 'admin/employee/designations.html', context)

    def post(self, request):
        form = DesignationForm(request.POST)
        if request.method == 'POST':
            if 'btnSubmitDesignation' in request.POST:
                designation = request.POST['designation_text']
                department = request.POST['department_text']
                form = Designation(designation_name=designation,
                                   department_name_id=department)
                form.save()
                messages.success(request, "Designation successfully Added!")
                return redirect('designations')

            if 'btndesigUpdate' in request.POST:
                desigid = request.POST.get("desigID")
                designame = request.POST.get("desig-name")
                departname = request.POST.get("depart-name")

                Designation.objects.filter(id=desigid).update(
                    designation_name=designame, department_name_id=departname)
                messages.success(request, "Designation successfully Updated!")
                return redirect('designations')

    @staticmethod
    def deleteDesig(request, id):
        desig = Designation.objects.get(id=id)
        desig.delete()
        messages.success(request, "Designation successfully Deleted!")
        return redirect('designations')


def timesheet_screen_view(request):
    return render(request, 'admin/employee/timesheet.html')


def shift_scheduling_screen_view(request):
    return render(request, 'admin/employee/shift-scheduling.html')


def overtime_screen_view(request):
    return render(request, 'admin/employee/overtime.html')


# START PAYROLL


def payroll_items_screen_view(request):
    return render(request, 'admin/payroll/payroll-items.html')


class salary_view_screen_view(View):
    def get(self, request, id):

        context = {

        }

        return render(request, 'admin/payroll/salary-view.html', context)

    @staticmethod
    def first_period(request, id):
        employee = Employee.objects.filter(employee_id=id)

        # GET DESIGNATION NAME
        for desig in employee:
            desigId = desig.designation_name_id

        designation = Designation.objects.filter(department_name_id=desigId)

        for role in designation:
            emp_role = role.designation_name

        # GET CURRENT DATE
        current_month = date.today().month

        today_month = calendar.month_name[current_month]
        todays_date = date.today()

        # PASS HEADER TO TEMPLATE
        payslip = "PAYSLIP FOR THE MONTH OF " + \
            today_month + " " + str(todays_date.year) + " (1st Period)"

        # GENERATE RANDOM NUMBER FOR PAYSLIP
        range_start = 10**(5-1)
        range_end = (10**5)-1
        payslip_number = randint(range_start, range_end)

        # Number to Words
        p = inflect.engine()

        # COUNT ABSENT FIRST PERIOD
        absent_first_period = EmployeeAttendance.objects.filter(employee_id_id=id).filter(
            status="NONE").filter(todaydate__range=[datetime.now().replace(day=1), datetime.now().replace(day=15)]).filter(remarks="ABSENT").count()

        # SUM TOTAL MINUTES LATE
        late_first_period = 0
        late_first_period = EmployeeAttendance.objects.filter(employee_id_id=id).filter(todaydate__range=[
            datetime.now().replace(day=1), datetime.now().replace(day=15)]).aggregate(TOTAL=Sum('lateMin'))['TOTAL']

        # PASS SALARY DETAILS
        salary = EmployeeSalary.objects.filter(employee_id_id=id)

        for sal in salary:
            base_salary = sal.base_salary
            daily_rate = sal.daily_rate
            gross_rate = sal.gross_salary
            pagibig = sal.pag_ibig
            philhealth = sal.philhealth
            sss = sal.sss

        absent_deductions = daily_rate * absent_first_period
        total_deductions = pagibig + philhealth + \
            sss + absent_deductions + late_first_period

        net_salary = int((gross_rate / 2) - total_deductions)

        context = {
            'id': id,
            'employee': employee,
            'emp_role': emp_role,
            'payslip': payslip,
            'today_month': today_month,
            'today_year':  str(todays_date.year),
            'payslip_number': payslip_number,
            'base_salary': base_salary,
            'daily_rate': daily_rate,
            'gross_rate': gross_rate,
            'pagibig': pagibig,
            'philhealth': philhealth,
            'sss': sss,
            'total_deductions': total_deductions,
            'net_salary': net_salary,
            'word_salary': p.number_to_words(net_salary),
            'absent_first_period': absent_first_period,
            'absent_deductions': absent_deductions,
            'late_first_period': str(late_first_period),
            'first_period_salary': int(base_salary/2),
        }

        return render(request, 'admin/payroll/salary-view.html', context)

    @staticmethod
    def second_period(request, id):
        employee = Employee.objects.filter(employee_id=id)

        # GET DESIGNATION NAME
        for desig in employee:
            desigId = desig.designation_name_id

        designation = Designation.objects.filter(department_name_id=desigId)

        for role in designation:
            emp_role = role.designation_name

        # GET CURRENT DATE
        current_month = date.today().month

        today_month = calendar.month_name[current_month]
        todays_date = date.today()

        # PASS HEADER TO TEMPLATE
        payslip = "PAYSLIP FOR THE MONTH OF " + \
            today_month + " " + str(todays_date.year) + " (2nd Period)"

        # GENERATE RANDOM NUMBER FOR PAYSLIP
        range_start = 10**(5-1)
        range_end = (10**5)-1
        payslip_number = randint(range_start, range_end)

        # Number to Words
        p = inflect.engine()

        # COUNT ABSENT SECOND PERIOD
        absent_second_period = EmployeeAttendance.objects.filter(employee_id_id=id).filter(
            status="NONE").filter(todaydate__range=[
                datetime.now().replace(day=16), datetime.now().replace(day=31)]).filter(remarks="ABSENT").count()

        # SUM TOTAL MINUTES LATE
        late_second_period = EmployeeAttendance.objects.filter(employee_id_id=id).filter(todaydate__range=[
            datetime.now().replace(day=16), datetime.now().replace(day=31)]).aggregate(TOTAL=Sum('lateMin'))['TOTAL']

        # PASS SALARY DETAILS
        salary = EmployeeSalary.objects.filter(employee_id_id=id)

        for sal in salary:
            base_salary = sal.base_salary
            daily_rate = sal.daily_rate
            gross_rate = sal.gross_salary
            pagibig = sal.pag_ibig
            philhealth = sal.philhealth
            sss = sal.sss

        absent_deductions = daily_rate * absent_second_period

        total_deductions = pagibig + philhealth + \
            sss + absent_deductions + late_second_period

        net_salary = int((gross_rate / 2) - total_deductions)

        context = {
            'id': id,
            'employee': employee,
            'emp_role': emp_role,
            'payslip': payslip,
            'today_month': today_month,
            'today_year':  str(todays_date.year),
            'payslip_number': payslip_number,
            'base_salary': base_salary,
            'daily_rate': daily_rate,
            'gross_rate': gross_rate,
            'pagibig': pagibig,
            'philhealth': philhealth,
            'sss': sss,
            'total_deductions': total_deductions,
            'net_salary': net_salary,
            'word_salary': p.number_to_words(net_salary),
            'absent_first_period': absent_second_period,
            'absent_deductions': absent_deductions,
            'late_first_period': str(late_second_period),
            'first_period_salary': int(base_salary/2),
        }

        return render(request, 'admin/payroll/salary-view.html', context)


class salary_screen_view(View):
    def get(self, request):
        employee = Employee.objects.all()
        context = {
            'empl': employee,
        }
        return render(request, 'admin/payroll/salary.html', context)

# END PAYROLL

# SCHEDULE


class employee_schedule_view(LoginRequiredMixin, View):
    login_url = 'admin-login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        schedule = EmployeeSchedule.objects.all()
        context = {
            'schedules': schedule,
        }
        return render(request, 'admin/employee/employees-schedule.html', context)

    def post(self, request):
        schedule = EmployeeSchedule.objects.all()
        form = EmployeeScheduleForm(request.POST)
        if "btnSubmitSchedule" in request.POST:
            schedin = request.POST.get("schedule_in")
            schedout = request.POST.get("schedule_out")

            inS = datetime.combine(datetime.now(), datetime.strptime(
                schedin + "000", "%H:%M:%S.%f").time())
            outS = datetime.combine(datetime.now(), datetime.strptime(
                schedout + "000", "%H:%M:%S.%f").time())

            form = EmployeeSchedule(timein=inS, timeout=outS)
            form.save()

            messages.success(request, "Schedule successfully Added!")
            return redirect('employee-schedule')

        if "activate" in request.POST:
            id = request.POST.get("activate")
            schedin = schedule.filter(id=id).values_list("timein")
            schedout = schedule.filter(id=id).values_list("timeout")

            for empShed in schedule:
                if empShed.id != id:
                    EmployeeSchedule.objects.filter(id=empShed.id).exclude(
                        id=id).update(status="INACTIVE")

            EmployeeSchedule.objects.filter(id=id).update(status="ACTIVE")
            messages.success(request, "Schedule successfully Activated!")

            Employee.objects.all().update(sched_start=schedin, sched_end=schedout)
            return redirect('employee-schedule')

        if "deactivate" in request.POST:
            id = request.POST.get("deactivate")

            EmployeeSchedule.objects.filter(id=id).update(status="INACTIVE")
            messages.success(request, "Schedule successfully Deactivated!")
            return redirect('employee-schedule')

# START OF REPORT VIEWS


def employee_reports_screen_view(request):
    return render(request, 'admin/reports/employee_reports.html', {})


def payslip_report_screen_view(request):
    return render(request, 'admin/reports/payslip_report.html', {})


def attendance_report_screen_view(request):
    return render(request, 'admin/reports/attendance_report.html', {})


def leave_report_screen_view(request):
    return render(request, 'admin/reports/leave_report.html', {})


def daily_report_screen_view(request):
    return render(request, 'admin/reports/daily_report.html', {})


def overtime_report_screen_view(request):
    return render(request, 'admin/reports/overtime_report.html', {})

# END OF REPORT VIEWS


# Final Exam Requirement


def landing_page_view(request):
    return render(request, 'home/home.html', {})


def gallery_view(request):
    return render(request, 'admin/employees/Chua', {})
