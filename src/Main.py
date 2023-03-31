import argparse

import GoogleIAMFunctions
import GoogleResourceManagerFunctions
import Logger

def print_features():
    Logger.info('         Command              |           Description')
    Logger.info('google_create_project         | Create a new Google cloud project')
    Logger.info('google_create_service_account | Create a new service account, attached to a project')


if __name__ == '__main__':
    Logger.info('Starting demo...')

    parser = argparse.ArgumentParser(description='This is a prototype, to show the features of the IAM and the resource manager api of Google.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    args = parser.parse_args()

    verbose_logging = args.verbose
    while True:
        print_features()
        cmd = input('Command  > ')
        cmd = cmd.lower()

        if cmd == 'quit' or cmd == 'q':
            break
        elif cmd == 'google_create_project':
            Logger.info('Creating google project...')
        elif cmd == 'google_create_service_account':
            Logger.info('Creating service account...')

