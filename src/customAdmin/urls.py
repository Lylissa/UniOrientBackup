"""Admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


from customAdmin.views import (
    attendance_screen_view,

    admin_screen_view,
    login_screen_view,
    logout_screen_view,

    accoff_login_screen_view,
    choose_screen_view,
    register_screen_view,

    # Employee View
    all_employee_screen_view,
    employee_list_screen_view,
    holidays_screen_view,
    leaves_admin_screen_view,
    leaves_employee_screen_view,
    leaves_settings_screen_view,
    attendance_admin_screen_view,
    attendance_employee_screen_view,
    departments_screen_view,
    designations_screen_view,
    timesheet_screen_view,
    shift_scheduling_screen_view,
    overtime_screen_view,
    profile_screen_view,


    # Reports View
    employee_reports_screen_view,
    payslip_report_screen_view,
    attendance_report_screen_view,
    leave_report_screen_view,
    daily_report_screen_view,
    overtime_report_screen_view,

    # Attendance
    initial_attendance_view,

    # Schedule
    employee_schedule_view,

    # Payroll View
    salary_screen_view,
    salary_view_screen_view,
    payroll_items_screen_view,

    # Final Exam Rquirement
    landing_page_view,

    # Face Recog Images
    gallery_view,
)


urlpatterns = [

    # FINAL EXAM REQUIREMENT
    path('landing-page', landing_page_view, name='landing-page'),

    # Face Recog Images
    path('gallery', gallery_view, name="gallery"),

    path('admin-dashboard', admin_screen_view.as_view(), name='admin-dashboard'),
    path('admin-login', login_screen_view, name='admin-login'),
    path('admin-logout', logout_screen_view, name='admin-logout'),

    path('account-officer', accoff_login_screen_view, name='account-officer'),
    path('choose', choose_screen_view, name='choose'),
    path('register', register_screen_view.as_view(), name='register'),

    # ATTENDANCE
    path('attendance', attendance_screen_view.as_view(), name='attendance'),
    path('initial-attendance', initial_attendance_view.as_view(),
         name='initial-attendance'),
    path('initial-timein/<int:id>',
         initial_attendance_view.initalTimein, name='initial-timein'),



    # EMPLOYEES TAB
    path('all-employee', all_employee_screen_view.as_view(), name='all-employee'),
    path('employee-list', employee_list_screen_view.as_view(), name='employee-list'),
    path('deleteEmployee/<int:id>',
         all_employee_screen_view.deleteEmp, name='deleteEmployee'),
    path('holidays', holidays_screen_view, name='holidays'),
    path('leaves-admin', leaves_admin_screen_view, name='leaves-admin'),
    path('leaves-employee', leaves_employee_screen_view, name='leaves-employee'),
    path('leaves-settings', leaves_settings_screen_view, name='leaves-settings'),
    path('attendance-admin', attendance_admin_screen_view, name='attendance-admin'),
    path('attendance-employee', attendance_employee_screen_view.as_view(),
         name='attendance-employee'),
    path('attendance-employee', attendance_employee_screen_view.as_view(),
         name='attendance-employee'),
    path('departments', departments_screen_view.as_view(), name='departments'),
    path('deleteDepart/<int:id>',
         departments_screen_view.deleteDepartment, name='deleteDepartment'),
    path('designations', designations_screen_view.as_view(), name='designations'),
    path('deleteDesig/<int:id>', designations_screen_view.deleteDesig,
         name='deleteDesignation'),
    path('timesheet', timesheet_screen_view, name='timesheet'),
    path('shift-scheduling', shift_scheduling_screen_view, name='shift-scheduling'),
    path('overtime', overtime_screen_view, name='overtime'),
    path('profile/<int:id>', profile_screen_view.as_view(), name="profile"),

    # SCHEDULE TAB
    path('employee-schedule', employee_schedule_view.as_view(),
         name='employee-schedule'),


    # REPORTS TAB
    path('employee-report', employee_reports_screen_view, name='employee-report'),
    path('payslip-report', payslip_report_screen_view, name='payslip-report'),
    path('attendance-report', attendance_report_screen_view,
         name='attendance-report'),
    path('leave-report', leave_report_screen_view, name='leave-report'),
    path('daily-report', daily_report_screen_view, name='daily-report'),
    path('overtime-report', overtime_report_screen_view, name='overtime-report'),

    # PAYROLL TAB
    path('salary-view/first-period/<int:id>',
         salary_view_screen_view.first_period, name='salary-view-first-period'),
    path('salary-view/second-period/<int:id>',
         salary_view_screen_view.second_period, name='salary-view-second-period'),
    path('payroll-items', payroll_items_screen_view, name='payroll-items'),
    path('salary', salary_screen_view.as_view(), name='salary'),
]
