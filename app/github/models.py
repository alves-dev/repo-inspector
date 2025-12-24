class Repository:
    def __init__(self, id: int, name: str, url: str, html_url: str, private: bool, updated_at: str, language: str,
                 visibility: str):
        self.id = id
        self.name = name
        self.url = url
        self.html_url = html_url
        self.private = private
        self.updated_at = updated_at
        self.language = language
        self.visibility = visibility

    @classmethod
    def from_dict(cls, data: dict):
        """Cria um objeto Repository a partir de um dicionário."""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            url=data.get('url'),
            html_url=data.get('html_url'),
            private=data.get("private"),
            updated_at=data.get("updated_at"),
            language=data.get("language", "INDEFINIDO"),
            visibility=data.get("visibility", "INDEFINIDO")
        )
