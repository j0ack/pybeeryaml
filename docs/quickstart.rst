Quick start
===========

|pyversion| |version| |license| |travis|

Installation
------------

.. code:: sh

    pip install pybeeryaml

Usage
-----

.. code:: python

    from pybeeryaml import Recipe

    path_to_beeryaml_file = "/tmp/my_recipe.yml"

    # create recipe from file
    recipe = Recipe.from_file(path_to_beeryaml_file)

    # or from string
    with open(path_to_beeryaml_file, "r") as mybeer:
        recipe2 = Recipe.from_yaml(mybeer.read())

    assert recipe == recipe2  # True

    # convert to beerxml format
    recipexml = recipe.to_xml()

    # create your recipe
    recipe = Recipe(
       name="Test", brewer="TROUVERIE Joachim", type="Pale Ale",
       batch_size=10.0, boil_time=60.0, boil_size=15.0, style="Test"
    )

    # convert it to yaml
    yaml_data = recipe.to_yaml()


Testing
-------

Unit tests can be run with `pytest <https://docs.pytest.org/en/latest/>`_.

.. code:: sh

    python -m pytest tests

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/pybeeryaml.svg
                 :target: https://pypi.python.org/pypi/pybeeryaml/
.. |version| image:: https://img.shields.io/pypi/v/pybeeryaml.svg
               :target: https://pypi.python.org/pypi/pybeeryaml/
.. |license| image:: https://img.shields.io/github/license/j0ack/pybeeryaml.svg
               :target: https://www.gnu.org/licenses/gpl-3.0.txt
.. |travis| image::  https://img.shields.io/travis/j0ack/pybeeryaml.svg
               :target: https://travis-ci.org/j0ack/pybeeryaml
