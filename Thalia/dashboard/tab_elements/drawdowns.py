import dash_html_components as html
from .elements import graph_box
import dash_table


def drawdowns_table(id):
    columns = [
        {"name": "Drawdown", "id": "Drawdown"},
        {"name": "Start", "id": "Start"},
        {"name": "End", "id": "End"},
        {"name": "Recovery", "id": "Recovery"},
        {"name": "Length", "id": "Length"},
        {"name": "Recovery Time", "id": "Recovery Time"},
        {"name": "Underwater Period", "id": "Underwater Period"},
    ]
    table = dash_table.DataTable(
        id=f"drawdowns-table-{id}",
        columns=columns,
        data=[],
        style_cell={"textAlign": "right"},
        style_as_list_view=True,
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
        ],
        style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
        style_table={"overflowX": "scroll"},
    )
    return html.Div(table, className="column is-12")


def drawdowns_dashboard():
    return html.Div(
        [
            graph_box(
                "Drawdowns",
                id="drawdowns-graph",
                size=12,
                visibility="block",
                height="600px",
            ),
            drawdowns_table(id=1),
            drawdowns_table(id=2),
            drawdowns_table(id=3),
            drawdowns_table(id=4),
            drawdowns_table(id=5),
        ],
        className="columns is-multiline",
    )
