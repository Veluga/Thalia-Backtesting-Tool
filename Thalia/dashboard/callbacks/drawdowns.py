from analyse_data import analyse_data as anda


def get_drawdowns_tables(portoflio_name, drawdowns):
    drawdowns_df = anda.drawdown_summary(drawdowns)

    table_name = f"{portoflio_name} Top Drawdowns"

    no_records = 10 if 10 < len(drawdowns_df) else len(drawdowns_df)
    table_data = drawdowns_df.to_dict("records")[:no_records]

    table_visibility = {"display": "block"}

    return [table_name, table_data, table_visibility]
