# -*- coding: utf-8 -*-
from django.conf import settings

COPYRIGHT = 'RIG'
COPYLEFT = 'LEF'
CREATIVE_COMMONS = 'CC'

DEFAULT_LICENSES = (
    (COPYRIGHT, "Copyright"),
    (COPYRIGHT, "Copyleft"),
    (COPYRIGHT, "Cretive Commons"),
)

# getattr busca sobre el objeto settings una variable que se llame LICENSES
# Si no la encuentra devuelve el valor DEFAULT_LICENSES
# Si en el settings general del proyecto no me definen una variable LICENSES
# Cogemos la licencia por defecto

LICENSES = getattr(settings, 'LICENSES', DEFAULT_LICENSES)

BADWORDS = getattr(settings, 'BADWORDS', [])

