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


import os.path
import xml.etree.ElementTree as ET
from yaml import safe_load
from copy import copy
from pybeeryaml import Recipe


def xmltodict(data: ET.Element, root=True) -> dict:
    """Convert xml into dict"""
    output = {data.tag: {}} if root else {}
    for child in data:
        if list(child):
            tagname = child.tag
            if tagname in output:
                tagname = "{}{}".format(
                    child.tag, len([
                        k for k in output.keys()
                        if k.startswith(child.tag)
                    ]))
            output[tagname] = xmltodict(child, False)
        else:
            output[child.tag] = child.text
    return output


def test_recipe_from_file():
    recipe_path = os.path.join(os.path.dirname(__file__), "beer.yml")
    recipe = Recipe.from_file(recipe_path)

    assert recipe.name == "Dry Stout"
    assert recipe.type == "All Grain"
    assert recipe.brewer == "Brad Smith"
    assert recipe.batch_size == 18.93
    assert recipe.boil_size == 20.82
    assert recipe.boil_time == 60.0
    assert recipe.date == "3 jan 04"
    assert recipe.style == "Dry Stout"

    assert len(recipe.hops) == 1
    hop = recipe.hops[0]
    assert hop.name == "Goldings, East Kent"
    assert hop.alpha == 5.0
    assert hop.amount == 0.0638
    assert hop.use == "boil"
    assert hop.time == 60.0
    assert hop.notes == "Great all purpose uk hop for ales, stouts, porters"

    assert len(recipe.fermentables) == 2
    pale_malt = recipe.fermentables[0]
    assert pale_malt.name == "Pale Malt (2 row) UK"
    assert pale_malt.amount == 2.27
    assert pale_malt.type == "Grain"
    assert pale_malt.beeryaml_yield == 78.0
    assert pale_malt.color == 3.0
    assert pale_malt.notes == "All purpose base malt for English styles"

    barley = recipe.fermentables[1]
    assert barley.name == "Barley, Flaked"
    assert barley.amount == 0.91
    assert barley.type == "Grain"
    assert barley.beeryaml_yield == 70.0
    assert barley.color == 2.0
    assert barley.notes == "Adds body to porters and stouts, must be mashed"

    assert len(recipe.yeasts) == 1
    irish_ale = recipe.yeasts[0]
    assert irish_ale.name == "Irish Ale"
    assert irish_ale.type == "Ale"
    assert irish_ale.form == "Liquid"
    assert irish_ale.amount == 0.250

    assert recipe.mash.name == "single step infusion, 68 c"
    assert len(recipe.mash.mash_steps) == 1
    conversion = recipe.mash.mash_steps[0]
    assert conversion.name == "Conversion Step, 68C"
    assert conversion.type == "Infusion"
    assert conversion.step_temp == 68.0
    assert conversion.step_time == 60.0


def test_recipe_from_yaml():
    minimal_yaml = """
    name: Test
    brewer: TROUVERIE Joachim
    batch_size: 10.0
    boil_time: 60.0
    hops:
      test:
        alpha: 3.50
        amount: 5.0
        use: boil
        time: 20.0
    fermentables:
      test2:
        yield: 78.0
        type: Grain
        amount: 10.0
        color: 5.0
    """
    recipe = Recipe.from_yaml(minimal_yaml)
    assert recipe.name == "Test"
    assert recipe.brewer == "TROUVERIE Joachim"
    assert recipe.batch_size == 10.0
    assert recipe.boil_time == 60.0

    assert len(recipe.hops) == 1
    hop = recipe.hops[0]
    assert hop.name == "test"
    assert hop.alpha == 3.50
    assert hop.amount == 5.0
    assert hop.use == "boil"
    assert hop.time == 20.0

    assert len(recipe.fermentables) == 1
    fermentable = recipe.fermentables[0]
    assert fermentable.name == "test2"
    assert fermentable.type == "Grain"
    assert fermentable.amount == 10.0
    assert fermentable.color == 5.0


def test_xml_export():
    recipe_path = os.path.join(os.path.dirname(__file__), "beer.yml")
    xml_path = os.path.join(os.path.dirname(__file__), "beer.xml")
    recipe = Recipe.from_file(recipe_path)

    xml = ET.fromstring(recipe.to_xml())
    xml2 = ET.parse(xml_path).getroot()

    assert xmltodict(xml) == xmltodict(xml2)


def test_yaml_export():
    # remove version keys
    def remove_keys(data):
        output = copy(data)
        for key, value in data.items():
            if key == "version":
                del output[key]
            if isinstance(value, dict):
                output[key] = remove_keys(value)
        return output

    recipe_path = os.path.join(os.path.dirname(__file__), "beer.yml")
    recipe = Recipe.from_file(recipe_path)

    with open(recipe_path, "r") as fi:
        data = safe_load(fi.read())

    assert data == remove_keys(recipe.to_yaml())
