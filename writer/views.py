from django.shortcuts import render, redirect
from .helpers import * 
# from rq import Queue
# q = Queue(connection=conn)

def query_page(request,query,email):
    list_para = get_document(query,email)
    return render(request,'writer/results.html',{'final':'Thanks! Your blog article will be emailed to you within 50 seconds'})