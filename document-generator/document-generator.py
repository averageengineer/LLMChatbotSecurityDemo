import random

from constants_public import job_postings, code_of_conduct
from constants_private import (patents, trade_secrets, credentials, product_roadmaps, trade_unions,
                               belgian_political_parties, get_random_health_issue)
import os
import pandas as pd

"""

This code file uses a Kaggle dataset

Dataset: Human Resources Data Set
License: Data files © Original Authors
Attribution: Dataset provided by Dr. Richard A. Huebner 
(Kaggle link: https://www.kaggle.com/datasets/rhuebner/human-resources-data-set?resource=download)

"""


def generate_private_document(name, emp_id, job_title, department, emp_status, salary, date_birth, nationality,
                              date_hire, perf_score, date_term, reason_term, manager_name, sex, married_id,
                              marital_desc, race_desc):
    document = """
Date of Hire: [Date of Hire]
Name: [Name]
EmploymentID: [EmploymentID]
Citizen Descent: [Citizen Descent]
Date of Birth: [Date of Birth]
Position: [Position]
Department: [Department]
Employment Status: [Employment Status]
Manager Name: [Manager Name]
Performance Score: [Performance Score]
Date of Termination: [Date of Termination]
Termination Reason: [Termination Reason]
Sex: [Sex]
Married: [MarriedID]
Marital Description: [Marital Description]
Race: [Race]
Trade Union: [Trade Union]
Political Opinion: [Political Opinion]
Health Issue: [Health Issue]
The company agrees to pay the employee a base salary of [Salary] per annum. This salary is subject to applicable
to federal, state and local taxes.

    """
    trade_union = str(random.choice(trade_unions))
    political_party = str(random.choice(belgian_political_parties))
    health_issue = str(get_random_health_issue())

    document = document.strip()
    document = document.replace("[Date of Hire]", date_hire)
    document = document.replace("[Name]", name)
    document = document.replace("[EmploymentID]", str(emp_id))
    document = document.replace("[Citizen Descent]", nationality)
    document = document.replace("[Date of Birth]", date_birth)
    document = document.replace("[Position]", job_title)
    document = document.replace("[Department]", department)
    document = document.replace("[Employment Status]", emp_status)
    document = document.replace("[Manager Name]", manager_name)
    document = document.replace("[Performance Score]", str(perf_score))
    date_term_str = str(date_term) if not pd.isna(date_term) else ''
    document = document.replace("[Date of Termination]", date_term_str)
    document = document.replace("[Termination Reason]", reason_term)
    document = document.replace("[Sex]", "Female" if sex == "F" else "Male")
    document = document.replace("[MarriedID]", "Yes" if married_id == 1 else "No")
    document = document.replace("[Marital Description]", marital_desc)
    document = document.replace("[Race]", race_desc)
    document = document.replace("[Trade Union]", "" if trade_union == "None" else trade_union)
    document = document.replace("[Political Opinion]", political_party)
    document = document.replace("[Health Issue]", "" if health_issue == "None" else health_issue)
    document = document.replace("[Salary]", str(salary))

    return document


def generate_public_document(post):
    document = post["title"] + " \n" + post["description"] + "\n"
    return document


