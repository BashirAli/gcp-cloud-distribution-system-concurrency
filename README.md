# GCP Cloud Event Based Concurrency 







To replicate concurrency typically experienced in a distributed system, we will write to Datastore using multi-threading, with the inclusion of Python Semaphores to limit the amount of threads that will access Datastore

