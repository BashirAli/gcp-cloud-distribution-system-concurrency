# GCP Cloud Event Based Concurrency 

This repository replicates a distributed system where multiple "nodes" write to a single storage instance (GCP Cloud Datastore). 
To replicate concurrency typically experienced in a distributed system, we will write to Datastore using multi-threading, with the inclusion of Python Semaphores to limit the amount of threads that will access Datastore

## Getting Started

1. Create a `.env` file and fill in the following variables

```
GCP_PROJECT_ID=<YOUR_PROJECT_ID>>
DATASTORE_NAMESPACE=<YOUR_DATASTORE_NAMESPACE>>
DATASTORE_KIND=<YOUR_DATASTORE_KIND>
```

2. Install poetry (if required) and the poetry files in your chosen virtual environment 

```
pip install poetry 
poetry install
```

3. run `main()`






*Developed in Python 3.12.0*

