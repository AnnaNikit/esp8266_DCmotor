import argparse
from logging import Logger as l
import logging as l
import sys
from invoke import run
import os
import shutil

def parse_args(args=None):
    parser = argparse.ArgumentParser(prog='bootstrap')

    sub_parser = parser.add_subparsers(help="Help text for sub commands",
            dest='operation')
    parser_test = sub_parser.add_parser("test", help="Test applications")
    parser_test.add_argument('app', action='store')
    
    parser_test = sub_parser.add_parser("deploy", help="Deploy applications")
    parser_test.add_argument('app', action='store')

    if args is None or len(args) == 0:
        parser.print_help()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    l.debug(parsed_args)
    
    return parsed_args

class Runner(object):
    def __init__(self):
        self.APPS_DIR = '/Users/joshb/Python/hardware/esp8266/apps/'
        self.TESTS_DIR = '/Users/joshb/Python/hardware/esp8266/tests/'
        self.TEST_DEST_DIR = \
            '/Users/joshb/Python/hardware/esp8266/development_docker/'

    def get_applications():
        # TODO: List folders in app directory
        return [];

    def deploy(self, args):
        appdir = self.APPS_DIR + args.app

        if not os.access(appdir, os.R_OK):
            raise ValueError('Invalid app: ' + appdir)

        deploy_cmd = \
            'mpfshell -n -c "open ser:/dev/tty.SLAB_USBtoUART;' + \
            'mrm ^(?!boot.py$|webrepl_cfg.py$).*;'+ \
                  'lcd {};'.format(appdir) + \
                  'mput .*\.py$;' + \
                  'exec import machine;' + \
                  'exec machine.reset();"'

        run(deploy_cmd)
        
    def test(self, args):
        appdir = self.APPS_DIR + args.app
        testdir = self.TESTS_DIR + args.app
        codedir = self.TEST_DEST_DIR + 'code/'
        destinationdir = codedir + args.app

        l.debug('Checking app folder for access: ' + appdir)

        if not os.access(appdir, os.R_OK):
            raise ValueError('Invalid app: ' + appdir)

        l.debug('Checking test folder for access: ' + testdir)

        if not os.access(testdir, os.R_OK):
            raise ValueError('Invalid test: ' + testdir)

        if os.access(destinationdir, os.W_OK):
            pass

        shutil.rmtree(codedir, ignore_errors=True)
        
        os.makedirs(destinationdir)

        copy_cmd = 'cp {}/*.py {}/*.py {}' \
                     .format(appdir,testdir,destinationdir)
        run(copy_cmd)

        # Execute Docker

        docker_cmd = 'docker build -t micropython ' + \
                     '{} && '.format(self.TEST_DEST_DIR) + \
                     'docker run micropython bash -c "' + \
                     'cd code/{}; '.format(args.app) + \
                     '/usr/src/app/micropython/unix/micropython -c ' + \
                     '\\"import unittest; ' + \
                     'unittest.main(\'test_main\')\\""'\

        l.debug('Running docker command: {}'.format(docker_cmd))

        run(docker_cmd, pty=True)

        # docker run micropython cd code/temperature;
        # micropython -c "import unittest;unittest.main('test_main')"

def main():
    l.debug(sys.argv)
    args = parse_args(sys.argv[1:])

    runner = Runner()
    
    getattr(runner, args.operation)(args)

if __name__ == '__main__':
    main()
