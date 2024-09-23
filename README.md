# Introduction to Autonomous Agents: Workshop
<img src="media/agent_picture.png" alt="Image description" width="700">
This repository introduces and helps organizations get started with creating autonomous agents with relevant business scenarious.

## Workshop Agenda
The objective of this workshop is to discuss realistic autonomous agent business scenarios and to learn how to leverage **autogen** for development. At the end of the workshop you will:

- Understand agentic reasoning and the core concepts behind agents
- Understand what agents can do and how to leverage them to maximimize the impact for the business
- Be able to create autonomous agents from scratch using **Autogen**
- Learn relevant business scenarious for autonomous agents

| Topic                          | Details                                                                                                                          | Comments |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- | -------- |
| Autonomous Agents Introduction | - From LLMs to autonomous agents <br> - Agent framework capabilities and market overview                                         | 20 min   |
| AutoGen                        | - AutoGen overview: concepts and capabilities <br> - Building a multi-agent conversation from scratch <br> - AutoGen Studio Demo | 60 min   |
| Business scenarious: Demos     | - Simplified troubleshooting customer service demo <br> - Onboarding buddy demo <br> - Guided image generation demo              | 60 min   |
| Envisioning                    | - Identification of potential use cases <br> - PoC scope definition                                                              | 90 min   |

## Setting up the resources

For the demos, Azure AI Search and Cosmos DB are needed. The sample data used for the simple demos is stored under `utils/sample_data`.

**Azure AI Search**


[List of supported regions for semantic ranking](https://learn.microsoft.com/en-us/azure/search/search-region-support)

We need to create AI search in one of the regions where semantic ranking feature is enabled.

![Creating AI search](media/search-service.png)

`Basic` tier would be sufficient for demo purposes, however if your index size is larger, consider reviewing the [list of supported tiers](https://learn.microsoft.com/en-us/azure/search/search-sku-tier).


**Cosmos DB with sample data**

To set up CosmosDB, choose the CosmosDB for NoSQL and the `Serverless` capacity option.

![Creating CosmosDB](media/cosmosdb.png)
