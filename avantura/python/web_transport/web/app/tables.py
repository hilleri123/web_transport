from app import app, db, lm, oid
#from .models import Products, Product_groups
from .query import *
from flask import render_template

class Table():
    def __init__(self, clm_names=None, data=None):
        self.clm_names=clm_names
        self.data=data

def html_class_to_table(text):
    #print(text)
    for i in MainQueryHandler.__subclasses__():
        if text == i.name():
            return i
    return MainQueryHandler


def table_html(text):
    table = html_class_to_table(text)
    return table.table_html


def form_html(text):
    table = html_class_to_table(text)
    return table.form_html


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
    





