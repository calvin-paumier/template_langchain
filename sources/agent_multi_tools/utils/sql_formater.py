from sources.agent_multi_tools.config.config_sql import ConfigSQL


class SQLFormater:
    @staticmethod
    def get_schema_from_config(list_config: list[ConfigSQL]) -> str:
        schema_parts = []
        for conf in list_config:
            table_name = conf.TABLE_NAME
            column_parts = []
            for column, col_type in conf.TYPE_DICT.items():
                column_parts.append(f"   - {column} : {col_type}")
            columns_str = "\n".join(column_parts)
            schema_parts.append(f"- {table_name} : \n{columns_str}")
        return "\n\n".join(schema_parts)
