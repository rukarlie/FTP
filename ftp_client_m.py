from ftplib import FTP
from typing import Tuple
#from Ui_commonDialog import Ui_Dialog as cDilog
#from Ui_infoDialog import Ui_Dialog as iDialog
from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtWidgets import (QTableWidgetItem,  QFileDialog, QMessageBox, QDialog)
#from threading import Thread
import sys

class iDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 159)
        font = QtGui.QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "FTP - Инфо"))
        self.label.setText(_translate("Dialog", "TextLabel"))




class cDialog(object):
    def setupUi(self, Dialog:QtWidgets.QDialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(388, 138)
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap(":/icons/icons/sndspdIcon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #Dialog.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 90, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 30, 211, 16))
        self.label.setObjectName("label")
        self.inLine = QtWidgets.QLineEdit(Dialog)
        self.inLine.setGeometry(QtCore.QRect(110, 50, 210, 20))
        self.inLine.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.inLine.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.inLine.setObjectName("inLine")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog:QtWidgets.QDialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle( "Окно ввода данных")
        #Dialog.setWhatsThis(_translate("Dialog", "Окно ввода скорости звука для дальнейших расчётов"))
        self.label.setText(_translate("Dialog", "Введите :"))
        #self.sndSpd.setStatusTip(_translate("Dialog", "Введите скорость звука в км/с"))
        #self.sndSpd.setWhatsThis(_translate("Dialog", "Поле для ввода скорости звука"))
        self.inLine.setText(_translate("Dialog", ""))





ignore_symbol=['\n',' ', '\\n', '\t']
err_msg = "Что-то пошло не так \n"

class ftpHndlr:
    def __init__(self, MainWindow:QtWidgets.QMainWindow) -> None:
        self.dir_list=[]
        self.config_dir={}
        self.ftp:FTP
        self.mwindow= MainWindow
        self.isOpen=False
        try:
            with open('ftpconnection.cfg','r') as f:
                for l in f:
                    if '=' in l:
                        lst = list(l.split('='))
                        for i in range(len(lst)):
                            for ismb in ignore_symbol:
                                lst[i]=lst[i].replace(ismb,'')
                            
                        self.config_dir[lst[0]]=lst[1]
        except:
            msg=str(sys.exc_info()[1])
            self.__info(err_msg+msg)
        pass
    
    def saveConfigs(self):
        with open('ftpconnection.cfg','w') as f:
            for l in self.config_dir.keys():
                f.write(l+'='+self.config_dir[l]+'\n')

    def connect(self):
        
       
        if 'server' in self.config_dir.keys():
            server=self.config_dir['server']
        else:
            res = self.__input("Введите адрес сервера:")
            
            if res[1]==0:
                return 0
            inl = res[0]
            for ismb in ignore_symbol:
                inl=inl.replace(ismb,'')
            server = inl
            #self.config_dir['server']=inl

        if 'login' in self.config_dir.keys():
            login=self.config_dir['login']
        else:
            res = self.__input("Введите логин:")
            if res[1]==0:
                return 0
            inl =res[0]
            for ismb in ignore_symbol:
                inl=inl.replace(ismb,'')
            login = inl
            #self.config_dir['login']=inl

        if 'pwd' in self.config_dir.keys():
            pwd=self.config_dir['pwd']
        else:
            res = self.__input("Введите пароль:")
            
            if res[1]==0:
                return 0
            inl = res[0]
            for ismb in ignore_symbol:
                inl=inl.replace(ismb,'')
            pwd = inl
            #self.config_dir['pwd']=inl
        self.ftp=FTP(server)
        
        try:
            print(self.ftp.login(login,pwd))
            msg="Выполнен вход\nСервер: {0}\nЛогин:{1}\nПароль:{2}".format(server,login,pwd)
            self.isOpen=True
        except:
            msg=str(sys.exc_info()[1])
            self.isOpen=False
        
        
        self.__info(msg)

    def disconnect(self):
        try:
            msg =self.ftp.quit()
            
        except:
            msg=str(sys.exc_info()[1])
            self.ftp.close()
        self.__info("Соединение закрыто\n"+msg)
        self.isOpen = False
    def __info(self,msg:str):
        dl2=iDialog()
        dlg2=QDialog(self.mwindow)
        dl2.setupUi(dlg2)
        dl2.label.setText(msg)
        dlg2.exec()
        return dlg2.result()

    def __input(self,msg:str,tmp:str = '') -> Tuple[str,int]:
        dlg=QDialog(self.mwindow)
        dl=cDialog()
        dl.setupUi(dlg)
        dl.label.setText(msg)
        dl.inLine.setText(tmp)
        dlg.exec()
        tpl = (dl.inLine.text(), dlg.result())
        return tpl

    def download(self,src:str,dst:str):
        try:
            with open(dst,'wb') as f:
                self.ftp.retrbinary('RETR '+src, f.write)
            return True
        except:
            msg=str(sys.exc_info()[1])
            self.__info(err_msg+msg)
            return False
        

    def upload(self,src:str,dst:str):
        try:
            with open(src,'rb') as f:
                self.ftp.storbinary('STOR '+dst,f)
        except:
            msg=str(sys.exc_info()[1])
            self.__info(err_msg+msg)
        pass
    
    def getDirList(self)->list:
        self.dir_list.clear()
        try:
            self.ftp.retrlines('LIST',fh.dirClbk)
        except:
            msg=str(sys.exc_info()[1])
            self.__info(err_msg+msg)
        return self.dir_list
    
    def changeDir(self, new_dir:str):
        self.ftp.cwd(new_dir)
        return self.getDirList()

    def dirClbk(self,p0:str) -> None:
        self.dir_list.append(p0.split(maxsplit=8))
    

      
   


if __name__ == "__main__":
    
    app=QtWidgets.QApplication([])
    MWindow =QtWidgets.QMainWindow()
    fh=ftpHndlr(MWindow)
    MWindow.show()
    fh.connect()
    #fh.download('test','test.txt')
    fh.upload('test/result12727.bin','ftp_share/result.bin')
    fh.getDirList()
    fh.disconnect()
    #fh.mwindow.show()
    app.exec()
 
    '''
    fh=ftpHndlr()
    with FTP('10.116.4.129') as ftp:
        print(ftp.login('karlin','S4)!zg%M'))
        #ftp.cwd("Документы")

        ftp.retrlines('LIST',fh.dirClbk)
        c=1
        print('0  ../')
        for i in fh.dir_list:
            print(c,'  ',i[8])
            c+=1
        print("Выбор за Вами:")
        dh = int(input())
        if dh ==0:
            ftp.cwd('../')
        else:
            ftp.cwd(fh.dir_list[dh-1][8])
        fh.dir_list.clear()
        ftp.retrlines('LIST',fh.dirClbk)

        c=0
        for i in fh.dir_list:
            print(c,'  ',i[8])
            c+=1
        '''

        
