
Shared KG Services
==================

Custom KG
---------
Custom knowledge graph API is designed to provide an easy interface to CRUD data to databases like TerminusDB and Neo4j in the runtime.

If you'd like to contribute, `fork us on GitHub! <https://github.com/deeppavlov/custom_kg_svc/tree/main>`_

.. **Behold, the power of Custom KG:**

.. .. code:: python

..     DB = "example_db"
..     TEAM ="example_team|1"
..     terminus_kg = TerminusdbKnowledgeGraph(team=TEAM, db_name=DB)


..     NEO4J_BOLT_URL = "bolt://neo4j:neo4j@localhost:7687"
..     ONTOLOGY_KINDS_HIERARCHY_PATH = "deeppavlov_kg/database/ontology_kinds_hierarchy.pickle"
..     ONTOLOGY_DATA_MODEL_PATH = "deeppavlov_kg/database/ontology_data_model.json"
..     DB_IDS_FILE_PATH = "deeppavlov_kg/database/db_ids.txt"

..     neo_kg = Neo4jKnowledgeGraph(
..             neo4j_bolt_url=NEO4J_BOLT_URL,
..             ontology_kinds_hierarchy_path=ONTOLOGY_KINDS_HIERARCHY_PATH,
..             ontology_data_model_path=ONTOLOGY_DATA_MODEL_PATH,
..             db_ids_file_path=DB_IDS_FILE_PATH,
..         )

**How to use each of these APIs**

Create and add entity kinds to the ontology graph:

.. code:: python
    
    terminus_kg.drop_database()

    terminus_kg.ontology.create_entity_kinds(
        entity_kinds=["Person", "User", "Habit"],
        parents=[None, "Person", None]
    )
    terminus_kg.ontology.get_all_entity_kinds()

Output:

.. code:: json

    {
        "Person":{
            "@id":"Person",
            "@type":"Class"
        },
        "Habit":{
            "@id":"Habit",
            "@type":"Class"
        },
        "User":{
            "@id":"User",
            "@inherits":"Person",
            "@type":"Class"
        }
    }

Allow entity kinds to have properties:

.. code:: python

    terminus_kg.ontology.create_property_kinds_of_entity_kinds(
        entity_kinds=["Person", "User", "Habit"],
        property_kinds=[
            ["Height", "Weight"],
            ["Login", "Password"],
            ["Start_date"],
        ],
        property_types=[
            [int, int],
            [str, str],
            [datetime.date],
        ]
    )
    terminus_kg.ontology.get_all_entity_kinds()

Output:

.. code:: json

    {
        "Habit":{
            "@id":"Habit",
            "@type":"Class",
            "Start_date":{
                "@class":"xsd:date",
                "@type":"Optional"
            }
        },
        "User":{
            "@id":"User",
            "@inherits":"Person",
            "@type":"Class",
            "Login":{
                "@class":"xsd:string",
                "@type":"Optional"
            },
            "Password":{
                "@class":"xsd:string",
                "@type":"Optional"
            }
        },
        "Person":{
            "@id":"Person",
            "@type":"Class",
            "Height":{
                "@class":"xsd:integer",
                "@type":"Optional"
            },
            "Weight":{
                "@class":"xsd:integer",
                "@type":"Optional"
            }
        }
    }

Create and add relationship kinds to ontology graph:

.. code:: python

    terminus_kg.ontology.create_relationship_kinds(
        ["Person", "Person"],
        ["KEEP_UP", "QUIT"],
        ["Habit", "Habit"],
    )
    terminus_kg.ontology.get_all_entity_kinds()

Output:

.. code:: json

    {
        "Person":{
            "@id":"Person",
            "@type":"Class",
            "Height":{
                "@class":"xsd:integer",
                "@type":"Optional"
            },
            "KEEP_UP":{
                "@class":"Habit",
                "@type":"Set"
            },
            "QUIT":{
                "@class":"Habit",
                "@type":"Set"
            },
            "Weight":{
                "@class":"xsd:integer",
                "@type":"Optional"
            }
        },
        "Habit":{
            "@id":"Habit",
            "@type":"Class",
            "Start_date":{
                "@class":"xsd:date",
                "@type":"Optional"
            }
        },
        "User":{
            "@id":"User",
            "@inherits":"Person",
            "@type":"Class",
            "Login":{
                "@class":"xsd:string",
                "@type":"Optional"
            },
            "Password":{
                "@class":"xsd:string",
                "@type":"Optional"
            }
        }
    }

Create and add new entities with their properties to the knowledge graph database:

.. code:: python

    terminus_kg.create_entities(
        entity_kinds=["User"]*2+["Habit"],
        entity_ids=["User/"+str(id) for id in range(2)]+["Habit/Sport"],
        property_kinds=[
            ["Height", "Login", "Password"],
            ["Weight", "Login", "Password"],
            ["Start_date"],
        ],
        property_values=[
            [170, "Jack333", "12345678"],
            [60, "Sandy111", "00000000"],
            [datetime.date(2010, 10, 10)],
        ]
    )
    terminus_kg.get_all_entities()

Output:

.. code:: json

    [
        {
            "@id":"Habit/Sport",
            "@type":"Habit",
            "Start_date":"2010-10-10"
        },
        {
            "@id":"User/0",
            "@type":"User",
            "Height":170,
            "Login":"Jack333",
            "Password":"12345678"
        },
        {
            "@id":"User/1",
            "@type":"User",
            "Login":"Sandy111",
            "Password":"00000000",
            "Weight":60
        }
    ]

Create and add new relationships to the knowledge graph database:

.. code:: python

    terminus_kg.create_relationships(
        ids_a=["User/0", "User/1"],
        relationship_kinds=["KEEP_UP", "QUIT"],
        ids_b=["Habit/Sport"]*2
    )

    terminus_kg.get_all_entities()

Output:

.. code:: json

    [
        {
            "@id":"Habit/Sport",
            "@type":"Habit",
            "Start_date":"2010-10-10"
        },
        {
            "@id":"User/0",
            "@type":"User",
            "Height":170,
            "Login":"Jack333",
            "Password":"12345678",
            "KEEP_UP":"Habit/Sport"
        },
        {
            "@id":"User/1",
            "@type":"User",
            "Login":"Sandy111",
            "Password":"00000000",
            "Weight":60,
            "QUIT":"Habit/Sport"
        }
    ]