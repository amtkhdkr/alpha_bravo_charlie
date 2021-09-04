#!/usr/bin/python3
import os
from jinja2 import Template
import yaml
import logging

if __name__ == '__main__':
    templates_dir = 'templates'
    rendered_dir = 'rendered'
    data_dir = 'data'
    results_dir = 'results'

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
        # Go through all the templates and replace them in data files
        for template in filter(lambda x: x.endswith('.j2'), os.listdir(templates_dir)):
            with open(os.path.join(templates_dir, template)) as f:
                contents = f.read()
                rendered_output = Template(contents).render(**template_args)
                if not os.path.isdir(rendered_dir):
                    os.makedirs(rendered_dir)
                with open(os.path.join(rendered_dir, template.replace('.j2', '')), mode='w') as fp:
                    fp.write(rendered_output)
                    logging.info('Generated: {}'.format(fp.name))
