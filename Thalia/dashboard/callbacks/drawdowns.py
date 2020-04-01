from analyse_data import analyse_data as anda


def get_drawdowns_tables(total_returns):
    drawdowns = anda.drawdowns(total_returns)
    drawdowns_df = anda.drawdown_summary(drawdowns)

    table_data = drawdowns_df.to_dict("records")[:10]
    table_visibility = {"display": "block"}

    return [table_data, table_visibility]
