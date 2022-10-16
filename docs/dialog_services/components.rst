
Dialog Services
================

User Property Extraction
-------------------

For generation utterances in scripted skills, relevant for a particular user, the dialogue assistant should know different user attributes, for example, favourite film, dish, pet etc. Property Extraction annotator in DREAM extracts user attributes from utterances.

Property Extraction annotator takes as input an utterance and outputs triplets in the format <subject, relation, object>, where the subject is, as usual, the user, the relation is the name of the attribute, the object is the value of the attribute. For example, for the utterance "I like skiing in winter" the triplet <user, like_activity, skiing> will be extracted.

Property Extraction annotator consists of the following components:
* T5-base <https://huggingface.co/t5-base>`__, which generates a sequence of triplet tokens, where subject, relation and object are separated with special tokens: <subj> subject <rel> relation <obj> object.
* (optional) DistilBERT model for relation classification. In the final output the triplets where the relation does not match with classified relation, are filtered out.

The models are trained on DialogueNLI dataset <https://wellecks.com/dialogue_nli/>`__ which has 59.2 K samples in train set, 6.2 K in valid set and 6.1 K in test set. Triplets in DialogueNLI contain 61 relation types, top-10 most frequent relations are listed in the table below.

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

Examples of property extraction usage:

.. code:: python

    >>> requests.post(property_extraction_url, json = {"utterances": ["i live in moscow"]}).json()
    [{"triplet": {"object": "moscow", "relation": "live in citystatecountry", "subject": "user"}}]
    >>> requests.post(property_extraction_url, json = {"utterances": ["i listen to scorpions"]}).json()
    [{"triplet": {"object": "scorpions", "relation": "like music", "subject": "user"}}]

Entity Detection
-------------------

Entity Detection annotator extracts entity substrings from the utterance and defines tags for entity substrings. Entities are extracted from user utterances the following way: first, entity recognition component detects substrings of entities, second, entity classification defines entity types. For example, in the utterance "I went to Germany" the former component extracts the substring "Germany" and the latter determines its type ("country").

Entity recognition process is implemented as the classification of text tokens into three classes: "B-ENT" for the beginning of the entity mention, "I-ENT" for the inner part of the mention, and "O" for other tokens. For entity recognition we trained the model with a dense layer on top of pretrained DistilBERT. Entity classifier is based on DistilBERT, in which averaged hidden states for the tokens of entity substring are fed into a dense layer for classification into 42 classes corresponding to entity types.

Examples of entity detection usage:

.. code:: python

    >>> requests.post(entity_detection_url, json = {"sentences": [["what is the capital of russia?"]]}).json()

Output:

```json

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

```

Elements of the output data:

* "entities" - entity substrings in the utterance
* "labelled_entities" - entity substrings with extra annotations:
      - "offsets" - indices of start and end symbols of entity substring in the utterance
      - "label" - entity tag
      - "finegrained_label" - more specific entity tag

Entity Linking
-------------------



 Check out our `Blogpost <https://medium.com/deeppavlov/using-annotators-for-the-utterances-analysis-in-dream-dialogue-assistant-730b99dcabbc>`_ about Dream services that work with Knowledge Graphs to learn more.
