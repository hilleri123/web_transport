from app import app, db, lm, oid
#from .models import Products, Product_groups
from .query import *

class Table():
    def __init__(self, clm_names=None, data=None):
        self.clm_names=clm_names
        self.data=data

def html_class_to_table(text):
    #print(text)
    if text == QProducts.name():
        return QProducts
    if text == QProduct_groups.name():
        return QProduct_groups
    return text



def create_table_content(text):
    table = html_class_to_table(text)
    #print(table, dir(table))
    clm_names = table.get_visible_clm_names()
    data = table.get_visible_data()
    return Table(clm_names, data)


def create_table_edit_form(text):
    table = html_class_to_table(text)
    return table.form()

    

def add_to_table(text, element = None):
    table = html_class_to_table(text)
    #print(table, dir(table))
    table.add_row(element)
    





