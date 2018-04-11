#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Pybeeryaml
# Copyright (C) 2018  TROUVERIE Joachim <joachim.trouverie@linoame.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


try:
    from lxml import etree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class BeerComponent:
    """Base class for beer component

    :param objname: object name
    :param data: object data
    :param mandatory_fields: mandatory_fields
    """

    def __init__(self, objname: str, data: dict, mandatory_fields: list):
        self.version = 1
        self._objname = objname
        self._mandatory_fields = mandatory_fields

        for field in self._mandatory_fields:
            setattr(self, field, data.pop(field))

        for key, value in data.items():
            if not isinstance(value, list):
                setattr(self, key, value)

    def to_xml(self) -> str:
        """Convert to beerxml format"""
        root = ET.Element(self._objname.upper())
        for key, value in self.__dict__.items():

            if key.startswith("_"):
                continue

            subelt = ET.SubElement(root, key.upper())

            if isinstance(value, list):
                for elt in value:
                    subelt.append(ET.fromstring(elt.to_xml()))

            elif isinstance(value, BeerComponent):
                subelt.append(ET.fromstring(value.to_xml()))

            else:
                subelt.text = str(value)
        return ET.tostring(root)
