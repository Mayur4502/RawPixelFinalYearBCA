from django.http import HttpResponse
from django.shortcuts import render

def demo(request):
	return HttpResponse("<a href='https://www.google.com'>Google</a>")

def demo2(request):
	return HttpResponse("<a href='https://www.instagram.com'>Instagram</a>")
	
def demo3(request):
	return HttpResponse("<a href='https://www.facebook.com'>Facebook</a>")

def loadDemo(request):
	return render(request,"view.html")

def printData(request):
	sname=request.GET.get("txtName")
	rno=request.GET.get("txtRno")

	sinfo={"sname":sname,"roll_no":rno}
	return render(request,"view2.html",sinfo)

def ListDemo(request):
	myList=[
			{"sname":'amaan',"rno":101},
			{"sname":'harsh',"rno":102},
			{"sname":'mayur',"rno":103}
		   ]
	return render(request,"view3.html",{"myList":myList})

