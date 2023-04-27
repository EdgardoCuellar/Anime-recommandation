from django.shortcuts import render
import subprocess
# from users_test import *
import sys
import os
 
# adding Folder_2 to the system path
# sys.path.insert(0, '../../users_test.py')

def index(request):
    if request.method == 'POST':
        algo = request.POST.get('algo')
        user = request.POST.get('user')

        if algo == 'apriori':
            script = 'apriori_recommandation.py'
        elif algo == 'tf_idf':
            script = 'cosine_similarity.py'
        else:
            script = None
        
        script_path = os.path.abspath(script)
        
        if script is not None:
            output = subprocess.check_output(['python', script_path, "USER_1"])
            output = output.decode('utf-8')  # Convert bytes to string
        else:
            output = "invalid algo"
            
        return render(request, 'index.html', {'output': output})
    else:
        return render(request, 'index.html')


