import os

from google.oauth2 import service_account
import googleapiclient.discovery

import Logger

def get_service():
    """ Internal getter to simplify API usage """
    credentials = service_account.Credentials.from_service_account_file(filename=os.environ['GOOGLE_CLOUD_CREDENTIALS'], scopes=['https://www.googleapis.com/auth/cloud-platform'])
    return googleapiclient.discovery.build('iam', 'v1', credentials=credentials)

def activate_service_account(email):
    """ activates an existing service account """
    service = get_service()
    service.projects().serviceAccounts().enable(name='projects/-/serviceAccounts/' + email).execute()

def deactivate_service_account(email):
    """ deactivates an existing service account """
    service = get_service()
    service.projects().serviceAccounts().disable(name='projects/-/serviceAccounts/' + email).execute()

def delete_service_account(email):
    """ Deletes an existing service account """
    service = get_service()
    service.projects().serviceAccounts().delete(name='projects/-/serviceAccounts/' + email).execute()

def create_service_account(name, display_name, project):
    """ Creates a new service account"""

    service = get_service()

    new_account = service.projects().serviceAccounts().create(
        name='projects/' + project,
        body={
            'accountId': name,
            'serviceAccount': {
                'displayName': display_name
            }
        }
    ).execute()

    new_email = new_account['email']
    Logger.success(f'Created service account {new_email}')
    return new_account

def list_service_accounts(project):
    """ Lists all service accounts created. """
    service = get_service()
    service_accounts = service.projects().serviceAccounts().list(name='projects/' + project).execute()

    Logger.success('Successfully got a list of service accounts:')
    for account in service_accounts['accounts']:
        account_name = account['name']
        account_email = account['email']
        Logger.info(f'  Name   : {account_name}')
        Logger.info(f'  E-Mail : {account_email}')
        Logger.info('\n')

    return service_accounts

def disable_role(role_name, project):
    """ Disables existing role. """
    service = get_service()
    role = service.projects().roles().patch(name='projects/' + project + '/roles/' + role_name, body={
        'stage': 'DISABLED'
    }).execute()
    Logger.success(f'Successfully disabled role {role_name}')
    return role

def delete_role(role_name, project):
    """ Deletes existing role. """
    service = get_service()
    role = service.projects().roles().delete(name='projects/' + project + '/roles/' + role_name).execute()
    Logger.success(f'Successfully deleted role {role_name}')
    return role

def create_role(role_name, project, title, description, permissions, stage):
    """ Creates new role. """

    service = get_service()
    role = service.projects().roles().create(
        parent='projects/' + project,
        body={
            'roleId': role_name,
            'role': {
                'title': title,
                'description': description,
                'includedPermissions': permissions,
                'stage': stage,
            }
        }
    ).execute()
    Logger.success(f'Successfully created role {role_name}')
    return role

def edit_role(role_name, project, title, description, permissions, stage):
    """ Updates existing role. """
    service = get_service()
    role = service.projects().roles().patch(
        name='projects/' + project + '/roles/' + role_name,
        body={
            'title': title,
            'description': description,
            'includedPermissions': permissions,
            'stage': stage,
        }
    )
    Logger.success(f'Successfully edited role {role_name}')
    return role

def recover_role(role_name, project):
    """ Is meant to recover a custom role, but looks like the same code, as for deleting a role """
    """ @see: https://cloud.google.com/iam/docs/samples/iam-undelete-role?hl=de """
    service = get_service()
    role = service.projects().roles().patch(
        name='projects/' + project + '/roles/' + role_name,
        body={
            'stage': 'DISABLED'
        }
    ).execute()
    return role

def list_roles(project):
    """ Lists all roles. """
    service = get_service()
    roles = service.roles().list(parent='projects/' + project).execute()

    for role in roles['roles']:
        role_name = role['name']
        Logger.success(f'Found role {role_name}')

    return roles

def get_role(role_name):
    """ Getter for existing role. """
    service = get_service()
    role = service.roles().get(name=role_name).execute()
    real_role_name = role['name']
    Logger.success(f'Found role {real_role_name}, Permissions:')

    for permission in role['includedPermissions']:
        Logger.info(permission)

    return role

def set_policy(project, policy):
    """ Sets IAM policy for a project. """
    service = get_service()
    policy = (service.projects().setIamPolicy(resource=project, body={'policy': policy}).execute())
    print(policy)
    return policy

def query_grantable_roles(name):
    """ Query all roles, which can be assigned. """

    service = get_service()
    roles = service.roles().queryGrantableRoles(body={
        'fullResourceName': name
    }).execute()

    for role in roles['roles']:
        if 'title' in role:
            Logger.info('Title: ' + role['title'])
        Logger.info('Name: ' + role['name'])
        if 'description' in role:
            Logger.info('Description: ' + role['description'])
        print('\n')
    return roles

def add_member_to_policy(policy, role, member):
    """Adds a new member to a role binding."""

    binding = next(b for b in policy["bindings"] if b["role"] == role)
    binding["members"].append(member)

    Logger.info(binding)
    return policy

