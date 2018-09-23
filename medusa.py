#!/usr/bin/env python3.6
import argparse
import os
import configparser
from lib.mysql import MySQL
from lib.nginx import NginX

store = {}
config = None


def main():
    os.chdir('/home/lun/Code/medusa')
    global config
    config = configparser.ConfigParser()

    try:
        config.read_file(open('config.ini'))
    except FileNotFoundError:
        exit('medusa: config.ini not found.')

    args = arg_parser()
    args.func(args)


def create_project(args):
    MySQL(config).create_db(args.project_name)
    NginX(args.project_name).make_cfg()

    with open('/etc/hosts', 'a') as fh:
        fh.write('127.0.0.1   {}.test\n'.format(args.project_name))


def delete_project(args):
    MySQL(config).drop_db(args.project_name)
    NginX(args.project_name).destroy_cfg()


def arg_parser():
    parser = argparse.ArgumentParser(
        prog="medusa"
    )
    subparsers = parser.add_subparsers()

    parser_create = subparsers.add_parser('create')
    parser_create.add_argument('-p', '--project-name', type=str, required=True)
    parser_create.set_defaults(func=create_project)

    parser_delete = subparsers.add_parser('delete')
    parser_delete.add_argument('-p', '--project-name', type=str, required=True)
    parser_delete.set_defaults(func=delete_project)

    args = parser.parse_args()
    if not vars(args):
        parser.print_help()
        parser.exit()

    return args


if __name__ == '__main__':
    main()
    exit()
