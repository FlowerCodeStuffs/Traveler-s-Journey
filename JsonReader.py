from json import dump, load, JSONDecodeError
from typing import Any

class JsonReader:
    @staticmethod
    def LoadJson(file: str) -> dict[str, Any]:
        try:
            with open(file, 'r') as f:
                return load(f)
        except FileNotFoundError:
            return { "ERROR": "File Doesnt Exist." }
        except JSONDecodeError:
            return {"ERROR": "Invalid JSON format."}
    
    @staticmethod
    def OverrideJson(file, Data: dict[str, Any]) -> None:
        with open(file, 'w', encoding="utf-8") as f:
            dump(Data, f, indent=4)
    