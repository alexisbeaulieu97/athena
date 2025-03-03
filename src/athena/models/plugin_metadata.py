from athena.models import BaseModel


class PluginMetadata(BaseModel):
    name: str
    description: str
