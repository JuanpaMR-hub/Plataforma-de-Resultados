from django.shortcuts import render

# Create your views here.
def reim1_view(request, *arg, **kwargs):
    return render(request,"reim1/reim1.htm",{})