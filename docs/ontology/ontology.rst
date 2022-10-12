
Ontology
===========

Kinds
------
Entity Kinds are defined by fine-grained types from the  `WNED-WIKI <https://arxiv.org/pdf/2009.02252v4.pdf>`_ dataset.

*Misc, loc, country, city, org, business, occupation, fac, product, sports_event, actor, politician, film, work_of_art, athlete, writer, musician, norp, per, county, event, sport_team, us_state, type_of_sport, song, nation, language, sports_season, software, association_football_club, science_and_technology, vehicle, literary_work, music_genre, political_party, academic_discipline, sports_league, river, road, food, national, law, championship, sports_venue, animal, painter, chemical_element, entrepreneur.*


Relationships
--------------
+------------------------+--------------------+------------+-------------+
| Relationship Type      | Model relationship | Head Kinds | Tail Kinds  |
+========================+====================+============+=============+
| Relatives              | have_chidren,      | Person     | Person      |
|                        | have_family,       |            |             |
|                        | have_sibling,      |            |             |
|                        | have               |            |             |
+------------------------+--------------------+------------+-------------+
| Celebrities            | ...                | ...        | ...         |
+------------------------+--------------------+------------+-------------+

Properties
-----------
+------------------------+--------------------+-----------------+
| Property Type          | Model property     | Head Kinds      |
+========================+====================+=================+
| Name                   | --- [#f1]_         | Person, Animal, |
|                        |                    | Organization    |
+------------------------+--------------------+-----------------+
| Age                    | has_age            | Person, Animal  |
+------------------------+--------------------+-----------------+
| Marital Status         | ...                | ...             |
+------------------------+--------------------+-----------------+


.. rubric:: Note

.. [#f1] Name property is extracted with rules, not with the Triplet extraction model.
.. https://arxiv.org/pdf/2009.02252v4.pdf
