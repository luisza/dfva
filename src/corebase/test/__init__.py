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
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

CERTIFICATE_FILE = """MIIGDTCCBPWgAwIBAgIKJ6PIrAABAARHZzANBgkqhkiG9w0BAQUFADCBmjEVMBMG
A1UEBRMMNC0wMDAtMDA0MDE3MQswCQYDVQQGEwJDUjEkMCIGA1UEChMbQkFOQ08g
Q0VOVFJBTCBERSBDT1NUQSBSSUNBMSowKAYDVQQLEyFESVZJU0lPTiBERSBTRVJW
SUNJT1MgRklOQU5DSUVST1MxIjAgBgNVBAMTGUNBIFNJTlBFIC0gUEVSU09OQSBG
SVNJQ0EwHhcNMTUxMjE1MTU1NDM2WhcNMTcxMjE0MTU1NDM2WjCBuzEZMBcGA1UE
BRMQQ1BGLTA0LTAyMTItMDExOTEXMBUGA1UEBBMOWkFSQVRFIE1PTlRFUk8xFTAT
BgNVBCoTDExVSVMgRU5SSVFVRTELMAkGA1UEBhMCQ1IxFzAVBgNVBAoTDlBFUlNP
TkEgRklTSUNBMRIwEAYDVQQLEwlDSVVEQURBTk8xNDAyBgNVBAMTK0xVSVMgRU5S
SVFVRSBaQVJBVEUgTU9OVEVSTyAoQVVURU5USUNBQ0lPTikwggEiMA0GCSqGSIb3
DQEBAQUAA4IBDwAwggEKAoIBAQDOskqHMQpN6r/kPjD3M5hrhwbJGz5Y4czy28BB
zALu7l/4EnJ38RRxMbQhJ3Zm7l1RvANRp8mh3YnbNtK1nCNCn8DV6Kw0gJbixDqI
0WQb6Di6+6IckCtVvoPUNS7zwpyKqF+1HUCMirkSbfVg98oIaspSM6KbFGLSwkdg
vvgOkWbb2VqQgc/o9einI2awnJW04ud1CE+U4kdBNDtB2jEEgskOH2z2mOrh4Vtx
gPT8YLB4LOHQyBe4KmqSoEs/WBl884M8nwJ4MDp9fe7Kw+fVItSl+fayHiJ/B/Et
WKiFLG+4e2RGqNZO0GQ4sdELIQ7QJGZWtI/qj7dSiXhAKix3AgMBAAGjggIwMIIC
LDAdBgNVHQ4EFgQU0ZsmETAjdu42zT75ZQRNWNa3uH0wHwYDVR0jBBgwFoAUSNSK
lKGgMog/qrE2EJQr7pRBgqwwXAYDVR0fBFUwUzBRoE+gTYZLaHR0cDovL2ZkaS5z
aW5wZS5maS5jci9yZXBvc2l0b3Jpby9DQSUyMFNJTlBFJTIwLSUyMFBFUlNPTkEl
MjBGSVNJQ0EoMSkuY3JsMIGTBggrBgEFBQcBAQSBhjCBgzAoBggrBgEFBQcwAYYc
aHR0cDovL29jc3Auc2lucGUuZmkuY3Ivb2NzcDBXBggrBgEFBQcwAoZLaHR0cDov
L2ZkaS5zaW5wZS5maS5jci9yZXBvc2l0b3Jpby9DQSUyMFNJTlBFJTIwLSUyMFBF
UlNPTkElMjBGSVNJQ0EoMSkuY3J0MA4GA1UdDwEB/wQEAwIFoDA9BgkrBgEEAYI3
FQcEMDAuBiYrBgEEAYI3FQiFxOpbgtHjNZWRG4L5lxiGpctrgX+FlPQbguWKCQIB
ZAIBAzAfBgNVHSUEGDAWBgorBgEEAYI3FAICBggrBgEFBQcDAjAVBgNVHSAEDjAM
MAoGCGCBPAEBAQEDMCkGCSsGAQQBgjcVCgQcMBowDAYKKwYBBAGCNxQCAjAKBggr
BgEFBQcDAjBEBgkqhkiG9w0BCQ8ENzA1MA4GCCqGSIb3DQMCAgIAgDAOBggqhkiG
9w0DBAICAIAwBwYFKw4DAgcwCgYIKoZIhvcNAwcwDQYJKoZIhvcNAQEFBQADggEB
ADWxSOBUS7d4NBiN9AAmDw3lQZAr3gg708fq/ABTqnwyj8Dw/m61T/aJmvwHtRBA
yZ67qUVLAFGA/DcVNwwbjLHITCdw3X0ByoZ1cti7pNaaS16jOcvvRzLvqrLK6BwR
9J+AVDWhLWya7H3rqovg9HN9qrzmsDFPFN101JzLsGdSWF83ZsJDmMWBknizpLpS
ON8R+DcLMrqay8qgP3zs/zwogvy9+2q/6/df0FJv/zumkI2h2+fSoVMZTQD4Voz9
MGcc7Na6PRxJjvd+skA+xN7dPSS5kciolQ9RC55kDa20I5Sc1n7sI8vCcA2siQj4
g6BvZ6Zo+XE4gH7ItBg9/ck="""

