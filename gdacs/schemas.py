from pydantic import BaseModel


class GeoJSON(BaseModel):
    type: str = "FeatureCollection"
    features: list
    bbox: list = None

    def __len__(self):
        return len(self.features)


class Feature(BaseModel):
    type: str
    properties: dict
    geometry: dict
    bbox: list
