
Tutorials
================

Getting Started
----------------

First, initialize the graph.

.. code:: python

  from deeppavlov_kg.core.graph import Neo4jKnowledgeGraph
  
  graph = Neo4jKnowledgeGraph(
    "bolt://neo4j:neo4j@neo4j:7687",
    ontology_kinds_hierarchy_path="deeppavlov_kg/database/ontology_kinds_hierarchy.pickle",
    ontology_data_model_path="deeppavlov_kg/database/ontology_data_model.json",
    db_ids_file_path="deeppavlov_kg/database/db_ids.txt")


You probably will need the User id. Retrieve it with the help of DFF functions.

.. code:: python

  import common.dff.integration.context as int_ctx
  
  utt = int_ctx.get_last_human_utterance(ctx, actor)
  user_id = utt.get("user", {}).get("id", "")
  
  user_id
  >>> "633c376d936b773783eb6ef1"



Usage Examples
---------------

There are some examples that should cover the basic usage of the Custom KG in some skill. Please, refer to the API if there is no answer to your question in these examples.

Get Entity Properties
^^^^^^^^^^^^^^^^^^^^^^
**Example objective:** find all of the existing properties of the User given their id.

**Solution:** There is a single function that does just that.

.. code:: python

  properties = graph.get_properties_of_entity(entity_id=user_id)
  
  properties
  >>> {'name': 'Diana', 'has_age': '30', '_deleted': False}
  
Get Entity Relationships
^^^^^^^^^^^^^^^^^^^^^^^^^^
**Example objective:** find all of the existing connections of the User including relationship types and information about tail entities.

**Solution:** it is done with a single function, but if you want to retrieve the properties of the tail entities, you would also need to find their current states. You may also format the output as suggested or in any other way.

.. code:: python

    result = graph.search_for_relationships(id_a=user_id)
    
    relationships = []
    for i, rel_info in enumerate(result):
        relationship = rel_info[-2]
        tail_entity = rel_info[-1]
        state = graph._get_current_state_node(tail_entity["Id"])
        
        rel_dict = {
        "type": relationship.type, 
        "tail name": state["name"], 
        "tail kind": list(tail_entity.labels)[0]
        }
        
        relationships.append(rel_dict)
        
     relationships
     >>> [{'type': 'LIKE_DRINK', 'tail name': 'tea', 'tail kind': 'Beverage'}, 
     {'type': 'LIKE_GOTO', 'tail name': 'London', 'tail kind': 'Capitalcity'}]
  
  
Get a Certain Type of Relationships
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Example objective:** find out what pets the User has, if any.

**Solution:** First, find all relationships with kind *HAVE_PET* related to the User. You can also extract the Ids of the found entities and use it to get the relevant information from their current states.

**Note:** The first function will return empty list if there are no such relationships.

.. code:: python

    pet_answer = graph.search_for_relationships(
        id_a=user_id,
        relationship_kind='HAVE_PET'
    )

    pets_info = []
    for answer in pet_answer:
        state = graph._get_current_state_node(answer[-1]["Id"])
        
        pet_dict = {
            "pet kind": list(answer[-1].labels)[0],
            "pet name": state["name"]
            }
            
        pets_info.append(pet_dict)
    
    pets_info
    >>> [{'pet kind': 'Mammal', 'pet name': 'dog'}]
  
  
Get Relationships with Certain Kinds of Entities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Example objective:** find out if the User has any relationships with any Mammals and specify which types of relationships.

**Solution:** Spectify the target kind of the tail entity and find the relationships. Retrieve the type of each found relationship.


**Note:** The function will return empty list if there are no such relationships.

.. code:: python

    mammal_answer = graph.search_for_relationships(
        id_a=user_id,
        kind_b='Mammal'
    )

    mammal_rels_info = []
    for answer in mammal_answer:
        mammal_rels_info.append(answer[-2].type)
        
    mammal_rels_info
    >>> ['HAVE_PET']
  
