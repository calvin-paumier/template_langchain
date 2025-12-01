import pandas as pd

from sources.agent_multi_tools.config.config_sql import ConfigSQL
from sources.agent_multi_tools.ports.database_handler import DatabaseHandler


def fill_in_database(database_handler: DatabaseHandler, df: pd.DataFrame, table_config: ConfigSQL) -> None:
    engine = database_handler.get_engine()
    df.to_sql(table_config.TABLE_NAME, engine, if_exists="replace", index=False)
