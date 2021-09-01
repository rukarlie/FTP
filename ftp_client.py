from ftplib import FTP
from Ui_commonDialog import Ui_Dialog as cDilog
from Ui_infoDialog import Ui_Dialog as iDialog
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QTableWidgetItem,  QFileDialog, QMessageBox, QDialog)
from threading import Thread
import sys

ignore_symbol=['\n',' ', '\\n', '\t']

class ftpHndlr:
    def __init__(self, MainWindow:QtWidgets.QMainWindow) -> None:
        self.dir_list=[]
        self.config_dir={}
        self.ftp:FTP
        self.mwindow= MainWindow
        self.isOpen=False
        with open('ftpconnection.cfg','r') as f:
            for l in f:
                lst = list(l.split('='))
                for i in range(len(lst)):
                    for ismb in ignore_symbol:
                        lst[i]=lst[i].replace(ismb,'')
                    
                self.config_dir[lst[0]]=lst[1]
        
        pass
    
    def connect(self):
        
        dlg=QDialog(self.mwindow)
        dl=cDilog()
        dl.setupUi(dlg)
        if 'server' in self.config_dir.keys():
            server=self.config_dir['server']
        else:
            dl.label.setText("Введите адрес сервера:")
            dl.inLine.setText('')
            dlg.exec()
            if dlg.result()==0:
                return 0
            inl = dl.inLine.text()
            for ismb in ignore_symbol:
                inl=inl.replace(ismb,'')
            server = inl
            #self.config_dir['server']=inl

        if 'login' in self.config_dir.keys():
            login=self.config_dir['login']
        else:
            dl.label.setText("Введите логин:")
            dl.inLine.setText('')
            dlg.exec()
            if dlg.result()==0:
                return 0
            inl = dl.inLine.text()
            for ismb in ignore_symbol:
                inl=inl.replace(ismb,'')
            login = inl
            #self.config_dir['login']=inl

        if 'pwd' in self.config_dir.keys():
            pwd=self.config_dir['pwd']
        else:
            dl.label.setText("Введите пароль:")
            dl.inLine.setText('')
            dlg.exec()
            if dlg.result()==0:
                return 0
            inl = dl.inLine.text()
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
        
        
        self.info(msg)

    def disconnect(self):
        self.ftp.close()
        self.info("Соединение закрыто")

    def info(self,msg:str):
        dl2=iDialog()
        dlg2=QDialog(self.mwindow)
        dl2.setupUi(dlg2)
        dl2.label.setText(msg)
        dlg2.exec()
        return dlg2.result()


    def dirClbk(self,p0:str) -> None:
        self.dir_list.append(p0.split(maxsplit=8))
    
    
   


if __name__ == "__main__":
    
    app=QtWidgets.QApplication([])
    MWindow =QtWidgets.QMainWindow()
    fh=ftpHndlr(MWindow)
    MWindow.show()
    fh.connect()
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

        
