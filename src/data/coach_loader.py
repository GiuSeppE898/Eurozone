import pandas as pd
import json

class CoachLoader:
    def __init__(self, path: str):
        self.path = path
        self.data = None

    def load(self) -> pd.DataFrame:
        self.data = pd.read_csv(self.path)
        return self.data

    def sanitize_data(self) -> pd.DataFrame:
        if self.data is None:
            raise ValueError("I dati non sono stati caricati.")
        self.data = self.data.where(pd.notnull(self.data), None)
        return self.data

    def dump_to_json(self, output_path: str) -> None:
        if self.data is None:
            raise ValueError("I dati non sono stati caricati o sanificati.")
        documento_unico = {
            "coaches": self.data.to_dict(orient="records")
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(documento_unico, f, ensure_ascii=False, indent=4)
        print(f"✅ File JSON creato: {output_path}")
