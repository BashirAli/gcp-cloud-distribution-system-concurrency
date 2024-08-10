import os
import threading

from model.logging import logger
from storage.datastore import Datastore
from utils.helpers import semaphore_lock


class ConcurrencyManager:
    semaphore = threading.Semaphore(5)

    def __init__(self):
        self._ds_client = Datastore(project_id=os.getenv("GCP_PROJECT_ID"), namespace=os.getenv("DATASTORE_NAMESPACE"),
                                    kind=os.getenv("DATASTORE_KIND"))

    def replicate_distribution_system_concurrency(self, data: list, callback=None):
        threads = []
        for entity in data:
            thread = threading.Thread(target=self._process_entity, args=(entity, callback))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    @semaphore_lock(semaphore=semaphore)
    def _process_entity(self, entity: dict, callback):
        success = self._ds_client.upsert_if_data_is_newer(entity)
        if callback:
            callback(entity, success, None if success else "Data is not newer or an error occurred")

    @staticmethod
    def completion_callback(entity: dict, success: bool, error: str):
        if success:
            logger.info(
                f"Successfully processed entity {entity["event_id"]} at ingestion timestamp {entity["event_timestamp"]}.")
        else:
            logger.warning(
                f"Failed to process entity {entity["event_id"]} at ingestion timestamp {entity["event_timestamp"]}. Error: {error}")
