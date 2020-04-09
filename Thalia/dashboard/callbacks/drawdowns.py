from analyse_data import analyse_data as anda
import humanize


def get_drawdowns_tables(portoflio_name, drawdowns):
    drawdowns_df = anda.drawdown_summary(drawdowns)

    table_name = f"{portoflio_name} Top Drawdowns"

    no_records = 10 if 10 < len(drawdowns_df) else len(drawdowns_df)
    table_data = drawdowns_df.to_dict("records")[:no_records]

    table_visibility = {"display": "block"}

    return [table_name, table_data, table_visibility]


def format_summary(drawdowns):
    drawdowns = drawdowns.head(10)
    return drawdowns.apply(format_row, axis=1, result_type="broadcast")


def format_row(row):
    return [
        round(row["Drawdown"], 2),
        row["Start"].strftime("%d/%m/%Y"),
        row["End"].strftime("%d/%m/%Y"),
        row["Recovery"].strftime("%d/%m/%Y"),
        humanize.naturaldelta(row["Length"]),
        humanize.naturaldelta(row["Recovery Time"]),
        humanize.naturaldelta(row["Underwater Period"]),
    ]
