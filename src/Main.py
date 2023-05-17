import argparse
import os
import json

import google.auth

import GoogleIAMFunctions
import GoogleResourceManagerFunctions
import Logger

def print_features():
    Logger.info('         Command                |           Description')
    Logger.info('quit || q || exit               | Exit this prototype and return to the command line')
    Logger.info('help || h                       | Show this help menu')
    Logger.info('clear                           | Clear the current screen')
    Logger.success('Google Resource Manager api functions:   ')
    Logger.info('  create_project                | Create a new Google cloud project')
    Logger.info('  delete_project                | Delete an existing Google cloud project')
    Logger.info('  get_project                   | Gets an existing project')
    Logger.info('  list_projects                 | Lists all existing projects, located in the provided folder or organization')
    Logger.info('  move_project                  | Move the project into a new folder or organization')
    Logger.info('  undelete_project              | Reverts the deletion of an previous deleted project')
    Logger.info('  update_project                | Updates the project internal name and retrieves the new generated name')
    Logger.info('  search_project                | Searches for an existing project, for more information about the query params see https://cloud.google.com/resource-manager/reference/rest/v3/projects/search#query-parameters')
    Logger.info('  project_set_iam_policy        | One of the connectors to the IAM api. Sets the current IAM policy')
    Logger.info('  project_get_iam_policy        | One of the connectors to the IAM api. Gets the current IAM policy')
    Logger.info('  create_folder                 | Creates a new folder inside another folder')
    Logger.info('  delete_folder                 | Deletes an existing folder')
    Logger.info('  get_folder                    | Retrieves a folder by name and returns an instance of https://cloud.google.com/resource-manager/reference/rest/v3/folders#Folder')
    Logger.info('  move_folder                   | Moves an existing folder to a new location')
    Logger.info('  undelete_folder               | Reverts the deletion of an previous deleted folder')
    Logger.info('  list_folders                  | Returns a list of all folders, associated with the current project')
    Logger.info('  get_organization              | Gets the organization object, by the specified name')
    Logger.success('Google IAM api functions:  ')
    Logger.info('  create_service_account        | Create a new service account, attached to a project')
    Logger.info('  delete_service_account        | Delete an existing service account')
    Logger.info('  list_service_accounts         | Returns a list of all service accounts, associated with the current project')
    Logger.info('  activate_service_account      | Activates a service account')
    Logger.info('  deactivate_service_account    | Deactivates a service account')
    Logger.info('  rename_service_account        | Renames a service account')
    Logger.info('  create_service_account_key    | Creates a new key for a service account')
    Logger.info('  list_service_account_keys     | Lists all keys from a service account')
    Logger.info('  delete_service_account_key    | Deletes a specific key from a service account')
    Logger.info('  enable_role                   | Enables a disabled role')
    Logger.info('  disable_role                  | Disables an existing role')
    Logger.info('  delete_role                   | Deletes an existing role')
    Logger.info('  create_role                   | Creates a new role')
    Logger.info('  edit_role                     | edits an existing role')
    Logger.info('  recover_role                  | Recovers a deleted role')
    Logger.info('  list_roles                    | Lists all roles')
    Logger.info('  get_role                      | Gets a specific role')
    Logger.info('  query_grantable_roles         | Queries all roles, that can be granted (returns a list of all standard google roles)')
    Logger.info('  set_policy                    | Sets the policy')
    Logger.info('  add_member_to_policy          | Adds a member to a policy')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is a prototype, to show the features of the IAM and the resource manager api of Google.')
    parser.add_argument('-v', '--version', action='store_true', help='Show version')
    args = parser.parse_args()

    if args.version:
        Logger.success('Version 1.0.0')
        quit(0)

    last_result = None
    last_error = None
    show_help_menu = False
    should_clear_screen = False

    # This function looks into the environment variable GOOGLE_APPLICATION_CREDENTIALS 
    # and retrieves all necessary information from the json key file
    credentials, project = google.auth.default()

    while True:
        if should_clear_screen:
            os.system('clear')
            should_clear_screen = False

        Logger.success(f'Currently selected project: {project}')

        if show_help_menu:
            show_help_menu = False
            print_features()

        if last_error is not None:
            Logger.error(f'An error occurred in your last input: {last_error}')
            last_error = None

        if last_result is not None:
            Logger.success('Result of your last input:')
            try:
                Logger.success(json.dumps(last_result, indent=4))
            except TypeError:
                Logger.success(last_result)
            last_result = None

        try:
            cmd = input('Command  > ')
            cmd = cmd.lower()
        except KeyboardInterrupt:
            break

        if cmd == 'quit' or cmd == 'q' or cmd == 'exit':
            break
        elif cmd == 'help' or cmd == 'h':
            show_help_menu = True
        elif cmd == 'clear':
            should_clear_screen = True
        elif cmd == 'create_project':
            Logger.info('Creating google project...')
            
            try:
                last_result = GoogleResourceManagerFunctions.create_project()
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.create_project failed.'
        elif cmd == 'delete_project':
            Logger.info('Deleting google project, please provide additional information...')

            try:
                project_name = input('The name of the project to be deleted...')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleResourceManagerFunctions.delete_project(project_name=project_name)
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.delete_project failed.'
        elif cmd == 'get_project':
            Logger.info('Getting an existing project, please provide additional information...')

            try:
                last_result = GoogleResourceManagerFunctions.get_project(project_name=project)
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.get_project failed.'
        elif cmd == 'list_projects':
            Logger.info('Listing all projects, please provide additional information...')

            try:
                resource_name = input('The folder, from which the projects should be listed (leave empty to list all projects by organization) > ')
                is_folder = True
                if len(resource_name) == 0:
                    resource_name = input('The organization, from which the projects should be listed > ')
                    is_folder = False
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleResourceManagerFunctions.list_projects(parent_resource=resource_name, is_folder=is_folder)
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.list_projects failed.'
        elif cmd == 'move_project':
            Logger.info('Moving project, please provide additional information...')

            try:
                project_name = input('The project name, which should be moved > ')
                resource_name = input('The destination folder, into which the project should be moved (leave empty to move the project into another organization) > ')
                is_folder = True
                if len(resource_name) == 0:
                    resource_name = input('The organization, into which the project should be moved > ')
                    is_folder = False
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleResourceManagerFunctions.move_project(
                    project_name=project_name, 
                    dest_resource=resource_name, 
                    is_folder=is_folder
                )
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.move_project failed.'
        elif cmd == 'search_projects':
            Logger.info('Searching for project, please provide additional information...')

            try:
                query = input('The query, which should be used for the search > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleResourceManagerFunctions.search_projects(query=query)
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.search_projects failed.'
        elif cmd == 'project_set_iam_policy':
            Logger.info('Setting the IAM policy, please provide additional information...')

            try:
                resource_name = input('The resource name > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleResourceManagerFunctions.project_set_iam_policy(resource_name=resource_name)
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.project_set_iam_policy failed.'
        elif cmd == 'project_get_iam_policy':
            Logger.info('Getting the IAM policy, please provide additional information...')

            try:
                resource_name = input('The resource name > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleResourceManagerFunctions.project_get_iam_policy(resource_name=resource_name)
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.project_get_iam_policy failed.'
        elif cmd == 'undelete_project':
            Logger.info('Undeleting project, please provide additional information...')
            
            try:
                project_name = input('The project name, which deletion should be cancelled > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleResourceManagerFunctions.undelete_project(project_name=project_name)
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.undelete_project failed.'
        elif cmd == 'update_project':
            Logger.info('Updating project...')
            try:
                last_result = GoogleResourceManagerFunctions.update_project()
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.update_project failed.'
        elif cmd == 'create_service_account':
            Logger.info('Creating service account, please provide additional information...')

            try:
                display_name = input('The display name of the new service account > ')
                name = input('The name of the new service account > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.create_service_account(name, display_name, project)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.create_service_account failed.'
        elif cmd == 'delete_service_account':
            Logger.info('Deleting google service account, please provide additional information...')

            try:
                email = input('Email of service account to delete  > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.delete_service_account(email)
                Logger.success('Service account deleted successfully')
            except Exception:
                last_error = 'Function GoogleIAMFunctions.delete_service_account failed.'
        elif cmd == 'create_folder':
            Logger.info('Creating a new folder, please provide additional information...')

            try:
                folder_name = input('The name of the new folder > ')
                parent_name = input('The name of the parent folder > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleResourceManagerFunctions.create_folder(display_name=display_name, parent_name=parent_name)
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.create_folder failed.'
        elif cmd == 'delete_folder':
            Logger.info('Deleting existing folder, please provide additional information...')

            try:
                folder_name = input('The name of the folder, which should be deleted > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleResourceManagerFunctions.delete_folder(folder_name=folder_name)
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.delete_folder failed.'
        elif cmd == 'get_folder':
            Logger.info('Retrieving existing folder, please provide additional information...')

            try:
                folder_name = input('The name of the existing folder > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleResourceManagerFunctions.get_folder(folder_name=folder_name)
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.get_folder failed.'
        elif cmd == 'move_folder':
            Logger.info('Moving existing folder, please provide additional information...')

            try:
                folder_name = input('The name of the existing folder > ')
                destination = input('The name of the destination folder, to move the folder to > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleResourceManagerFunctions.move_folder(folder_name=folder_name, destination_path=destination)
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.move_folder failed.'
        elif cmd == 'undelete_folder':
            Logger.info('Undeleting folder, please provide additional information...')

            try:
                folder_name = input('The name of the folder to undelete > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleResourceManagerFunctions.undelete_folder(folder_name=folder_name)
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.undelete_folder failed.'
        elif cmd == 'list_folders':
            Logger.info('Listing all google folders...')

            try:
                resource_name = input('The parent folder to show the contents from (leave empty to show the folders of an organization) > ')
                is_folder = True
                if len(resource_name) == 0:
                    is_folder = False
                    resource_name = input('The organization to show the contents from > ')

            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleResourceManagerFunctions.list_folders(parent_resource=resource_name, is_folder=is_folder)
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.list_folders failed.'
        elif cmd == 'list_service_accounts':
            Logger.info('Listing all service accounts...')
            try:
                last_result = GoogleIAMFunctions.list_service_accounts(project=project)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.list_service_accounts failed.'
        elif cmd == 'get_organization':
            Logger.info('Showing all organization properties of current project...')

            try:
                name = input('The name of the organization > ')
            except KeyboardInterrupt:
                continue
            
            try:
                last_result = GoogleResourceManagerFunctions.get_organization(name=name)
            except Exception:
                last_error = 'Function GoogleResourceManagerFunctions.get_organization failed.'
        elif cmd == 'activate_service_account':
            Logger.info('Activating a service account, please provide additional information...')

            try:
                email = input('The email of the service account > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.activate_service_account(email=email)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.activate_service_account failed.'
        elif cmd == 'deactivate_service_account':
            Logger.info('Deactivating a service account, please provide additional information...')

            try:
                email = input('The email of the service account > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.deactivate_service_account(email=email)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.deactivate_service_account failed.'
        elif cmd == 'rename_service_account':
            Logger.info('Renaming a service account, please provide additional information...')

            try:
                email = input('The email of the service account > ')
                new_display_name = input('The new display name the service account should be renamed to > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.rename_service_account(email=email, new_display_name=new_display_name)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.rename_service_account failed.'
        elif cmd == 'create_service_account_key':
            Logger.info('Creating a new service account key, please provide additional information...')

            try:
                email = input('The email of the service account > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.create_service_account_key(service_account_email=email)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.create_service_account_key failed.'
        elif cmd == 'list_service_account_keys':
            Logger.info('Listing all service account keys, please provide additional information...')

            try:
                email = input('The email of the service account > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.list_service_account_keys(service_account_email=email)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.list_service_account_keys failed.'
        elif cmd == 'delete_service_account_key':
            Logger.info('Deleting a specific service account key, please provide additional information...')

            try:
                key = input('The service account key to be deleted > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.delete_service_account_key(key_name=key)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.delete_service_account_key failed.'
        elif cmd == 'enable_role':
            Logger.info('Enabling a role, please provide additional information...')

            try:
                role = input('The role name to be enabled > ')
                stage = input('The new stage tot set the role to (either GA, ALPHA or BETA) > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.enable_role(role_name=role, stage=stage, project=project)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.enable_role failed.'
        elif cmd == 'disable_role':
            Logger.info('Disabling a role, please provide additional information...')

            try:
                role = input('The role name to be disabled > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.disable_role(role_name=role, project=project)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.disable_role failed.'
        elif cmd == 'delete_role':
            Logger.info('Deleting a role, please provide additional information...')

            try:
                role = input('The role name to be deleted > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.delete_role(role_name=role, project=project)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.delete_role failed.'
        elif cmd == 'create_role':
            Logger.info('Creating a role, please provide additional information...')

            try:
                role = input('The role name > ')
                title = input('The role display title > ')
                description = input('The role description > ')
                stage = input('The role stage (Either GA, ALPHA or BETA) > ')

                permissions = []
                while True:
                    current_permission = input('Permissions (enter \'q\' to stop entering permissions) > ')
                    if current_permission == 'q':
                        break

                    permissions.append(current_permission)
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.create_role(
                    role_name=role,
                    project=project,
                    title=title,
                    description=description, 
                    permissions=permissions, 
                    stage=stage
                )
            except Exception:
                last_error = 'Function GoogleIAMFunctions.create_role failed.'
        elif cmd == 'edit_role':
            Logger.info('Editing a role, please provide additional information...')
            
            try:
                role = input('The role name > ')
                title = input('The role display title > ')
                description = input('The role description > ')
                stage = input('The role stage (Either GA, ALPHA or BETA)  > ')

                permissions = []
                while True:
                    current_permission = input('Permissions (enter \'q\' to stop entering permissions) > ')
                    if current_permission == 'q':
                        break

                    permissions.append(current_permission)
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.edit_role(
                    role_name=role, 
                    project=project, 
                    title=title, 
                    description=description, 
                    permissions=permissions, 
                    stage=stage
                )
            except Exception:
                last_error = 'Function GoogleIAMFunctions.edit_role failed.'
        elif cmd == 'recover_role':
            Logger.info('Recovering a role, please provide additional information...')

            try:
                role = input('The role to be recovered > ')
            except KeyboardInterrupt:
                continue
        
            try:
                last_result = GoogleIAMFunctions.recover_role(role_name=role, project=project)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.recover_role failed.'
        elif cmd == 'list_roles':
            Logger.info('Listing all roles...')
            last_result = GoogleIAMFunctions.list_roles(project=project)
        elif cmd == 'get_role':
            Logger.info('Retrieving a specific role, please provide additional information...')

            try:
                role = input('The specific role name to be retrieved > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.get_role(role_name=role)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.get_role failed.'
        elif cmd == 'query_grantable_roles':
            Logger.info('Retrieving all grantable roles, please provide additional information...')

            try:
                name = input('The full resource name to query the grantable roles from > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.query_grantable_roles(name=name)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.query_grantable_roles failed.'
        elif cmd == 'set_policy':
            Logger.info('Setting the IAM policy, please provide additional information...')

            try:
                name = input('The resource name, which is used to get the policy from the resource manager api and then is set to the IAM api > ')
            except KeyboardInterrupt:
                continue

            policy = GoogleResourceManagerFunctions.project_get_iam_policy(resource_name=name)

            try:
                last_result = GoogleIAMFunctions.set_policy(project=project, policy=policy)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.set_policy failed.'

        elif cmd == 'add_member_to_policy':
            Logger.info('Adding a member to the IAM policy, please provide additional information...')
            
            try:
                name = input('The resource name, which is used to get the policy from the resource manager api > ')
                role = input('The role name to be set > ')
                member = input('The member to be set > ')
            except KeyboardInterrupt:
                continue

            try:
                last_result = GoogleIAMFunctions.add_member_to_policy(policy=policy, role=role, member=member)
            except Exception:
                last_error = 'Function GoogleIAMFunctions.add_member_to_policy failed.'
        else:
            last_error = 'Unknown command'
