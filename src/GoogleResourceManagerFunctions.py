import os
import requests

import google.auth
from google.cloud import resourcemanager_v3
from google.oauth2 import service_account
from google.iam.v1 import iam_policy_pb2

def create_project():
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformprojects'
    ])

    # Create a client
    client = resourcemanager_v3.ProjectsClient(credentials=scoped_credentials)
    """
    
    # Create a client
    client = resourcemanager_v3.ProjectsClient()

    # Initialize request argument(s)
    request = resourcemanager_v3.CreateProjectRequest(
    )

    # Make the request
    operation = client.create_project(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()
    return response

def delete_project(project_name):
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformprojects'
    ])

    # Create a client
    client = resourcemanager_v3.ProjectsClient(credentials=scoped_credentials)
    """

    # Create a client
    client = resourcemanager_v3.ProjectsClient()

    # Initialize request argument(s)
    request = resourcemanager_v3.DeleteProjectRequest(
        name=f'projects/{project_name}',
    )

    # Make the request
    operation = client.delete_project(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()
    return response

def get_project(project_name):
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformprojects'
    ])

    # Create a client
    client = resourcemanager_v3.ProjectsClient(credentials=scoped_credentials)
    """

    # Create a client
    client = resourcemanager_v3.ProjectsClient()

    # Initialize request argument(s)
    request = resourcemanager_v3.GetProjectRequest(
        name=f'projects/{project_name}',
    )

    # Make the request
    response = client.get_project(request=request)
    return response

def list_projects(parent_resource, is_folder = True):
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformprojects'
    ])

    # Create a client
    client = resourcemanager_v3.ProjectsClient(credentials=scoped_credentials)
    """

    # Create a client
    client = resourcemanager_v3.ProjectsClient()

    # Initialize request argument(s)
    payload = f'folders/{parent_resource}'
    if not is_folder:
        payload = f'organizations/{parent_resource}'

    request = resourcemanager_v3.ListProjectsRequest(
        parent=payload,
    )

    # Make the request
    page_result = client.list_projects(request=request)

    # Handle the response
    for response in page_result:
        print(response)

    return page_result

def move_project(project_name, dest_resource, is_folder=True):
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformprojects'
    ])

    # Create a client
    client = resourcemanager_v3.ProjectsClient(credentials=scoped_credentials)
    """

    # Create a client
    client = resourcemanager_v3.ProjectsClient()

    new_parent = f'folders/{dest_resource}'
    if not is_folder:
        new_parent = f'organizations/{dest_resource}'

    # Initialize request argument(s)
    request = resourcemanager_v3.MoveProjectRequest(
        name=f'projects/{project_name}',
        destination_parent=new_parent,
    )

    # Make the request
    operation = client.move_project(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()
    return response

def search_projects(query):
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformprojects'
    ])

    # Create a client
    client = resourcemanager_v3.ProjectsClient(credentials=scoped_credentials)
    """

    # Create a client
    client = resourcemanager_v3.ProjectsClient()

    # Initialize request argument(s)
    request = resourcemanager_v3.SearchProjectsRequest(
        query=query
    )

    # Make the request
    page_result = client.search_projects(request=request)

    # Handle the response
    for response in page_result:
        print(response)

    return page_result

def project_set_iam_policy(resource_name):
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformprojects'
    ])

    # Create a client
    client = resourcemanager_v3.ProjectsClient(credentials=scoped_credentials)
    """
    
    # Create a client
    client = resourcemanager_v3.ProjectsClient()

    # Initialize request argument(s)
    request = iam_policy_pb2.SetIamPolicyRequest(
        resource=resource_name,
    )

    # Make the request
    response = client.set_iam_policy(request=request)
    return response

def project_get_iam_policy(resource_name):
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformprojects'
    ])

    # Create a client
    client = resourcemanager_v3.ProjectsClient(credentials=scoped_credentials)
    """

    # Create a client
    client = resourcemanager_v3.ProjectsClient()

    # Initialize request argument(s)
    request = iam_policy_pb2.GetIamPolicyRequest(
        resource=resource_name,
    )

    # Make the request
    response = client.get_iam_policy(request=request)
    return response

