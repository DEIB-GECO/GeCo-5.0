import os,sys

os.system('cd ../../frontend && nohup npm run serve &')
#os.system('nohup poetry run rasa run actions &')
#os.system('open -a Terminal ~/Documents/polimi/tesi/"rasa-master 2"/geco')
os.system('poetry run rasa run -m models --enable-api --cors "*" --debug')

#os.system('nohup npm run serve &')


#stream = os.popen('cd ../../../../Downloads/GeCo-5-2.0-version_context/frontend & npm start serve')
#output = stream.read()
#output
#print(output)
#stream = os.popen('npm start serve &')
#output = stream.read()
#output
#stream = os.popen('cd ../../../Documents/Polimi/tesi/"rasa-master 2"/geco')
#stream = os.popen('npm start serve')
#output = stream.read()
#
#output