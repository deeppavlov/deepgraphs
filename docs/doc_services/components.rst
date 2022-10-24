
Document Services
===================

Entity Extraction Service
-------------------------

Entity extraction enhances our understanding of unstructured text by extracting information which can be further used to improve user experience in different ways. It converts unstructured text into structured data by identifying named entities mentioned in the given text and linking them to unique identifiers in a knowledge base, such as Wikidata. This way, developers can extract meaningful information from large texts and make use of that knowledge in their own apps.

Entity Extraction Service consists of 4 components:

* **Entity Detection** - RoBERTa based model that classifies each token to BIO tags
* **Entity Type Classification** - classifies extracted substrings to one of the 42 entity types from Wikidata
* **Entity Extraction** - matches substrings to candidate entities in the SQLite database filtering by type
* **Entity Disambiguation** - links entities to unique identifiers in Wikidata

Comparison with other solutions:

+----------------------------------+---------------------+
| Service                          | Accuracy WNED-WIKI  |
+==================================+=====================+
| Entity Extraction Service        |      0.67           |
+----------------------------------+---------------------+
| Dandelion                        |      0.64           |
+----------------------------------+---------------------+


Example usage:

>>> requests.post("http://7040.deeppavlov.ai/", json={"text": "The Mona Lisa is a sixteenth century oil painting created by Leonardo. It's held at the Louvre in Paris."}).json()

Output:

.. code:: json

    {
        "annotations":[
            {
              "start": 0,
              "end": 13,
              "spot": "The Mona Lisa",
              "confidence": 1.0,
              "id": "Q2126369",
              "title": "Mona Lisa (Prado)",
              "uri": "https://en.wikipedia.org/wiki/Mona_Lisa_(Prado)",
              "abstract": "The Prado Mona Lisa is a painting by [...]",
              "label": "Mona Lisa (Prado)",
              "categories": ["Mona Lisa", "Paintings of the Museo del Prado by Italian artists"],
              "tags": ["WORK_OF_ART", "LITERARY_WORK", "FAC"],
              "types": [],
              "image":{
                "full": <image>,
                "thumbnail": <thumbnail>
                },
              "lod":{
                "wikipedia": "https://en.wikipedia.org/wiki/Mona_Lisa_(Prado)"
                },
              "extras": []
            }
        ]
    }

Elements of the output data:

* "start" - start position of entity substring in the text
* "end" - end position of entity substring in the text
* "spot"  - entity substring extracted from the text
* "confidence" - confidence of extracted Wikidata entity for the substring
* "id” - Wikidata entity ID linked for the substring in the utterance
* "title" - Wikipedia page title corresponding to Wikidata entity ID
* "uri" - Wikipedia page url
* "abstract" - first paragraph from the Wikipedia page
* "label" - Wikidata label corresponding to the entity ID
* "categories" - Wikidata categories corresponding to the entity ID
* "tags" - entity detection tags for the extracted Wikidata entity
* "types" - DBpedia types corresponding to the extracted Wikidata entity
* "image" - Wikidata image information
* "lod" - 
* "extras" - information about alternative entity IDs with smaller probabilities


Authors: Dima (everything except HTML), Max (HTML endpoint)


Custom Entity Extraction Service
--------------------------------

Custom Entity Extraction service allows developers to index their own knowledge graphs and then apply the same Entity Extraction Service to the texts to link entities to their own knowledge graphs. 

Example usage:

Let's consider a small custom database in .nt format given below. To add these triplets to knowledge graph, firstly, relations connecting entity IDs and labels/types have to be specified using the "kb_schema" endpoint, and then the triplets can be added through the "add_kb" andpoint. 

|    <Q1> <label> "Elon Musk" .
|    <Q2> <label> "SpaceX" .
|    <Q3> <label> "Crew-4" .
|    <Q4> <label> "International Space Station" .
|    <Q5> <label> "NASA" .
|    <Q6> <label> "Dragon" .

>>> requests.post("http://0.0.0.0:9103/kb_schema", json={"relation_info": {"label_rel": "label", "type_rel": "type"}})
>>> requests.post("http://0.0.0.0:9103/add_kb", json={"triplets": lines})

After that, the usual Entity Extraction Service will be able to extract these new entities from text.

>>> text = "SpaceX just set a new record for its fastest Dragon astronaut trip yet. Elon Musk's spaceflight company launched four Crew-4 astronauts to the International Space Station for NASA in less than 16 hours on Wednesday (April 27), the shortest flight time since SpaceX began crewed flights in 2020."
>>> requests.post("http://7040.deeppavlov.ai/", json={"text": text}).json()

Output:

.. code:: json

    {	
        “entity_substr”: [['spacex', 'dragon', 'elon musk', 'crew-4', 'international space station', 'nasa', 'spacex']],
        “entity_offsets”: [[[0, 6], [45, 51], [72, 81], [116, 122], [141, 168], [173, 177], [256, 262]]],
        “entity_ids”: [[['Q2'], ['Q6'], ['Q1'], ['Q3'], ['Q4'], ['Q5'], ['Q2']]],
        “entity_tags”: [[['misc'], ['misc'], ['misc'], ['misc'], ['misc'], ['misc'], ['misc']]],
        “entity_conf”: [[[1.0], [1.0], [1.0], [0.4], [1.0], [1.0], [1.0]]]
    }
