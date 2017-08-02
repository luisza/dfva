'''
Created on 2 ago. 2017

@author: luis
'''

from clients.person import PersonClient

client = PersonClient('04-0212-0119')

client.sign('08-0888-0888',  None, "Readme file test",
            file_path='README.md', wait=True)
