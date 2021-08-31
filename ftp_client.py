from ftplib import FTP

ignore_symbol=['\n',' ', '\\n', '\t']

class ftpHndlr:
    def __init__(self) -> None:
        self.dir_list=[]
        config_dir={}
        with open('ftpconnection.cfg','r') as f:
            for l in f:
                lst = list(l.split('='))
                for i in range(len(lst)):
                    for ismb in ignore_symbol:
                        lst[i]=lst[i].replace(ismb,'')
                    
                config_dir[lst[0]]=lst[1]
        
        pass
    
    def dirClbk(self,p0:str) -> None:
        self.dir_list.append(p0.split(maxsplit=8))
    


if __name__ == "__main__":
    fh=ftpHndlr()
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

        
