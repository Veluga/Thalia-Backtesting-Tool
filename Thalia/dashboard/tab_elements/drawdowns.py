import dash_html_components as html
from .elements import graph_box
import dash_table


def drawdowns_table(id):
    columns = [
        {"name": "Rank", "id": "rank"},
        {"name": "Start", "id": "start"},
        {"name": "End", "id": "end"},
        {"name": "Length", "id": "length"},
        {"name": "Recovered by", "id": "revovered_by"},
        {"name": "Recovered Time", "id": "recovered_time"},
        {"name": "Underwater", "id": "underwater"},
        {"name": "Drawdown", "id": "drawdown"},
    ]
    return dash_table.DataTable(id=f"drawdowns-table-{id}", columns=columns, data=[])


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
