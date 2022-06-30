from datetime import datetime
import random

class Table():
    '''
    Class for create tables, extract parametrs and create fake data
    '''
    table_par = []

    def table_from_file(self,path:str,count):
        '''Create table from file'''
        tmp = []
        #TODO посмотреть, из каких файлов можно открыть таблицы БД и реализовать отдельные методы
        if '.xls' in path:
            import win32com.client

            Excel = win32com.client.gencache.EnsureDispatch('Excel.Application')
            wb = Excel.Workbooks.Open(path)
            sheet = wb.ActiveSheet
            i = 1
            while sheet.Cells(1,i).Value != None:
                tmp.append(sheet.Cells(1,i).Value)
                i += 1
            
            self.table_par = self.__extract(tmp)
            tmp = self.generator(count)
            i = 0
            while i < len(tmp):
                j = 0
                tm:str = tmp[i]
                t = tm.split()
                while j < len(self.table_par):
                    sheet.Cells(i+2,j+1).Value = t[j]
                    j += 1
                i += 1
            
            wb.Save()        
            wb.Close()
            Excel.Quit()
        elif '.csv' in path:
            import csv

            with open(path, 'r+', newline='') as myFile:
                tm = myFile.readline().split(',')
                for i in tm:
                    tmp.append(i)
                self.table_par = self.__extract(tmp)

                tmp = self.generator(count)
                i = 0
                writer = csv.writer(myFile)
                t = []
                for i in tmp:
                    t.append(list(str(i).split()))
                writer.writerows(t)

    def table_from_parametrs(self,par):
        '''Create table from parametrs'''
        self.table_par = self.__extract(par)
    
    def generator(self,count):
        '''Generate fake data from parametrs'''
        iter = count
        mas = 1000
        if count > mas : iter = count / mas
        if(iter%1 != 0): 
            iter += 1
        iter = round(iter)
        tmp = []
        for i in range(0,iter):
            len = count - mas*(i+1)
            if(len < 0): len = mas + len
            else: len = mas
            tmp.extend(_DataGenerator.generator(_DataGenerator,self.table_par,len))
        return tmp
    
    def __extract(self, tmp):
        par = []
        #TODO придумать, как извлекать параметры в нужном виде
        i = 0
        string: str
        while i < len(tmp):
            string = tmp[i]
            par.append(string.lower())
            i += 1
        return par


class _DataGenerator():
    from mimesis import Person
    from mimesis.builtins import RussiaSpecProvider
    from mimesis.enums import Gender
    p = Person('ru')
    sp = RussiaSpecProvider()
    m = Gender.MALE
    f = Gender.FEMALE

    def generator(self, par, count): #TODO доработать для большего покрытия возможных случаев
        res = []
        gender = self.m
        for j in range(0,count):
            tmp = ''
            r = random.randint(0,1)
            if(r == 1): gender = self.f
            else: gender = self.m
            for i in par:
                if(i == 'id'): tmp += str(j) + ' '
                elif(i == 'gender'): tmp += self.p.gender() + ' '
                elif(i == 'fio'): tmp += self.p.last_name(gender) + ' ' + self.p.first_name(gender) + ' ' + self.sp.patronymic(gender) + ' '
                elif(i == 'lastname' or i == 'surname'): tmp += self.p.last_name(gender) + ' '
                elif(i == 'name' or i == 'firstname'): tmp += self.p.first_name(gender) + ' '
                elif(i == 'patronimic'): tmp += self.sp.patronymic(gender) + ' '
                elif(i == 'age'): tmp += str(self.p.age()) + ' '
                elif(i == 'email' or i == 'e-mail'): tmp += self.p.email() + ' '
                elif(i == 'phone'): tmp += self.p.telephone() + ' '
                elif(i == 'height'): tmp += str(self.p.height()) + ' '
                elif(i == 'weight'): tmp += str(self.p.weight()) + ' '
            res.append(tmp[:-1])
        return res


#testing
par = ['gender', 'fio', 'age'] #Only for testing

t_start = datetime.now()

table1 = Table()
#table1.table_from_parametrs(par)
table1.table_from_file(u'D:\\Libraries\\Documents\\FIO_Age_E-mail.csv',100000)
#fake = table1.generator(10000)
# with open('test.txt', 'w', encoding='utf-8') as w:
#     for i in fake:
#         print(i)
#         w.write(i + '\n')
# print('Count of objects: ' + str(len(fake)))
print(table1.table_par)

t_finish = datetime.now()
itog = (t_finish - t_start).total_seconds() #sec
print(str(itog) + ' sec')