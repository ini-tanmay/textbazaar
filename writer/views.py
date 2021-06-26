from django.shortcuts import render, redirect
from .helpers import * 
from rq import Queue
from ../worker import *

q = Queue(connection=conn)


def query_page(request,query):
    list_para = q.enqueue(get_document, query)
    print(list_para)
    article_string = '\n\n'.join(list_para)
    print(article_string)
    return render(request,'writer/results.html',{'final':article_string})