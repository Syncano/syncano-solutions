# coding=UTF8
from __future__ import print_function, unicode_literals

import logging
import os
import subprocess

import syncano
from syncano import exceptions

LOG = logging.getLogger('import_solutions')


def get_solutions(registry):
    connection = registry.connection()
    data = connection.request('GET', 'v1.1/marketplace/solutions/')
    while True:
        for x in data['objects']:
            yield x
        if data['next']:
            data = connection.request('GET', data['next'])
        else:
            break


def import_solution(solution, instance):
    con = instance._get_connection()
    versions = con.request('GET', solution['links']['versions'])
    if not len(versions['objects']):
        return
    latest = versions['objects'][-1]
    con.request('POST', latest['links']['install'],
                data={'instance': instance.name})


def label_to_path(label):
    return label.lower().replace(' ', '_').replace('/', '-')


def main():
    registry = syncano.connect(api_key=syncano.APIKEY)
    parent = os.getcwd()
    for solution in get_solutions(registry):
        # print(solution)
        if not solution['description']:
            continue
        LOG.info('importing_solution {id}: {description}'.format(**solution))
        temp_instance = registry.instances.create(
            name='solution_import_{id}'.format(**solution)
        )
        try:
            import_solution(solution, temp_instance)
            dirname = label_to_path(solution['label'])
            if not os.path.exists(dirname):
                os.mkdir(dirname)
            os.chdir(dirname)
            with open('README.md', 'wb') as readme:
                readme.write(solution['description'])
                readme.write('\n')
            subprocess.check_call(['syncano', 'sync', 'pull', '-a',
                                   temp_instance.name])
            os.chdir(parent)
        except exceptions.SyncanoRequestError as e:
            LOG.exception(e)
        finally:
            temp_instance.delete()

if __name__ == '__main__':
    main()
