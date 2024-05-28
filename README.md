# MedicalAIchatbot

**Architecture**

![](https://github.com/Vishnusai4/MedicalAIchatbot/blob/main/data/RAG%20Architecture%20for%20Medical%20Q%26A%20bot-1.png)

**Details**

This repo explores building conversational Q&A bots using large language models and retrieval augmented generation (RAG). This Q&A bot helps answer questions related to diabetes.

The flow sequence to build this pipeline:
1. Extract relevant pubmed article abstracts related to diabetes.
2. Split the abstracts into chunks. Chunks help to overcome the limitatios around token_size in llm's. In this repo, **RecursiveCharacterTextSplitter** is used as it helps keep all the context required to answer the question within one chunk.
3. Convert the chunks into embeddings. An open source sentence transformer from huggingface is used for this purpose.
4. Store the embeddings into a vector database for retrievel durng query. Facebook AI similarity search vectorstore is used.
5. Load LLM : Mistral7B
6. Once the user inputs his query/question, use the query to extract relevant context from the vector database. Append the query and the context to the prompt templete. The prompt template is passed into an LLM to generate a response.

The RAG pipeline is in the notebook DiabetesQ&Achatbot.ipynb
