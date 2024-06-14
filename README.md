# Medical_Research_RAG

This project utilizes LLMs (Large Language Model) and RAG (Retrieval-Augmented Generation) to create a helpful medical research assistant that guides students in writing research papers.

## Usage

On first use of the tool, a user will provide a subject to the RAG agent to help write the topic sentences for each paragraph.
On second pass, another agent will guide the user on how best to fill out each paragraph with the supplied topic sentence.

## Loading Data

The assistant utilizes two supplemental vector databases, one for background information and another for bibliographic references.
Documents to load those databases are downloaded from [PubMed](https://pubmed.ncbi.nlm.nih.gov/)

A download script is provided [pubmed_download.py](https://github.com/VincentYing/Medical_Research_RAG/blob/main/pubmed_download.py) to retrieve the documents and save them in the **data** subdirectory.

Example script execution to download 2023 documents from PubMed:
```
python download_pubmed.py --start  "2023/01/01" --end "2023/12/31"
```

Letters, review articles, and conference abstracts are saved in **pubmed_background.json**

Journal article and clinical trials are saved in **pubmed_reference.json**

## LLMs

The LLM  used in most of the RAG chains for this repo is llama3 with [Ollama](https://github.com/ollama/ollama)

For convenience, [llamafile](https://github.com/Mozilla-Ocho/llamafile) can also be used to download and manage different LLMs.

[LLamaIndex](https://github.com/run-llama/llama_index) is used as the vector store[^1] for the RAG chains below. ChromaDB is another good choice to store the reference documents.[^2]

LlamaIndex and llamafile are used together to build a local, private research assistant.[^3]

## RAG Chains

Although RAG can be excuted directly in the commandline[^4] for quick feedback and prototyping, we've saved the execution in jupyter notebooks.

## Completed

[medical_research_rag-crewai.ipynb](https://github.com/VincentYing/Medical_Research_RAG/blob/main/medical_research_rag-crewai.ipynb) : This notebook demonstrates multi-agent RAG with our research assistant workflow but doesn't include medical document ingestion.[^5]

### Under Development

[medical_ra_rag.ipynb](https://github.com/VincentYing/Medical_Research_RAG/blob/main/medical_ra_rag.ipynb) : Initial RAG Search on Academic Papers with LlamaIndex as **Chat Engine** in Context Mode[^6]

[medical_ra_rag-json_reader.ipynb](https://github.com/VincentYing/Medical_Research_RAG/blob/main/medical_ra_rag-json_reader.ipynb) : Instead of using SimpleDirectory for document ingestion, this notebook utilizes **JSONReader** from [LlamaHub](https://docs.llamaindex.ai/en/stable/understanding/loading/llamahub/).[^7]

[medical_ra_rag-json_engine.ipynb](https://github.com/VincentYing/Medical_Research_RAG/blob/main/medical_ra_rag-json_engine.ipynb) : This notebook utilizes **JSONQueryEngine** with added schema knowledge of the indexed JSON documents.[^8]

[medical_ra_rag-query_engines.ipynb](https://github.com/VincentYing/Medical_Research_RAG/blob/main/medical_ra_rag-query_engines.ipynb) : This notebook uses a **ReActAgent** with RAG QueryEngine Tools, a separate engine for background and reference.[^9]

[medical_ra_rag-json_loader.ipynb](https://github.com/VincentYing/Medical_Research_RAG/blob/main/medical_ra_rag-json_loader.ipynb) : This notebook uses LangChain **JSONLoader** and **ChromaDB** instead of LlamaIndex vector store. [^10]

## References

[^1]: [https://docs.llamaindex.ai/en/stable/understanding/indexing/indexing/](https://docs.llamaindex.ai/en/stable/understanding/indexing/indexing/)

[^2]: [https://docs.llamaindex.ai/en/stable/examples/vector_stores/ChromaIndexDemo/](https://docs.llamaindex.ai/en/stable/examples/vector_stores/ChromaIndexDemo/)

[^3]: [https://www.llamaindex.ai/blog/using-llamaindex-and-llamafile-to-build-a-local-private-research-assistant](https://www.llamaindex.ai/blog/using-llamaindex-and-llamafile-to-build-a-local-private-research-assistant)

[^4]: [https://docs.llamaindex.ai/en/stable/getting_started/starter_tools/rag_cli/](https://docs.llamaindex.ai/en/stable/getting_started/starter_tools/rag_cli/)

[^5]: [https://medium.com/the-ai-forum/create-a-blog-writer-multi-agent-system-using-crewai-and-ollama-f47654a5e1cd](https://medium.com/the-ai-forum/create-a-blog-writer-multi-agent-system-using-crewai-and-ollama-f47654a5e1cd)

[^6]: [https://docs.llamaindex.ai/en/latest/examples/chat_engine/chat_engine_context/](https://docs.llamaindex.ai/en/latest/examples/chat_engine/chat_engine_context/)

[^7]: [https://llamahub.ai/l/readers/llama-index-readers-json](https://llamahub.ai/l/readers/llama-index-readers-json)

[^8]: [https://docs.llamaindex.ai/en/stable/examples/query_engine/json_query_engine/](https://docs.llamaindex.ai/en/stable/examples/query_engine/json_query_engine/)

[^9]: [https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/usage_pattern/#query-engine-tools](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/usage_pattern/#query-engine-tools)

[^10]: [https://python.langchain.com/v0.1/docs/modules/data_connection/document_loaders/json/](https://python.langchain.com/v0.1/docs/modules/data_connection/document_loaders/json/)