class Car:
    speed = 0
    year = 0
    model = 'md'
    def __init__(self, speed, year, model):
        self.speed = speed
        self.model = model
        self.year = year


class Track(Car):
    def cargo(self):
        print(f'''ви взяли вантаж за допомогою: {self.model}.
ваша швидкість: {self.speed}''')
class ElectickCar(Car):
    def AutoPilot(self):
        print(f'ви включили автопілот в: {self.model}.'
              f'ваша швидкість: {self.speed}')
scania = Track(10, 2022, 'Scania')
scania.cargo()
TeslaModelX = ElectickCar(22, 2020, 'Tesla model X')
TeslaModelX.AutoPilot()
print(TeslaModelX)