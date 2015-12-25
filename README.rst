INSTALLATION
============

    ::

    $ sudo pip install -r requirements.txt
    $ cp config/brome.yml.example config/brome.yml
    $ cp config/browsers_config.yml.example config/browsers_config.yml
    $ cp settings.yaml.example settings.yaml
    $ vim config/brome.yml -c ":/#CHANGEME"
    $ vim settings.yaml -c ":/#CHANGEME"

CONFIGURATION
=============

http://pythonhosted.org/PyDrive/quickstart.html#authentication

CRONTAB
=======
0 20 */15 * * cd /path/to/project/ && xvfb-run ./bro
