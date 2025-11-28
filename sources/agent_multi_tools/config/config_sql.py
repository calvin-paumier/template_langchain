class ConfigSQL:
    TABLE_NAME: str
    TYPE_DICT: dict[str, str]


class ConfigSQLEmbedding:
    TABLE_NAME: str
    COLLECTION_NAME: str
    TEXT_TABLE_COLUMN: str


class ConfigTableWikitext(ConfigSQL):
    TABLE_NAME = "wikitext"
    COLUMN_ID = "id"
    COLUMN_TEXT = "text"

    TYPE_DICT = {
        COLUMN_ID: "INTEGER",
        COLUMN_TEXT: "TEXT",
    }


class ConfigEmbeddingWikitext(ConfigSQLEmbedding):
    TABLE_NAME = ConfigTableWikitext.TABLE_NAME
    COLLECTION_NAME = "wikitext_embedding"
    TEXT_TABLE_COLUMN = ConfigTableWikitext.COLUMN_TEXT


class ConfigSanrioData(ConfigSQL):
    TABLE_NAME = "sanrio_characters"
    COLUMN_ID = "id"
    COLUMN_NAME = "name"
    COLUMN_AGE = "age"
    COLUMN_CITY = "city"

    TYPE_DICT = {
        COLUMN_ID: "INTEGER",
        COLUMN_NAME: "TEXT",
        COLUMN_AGE: "INTEGER",
        COLUMN_CITY: "TEXT",
    }
