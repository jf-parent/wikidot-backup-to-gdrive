#! -*- coding: utf-8 -*-

from time import sleep

import requests

class App(object):
    def __init__(self, pdriver):
        self.pdriver = pdriver

    def go_to_backup_page(self):
        self.pdriver.info_log("Going to backup page...")

        self.pdriver.find("sv:nav_security_btn").click()

        self.pdriver.wait_until_visible("sv:nav_backup_btn")
        self.pdriver.find("sv:nav_backup_btn").click()

    def create_backup(self):
        self.pdriver.info_log("Creating backup...")

        self.pdriver.wait_until_visible("sv:create_backup_btn")
        self.pdriver.find("sv:create_backup_btn").click()

        self.pdriver.find("sv:backup_type_zip_btn").click()

        self.pdriver.find("sv:effective_create_backup_btn").click()

        for _ in range(60 * 5):
            ret = self.pdriver.wait_until_visible("sv:refresh_status_btn", raise_exception = False)
            if ret:
                self.pdriver.find("sv:refresh_status_btn").click()
                if self.pdriver.is_visible("sv:completed_status_div"):
                    break
                else:
                    self.pdriver.info_log("Waiting for the backup to be completed")
                    sleep(5)
            else:
                break

    def download_backup(self):
        self.pdriver.info_log("Downloading the backup...")

        url = self.pdriver.find("sv:backup_url").get_attribute('href')

        with open('wikidot-backup.zip', 'wb') as handle:
            response = requests.get(url, stream=True)

            for block in response.iter_content(1024):
                handle.write(block)

    def login(self, user):
        self.pdriver.info_log("Login with %s..."%user)

        self.pdriver.get(self.pdriver.get_config_value("project:url"))

        self.pdriver.find("sv:signin_btn").click()

        current_window_handle = self.pdriver.current_window_handle
        for handle in self.pdriver.window_handles:
            if handle != current_window_handle:
                self.pdriver.switch_to_window(handle)
                break

        self.pdriver.wait_until_visible("sv:username_input", timeout = 10)
        self.pdriver.find("sv:username_input").send_keys(user.username)
        self.pdriver.find("sv:password_input").send_keys(user.password)

        self.pdriver.find("sv:login_btn").click()

        current_window_handle = self.pdriver.current_window_handle
        for handle in self.pdriver.window_handles:
            if handle != current_window_handle:
                self.pdriver.switch_to_window(handle)
                break

        self.pdriver.wait_until_visible("sv:dashboard_header_div", timeout = 30)
