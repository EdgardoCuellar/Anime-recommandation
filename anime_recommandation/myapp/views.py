from django.shortcuts import render

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # Do something with the name
    return render(request, 'index.html')
