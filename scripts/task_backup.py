#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest
from model.user import User

class Test(BaseTest):

    name = 'Test'

    def run(self, **kwargs):

        self.info_log("Running...")

        user = User(
                    self.pdriver,
                    self.pdriver.get_config_value("project:username"),
                    self.pdriver.get_config_value("project:password")
        )

        self.app.login(user)

        self.app.go_to_backup_page()
        
        self.app.create_backup()
    
        self.app.download_backup()
