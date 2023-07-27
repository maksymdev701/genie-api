from pymongo import MongoClient, ASCENDING
from config import settings

client = MongoClient(settings.DATABASE_URL, serverSelectionTimeoutMS=5000)

try:
    conn = client.server_info()
    print(f'Connected to MongoDB {conn.get("version")}')
except Exception:
    print("Unable to connect MongoDB Server.")

db = client[settings.MONGO_INITDB_DATABASE]

Settings = db.settings


def initialize_settings():
    Settings.delete_many({})

    # Initialize Product Configuration
    Settings.insert_one(
        {
            "type": "product",
            "name": "CodeGenie",
            "modules": [
                {
                    "name": "Any Code",
                    "description": "",
                    "source_labels": [
                        {"text": "Text", "checked": True},
                        {"text": "Image", "checked": True},
                        {"text": "URL", "checked": True},
                    ],
                    "input_box": {"label": "Current Code", "description": ""},
                    "export_options": [
                        {"text": "MS Word", "checked": True},
                        {"text": "PDF", "checked": True},
                        {"text": "Text", "checked": True},
                    ],
                },
                {
                    "name": "Smart Contract",
                    "description": "",
                    "source_labels": [
                        {"text": "Text", "checked": True},
                        {"text": "Image", "checked": True},
                        {"text": "URL", "checked": True},
                    ],
                    "input_box": {"label": "Current Code", "description": ""},
                    "export_options": [
                        {"text": "MS Word", "checked": True},
                        {"text": "PDF", "checked": True},
                        {"text": "Text", "checked": True},
                    ],
                },
                {
                    "name": "API Documentation",
                    "description": "",
                    "source_labels": [
                        {"text": "Text", "checked": True},
                        {"text": "Image", "checked": True},
                        {"text": "URL", "checked": True},
                    ],
                    "input_box": {"label": "Current Code", "description": ""},
                    "export_options": [
                        {"text": "MS Word", "checked": True},
                        {"text": "PDF", "checked": True},
                        {"text": "Text", "checked": True},
                    ],
                },
            ],
        }
    )

    # Initialize Price Configuration
    Settings.insert_one(
        {
            "type": "price",
            "plans": [
                {
                    "name": "Free",
                    "total_wishes": 1,
                    "price": 0,
                    "period": "Monthly",
                }
            ],
        }
    )

    Settings.insert_one(
        {
            "type": "api",
            "language": "New API",
            "authentication": None,
            "shared_headers": [],
            "shared_parameters": [],
        }
    )


# initialize_settings()
