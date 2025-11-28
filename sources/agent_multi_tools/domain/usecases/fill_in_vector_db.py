from sources.agent_multi_tools.config.config_sql import ConfigSQLEmbedding
from sources.agent_multi_tools.domain.ports.database_handler import DatabaseHandler


def fill_in_vector_db(database_handler: DatabaseHandler, table_config: ConfigSQLEmbedding) -> None:
    df = database_handler.load_table(table_config.TABLE_NAME)
    database_handler.embed_documents(
        df=df,
        text_column=table_config.TEXT_TABLE_COLUMN,
        collection_name=table_config.COLLECTION_NAME,
    )
