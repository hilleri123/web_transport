
from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm




class MenuAction():
    def __init__(self, num = 0, text = 'POPA', onclick = '', children = []):
        self.main_class = 'action_class'
        self.child_action_class = 'child_action_class'
        self.html_class = 'parent'+str(num)
        self.child_name = 'child'+str(num)
        self.onclick = onclick
        self.text = text

        self.children = children.copy()
        self.set_num(num)

    #Рекурсия(осторожно)
    def set_num(self, num):
        self.num = num
        for i, _ in enumerate(self.children):
            self.children[i].set_num(self.num)

def create_main_menu():
    res = []

    clients = MenuAction(len(res), 'Клиенты', '')
    res.append(clients)

    prepared_cars = MenuAction(len(res), 'Предварительные', '')
    spent_cars = MenuAction(len(res), 'Закрытые', '')
    cars = MenuAction(len(res), 'Машины', '', [prepared_cars, spent_cars])
    res.append(cars)

    finances = MenuAction(len(res), 'Финансы', '')
    res.append(finances)

    exchange_rates = MenuAction(len(res), 'Курсы валют', '')
    product_groups = MenuAction(len(res), 'Группы товаров', '')
    products = MenuAction(len(res), 'Товары', '')
    car_types = MenuAction(len(res), 'Тип машины', '')
    car_numbers = MenuAction(len(res), 'Номера машин', '')
    handbooks = MenuAction(len(res), 'Справочники', '', [exchange_rates, product_groups, products, car_types, car_numbers])
    res.append(handbooks)

    admin_employes = MenuAction(len(res), 'Сотрудники', '')
    admin_clients = MenuAction(len(res), 'Клиенты', '')
    admin = MenuAction(len(res), 'Администрирование', '', [admin_employes, admin_clients])
    res.append(admin)

    exit = MenuAction(len(res), 'Выход', '')
    res.append(exit)

    return res