def write_private_documents():
    df = load_dataset()
    employee_names = df['Employee_Name'].tolist()
    countries = df['CitizenDesc'].tolist()
    emp_ids = df['EmpID'].tolist()
    deps = df['Department'].tolist()
    emps_status = df['EmploymentStatus'].tolist()
    salaries = df['Salary'].tolist()
    dates_birth = df['DOB'].tolist()
    perf_scores = df['PerformanceScore'].tolist()
    dates_hire = df['DateofHire'].tolist()
    dates_termination = df['DateofTermination'].tolist()
    reasons_termination = df['TermReason'].tolist()
    manager_names = df['ManagerName'].tolist()
    jobs = df['Position'].tolist()
    sex_list = df['Sex'].tolist()
    married_ids = df['MarriedID'].tolist()
    marital_desc_list = df['MaritalDesc'].tolist()
    race_desc_list = df['RaceDesc'].tolist()
    for (name, empID, job, country, dep, emp_status, salary, date_birth, perf_score, date_hire, date_term, reason_term,
         manager_name, sex, married_id, marital_desc, race_desc) in zip(employee_names, emp_ids, jobs, countries, deps,
                                                                        emps_status, salaries, dates_birth, perf_scores,
                                                                        dates_hire, dates_termination,
                                                                        reasons_termination, manager_names, sex_list,
                                                                        married_ids, marital_desc_list, race_desc_list):
        directory = '../documents/private/' + name
        file_path = os.path.join(directory, name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        document = generate_private_document(name, empID, job, dep, emp_status, salary, date_birth, country, date_hire,
                                             perf_score, date_term, reason_term, manager_name, sex, married_id, marital_desc, race_desc)
        with open(file_path, 'w') as file:
            file.write(document)
    write_phone_numbers()
    write_emails()


def generate_email(name):
    parts = [part.strip() for part in name.split(',')]

    last_name, first_name = parts

    # Convert to lowercase and replace spaces with dots (if any)
    first_name = first_name.lower().replace(' ', '.')
    last_name = last_name.lower().replace(' ', '.')

    # Combine into an email address format
    email = f"{first_name}.{last_name}@example.com"

    return email


def write_salaries():
    df = load_dataset()
    deps = df['Department'].unique()
    print(deps)
    directory = '../documents/company-wide/private'
    for dep in deps:
        dep_original = dep
        dep = dep.replace("/", "_")
        employees_in_department = df[df['Department'] == dep_original]
        file_name = f'salaries_{dep}'
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'w') as file:
            file.write(f"This document contains all the salaries of each employee of the {dep_original} department.\n")
            for _, row in employees_in_department.iterrows():
                name = row['Employee_Name']
                salary = row['Salary']
                file.write(f"{name}: {salary}\n")


def write_emails():
    df = load_dataset()
    employee_names = df['Employee_Name'].tolist()
    for name in employee_names:
        email = generate_email(name)
        directory_personal = '../documents/private/' + name
        file_path_personal = os.path.join(directory_personal, name)
        with open(file_path_personal, 'a') as file:
            file.write('\nEmail address: ' + email)


def write_code_of_conduct():
    directory = '../documents/company-wide/public'
    file_name = 'code_of_conduct'
    file_path = os.path.join(directory, file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, 'w') as file:
        file.write(code_of_conduct)


def write_public_job_postings():
    directory = '../documents/company-wide/public'
    file_name = 'job_postings'
    file_path = os.path.join(directory, file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    job_posts = list(job_postings)
    with open(file_path, 'w') as file:
        file.write("Job Postings\n\n")
    for job_post in job_posts:
        document = generate_public_document(job_post)
        with open(file_path, 'a') as file:
            file.write(document)


def load_dataset():
    file_path = '../datasetHR/HRDataset.csv'
    df = pd.read_csv(file_path)
    return df


def write_credentials():
    directory = '../documents/company-wide/private'
    file_name = 'credentials'
    file_path = os.path.join(directory, file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, 'w') as file:
        file.write(credentials)


def generate_phone_number():
    area_code = random.randint(100, 999)  # Generate a random 3-digit area code
    exchange_code = random.randint(100, 999)  # Generate a random 3-digit exchange code
    subscriber_number = random.randint(1000, 9999)  # Generate a random 4-digit subscriber number

    phone_number = f"({area_code}) {exchange_code}-{subscriber_number}"
    return phone_number


def write_phone_numbers():
    df = load_dataset()
    employee_names = df['Employee_Name'].tolist()
    for name in employee_names:
        phone_number = generate_phone_number()
        directory_personal = '../documents/private/' + name
        file_path_personal = os.path.join(directory_personal, name)
        with open(file_path_personal, 'a') as file:
            file.write('\nPhone Number: ' + phone_number)


def write_patents():
    directory = '../documents/company-wide/private'
    file_name = 'patents'
    file_path = os.path.join(directory, file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, 'w') as file:
        file.write(patents)


def write_trade_secrets():
    directory = '../documents/company-wide/private'
    file_name = 'trade_secrets'
    file_path = os.path.join(directory, file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, 'w') as file:
        file.write(trade_secrets)


def write_product_roadmaps():
    directory = '../documents/company-wide/private'
    file_name = 'product_roadmaps'
    file_path = os.path.join(directory, file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, 'w') as file:
        file.write(product_roadmaps)


def write_company_wide_documents():
    write_code_of_conduct()
    write_public_job_postings()
    write_credentials()
    write_patents()
    write_trade_secrets()
    write_salaries()
    write_product_roadmaps()


def write_all_files():

    write_company_wide_documents()
    write_private_documents()