#!/usr/bin/python3
import os
from jinja2 import Template
import yaml
import logging

if __name__ == '__main__':
    templates_dir = 'templates'
    rendered_dir = 'build'
    data_dir = 'data'
    results_dir = 'logs'

    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    logging.basicConfig(filename=os.path.join(results_dir, 'bootstrap.log'), filemode='w', level='INFO',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S %z')
    template_args = os.path.join(data_dir, 'constants.yml')
    if not os.path.isfile(template_args):
        raise FileNotFoundError(
            '{} not found, cannot generate files from template'.format(os.path.abspath(template_args)))
    else:
        logging.info('Generating templates from folder: {}'.format(templates_dir))
        with open(template_args) as fp:
            template_args = yaml.safe_load(fp)
        # Insert CONTI_ENV as a default
        template_args['CONTI_ENV'] = os.environ.get('CONTI_ENV', 'prod')
        if not os.environ.get('CONTI_DB_NAME'):
            raise EnvironmentError('“You must specify CONTI_DB_NAME in the environment.')
        else:
            template_args['CONT_DB_NAME'] = os.environ.get('CONTI_DB_NAME')
        # Go through all the templates and replace them in data files
        for root, dirs, files in os.walk(templates_dir):
            for template in filter(lambda x: x.endswith('.j2'), files):
                rendered_name_parent = root.replace(templates_dir, rendered_dir)
                rendered_name = os.path.join(rendered_name_parent, template.replace('.j2', ''))
                with open(os.path.join(root, template)) as f:
                    contents = f.read()
                rendered_contents = Template(contents).render(**template_args)
                if not os.path.isdir(rendered_name_parent):
                    os.makedirs(rendered_name_parent)
                with open(rendered_name, mode='w') as fp:
                    fp.write(rendered_contents)
                    logging.info('Generated: {}'.format(fp.name))
