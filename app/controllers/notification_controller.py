# app/controllers/notification_controller.py
# Notification pages for user notification settings.

from flask import render_template


def show_notifications():
    return render_template('notifications/notifications.html')


def show_notification_settings():
    return render_template('notifications/notification_settings.html')
