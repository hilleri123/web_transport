from app import app, db, lm, oid
from .models import Products, Product_groups

class Table():
    def __init__(self, clm_names=None, data=None):
        self.clm_names=clm_names
        self.data=data

def html_class_to_table(text):
    print(text)
    if text == 'products':
        return Products
    return text



def create_table_content(text):
    table = html_class_to_table(text)
    print(table, dir(table))
    clm_names = table.get_visible_clm_names()
    data = table.get_visible_data()
    return Table(clm_names, data)



    

def add_to_table(text, element = None):
    table = html_class_to_table(text)
    print(table, dir(table))
    table.add_row(element)
    





