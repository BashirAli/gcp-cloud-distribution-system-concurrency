import os
import threading
from storage.datastore import Datastore
from model.logging import logger


class ConcurrencyManager:
    def __init__(self):
        self._ds_client = Datastore(project_id=os.getenv("GCP_PROJECT_ID"), namespace=os.getenv("DATASTORE_NAMESPACE"), kind=os.getenv("DATASTORE_KIND"))
        self.semaphore = threading.Semaphore(5)  # Allow up to 5 concurrent accesses

    def replicate_distribution_system_concurrency(self, data: list, callback=None):
        """
        Uses threading to simulate concurrent processing, and executes a callback after each update.
        """
        threads = []
        for entity in data:
            thread = threading.Thread(target=self._ds_client.upsert_if_data_is_newer, args=(
                entity['entity_id'], entity['ingestion_timestamp'], entity['value'], callback))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    @staticmethod
    def completion_callback(entity_id: str, success: bool, error: str):
        if success:
            logger.info(f"Successfully processed entity {entity_id}.")
        else:
            logger.warning(f"Failed to process entity {entity_id}. Error: {error}")
