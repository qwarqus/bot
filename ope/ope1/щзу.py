class Person:





    name = 'Person' #поля классу
    attack = 0      #поля классу
    speed = 15      #поля классу
    def __init__(self, name, attack, speed):
        self.name = name
        self.attack = attack
        self.speed = speed

    def __str__(self):
        return f'I am {self.name} and my {self.attack=} and my {self.speed=}'

    def say_my_name(self):
        print(self.name)
    def say_my_attack(self):
        print(self.attack)
crip = Person(name='creeper', attack=400, speed=100)
crip.say_my_name()


vovchik = Person(name='vova', attack=11100, speed=11100)
vovchik.say_my_name()
vovchik.say_my_attack()
print(crip)
"""""
zombie = Person()
zombie.say_my_name()
zombie.name = 'zombik'
zombie.say_my_name()
"""""
