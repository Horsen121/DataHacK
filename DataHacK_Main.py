from datetime import datetime

class Table():
    '''
    Class for create tables, extract parametrs and create fake data
    '''
    par = []

    def table_from_file(self,path:str):
        '''Create table from file'''
        tmp = []
        with open(path, 'a') as r:
            tmp = r.readline().split() #TODO посмотреть, из каких файлов можно открыть таблицы БД и реализовать отдельные методы
        self.par = self.__extract(tmp)

    def table_from_parametrs(self,par):
        '''Create table from parametrs'''
        self.par = self.__extract(par)
    
    def generator(self,par,count):
        '''Generate fake data from parametrs'''
        iter = count
        if count > 5000 : iter = count // 5000 + 1
        for i in range(0,iter):
            tmp = _DataGenerator.generator(_DataGenerator,par,count)
            return tmp # for test
            # export to database
    
    def __extract(self, tmp):
        par = []
        for i in tmp:
            pass #TODO придумать, как извлекать параметры в нужном виде
        return par


class _DataGenerator():
    from mimesis import Person
    from mimesis.builtins import RussiaSpecProvider
    from mimesis.enums import Gender
    p = Person('ru')
    sp = RussiaSpecProvider()
    m = Gender.MALE
    f = Gender.FEMALE

    def generator(self, dataclass, count): #TODO доработать для большего покрытия возможных случаев
        res = []
        gender = self.m
        for i in range(0,count):
            tmp = ''
            for i in dataclass:
                if(i == 'gender'): 
                    tmp += self.p.gender() + ' '
                    if tmp.find('Жен.'): gender = self.m
                    else : gender = self.f
                elif(i == 'fio'): tmp += self.p.last_name(gender) + ' ' + self.p.first_name(gender) + ' ' + self.sp.patronymic(gender) + ' '
                elif(i == 'age'): tmp += str(self.p.age()) + ' '
                elif(i == 'email'): tmp += self.p.email() + ' '
                elif(i == 'phone'): tmp += self.p.telephone() + ' '
                elif(i == 'height'): tmp += str(self.p.height()) + ' '
                elif(i == 'weight'): tmp += str(self.p.weight())
            res.append(tmp)
        return res


#testing
par = ['gender', 'fio', 'age']
table1 = Table()
table1.table_from_parametrs(par)

t_start = datetime.now()
fake = table1.generator(par, 100000)

with open('test.txt', 'w', encoding='utf-8') as w:
    for i in fake:
        print(i)
        w.write(i + '\n')
print('Count of objects: ' + str(len(fake)))

t_finish = datetime.now()
itog = (t_finish - t_start).microseconds #microsec
itog /= 1000000 #sec
print(itog/60) #min