from app import app, db, lm
#from .models import Products, Product_groups
from .query import *
from flask import render_template


class Table():
    def __init__(self, main_query_handler=None, table_type='table1', onclick_add='PopUpShow', hide_add='PopUpHide', target_add='#popup1', onclick_edit=''):
        self.clm_names=main_query_handler.get_visible_clm_names()
        self.data=main_query_handler.get_visible_data()
        self.label_text=main_query_handler.get_visible_table_name()
        self.onclick_add = onclick_add
        self.hide_add = hide_add
        self.target_add = target_add

        self.type = table_type

        self.onclick_edit = onclick_edit

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
    tables = [Table(html_class_to_table(i)) for i in table.get_visible_tables()]
    tables.append(Table(table))
    return tables

def create_inner_tables(text):
    table = html_class_to_table(text)
    inner_tables = [Table(html_class_to_table(inner_table), 'inner_table1', 'PopUpInnerTable'+str(i), 'PopHideInnerTable'+str(i), 'inner_target'+str(i))
            for i, inner_table in enumerate(table.inner_tables())]
    return inner_tables



def create_table_edit_form(text):
    table = html_class_to_table(text)
    return table.form()



def add_to_table(text, element = None):
    table = html_class_to_table(text)
    table.add_row(element)
