import GoogleIAMFunctions
import GoogleResourceManagerFunctions
import Logger

def print_features():
    Logger.info('         Command              |           Description')
    Logger.info('google_create_project         | Create a new Google cloud project')
    Logger.info('google_create_service_account | Create a new service account, attached to a project')

def main():
    Logger.info('Starting demo...')

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

if __name__ == '__main__':
    main()

