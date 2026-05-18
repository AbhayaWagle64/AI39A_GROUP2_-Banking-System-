# app/controllers/bills_controller.py
# Controllers for bill payment pages.

from flask import render_template


def show_bill_history():
    return render_template('bills/bill_history.html')


def show_electricity_bill():
    return render_template('bills/electricity_bill.html')


def show_internet_bill():
    return render_template('bills/internet_bill.html')


def show_mobile_recharge():
    return render_template('bills/mobile_recharge.html')


def show_tv_bill():
    return render_template('bills/tv_bill.html')


def show_water_bill():
    return render_template('bills/water_bill.html')
