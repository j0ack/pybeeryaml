Why using YAML to store beer recipes ?
======================================

|pyversion| |version| |license| |travis|

**Why are you using another format since beerxml is widely used ?**

The reason is very simple, `XML <https://en.wikipedia.org/wiki/XML>`_ is very
verbose. Furthermore `beerxml <http://beerxml.com>`_ format is a very complete
data description containing lots of mandatory keys which can be irrelevant for
your recipe. This two formats have their own purpose and are well formatted
markup languages. The goal of this project is not to replace beerxml but to
make it simpler to use in plain text files.

The main purpose of storing recipes in the `YAML <https://en.wikipedia.org/wiki/YAML>`_
format is to make recipes more *human-readable*. It should be really simple to
write your own recipes in a simple format and read it without needing to use an
external software.

What are the differences with the beerxml format ?
--------------------------------------------------

- BeerYAML format shares the mandatory fields for beer items with the beerxml
  format.
- Items' version are all set to `1` by default.
- Recipe's style can either be a dict containing all the mandatory keys like in
  beerxml format or a simple string.
- Recipe *record sets* are optionnals and will be set empty when exporting to
  xml. A minimal recipe can be represented by this yaml

  .. code:: yaml

     name: Test
     brewer: TROUVERIE Joachim
     type: Pale Ale
     batch_size: 10.0
     boil_time: 60.0
     boil_size: 15.0
     style: Test

- It is possible to define a *record set* name by its YAML key. Thus

  .. code:: yaml

     mash_steps:
       proteic:
         step_time: 60
         step_temp: 100
         type: Infusion

  is equal to

  .. code:: yaml

    mash_steps:
       mash_step:
         name: proteic
         step_time: 60
         step_temp: 100
         type: Infusion


.. |pyversion| image:: https://img.shields.io/pypi/pyversions/pybeeryaml.svg
                 :target: https://pypi.python.org/pypi/pybeeryaml/
.. |version| image:: https://img.shields.io/pypi/v/pybeeryaml.svg
               :target: https://pypi.python.org/pypi/pybeeryaml/
.. |license| image:: https://img.shields.io/github/license/j0ack/pybeeryaml.svg
               :target: https://www.gnu.org/licenses/gpl-3.0.txt
.. |travis| image::  https://img.shields.io/travis/j0ack/pybeeryaml.svg
               :target: https://travis-ci.org/j0ack/pybeeryaml
