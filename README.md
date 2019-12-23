# flask_github_app
# run the github_load.py in the background this will pull 200 records from github wait an hour and try to update any records that have changed in the past hour
python github_load.py
# to run the flask program first install flask

pip install flask
# to run the web program
python flask_web.py
# it will run in local mode  using the local ip and port 5000 and go to a web browser and type the local ip and port followed by /
http://127.0.0.1:5000/
# then follow the link and it will list the top 50 records of python github repos click on the link and it will show you a detail page for each repo. 
