from django.shortcuts import render
import subprocess
from users_test import *
import sys
 
# adding Folder_2 to the system path
sys.path.insert(0, '../../users_test.py')

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # Do something with the name
    return render(request, 'index.html')

def recommendation(request):
    if request.method == 'POST':
        algo = request.POST.get('algo')
        user = request.POST.get('user')

        if algo == 'apriori':
            script = 'apriori_recommandation.py'
        elif algo == 'tf_idf':
            script = 'tf_idf.py'
        else:
            script = None
        
        if script is not None:
            output = subprocess.check_output(['python', script, user, variable1, variable2])
            output = output.decode('utf-8')  # Convert bytes to string
        else:
            output = 'Invalid algorithm selection'

        return render(request, 'recommendation.html', {'output': output, 'algo': algo, 'user': user})
    else:
        return render(request, 'recommendation.html')


