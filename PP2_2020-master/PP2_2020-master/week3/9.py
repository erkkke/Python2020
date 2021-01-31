class Subject:
    pass
    
class Student:

    def __init__(self, name, surname, gpa):
        self.name = name 
        self.surname = surname 
        self.gpa = gpa

    def calc_gpa(self):
        return self.gpa / 2

a = Student(name="AAA", surname="BBB", gpa=3.4)

b = Student("CCC", "DDD", 3.0)

print(a.name, a.surname, a.gpa)
print(b.name, b.surname, b.gpa)

print(a.calc_gpa())
print(b.calc_gpa())

