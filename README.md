# django_web_app
A web application written in django used for chatting, posting and much more...<br/>
You can go and check it out here: https://djangowebapp.platt.repl.co/

I would appreciate it if you would report any issues you see....<br/>
and feel free to create pull requests


## Host repo yourself
Dependencies:
- Git
- Docker
Write the following commands into your commandline:
```
git clone https://github.com/Pl4tt/django_web_app.git
cd ./django_web_app/src
```
Then you need to create a .env file including the following variables:
- SECRET_KEY
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD

Finally you can to run the docker-compose-deploy.yml file:
```
docker-compose -f docker-compose-deploy.yml build
docker exec -it <container_id_of_app:django_image> python3 manage.py makemigrations account chat friend posts --noinput
docker exec -it <container_id_of_app:django_image> python3 manage.py migrate --noinput
docker-compose -f docker-compose-deploy.yml up
```
During this process you could might come accross the following error: "standard_init_linux.go:228: exec user process caused: no such file or directory".
To fix this you just need convert the windows line breaks inside the src/scripts/entrypoint.sh file to unix line breaks (CRLF -> LF).

After that the webapp should run on http://127.0.0.1
