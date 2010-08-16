ServerTail is a service which lets you quickly and easily see real time
output of log files on your servers, with just a web browser!

Just enter in your server's hostname, a username, and an optional password, and
the path to your log file, and we'll start showing you that log file right
away.

The URL that we give you is unique and cannot be guessed. You can feel free to
share that URL to anyone or noone--the choice is yours.


INSTALLATION AND RUNNING
========================

$ git clone git://github.com/ericflo/servertail.git
$ sudo easy_install -U virtualenv
$ virtualenv stenv
$ source stenv/bin/activate
$ easy_install -U pip
$ cd servertail
$ pip install -U -r requirements.txt
$ python manage.py syncdb
$ python manage.py migrate
$ ./bin/serve

Now you can open your browser to http://127.0.0.1:8000/ and have fun!

For extra flair, navigate to http://127.0.0.1:8000/admin/ and under the
"Front pages" item, you can choose a featured tail to show on the front page.