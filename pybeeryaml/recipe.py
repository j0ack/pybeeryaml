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


from yaml import safe_load
from pybeeryaml import BeerComponent

RECIPE_FIELDS = ["name", "brewer", "batch_size", "boil_time"]
HOP_FIELDS = ["name", "alpha", "amount", "use", "time"]
YEAST_FIELDS = ["name", "type", "form", "amount"]
FERMENTABLE_FIELDS = ["name", "type", "amount", "color"]
MISC_FIELDS = ["name", "type", "use", "time", "amount"]
MASH_FIELDS = ["name"]
MASH_STEP_FIELDS = ["name", "type", "step_time", "step_temp"]


class Recipe(BeerComponent):
    """Recipe model

    :param data: dict recipe data
    """

    def __init__(self, data: dict):
        super().__init__("recipe", data, RECIPE_FIELDS)

        hops = self.flatten(data.get("hops", {}))
        self.hops = [BeerComponent("hop", hdata, HOP_FIELDS) for hdata in hops]

        yeasts = self.flatten(data.get("yeasts", {}))
        self.yeasts = [
            BeerComponent("yeast", ydata, YEAST_FIELDS) for ydata in yeasts
        ]

        ferments = self.flatten(data.get("fermentables", {}))
        self.fermentables = [
            BeerComponent("fermentable", fdata, FERMENTABLE_FIELDS)
            for fdata in ferments
        ]

        miscs = self.flatten(data.get("miscs", {}))
        self.miscs = [
            BeerComponent("misc", mdata, MISC_FIELDS)
            for mdata in miscs
        ]

        self.mash = BeerComponent("mash", data.get("mash", {}), MASH_FIELDS)
        steps = []
        if hasattr(self.mash, "mash_steps"):
            msdata = self.flatten(self.mash.mash_steps)
            for mash_step in msdata:
                steps.append(
                    BeerComponent("mash_step", mash_step, MASH_STEP_FIELDS)
                )

        self.mash.mash_steps = steps

    def flatten(self, data: dict) -> list:
        """Flatten yaml dict

        :param data: YAML dict
        """
        output = []
        for key, value in data.items():
            if isinstance(value, dict):
                value["name"] = key
            output.append(value)
        return output

    @classmethod
    def from_file(cls, filepath: str) -> Recipe:
        """Create recipe from YAML file

        :param filepath: YAML file containing recipe data
        """
        with open(filepath, "r") as fi:
            data = safe_load(fi.read())
        return cls(data)

    @classmethod
    def from_yaml(cls, data: str) -> Recipe:
        """Create recipe from YAML data

        :param data: YAML recipe data
        """
        return cls(data)
