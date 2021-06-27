from django.shortcuts import render, redirect
from .helpers import * 
# from rq import Queue
# q = Queue(connection=conn)

def query_page(request,query):
    list_para = get_document(query)
    # print(list_para)
    # article_string = '\n\n'.join(list_para)
    # print(article_string)
    # if job.is_finished:
    #     return render(request,'writer/results.html',{'final':'yayyy'})

    return render(request,'writer/results.html',{'final':str(list_para)})