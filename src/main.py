from dotenv import load_dotenv

from core.concurrency import ConcurrencyManager
from utils.helpers import load_json_file

# Load the .env file
load_dotenv()
dummy_data_dir = "../data/dummy_datastore_entities.json"


def main():
    data = load_json_file(dummy_data_dir)
    if data:
        concurrency_manager = ConcurrencyManager()
        concurrency_manager.replicate_distribution_system_concurrency(data, concurrency_manager.completion_callback)


if __name__ == '__main__':
    main()
