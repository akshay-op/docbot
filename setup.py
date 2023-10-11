from setuptools import find_packages,setup
from typing import List

HE ='-e .'

def get_requirements(file_path:str)->List[str]:
    requirements=[]
    with open (file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","")for req in requirements]
        if HE in requirements:
            requirements.remove(HE)
    return requirements





setup(
    name='datascience project',
    version='0.0.1',
    author='op',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)