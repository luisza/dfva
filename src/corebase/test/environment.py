# encoding: utf-8

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
@date: 12/9/2017
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

INSTITUTION = "e55ffc21-f2b7-462b-960b-35fd45d11151"
LISTEN_URL = "http://localhost:8000/receptor_notificacion"
ALGORITHM = 'sha512'
SERVER_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyP3oYZAJ6lKz4mQh63Yg
xNabO1pDG9ylYH5hHXYQDTLdg1mgWgG5KaNGfd6yHZixMy7peTrtbqrnAEvC0oGs
Te7f/pjMDBZkX9UQpdx5tumsp2Q0HxsdVtmtFo/MijbQNeTJa/wvzCYmmiuY5S2y
lebIa+2rVUYDpTqKsnPTqfrNDg2W1ycgC83PptqiN5jSeTlY+NLvJhx3CEw7QwAN
wOlVc/OqL5Ghp98kqD/7pr64JOOBB1MIZLg77mupkSYTw6+UZfQuRWx+AqHe4l0k
7Q7r3p7bTJFJMPyEug2f2Xa26Kuw4YHlx1CemJqcbR79s8sw7Cvxmt/MyPCpQiJr
kQIDAQAB
-----END PUBLIC KEY-----"""
PUBLIC_CERTIFICATE = """-----BEGIN CERTIFICATE-----
MIIE1TCCAr2gAwIBAgIIXt8XPXxVIrwwDQYJKoZIhvcNAQELBQAwazELMAkGA1UE
BhMCQ1IxETAPBgNVBAgMCFNhbiBKb3NlMRMwEQYDVQQHDApDb3N0YSBSaWNhMRsw
GQYDVQQKDBJERlZBIEluZGVwZW5kaWVudGUxFzAVBgNVBAMMDkRGVkEgUm9vdCBD
QSAxMB4XDTIwMDYwOTA0NTk0MVoXDTIxMDYwOTA0NTk0MVowbDELMAkGA1UEBhMC
Q1IxETAPBgNVBAgMCFNhbiBKb3NlMRMwEQYDVQQHDApDb3N0YSBSaWNhMQ0wCwYD
VQQKDARUZXN0MQ4wDAYDVQQLDAVTb2x2bzEWMBQGA1UEAwwNbWlmaXJtYWNyLm9y
ZzCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMdL2UlOZLfFdvwM5mM5
+0clsbWHFo4Se+3xxWx6VUdELZY1Dn/6hvaaq66A20NLFB558WUr+POL/JcryasW
wzVhA0izqRxSXp4MeBzVFISf+fmmHvI3LxhzRk8WIDGdtaZaio1x5rh8IAVuDiPL
Vt4SQgHS4f6QLh2esm9ryPmC1HRMfTrjgslVf3w19PriPfspNKC4mp5u6B7dNSqQ
T3+LXSs4qM0y0CJlSuy1GM69xvgPp1nzySCPP18qCi6Gvo0+fIznV+rGHg43k4zI
4tKgvFVmxXCZpyPXfeHhnjc9BUhULqvrurfq0QbthKcyFCdb8BR7LnF+JdDJVAtC
R4UCAwEAAaN8MHowHwYDVR0jBBgwFoAU6qZjf3q/9wx0QWYFCxlgw2sC4rwwCQYD
VR0TBAIwADAdBgNVHSUEFjAUBggrBgEFBQcDAQYIKwYBBQUHAwIwHQYDVR0OBBYE
FPfjKUJtMO1wy0pUMiUOW6vM3Z5CMA4GA1UdDwEB/wQEAwIHgDANBgkqhkiG9w0B
AQsFAAOCAgEAH8cj4JEirKBKgn15YfkmhbnWcMTDOB9ANVGNrHrrMUvp1pCnecRn
JVV7bttZS/kaKuovU6z0L+aJWwqZdsLqBd3fIxa9JR/ZcV1EGMufY5OyI3G3MqDe
GPzFYAnfr4R+dFvIhAgqYjCfBFdbx6TIndEJqHaDSoYqdesoKqTph7Fey1oP22ll
zNWdOZFVge5c/IycuQGYB3jMfw8vEsbaQzPG1S6+kiuRXW9l3liKLYv23Ej5RW0i
Xq1RiHdmqBdoaOGAGea+QZN/AscmcnF7SFntrAx085xz+ulrmP2XyCDIWIq8l7gF
MvW0R+Sbf1k/CaQwkI22mE8dddGnqAVTnLjbvAy0JOuVB2XdFys7OZEIDDeOKcCv
Su09cCayxpEiZcQSNKV3yHibzNe49zj2VYQCd4q7c+vYBuudhMW2HZcZA+brGyn4
/3Y0nN8MfVQ3eDR/6Fz5wEl7wl1n2EdlIUn9ovI/yYdet0oYcTGy9Ibn7/nxAZwX
cAOd89g7KtQji48UBXIG4V9MRKY33+pTr+qjtV/aYGfu2fI+QgxNP7PNU5AbvdbW
ZJDYfEh97unKzYEqAZCcYdgyI/8NpUN6oXg8OyFjuIROgu+3ziXYzz4rrzzNQqtp
m6d5Y5bPt5aTWjSVvqbC0MxwrcUBbnao2goMlPLrsJf8lH3gXysffAU=
-----END CERTIFICATE-----"""
SERVER_URL = 'http://localhost:8000'
