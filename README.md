# XNAT client
A file downloader for XNAT platforms

XNAT is a popular informatics platform for imaging research. This script works with any repositories based on XNAT.

PyXnat is required
https://pythonhosted.org/pyxnat/

## Basic
```
python downloader.py -u USERNAME -p PASSWORD -r REPOSITORY_URL
```
Mandatory options are your user name, password and a repository URL. The URL will include as follows.
* https://central.xnat.org
* https://www.nitrc.org/ir

## List of projects
```
python downloader.py -u USERNAME -p PASSWORD -r REPOSITORY_URL -l
```

If you turn on '-l' or '--list' option, you can browse the list of projects for which you have the access rights in the specified repository.

## Filter projects or subjects
```
python downloader.py -u USERNAME -p PASSWORD -r REPOSITORY_URL -pr PROJECT_NAME -s SUBJECT_STRING
```

You can download only one project by specifying the project name. When you do not enter a project name, all projects are downloaded.

You can filter subjects by setting the '-s' option. If a subject name includes this SUBJECT_STRING, the subject data is downloaded.

## Download directory
```
python downloader.py -u USERNAME -p PASSWORD -r REPOSITORY_URL -d DIR
```

You can specify your local download directory.

## Log
All messages are written in 'downloader.log'

