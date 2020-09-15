
from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm




class MenuAction():
    def __init__(self, num = 0, unique_class = '', text = 'POPA', onclick = '', children = []):
        self.main_class = 'action_class'
        self.child_action_class = 'child_action_class'
        self.html_class = 'parent'+str(num)
        self.child_name = 'child'+str(num)
        self.unique_class = unique_class
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

    clients_child = MenuAction(len(res), 'clients', 'Клиенты', '')
    clients = MenuAction(len(res), 'clients_main', 'Клиенты', '', [clients_child])
    res.append(clients)

    prepared_cars = MenuAction(len(res), 'prepared_cars', 'Предварительные', '')
    spent_cars = MenuAction(len(res), 'spent_cars', 'Закрытые', '')
    cars = MenuAction(len(res), 'cars', 'Машины', '', [prepared_cars, spent_cars])
    res.append(cars)

    finances = MenuAction(len(res), 'finances', 'Финансы', '')
    res.append(finances)

    exchange_rates = MenuAction(len(res), 'exchange_rates', 'Курсы валют', '')
    product_groups = MenuAction(len(res), 'product_groups', 'Группы товаров', '')
    products = MenuAction(len(res), 'products', 'Товары', '')
    car_types = MenuAction(len(res), 'car_types', 'Тип машины', '')
    car_numbers = MenuAction(len(res), 'car_numbers', 'Номера машин', '')
    handbooks = MenuAction(len(res), 'handbooks', 'Справочники', '', [exchange_rates, product_groups, products, car_types, car_numbers])
    res.append(handbooks)

    admin_employees = MenuAction(len(res), 'admin_employes', 'Сотрудники', '')
    admin_clients = MenuAction(len(res), 'admin_clients', 'Клиенты', '')
    admin = MenuAction(len(res), 'admin', 'Администрирование', '', [admin_employees, admin_clients])
    res.append(admin)

    exit = MenuAction(len(res), 'exit', 'Выход', '')
    res.append(exit)

    return res
