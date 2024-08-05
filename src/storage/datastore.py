from google.cloud import datastore
from google.api_core.exceptions import BadRequest, ServiceUnavailable

from model.logging import logger


class Datastore:
    def __init__(self, project_id: str, namespace: str):
        self._ds_client = datastore.Client(project=project_id, namespace=namespace)

    def get_entity_with_key(self, ds_kind: str, key: str) -> datastore.Entity | None:
        ds_key = self._ds_client.key(ds_kind, key)
        try:
            return self._ds_client.get(ds_key)
        except (BadRequest | ServiceUnavailable) as err:
            logger.error(f"Datastore Client retrieve entity error occurred: {err}")
            return None

    def insert_entity_with_key(self, ds_kind: str, key: str, data: dict):
        try:
            with self._ds_client.transaction():  # locking to avoid race conditions
                ds_key = self._ds_client.key(ds_kind, key)

                insert_entity = datastore.Entity(key=ds_key)
                insert_entity.update(data)
                self._ds_client.put(insert_entity)
                logger.info(f"Data not found in cache, writing to cache with key: {key}")
        except (BadRequest | ServiceUnavailable) as err:
            logger.error(f"Datastore Client write to entity error occurred: {err}")
