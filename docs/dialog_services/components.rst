
Dialog Services
================

User Property Extraction
------------------------

Property Extraction is relevant to exract user attributes for a particular user. Thay way a dialog assistant can obtain knowledgea about the userr;s favourite film, dish, place etc. and use it to generate a personalized resonse. 

Property Extraction annotator in DREAM can extract several user attributes from utterances in the form of (subject, predicate, object) triplets, where the subject is the "user", the relation is the name of the attribute and the object is the value of the attribute. For example, for the utterance "I love going for a walk with my two dogs every day." the triplets [<user, like_activity, walking>, <user, have_pet, two dogs>] will be extracted. The annotator currently supports 61 user attributes. 

Property Extraction annotator consists of the following components:

* Relation classifier - a BERT-based model that finds all the user attributes present in the current utterance, if there are any.
* Entity generator - a se2seq model which generates the subject and object for each attribute found in the previuos step.

The models were trained on DialogueNLI dataset which has 59.2 K samples in train set, 6.2 K in valid set and 6.1 K in test set. Triplets in DialogueNLI contain 61 relation types, top-10 most frequent relations are listed in the table below.

+-----------------+-------------------+
| Relation        | Number of samples |
+=================+===================+
| have_pet        |       5184        |
+-----------------+-------------------+
| like_activity   |       4620        |
+-----------------+-------------------+
| has_profession  |       2920        |
+-----------------+-------------------+
| has_hobby       |       2864        |
+-----------------+-------------------+
| have            |       2824        |
+-----------------+-------------------+
| have_children   |       2713        |
+-----------------+-------------------+
| like_general    |       2559        |
+-----------------+-------------------+
| other           |       2159        |
+-----------------+-------------------+
| like_food       |       1997        |
+-----------------+-------------------+
| misc_attribute  |       1722        |
+-----------------+-------------------+

Comparison with other solutions:

+----------------------------------+-----------------+
| Model                            | DialogueNLI, F1 |
+==================================+=================+
| DREAM property extraction        |      0.44       |
+----------------------------------+-----------------+
| `GenRe`_                         |      0.44       |
+----------------------------------+-----------------+
| `Two-stage Attribute Extractor`_ |      0.28       |
+----------------------------------+-----------------+

.. _`GenRe`: https://arxiv.org/abs/2109.12702
.. _`Two-stage Attribute Extractor`: https://arxiv.org/abs/1908.04621

Examples of Property Extraction usage:

.. code:: python

    property_extraction_url = "http://0.0.0.0:8136/respond"
    >>> requests.post(property_extraction_url, json = {"utterances": [["i live in moscow"]]}).json()
    [[{"triplets": [{"object": "moscow", "relation": "live in citystatecountry", "subject": "user"}]}]]
    >>> requests.post(property_extraction_url, json = {"utterances": [["My favorite city in Italy is Venice. And what's yours?"]]}).json()
    [[{"triplets": [{"object": "venice", "relation": "favorite place", "subject": "user"}]}]]



Entity Detection
-------------------

Entity Detection annotator extracts entity substrings from the utterance and defines tags for entity substrings. Entities are extracted from user utterances the following way: first, entity recognition component detects substrings of entities, second, entity classification defines entity types. For example, in the utterance "I went to Germany" the former component extracts the substring "Germany" and the latter determines its type ("country").

Entity recognition process is implemented as the classification of text tokens into three classes: "B-ENT" for the beginning of the entity mention, "I-ENT" for the inner part of the mention, and "O" for other tokens. For entity recognition we trained the model with a dense layer on top of pretrained DistilBERT. Entity classifier is based on DistilBERT, in which averaged hidden states for the tokens of entity substring are fed into a dense layer for classification into 42 classes corresponding to entity types.

Examples of Entity Detection usage:

.. code:: python

    >>> requests.post(entity_detection_url, json = {"sentences": [["what is the capital of russia?"]]}).json()
    
Output:

.. code:: json

    {
        "entities": ["capital", "russia"],
        "labelled_entities": [
            {"text": "capital", "offsets": [12, 19], "label": "misc", "finegrained_label": [["misc", 1.0]]},
            {
                "text": "russia",
                "offsets": [23, 29],
                "label": "location",
                "finegrained_label": [["country", 0.953]]
            }
        ]
    }

Elements of the output data:

* "entities" - entity substrings in the utterance;
* "labelled_entities" - entity substrings with extra annotations:

  * "offsets" - indices of start and end symbols of entity substring in the utterance;
  * "label" - entity tag;
  * "finegrained_label" - more specific entity tag.


Custom Entity Linking
-------------------

Custom Entity Linking allows developers to index their own knowledge graphs and then link entities to their own knowledge graphs. the outputs of the annotator can be used to find the linked entities in user's custom KG.

.. code:: python

    url_custom_el = 'http://0.0.0.0:8075/model'
    data ={"entity_substr": [["pizza"]], "entity_tags": [["misc"]], "context": [["Maybe I will order pizza for lunch."]]}
    requests.post(url_custom_el, json=data).json()
    >>> [{"entity_substr": "pizza", "entity_ids": ["AbstractFood/68e82b41-b8bb-40d3-b4a0-73f8ff6bced5"], "confidences": [1.0]}]
    
