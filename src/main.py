from core.concurrency import ConcurrencyManager
from utils.helpers import load_json_file
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
dummy_data_dir = "data/dummy_datastore_entities.json"


def main():
    data = load_json_file(dummy_data_dir)
    if data:
        concurrency_manager = ConcurrencyManager()
        concurrency_manager.thread_data_to_datastore(data)


if __name__ == '__main__':
    main()
