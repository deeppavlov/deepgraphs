Working with Knowledge Graphs at DeepPavlov
=============================================

This page is dedicated to the DeepPalov services that are related to Knowledge Graphs. There are two separate directions:

* **Dialog serivces.** These are a part of the Dream chatbot pipeline and can be used for any of your skills. These services work with conversational data. They work with two types of Knowledge Graphs:

  * **Custom KG** stores information about Users. Check :doc:`../dialog_services/concept` to find out how information is stored and can be used in the dialog pipeline. Go to :doc:`../ontology/ontology` to see which kinds of relationships, properties and entities are stored in the Custom KG. Section :doc:`..//dialog_services/tutorials` will help you to build your own skill using Custom KG.
  * **External KGs** are used to extract information about the world. Go to :doc:`../dialog_services/components` section to learn more.
    

* **Document services.** These are the separate services and can be used in any types of your applications. These services work with regual text data. Check the :doc:`doc_services/components` and :doc:`doc_services/components` in order to learn more about them.

   
.. toctree::
   :glob:
   :maxdepth: 3
   :caption: Ontology

   Ontology <ontology/ontology>
   
.. toctree::
   :glob:
   :maxdepth: 3
   :caption: Dialog Services
  
   Concept <dialog_services/concept>
   Components <dialog_services/components>
   Tutorials <dialog_services/tutorials>
   
.. toctree::
   :glob:
   :maxdepth: 3
   :caption: Document Services

   Components <doc_services/components>
   Tutorials <doc_services/tutorials>
   

.. toctree::
   :glob:
   :maxdepth: 3
   :caption: API Reference

   apiref/*


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