WRONG_CERTIFICATE = """-----BEGIN CERTIFICATE-----
MIIGnDCCBYSgAwIBAgISA3W2aPJ9yiDsHpDCZP2F9Q4FMA0GCSqGSIb3DQEBCwUA
MEoxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MSMwIQYDVQQD
ExpMZXQncyBFbmNyeXB0IEF1dGhvcml0eSBYMzAeFw0xNzA4MDUwMzAzMDBaFw0x
NzExMDMwMzAzMDBaMBwxGjAYBgNVBAMTEWRqYW5nb3Byb2plY3QuY29tMIICIjAN
BgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAvPeof1WrXo/O0f2jpdqSgY+kNZCX
Hkvs1Q36u1e7bUFZWJm3wETL4iqbQV36OEQTgBrZqxwxojaN+lOMT3FZs2ABBHlT
yBms78+Q5bS1a2mkCCF7pSi6E3gV6+TQ2paWywq63NrBDJQGTBLptDqAIHf2gPgG
7x/dIo2rVb8uSree0uFzbUh17GoePE24WWzrVXHIAPa9OB9WuQKlbZtessKeqAqs
D+spvKxjVLuaFZDf9fDZTXs/styL494ilry/HPNfUUUOlFwAvFl7EH+YEoDgQ0L1
EStg45rpKrrtnEeRbbWmfkEvI1OkHfDSHX9qu3flW/Ek5OU6KP7YQRgHRZ82LqG9
gFssaOm1rEfOSVuAFgJCmO8Ae++kJMvu8WlVDlvyY14K/eqsDLq6nafF3NjJctgr
iy8/eE1ta7VffNlowtBD0veiKLS0dGrCFQP+YA0ZPnZ0BY0D7ylr9BAAghJUtKn4
RhdaozNTFA7+6NbhK/dI1qjRRIFRkGCyb6SeUHalsP9GUR6ApsK1qcO38dvS5bv0
azz2QctQI8IYHxqFxg6MUScpeJzLSooI2LCLx+NByZ+wqx9zG288OrLZInA9r7qp
68ZfGALgLu6NsYKh8nrw85wzsSoCK7jBS3oCXHivXoUyHLLlHjyOLXLPHrvHA9Qd
aVgbckQoLLQqpHECAwEAAaOCAqgwggKkMA4GA1UdDwEB/wQEAwIFoDAdBgNVHSUE
FjAUBggrBgEFBQcDAQYIKwYBBQUHAwIwDAYDVR0TAQH/BAIwADAdBgNVHQ4EFgQU
aa95guQ9CAYvpquNuxmTPdVhtzkwHwYDVR0jBBgwFoAUqEpqYwR93brm0Tm3pkVl
7/Oo7KEwbwYIKwYBBQUHAQEEYzBhMC4GCCsGAQUFBzABhiJodHRwOi8vb2NzcC5p
bnQteDMubGV0c2VuY3J5cHQub3JnMC8GCCsGAQUFBzAChiNodHRwOi8vY2VydC5p
bnQteDMubGV0c2VuY3J5cHQub3JnLzCBsgYDVR0RBIGqMIGnghRjaS5kamFuZ29w
cm9qZWN0LmNvbYIWY29kZS5kamFuZ29wcm9qZWN0LmNvbYIbZGFzaGJvYXJkLmRq
YW5nb3Byb2plY3QuY29tghFkamFuZ29wcm9qZWN0LmNvbYIWZG9jcy5kamFuZ29w
cm9qZWN0LmNvbYIYcGVvcGxlLmRqYW5nb3Byb2plY3QuY29tghV3d3cuZGphbmdv
cHJvamVjdC5jb20wgf4GA1UdIASB9jCB8zAIBgZngQwBAgEwgeYGCysGAQQBgt8T
AQEBMIHWMCYGCCsGAQUFBwIBFhpodHRwOi8vY3BzLmxldHNlbmNyeXB0Lm9yZzCB
qwYIKwYBBQUHAgIwgZ4MgZtUaGlzIENlcnRpZmljYXRlIG1heSBvbmx5IGJlIHJl
bGllZCB1cG9uIGJ5IFJlbHlpbmcgUGFydGllcyBhbmQgb25seSBpbiBhY2NvcmRh
bmNlIHdpdGggdGhlIENlcnRpZmljYXRlIFBvbGljeSBmb3VuZCBhdCBodHRwczov
L2xldHNlbmNyeXB0Lm9yZy9yZXBvc2l0b3J5LzANBgkqhkiG9w0BAQsFAAOCAQEA
lWPiAgeMeABYVKG8wxODmMUTnNOpKQAugwwpf7VMNL50kZ06jD5J6CyGuTxRGz65
x9keOinp6zY07KJz8/Xki3OBE5JiitWfZCGFNsWz/bFpwIeN7mB21KRwRjmOs3Af
O0D08zjz0FH/iZB1mI9l2OzWj/GbkhfR1tTVfbcgYe0wn253z+kVpep1nRT+LG5y
bUcQxqtyyYrkWHE/WD4s6dsDzAR68szJ445VUtYfzl9Bb666e+QK9meZpOsl1dx/
xNnR1a99A7OChv5DBFOljXQoFxD/hZ5Rcxy7HA5guil2Wg9hgdkjX7X75GPsr1sx
q9PDiOcmjUXKu9I0ot5VOg==
-----END CERTIFICATE-----"""