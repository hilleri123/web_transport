from app import app, db, lm
#from .models import Products, Product_groups
from .query import *
from flask import render_template


class Table():
    def __init__(self, main_query_handler=None, table_prefix='', onclick_add='PopUpShow', hide_add='PopUpHide', target_add='popup1', onclick_edit=''):
        self.handler=main_query_handler
        self.clm_names=main_query_handler.get_visible_clm_names()
        self.data=main_query_handler.get_visible_data()
        self.label_text=main_query_handler.get_visible_table_name()
        self.onclick_add = onclick_add
        self.hide_add = hide_add
        self.target_add = target_add

        self.prefix = table_prefix

        self.onclick_edit = onclick_edit


        self.inner_tables = [Table(html_class_to_table(inner_table), 'inner_', 'PopUpInnerTable'+str(i), 'PopHideInnerTable'+str(i), 'inner_target'+str(i))
            for i, inner_table in enumerate(main_query_handler.inner_tables())]

        self.inner = False
        for i in self.inner_tables:
            i.inner = True

        self.form = main_query_handler.form()
        self.dbname = main_query_handler.name()

        self.place_for_table = 'place_for_table_'+self.dbname 

    def inner_for_html(self):
        if self.inner:
            return 'true'
        else:
            return 'false'

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


def create_table_content(text, inner=False):
    table = html_class_to_table(text)
    #print(table, dir(table))
    tables = [Table(html_class_to_table(i)) for i in table.get_visible_tables()]
    tables.append(Table(table))
    if inner:
        for i in tables:
            i.prefix = 'inner_'
            i.inner = True
    return tables

def create_inner_tables(text):
    table = html_class_to_table(text)
    inner_tables = [Table(html_class_to_table(inner_table), 'inner_', 'PopUpInnerTable'+str(i), 'PopHideInnerTable'+str(i), 'inner_target'+str(i))
            for i, inner_table in enumerate(table.inner_tables())]
    return inner_tables



def create_table_edit_form(text, data=None, empty=False):
    table = html_class_to_table(text)
    return table.form(data=data, empty=empty)



def add_to_table(text, element = None):
    table = html_class_to_table(text)
    table.add_row(element)
