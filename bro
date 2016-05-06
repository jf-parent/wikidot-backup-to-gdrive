#!/usr/bin/env python

import sys
import os
from datetime import datetime
import subprocess

from brome import Brome
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from mailer import Mailer, Message

from config.selector import selector_dict

HERE = os.path.abspath(os.path.dirname(__file__))

def upload_backup_to_gdrive(brome):
    backup_file = os.path.join(HERE, 'wikidot-backup.zip')
    if os.path.isfile(backup_file):
        gauth = GoogleAuth()

        gauth.LocalWebserverAuth()

        drive = GoogleDrive(gauth)

        now = datetime.now().strftime("%d-%m-%Y")
        gfile = drive.CreateFile({
                'title': "backup-wiki-%s.zip"%now,
                'parents': [{"id":brome.get_config_value("project:folder_id")}]
        })
        gfile.Upload()

        os.remove(backup_file)

        return True
    else:
        print 'No backup file found!'
        return False

def notify(brome, result):

    if result:
        message_text = "Backup succeeded!"
    else:
        message_text = "Backup failed!"

    if brome.get_config_value("project:notification_type") == 'mailer':
        message = Message(
                    From = brome.get_config_value('mailer:from'),
                    To = brome.get_config_value('mailer:to'),
                    charset = "utf-8"
        )

        message.Subject = message_text
        message.Html = message_text
        message.Body = message_text

        sender = Mailer(brome.get_config_value('mailer:smtp_server'))
        sender.send(message)

    elif brome.get_config_value("project:notification_type") == 'terminal-notifier':
        group_id = "'wikidot-backup-to-gdrive'"
        command = [
            "/usr/local/bin/terminal-notifier",
            "-message",
            "'%s'"%message_text,
            "-sound",
            "'default'",
            "-title",
            group_id,
            "-group",
            group_id,
            "-remove",
            group_id

        ]
        subprocess.call(" ".join(command), shell = True)

if __name__ == '__main__':

    brome = Brome(
        config_path = os.path.join(HERE, "config", "brome.yml"),
        selector_dict = selector_dict,
        browsers_config_path = os.path.join(HERE, "config", "browsers_config.yml"),
        absolute_path = HERE
    )

    brome.run(['-l', 'firefox', '-s', 'backup'])

    result = upload_backup_to_gdrive(brome)

    notify(brome, result)