def undelete_project(project_name):
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformprojects'
    ])

    # Create a client
    client = resourcemanager_v3.ProjectsClient(credentials=scoped_credentials)
    """

    # Create a client
    client = resourcemanager_v3.ProjectsClient()

    # Initialize request argument(s)
    request = resourcemanager_v3.UndeleteProjectRequest(
        name=f'projects/{project_name}',
    )

    # Make the request
    operation = client.undelete_project(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()
    return response

def update_project():
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformprojects'
    ])

    # Create a client
    client = resourcemanager_v3.ProjectsClient(credentials=scoped_credentials)
    """

    # Create a client
    client = resourcemanager_v3.ProjectsClient()

    # Initialize request argument(s)
    request = resourcemanager_v3.UpdateProjectRequest(
    )

    # Make the request
    operation = client.update_project(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()
    return response

def get_organization(name):
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformorganizations'
    ])

    # Create a client
    client = resourcemanager_v3.OrganizationsClient(credentials=scoped_credentials)
    """

     # Create a client
    client = resourcemanager_v3.OrganizationsClient()

    # Initialize request argument(s)
    request = resourcemanager_v3.GetOrganizationRequest(
        name=f'organizations/{name}',
    )

    # Make the request
    response = client.get_organization(request=request)
    return response

def create_folder(display_name, parent_name):
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformfolders'
    ])

    # Create a client
    client = resourcemanager_v3.FoldersClient(credentials=scoped_credentials)
    """

    # Create a client
    client = resourcemanager_v3.FoldersClient()

    # Initialize request argument(s)
    folder = resourcemanager_v3.Folder()
    folder.parent = f'folders/{parent_name}'
    folder.displayName = display_name

    request = resourcemanager_v3.CreateFolderRequest(
        folder=folder,
    )

    # Make the request
    operation = client.create_folder(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()
    return response

def delete_folder(folder_name):
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformfolders'
    ])

    # Create a client
    client = resourcemanager_v3.FoldersClient(credentials=scoped_credentials)
    """

    # Create a client
    client = resourcemanager_v3.FoldersClient()

    # Initialize request argument(s)
    request = resourcemanager_v3.DeleteFolderRequest(
        name=f'folders/{folder_name}',
    )

    # Make the request
    operation = client.delete_folder(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()
    return response

def get_folder(folder_name):
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformfolders'
    ])

    # Create a client
    client = resourcemanager_v3.FoldersClient(credentials=scoped_credentials)
    """

    # Create a client
    client = resourcemanager_v3.FoldersClient()

    # Initialize request argument(s)
    request = resourcemanager_v3.GetFolderRequest(
        name=f'folders/{folder_name}',
    )

    # Make the request
    response = client.get_folder(request=request)
    return response

def move_folder(folder_name, destination_path):
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformfolders'
    ])

    # Create a client
    client = resourcemanager_v3.FoldersClient(credentials=scoped_credentials)
    """
    
    # Create a client
    client = resourcemanager_v3.FoldersClient()

    # Initialize request argument(s)
    request = resourcemanager_v3.MoveFolderRequest(
        name=f'folders/{folder_name}',
        destination_parent=f'folders/{destination_path}',
    )

    # Make the request
    operation = client.move_folder(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()
    return response

def undelete_folder(folder_name):
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformfolders'
    ])

    # Create a client
    client = resourcemanager_v3.FoldersClient(credentials=scoped_credentials)
    """

    # Create a client
    client = resourcemanager_v3.FoldersClient()

    # Initialize request argument(s)
    request = resourcemanager_v3.UndeleteFolderRequest(
        name=f'folders/{folder_name}',
    )

    # Make the request
    operation = client.undelete_folder(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()
    return response

def list_folders(parent_resource, is_folder=True):
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    scoped_credentials = credentials.with_scopes([
        'https://www.googleapis.com/auth/cloud-platform', 
        'https://www.googleapis.com/auth/cloudplatformfolders'
    ])

    # Create a client
    client = resourcemanager_v3.FoldersClient(credentials=scoped_credentials)
    """

    # Create a client
    client = resourcemanager_v3.FoldersClient()

    # Initialize request argument(s)
    payload = f'folders/{parent_resource}'
    if not is_folder:
        payload = f'organizations/{parent_resource}'

    request = resourcemanager_v3.ListFoldersRequest(
        parent=payload,
    )

    # Make the request
    page_result = client.list_folders(request=request)

    # Handle the response
    for response in page_result:
        print(response)

    return page_result

"""
def list_folders_old():
    base_url = os.environ['GOOGLE_CLOUD_RESOURCE_MANAGER_BASE_API']
    api_key = os.environ['GOOGLE_CLOUD_API_KEY']
    payload = {'key': api_key}
    response = requests.get(f'{base_url}/folders', params=payload)
    return response
"""
