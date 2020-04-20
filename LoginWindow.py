# -*- coding: utf-8 -*-


from threading import Thread
import requests
import settings
from PySide2 import QtWidgets
import vk_api

import time
class LoginDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        self._appId=6121396
        self._twoFactorAuthenticationIsComplete=False
        self.auth=False
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Login')

        self.loginEdit=QtWidgets.QLineEdit()
        self.passwordEdit=QtWidgets.QLineEdit()

        self.twofactorcodeEdit=QtWidgets.QLineEdit()

        self.infoLabel=QtWidgets.QLabel("Авторизация")
        self.passwordLabel=QtWidgets.QLabel("Введите пароль")
        self.loginLabel=QtWidgets.QLabel("Введите логин")
       
        self.loginButton = QtWidgets.QPushButton('Авторизация')
        self.captchaSendButton=QtWidgets.QPushButton("Авторизация")

        self.sendTwoFactorCodeButton=QtWidgets.QPushButton("Продолжить")
        self.sendTwoFactorCodeButton.clicked.connect(self.send_two_factor_auntification_Code_click)
        
       
        self.loginLayout = QtWidgets.QVBoxLayout()

        self.loginLayout.addWidget(self.loginLabel)
        self.loginLayout.addWidget(self.loginEdit)
        self.loginLayout.addWidget(self.passwordLabel)
        self.loginLayout.addWidget(self.passwordEdit)
      
        self.proxyAdressEdit=QtWidgets.QLineEdit()
        self.proxyLabel=QtWidgets.QLabel("Прокси адресс")
        self.loginLayout.addWidget(self.proxyLabel)
        self.loginLayout.addWidget(self.proxyAdressEdit)
        self.loginLayout.addWidget(self.loginButton)
        self.loginButton.clicked.connect(self.start_login_thread)
        self.setLayout(self.loginLayout)
        self.passwordEdit.setEchoMode(self.passwordEdit.PasswordEchoOnEdit)
       
        
      
        
       


    def start_login_thread(self):
         t =Thread(target= self.login)
         t.isDaemon=True
         t.start()
         
    def clearWidget(self):
        for i in range(0,self.loginLayout.count()):
            self.loginLayout.itemAt(i).widget().deleteLater()

    def login(self):
        vkSession= vk_api.VkApi(app_id=self._appId,login=self.loginEdit.text(),password=self.passwordEdit.text(),
        auth_handler=self.two_factor_handler,scope=268972043)
        try:
            vkSession.auth()
            settings.access_token=vkSession.token['access_token']
            settings.userid=vkSession.token['user_id']
            self.auth=True
        except vk_api.exceptions.BadPassword:
            print("Вы неверный логин или пароль")
        except vk_api.exceptions.AuthError:
            print("Ошибка авторизации")

    def send_two_factor_auntification_Code_click(self):
        self._twoFactorAuthenticationIsComplete=True
    
    def two_factor_handler(self):
        self.clearWidget()
        self._twoFactorAuthenticationIsComplete=False
        self.infoLabel.text ="Введите код:"
        self.loginLayout.addWidget(self.infoLabel)
        self.loginLayout.addWidget(self.twofactorcodeEdit)
        self.loginLayout.addWidget(self.sendTwoFactorCodeButton)
        while self._twoFactorAuthenticationIsComplete==False:
            time.sleep(0.5)
        code=self.twofactorcodeEdit.text()
        if self.checkData(code)==False:
            return 0,False
        return int(code),False

    def checkData(self,data):
        try:
            int(data)
            return True
        except: return False
            


        
       
      
   


        
        
       

    
   
  
  