from datasets import load_dataset

from sources.agent_multi_tools.config.config_sql import ConfigTableWikitext
from sources.agent_multi_tools.infrastructure.database.postgres_databse_handler import (
    PostgresDatabaseHandler,
)
from sources.agent_multi_tools.usecases.fill_in_database import fill_in_database

if __name__ == "__main__":
    dataset = load_dataset("wikitext", "wikitext-103-v1", split="train[:2000]")
    raw_df = dataset.to_pandas()

    df_wikitset = raw_df.reset_index().rename({"index": ConfigTableWikitext.COLUMN_ID})

    database_handler = PostgresDatabaseHandler()
    fill_in_database(database_handler, df_wikitset, ConfigTableWikitext)
