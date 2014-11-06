Angerona Quick-Start Guide
==========================

Docker
------
The Angerona quick-start leverages Docker to make your evaluation as painless as possible.  In order to use the Docker image, you will need to have Docker installed in your environment.  See [this link](https://docs.docker.com/installation/) for details on how to install Docker on your Linux-based system.

Quick-Start
-----------
Once you have Docker installed (and the docker daemon is running), all you need to do is execute this statement to start Angerona:

    $ CID=$(docker run -dP petergrace/angerona)

This command will start the container and save the container ID in variable $CID.  We want this ID, because our next step will be to find which port Docker has decided to use as the proxy port for our https traffic:

    $ docker port $(CID) 443
    0.0.0.0:49171

This example output indicates that Angerona is running on port 49171.  Point your browser to https://<ip-of-your-docker-server:49171 and after accepting the security warning, you will be presented with the Angerona interface.

What's the docker container doing?
----------------------------------
The Docker container that is provided from the docker registry uses supervisord to run nginx, waitress, and also spawns the process that generates the self-signed certificate for the server.

- nginx
  - nginx is used to proxy the SSL traffic from your outside world to the Angerona app.
- waitress
  - waitress is the lightweight server that Pyramid-based Python apps use by default.  It does not support SSL currently, hence why we need nginx.
- makeCert.sh
  - makeCert.sh generates a self-signed SSL certificate when you first run your Angerona container.  This ensures that nobody has a copy of your private key, thereby compromising the security of your test instance.
  
Example output from `docker -ti`
--------------------------------
In the below example output, you will notice that makecert enters a "FATAL" state.  This is expected!  supervisor tries to restart the process when it sees the process has closed.  

    /usr/lib/python2.7/dist-packages/supervisor/options.py:295: UserWarning: Supervisord is running as root and it is searching for its configuration file in default locations (including its current working directory); you probably want to specify a "-c" argument     specifying an absolute path to a configuration file for improved security.
      'Supervisord is running as root and it is searching '
    2014-11-05 17:29:49,893 CRIT Supervisor running as root (no user in config file)
    2014-11-05 17:29:49,893 WARN Included extra file "/etc/supervisor/conf.d/nginx.conf" during parsing
    2014-11-05 17:29:49,894 WARN Included extra file "/etc/supervisor/conf.d/makecert.conf" during parsing
    2014-11-05 17:29:49,894 WARN Included extra file "/etc/supervisor/conf.d/angerona.conf" during parsing
    2014-11-05 17:29:49,894 WARN Included extra file "/etc/supervisor/conf.d/system.conf" during parsing
    2014-11-05 17:29:49,948 INFO RPC interface 'supervisor' initialized
    2014-11-05 17:29:49,949 CRIT Server 'unix_http_server' running without any HTTP authentication checking
    2014-11-05 17:29:49,950 INFO supervisord started with pid 1
    2014-11-05 17:29:50,957 INFO spawned: 'nginx' with pid 10
    2014-11-05 17:29:50,964 INFO spawned: 'angerona' with pid 11
    2014-11-05 17:29:50,973 INFO spawned: 'makecert' with pid 12
    2014-11-05 17:29:51,024 INFO exited: nginx (exit status 1; not expected)
    2014-11-05 17:29:52,093 INFO spawned: 'nginx' with pid 24
    2014-11-05 17:29:52,094 INFO success: angerona entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
    2014-11-05 17:29:52,095 INFO success: makecert entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
    2014-11-05 17:29:53,122 INFO success: nginx entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
    2014-11-05 17:30:01,090 INFO exited: makecert (exit status 0; expected)
    2014-11-05 17:30:01,091 WARN received SIGHUP indicating restart request
    2014-11-05 17:30:01,091 INFO waiting for nginx, angerona to die
    2014-11-05 17:30:02,107 INFO stopped: angerona (terminated by SIGTERM)
    2014-11-05 17:30:02,124 INFO stopped: nginx (exit status 0)
    2014-11-05 17:30:02,145 CRIT Supervisor running as root (no user in config file)
    2014-11-05 17:30:02,146 WARN Included extra file "/etc/supervisor/conf.d/nginx.conf" during parsing
    2014-11-05 17:30:02,146 WARN Included extra file "/etc/supervisor/conf.d/makecert.conf" during parsing
    2014-11-05 17:30:02,146 WARN Included extra file "/etc/supervisor/conf.d/angerona.conf" during parsing
    2014-11-05 17:30:02,146 WARN Included extra file "/etc/supervisor/conf.d/system.conf" during parsing
    2014-11-05 17:30:02,148 INFO RPC interface 'supervisor' initialized
    2014-11-05 17:30:02,149 CRIT Server 'unix_http_server' running without any HTTP authentication checking
    2014-11-05 17:30:02,149 INFO supervisord started with pid 1
    2014-11-05 17:30:03,157 INFO spawned: 'nginx' with pid 29
    2014-11-05 17:30:03,165 INFO spawned: 'angerona' with pid 30
    2014-11-05 17:30:03,178 INFO spawned: 'makecert' with pid 31
    2014-11-05 17:30:03,222 INFO exited: makecert (exit status 0; not expected)
    2014-11-05 17:30:04,224 INFO success: nginx entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
    2014-11-05 17:30:04,224 INFO success: angerona entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
    2014-11-05 17:30:04,230 INFO spawned: 'makecert' with pid 44
    2014-11-05 17:30:04,249 INFO exited: makecert (exit status 0; not expected)
    2014-11-05 17:30:06,258 INFO spawned: 'makecert' with pid 45
    2014-11-05 17:30:06,278 INFO exited: makecert (exit status 0; not expected)
    2014-11-05 17:30:09,288 INFO spawned: 'makecert' with pid 46
    2014-11-05 17:30:09,304 INFO exited: makecert (exit status 0; not expected)
    2014-11-05 17:30:10,306 INFO gave up: makecert entered FATAL state, too many start retries too quickly

