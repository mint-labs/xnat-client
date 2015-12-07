#!/usr/bin/env python

from pyxnat import Interface
import argparse, logging

DESCRIPTION = "A file downloader for XNAT platforms"

LOGGER = logging.getLogger('xnat_client')
logging.basicConfig(filename='downloader.log',level=logging.INFO)

def get_server_interface(options):
    return Interface(server=options.repository,
                        user=options.user,
                        password=options.password,
                        cachedir=options.cachedir)

def list(central):
    LOGGER.info('--- List projects ---')
    projects = central.select.projects().get()
    for project in projects:
        subjects = central.select.project(project).subjects().get()
        LOGGER.info('Project: %s, #subject: %s' % (project, len(subjects)))

def download(central, download_dir, dest_project, subject_str):
    LOGGER.info('--- Start downloading ---')
    if dest_project is None:
        projects = central.select.projects().get()
    else:
        projects = [dest_project]
    
    for project in projects:
        LOGGER.info('--- Project: %s ---' % project)
        subjects = central.select.project(project).subjects().get()
        if subject_str is not None:
            subjects = filter(lambda subject: subject_str in subject, subjects)
        
        if len(subjects) > 0:
            for subject in subjects:
                experiments = central.select.project(project).subject(subject).experiments().get()
                
                if len(experiments) > 0:
                    for experiment in experiments:
                        scans = central.select.project(project).subject(subject).experiment(experiment).scans().get()
                        
                        if len(scans) > 0:
                            LOGGER.info( 'Start downloading: %s , %s , %s, #scans:%s'  % (project, subject, experiment, len(scans)) )
                            try:
                                central.select.project(project).subject(subject).experiment(experiment).scans().download(download_dir, type='ALL', extract=True)
                                LOGGER.info( 'Finish downloading: %s , %s , %s, #scans:%s'  % (project, subject, experiment, len(scans)) )
                            except:
                                LOGGER.warning( 'ERROR downloading: %s , %s , %s, #scans:%s'  % (project, subject, experiment, len(scans)) )
        LOGGER.info('--- End of Project: %s ---' % project)
    LOGGER.info('--- Finish downloading ---')
        
def main(options):
    if not options.user:
        LOGGER.error('No user provided')
        return
    if not options.password:
        LOGGER.error('No password provided')
        return
    if not options.repository:
        LOGGER.error('No repository provided')
        return
    central = get_server_interface(options)
    if options.list == True:
        list(central)
    else:
        download(central, options.download_dir, options.project, options.subject_str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-u', '--user',
                        dest='user',
                        action='store',
                        default=None)
    parser.add_argument('-p', '--password',
                        dest='password',
                        action='store',
                        default=None)
    parser.add_argument('-c', '--cachedir',
                        dest='cachedir',
                        action='store',
                        default='/tmp')
    parser.add_argument('-d', '--download_dir',
                        dest='download_dir',
                        action='store',
                        default='/tmp')
    parser.add_argument('-r', '--repository',
                        dest='repository',
                        action='store',
                        default='https://central.xnat.org')
    parser.add_argument('-pr', '--project',
                        dest='project',
                        action='store',
                        default=None)
    parser.add_argument('-s', '--subject',
                        dest='subject_str',
                        action='store',
                        default=None)
    parser.add_argument('-l', '--list',
                        dest='list',
                        action='store_true')
    options = parser.parse_args()
    main(options)