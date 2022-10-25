
Working with Document Services
===============================

How to call the service REST API
-------------------------------

The service can be called via http://7040.deeppavlov.ai/ directly in your app. 

>>> requests.post("http://7040.deeppavlov.ai/", json={"text": "The Mona Lisa is a sixteenth century oil painting created by Leonardo."}).json()

.. code:: json

    {
    "annotations":[
        {
        "start":0,
        "end":13,
        "spot":"The Mona Lisa",
        "confidence":1.0,
        "id":"Q2126369",
        "title":"Mona Lisa (Prado)",
        "uri":"https://en.wikipedia.org/wiki/Mona_Lisa_(Prado)",
        "abstract":"The Prado Mona Lisa is a painting by the workshop of Leonardo da Vinci and [...] ",
        "label":"Mona Lisa (Prado)",
        "categories":[ "Mona Lisa", "Paintings of the Museo del Prado by Italian artists"],
        "tags":["WORK_OF_ART", "LITERARY_WORK", "FAC"],
        "types":[],
        "image":{
            "full":"https://commons.wikimedia.org/wiki/Special:FilePath/Gioconda_(copia_del_Museo_del_Prado_restaurada).jpg",
            "thumbnail":"https://commons.wikimedia.org/wiki/Special:FilePath/Gioconda_(copia_del_Museo_del_Prado_restaurada).jpg?width=300"
        },
        "lod":{
            "wikipedia":"https://en.wikipedia.org/wiki/Mona_Lisa_(Prado)"
        },
        "extras":[]
        },
        {
        "start":61,
        "end":69,
        "spot":"Leonardo",
        "confidence":1.0,
        "id":"Q762",
        "title":"Leonardo da Vinci",
        "uri":"https://en.wikipedia.org/wiki/Leonardo_da_Vinci",
        "abstract":"Leonardo di ser Piero da Vinci (15 April 14522 May 1519) was an [...] ",
        "label":"Leonardo da Vinci",
        "categories":["Leonardo da Vinci", "1452 births", "1519 deaths", [...]],
        "tags":["PER", "WRITER", "BUSINESS"],
        "types":["https://dbpedia.org/ontology/Agent"],
        "image":{
            "full":"https://commons.wikimedia.org/wiki/Special:FilePath/Francesco_Melzi_-_Portrait_of_Leonardo.png",
            "thumbnail":"https://commons.wikimedia.org/wiki/Special:FilePath/Francesco_Melzi_-_Portrait_of_Leonardo.png?width=300"
        },
        "lod":{
            "wikipedia":"https://en.wikipedia.org/wiki/Leonardo_da_Vinci"
        },
        "extras":[
            {
            "start":61,
            "end":69,
            "spot":"Leonardo",
            "confidence":0.35,
            "id":"Q2155112",
            "title":"Bartolomé Leonardo de Argensola",
            "uri":"https://en.wikipedia.org/wiki/Bartolomé_Leonardo_de_Argensola",
            "abstract":"Bartolomé Leonardo de Argensola was baptized at Barbastro on August 26, 1562. He studied at [...] ",
            "label":"Bartolomé Leonardo de Argensola",
            "categories":["1562 births", "1631 deaths", "People from Barbastro", [...]],
            "tags":["PER", "WRITER", "BUSINESS"],
            "types":["https://dbpedia.org/ontology/Agent"],
            "image":{
                "full":"https://commons.wikimedia.org/wiki/Special:FilePath/Bartolomé_Leonardo_de_Argensola_(Diputación_Provincial_de_Zaragoza).jpg",
                "thumbnail":"https://commons.wikimedia.org/wiki/Special:FilePath/Bartolomé_Leonardo_de_Argensola_(Diputación_Provincial_de_Zaragoza).jpg?width=300"
            },
            "lod":{
                "wikipedia":"https://en.wikipedia.org/wiki/Bartolomé_Leonardo_de_Argensola"
            }
            }
        ]
        },
    ],
    "lang":"en",
    "timestamp":"2022-10-23T17:28:04.955988"
    }



How to launch the service locally
-------------------------------

To launch Entity Extraction Service locally, you should clone the repository and then build and launch the service containers:

| git clone https://github.com/deeppavlov/entity_extraction_svc.git
| docker-compose up --build
|

After that, you can use local service through 7040 TCP port the same way as above.

>>> requests.post("http://127.0.0.1:7040/", json={"text": "The Mona Lisa is a sixteenth century oil painting created by Leonardo."}).json()
