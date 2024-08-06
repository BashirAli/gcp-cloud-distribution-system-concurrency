from google.api_core.exceptions import BadRequest, ServiceUnavailable
from google.cloud import datastore

from model.logging import logger
from utils.helpers import hash_datastore_key, is_stored_older_than_inbound_timestamp


class Datastore:
    def __init__(self, project_id: str, namespace: str, kind: str):
        self._ds_client = datastore.Client(project=project_id, namespace=namespace)
        self.kind = kind

    def get_entity_with_key(self, key: str) -> datastore.Entity | None:
        ds_key = self._ds_client.key(self.kind, key)
        try:
            return self._ds_client.get(ds_key)
        except (BadRequest | ServiceUnavailable) as err:
            logger.error(f"Datastore Client retrieve entity error occurred: {err}")
            return None

    def insert_entity_with_key(self, key: str, data: dict) -> None:
        try:
            ds_key = self._ds_client.key(self.kind, key)

            insert_entity = datastore.Entity(key=ds_key)
            insert_entity.update(data)
            self._ds_client.put(insert_entity)
            logger.info(f"put")
        except (BadRequest | ServiceUnavailable) as err:
            logger.error(f"Datastore Client write to entity error occurred: {err}")

    def upsert_if_data_is_newer(self, entity_dict: dict) -> bool:
        hashed_entity_id = hash_datastore_key(entity_dict["entity_id"])
        try:
            with self._ds_client.transaction():
                entity = self.get_entity_with_key(hashed_entity_id)
                if not entity:
                    self.insert_entity_with_key(hashed_entity_id, entity_dict)
                    return True

                if is_stored_older_than_inbound_timestamp(stored_timestamp=entity["ingestion_timestamp"],
                                                          inbound_timestamp=entity_dict["ingestion_timestamp"]):
                    self.insert_entity_with_key(hashed_entity_id, entity_dict)
                    return True

            return False
        except Exception as e:
            logger.error(f"Exception during upsert: {e}")
            return False


