
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

Examples of Property Extraction usage:

.. code:: python

    >>> requests.post(property_extraction_url, json = {"utterances": ["i live in moscow"]}).json()
    [{"triplet": {"object": "moscow", "relation": "live in citystatecountry", "subject": "user"}}]
    >>> requests.post(property_extraction_url, json = {"utterances": ["i listen to scorpions"]}).json()
    [{"triplet": {"object": "scorpions", "relation": "like music", "subject": "user"}}]

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

Entity Linking
-------------------

Entity Linking annotator defines Wikidata IDs for entity substrings in the user utterance. For example, for the entity "Germany" in the utterance "I went to Germany" the annotator finds the ID "Q183" and corresponding Wikipedia page title "Germany". First, Entity Linking service extracts candidate entities from the inverted index and then defines which of these entities better fit the context.

Index of entities with the corresponding Wikipedia page titles is stored in the SQLite database with the FTS5 extension. In the SQLite database only indexes are loaded into RAM, which leads to low memory usage. The row in the entities table contains an entity title, entity ID in Wikidata, Wikipedia page title, an entity tag, and an entity description. To retrieve candidate entities, we execute a query to the database that contains entity substring and the top-3 tags, detected with the entity type classification model.

Entity disambiguation helps to define which entity is more appropriate to the context. Candidate entities are sorted by dot product of context and description embeddings. Context embedding is obtained by replacing entity substring with a special ENT-token and taking its BERT-small output vector. Entity representation is also calculated with BERT-small from entity description with hidden state of CLS token. The model is trained to maximize the dot product of context and entity embeddings if the entity is appropriate to the context and minimize otherwise.

Examples of Entity Linking usage:

.. code:: python

    >>> requests.post(entity_linking_url, json = {"entity_substr": [["forrest gump"]], "entity_tags": [[[("film", 0.9)]]], "context": [["who directed forrest gump?"]]}).json()
    
Output:

.. code:: json

    [
        [
            {
                "entity_substr": "forrest gump",
                "entity_id_tags": ["FILM"],
                "entity_ids": ["Q134773"],
                "pages_titles": ["Forrest Gump"],
                "confidences": [46.0],
                "dbpedia_types": [["http://dbpedia.org/ontology/Film", "http://dbpedia.org/ontology/Work"]],
                "first_paragraphs": ["Forrest Gump is a 1994 American comedy-drama film directed by Robert Zemeckis and written by Eric Roth."],
                "tokens_match_conf": [1.0]
            }
        ]
    ]

Elements of the output data:

* "entity_substr" - entity substring from the utterance;
* "entity_id_tags" - Entity Detection tags for extracted Wikidata entities;
* "entity_ids" - Wikidata entity IDs, linked for the substring in the utterance;
* "pages_titles" - Wikipedia page titles, corresponding to Wikidata entity IDs;
* "confidences" - confidences of extracted Wikidata entities for the substring;
* "dbpedia_types" - DBpedia types, corresponding to extracted Wikidata entities;
* "first_paragraphs": first paragraphs from Wikipedia pages;
* "tokens_match_conf" - the ratios of matching of entity substring and extracted entity IDs titles.

 Check out our `Blogpost <https://medium.com/deeppavlov/using-annotators-for-the-utterances-analysis-in-dream-dialogue-assistant-730b99dcabbc>`_ about Dream services that work with Knowledge Graphs to learn more.
