import glob
import os

import pandas as pd

directory_private = '../documents/private'
directory_company_wide_public = '../documents/company-wide/public'
directory_company_wide_private = '../documents/company-wide/private'


def load_dataset():
    file_path = '../datasetHR/HRDataset.csv'
    df = pd.read_csv(file_path)
    return df


def get_all_usernames():
    df = load_dataset()
    employee_names = df['Employee_Name'].tolist()
    return employee_names


def getDocuments(allFiles=False, user=None):
    documents = []
    names = []
    if allFiles:
        for employee in os.listdir(directory_private):
            employee_directory = os.path.join(directory_private, employee)
            for file_name in os.listdir(employee_directory):
                file_path = os.path.join(employee_directory, file_name)
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as file:
                        contents = file.read()
                        documents.append(contents)
                        names.append(file_name)
        documents, names = add_company_wide_private_documents(documents, names)
    elif user is not None:
        user_path = os.path.join(directory_private, user)
        if os.path.isdir(user_path):
            text_files = glob.glob(os.path.join(user_path, user))
            for file_path in text_files:
                with open(file_path, 'r') as file:
                    contents = file.read()
                    documents.append(contents)
                    names.append(user)
            documents, names = add_company_wide_private_documents(documents, names)
    documents, names = add_public_documents(documents, names)
    return documents, names


def add_company_wide_private_documents(documents, names):
    if os.path.isdir(directory_company_wide_private):
        for file_name in os.listdir(directory_company_wide_private):
            file_path = os.path.join(directory_company_wide_private, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    contents = file.read()
                    documents.append(contents)
                    names.append(file_name)
    return documents, names


def add_public_documents(documents, names):
    if os.path.isdir(directory_company_wide_public):
        for file_name in os.listdir(directory_company_wide_public):
            file_path = os.path.join(directory_company_wide_public, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    contents = file.read()
                    documents.append(contents)
                    names.append(file_name)
    return documents, names


def check_username(username):
    return username in get_all_usernames()
