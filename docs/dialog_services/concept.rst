
Concept
========

The system collects information about the User from dialogues in the form of relationship or property triplets and stores it in the Custom Knowledge Graph (KG). Stored information can be used in any Dream Skill.

Storing Information
--------------------

The storing pipeline cosists of the following steps:

* Extracting triplets from an utterance with the **Property Extraction** service.
* Linking entities from the extracted triplet to the exsisting ones in the KG with the **Entity linking** service.
* Storing new relationships or properties in the KG with the **User Knowledge Graph**.

.. image:: schema_user_kg.png

Using Information
------------------

Using Custom KG in your skill should consist of the following steps:

* Formulating the query: decide what exactly do you want to know about the User.
* Using additional infromation from annotators. For example, use **Property extraction** annotators to formulate personalized response to the user or use **Custom Entity Linking** to recall user attributes from previuos conversations.
* Getting the information and using it as you wish.

See *skills/user_kg_skill* for reference.




