import pandas as pd
from enum import Enum

class PlayerPosition(Enum):
    DIFENSORE = "Defender"
    ATTACCANTE = "Forward"
    PORTIERE = "Goalkeeper"
    CENTROCAMPISTA = "Midfielder"
    ALTRO = "Other"
    
    @staticmethod
    def from_string(position: str) -> "PlayerPosition":
        """
        Converte una stringa in un valore di PlayerPosition.
        """
        try:
            return PlayerPosition(position.capitalize())
        except ValueError:
            raise ValueError(f"Posizione non riconosciuta: {position}")
        
class StartPosition(Enum):
    TITOLARE = "Field"
    PANCHINA = "Bench"
    
    @staticmethod
    def from_string(position: str) -> "StartPosition":
        """
        Converte una stringa in un valore di StartPosition.
        """
        try:
            return StartPosition(position.capitalize())
        except ValueError:
            raise ValueError(f"????? : {position}")

class PlayerLoader:
    """
    Carica i dati di un giocatore da un file csv.
    """
    def __init__(self, path: str):
        self.path = path
        self.data = None

    def load(self) -> pd.DataFrame:
        self.data = pd.read_csv(self.path, sep=",")
        return self.data
    
    def kowalsky(self) -> dict:
        """
        Analizza i dati e mostra le statistiche di ogni colonna.
        """
        data = self.data
        stats = {}
        for column in data.columns:
            if pd.api.types.is_numeric_dtype(data[column]):
                stats[column] = {
                    "mean": float(data[column].mean()),
                    "std": float(data[column].std()),
                    "min": float(data[column].min()),
                    "max": float(data[column].max()),
                    "count": float(data[column].count()),
                    "na_count": float(data[column].isna().sum())
                }
            else:
                stats[column] = {
                    "na_count": float(data[column].isna().sum()),
                }
                
        na_counts = data.isna().sum().sort_values(ascending=False)
            
        stats["na_counts"] = na_counts.to_dict()

        return stats
    
    def clean_data(self) -> pd.DataFrame:
        data = self.data
        
        # Rimuovo le colonne country_birth, weight, start_position_x, start_position_y, height, position_field_detailed
        columns_to_drop = [
            "country_birth", "weight", "start_position_x", 
            "start_position_y", "height", "position_field_detailed"
        ]
        cleaned_data = data.drop(columns=columns_to_drop, errors='ignore')
        
        self.data = cleaned_data
        
        return data
    
    def sanitize_data(self) -> pd.DataFrame:
        sanitized_data = self.data
                
        # Trasformo i valori nulli della colonna id_club in -1
        if 'id_club' in sanitized_data.columns:
            sanitized_data['id_club'] = sanitized_data['id_club'].fillna(-1).astype(int)
        
        # Trasformo tutti i valori della colonna id_club in interi
        if 'id_club' in sanitized_data.columns:
            sanitized_data['id_club'] = sanitized_data['id_club'].astype(int)
            
        # Trasformo i valori nulli della colonna id_player in -1
        if 'id_player' in sanitized_data.columns:
            sanitized_data['id_player'] = sanitized_data['id_player'].fillna(-1).astype(int)

        # Trasformo tutti i valori della colonna id_player in interi
        if 'id_player' in sanitized_data.columns:
            sanitized_data['id_player'] = sanitized_data['id_player'].astype(int)
            
        # Trasformo i valori nulli della colonna position_national in "Other"
        if 'position_national' in sanitized_data.columns:
            sanitized_data['position_national'] = sanitized_data['position_national'].fillna("Other")
            sanitized_data['position_national'] = sanitized_data['position_national'].apply(
                lambda x: PlayerPosition.from_string(x).value if isinstance(x, str) else "Other"
            )
        
        # Trasformo i valori nulli della colonna position_field in "Other"
        if 'position_field' in sanitized_data.columns:
            sanitized_data['position_field'] = sanitized_data['position_field'].fillna("Other")
            sanitized_data['position_field'] = sanitized_data['position_field'].apply(
                lambda x: PlayerPosition.from_string(x).value if isinstance(x, str) else "Other"
            )

        # Trasformo i valori della colonna start in Field o Bench
        if 'start' in sanitized_data.columns:
            sanitized_data['start'] = sanitized_data['start'].apply(
                lambda x: StartPosition.from_string(x).value if isinstance(x, str) else StartPosition.BENCH.value
            )
        
        # Nei valori in cui name_shirt è nullo, lo sostituisco con il nome del giocatore
        if 'name_shirt' in sanitized_data.columns:
            sanitized_data['name_shirt'] = sanitized_data.apply(
                lambda row: row['name'] if pd.isna(row['name_shirt']) and isinstance(row['name'], str) else row['name_shirt'], axis=1
            )
            
        # Rimuovo i giocatori che hanno birth_date nullo (dato che sono 3)
        if 'birth_date' in sanitized_data.columns:
            sanitized_data = sanitized_data[sanitized_data['birth_date'].notna()]
            
        # Trasformo i valori nulli della colonna id_national_team in -1
        if 'id_national_team' in sanitized_data.columns:
            sanitized_data['id_national_team'] = sanitized_data['id_national_team'].fillna(-1).astype(int)

        # Trasformo i valori nulli della colonna country_code in "Unknown"
        if 'country_code' in sanitized_data.columns:
            sanitized_data['country_code'] = sanitized_data['country_code'].fillna("Unknown")
            
        self.data = sanitized_data
        return sanitized_data
    
    def dump_to_json(self, path: str) -> None:
        """
        Salva i dati in un file json.
        """
        if self.data is not None:
            self.data.to_json(path, orient='records', lines=True)
        else:
            raise ValueError("Data è None")
