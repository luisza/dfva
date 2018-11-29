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

DOCXFILE = """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 eG1sUEsFBgAAAAAJAAkAPAIAAJYNAAAAAA=="""
HASHDOCX = """42708fe4cca43b8159a86aab648b3456f499a3f757afd0eaadac9a204b9d2d7b138c252bf2432358847a618fd0100adc6454c8c81adcbe28151841777e707b92"""
ODFFILE = """UEsDBBQAAAgAAOYD9EpexjIMJwAAACcAAAAIAAAAbWltZXR5cGVhcHBsaWNhdGlvbi92bmQub2Fz aXMub3BlbmRvY3VtZW50LnRleHRQSwMEFAAACAAA5gP0SkRmcU2lAQAApQEAABgAAABUaHVtYm5h aWxzL3RodW1ibmFpbC5wbmeJUE5HDQoaCgAAAA1JSERSAAAAtQAAAQAIAwAAAML9x+kAAABdUExU RYCBh5WRiZSTlJOamp+bl5ucnbGknqSlpKikoKuusqaxure0r7y7vK64wLy/xLjL3MXBvdXTzdvn 8eXWx+fazevYx+Li4urm4+Hr8+zz+fX19fT4/P7+/gAAAP///zZhNrUAAAEDSURBVHja7dIxEoIw FEDBCEpGDRqVQfzk/ue0t7fIzL4TbPFS67FETU1NTU1NTU1NTU390+tybhHRoq1tj/feh3q5T+Nh OKXrMx/zMG2dqOdbfZSSy6eWtc6br6mpqampqampqampqampqampqampqampqampqampqampqamp qampqampqampqampqampqampqampqampqampqampqampqampqampqampqampqampqampqampqamp qampqampqampqampqampqampqampqampqampqampqampqampqampqampqampqampqampqampqamp qampqampqampqampqampqf/XFxFXytdl9JizAAAAAElFTkSuQmCCUEsDBBQACAgIAOYD9EoAAAAA AAAAAAAAAAALAAAAY29udGVudC54bWylV8Fu4zYQvfcrBC3QG0M7boG1GnsvwQIFEqBoskWvDEXZ 3IqkSlKW/fcdkhZNOZajri9OzHlv+DgznKEfvuxFne2YNlzJVT6/m+UZk1SVXG5W+bfXr+hz/mX9 04OqKk5ZUSraCiYtokpa+JsBW5oiWFd5q2WhiOGmkEQwU1haqIbJnlWk6MLvFVaMPdST6R6csi3b 26lkhx1wydv0nT04ZZeadFPJDgtBTemVmkremxpVCqIuGmL5mYp9zeU/q3xrbVNg3HXdXbe4U3qD 58vlEntrFEwjrml17VElxaxmbjOD53dz3GMFs2SqPodNJclWvDE9OTTEkndZNbvN5IrYbUZCQ7dE T64NDx6md1FOT++iTLmC2O1ITj7jZzD6j+enUy1oMXUvhx2EimreTD5mQKd8pVSU6gjhgnq597PZ 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"""
HASHODF = """55489564a7f3fb5bfd56606fe7186b6144ee8301be2b011dfea5f64085d7c53910a1baa74ea905db260dcae4be81edc612577928370dd15f2c3bfa8ac518be9c"""
XMLFILE = """PG1vdmllPgogIDx0aXRsZT5QSFA6IEJlaGluZCB0aGUgUGFyc2VyPC90aXRsZT4KICA8Y2hhcmFj dGVycz4KICAgPGNoYXJhY3Rlcj4KICAgIDxuYW1lPk1zLiBDb2RlcjwvbmFtZT4KICAgIDxhY3Rv cj5PbmxpdmlhIEFjdG9yYTwvYWN0b3I+CiAgIDwvY2hhcmFjdGVyPgogICA8Y2hhcmFjdGVyPgog ICAgPG5hbWU+TXIuIENvZGVyPC9uYW1lPgogICAgPGFjdG9yPk5hZGllL2FjdG9yPgogICA8L2No YXJhY3Rlcj4KICA8L2NoYXJhY3RlcnM+CjwvbW92aWU+Cg=="""
HASHXML = """637a7d07c5dbee59695aafbd3933b359d64613926d6cfc168e2e70dd0690e73379eee500e2fca4b5cde644c028b22b89accffa5c65313de1f956f0a6aec81d7a"""
