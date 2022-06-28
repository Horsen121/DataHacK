from datetime import datetime
import dataclasses


class Generator():
    from mimesis import Person
    from mimesis.builtins import RussiaSpecProvider
    from mimesis.enums import Gender
    p = Person('ru')
    sp = RussiaSpecProvider()
    m = Gender.MALE
    f = Gender.FEMALE

    def generator(self, dataclass, count):
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

par = ['gender', 'fio', 'age']
gen = Generator()
fake = gen.generator(par, 10)
for i in fake:
    print(i)