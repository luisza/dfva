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
@date: 27/10/2017
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''


def fix_certificate(certificate):
    """
    Arregla el formato PEM, pues en algunos casos se obtienen los datos den base64 sin los encabezados por lo
    que este método se encarga de agregarlos si estos no están.
    :param certificate: String que contiene un certificado
    :return: certificados en formato PEM
    """
    certificate = certificate.replace("-----BEGIN CERTIFICATE-----", '')
    certificate = certificate.replace("-----END CERTIFICATE-----", '')
    certificate = certificate.replace(" ", '\n')
    return "%s%s%s" % (
        "-----BEGIN CERTIFICATE-----",
        certificate,
        "-----END CERTIFICATE-----"
    )


class CAManagerInterface:
    """
    Todo gestor de certificados que se conecte a UCRFVA que sirva para la emisión y validación de certificados debe
    heredar de esta interfaz e implementar los métodos de esta.
    """
    def generate_certificate(self, domain, save_model):
        """
        Genera un certificado  para la institución (aplicación), se genera 2 llaves públicas y 2 llaves privadas
        todo se almacena en la base de datos excepto la llave privada de la aplicación

        :param domain:  Nombre de dominio de la aplicación a registrar
        :param save_model:  `institution.models.Institution` Modelo donde guardar la información.
        :return:  `institution.models.Institution`
        """
        pass

    def check_certificate(self, certificate):
        """
        Dado un certificado en formato PEM se verifica si el certificado es válido y vigente

        :param certificate: Certificado en formato PEM
        :return: True si el certificado es válido, False si no lo es
        """
        pass

    def revoke_certificate(self, certificate):
        """
        Agrega el certificado a la lista de revocación, lo que representa revocar el certificado

        .. warning:: Revocar el certificado invalida el certificado por lo que no podrá seguir usandose,
                debe solicitar la creación de un nuevo certificado para si institución si desea continuar usando los servicios

        :param certificate:  Certificado en formato PEM
        :return: None
        """
        pass
