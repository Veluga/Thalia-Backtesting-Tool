import dash_html_components as html
from .elements import box, graph_box


def summary_dashboard():
    return html.Div(
        [
            box(
                ["Top Seller Total", "Sales", "Overall", "Sales %"],
                [56950, 250000, 750000, 25],
            ),
            box(
                ["Top Seller Total", "Sales", "Overall", "Sales %"],
                [56950, 250000, 750000, 25],
            ),
            box(
                ["Top Seller Total", "Sales", "Overall", "Sales %"],
                [56950, 250000, 750000, 25],
            ),
            graph_box("Overall Graph", figure={}, id="graph", size=12),
            graph_box("Another Graph", figure={}, id="graph2", size=6),
            graph_box("More Graphs", figure={}, id="graph3", size=6),
        ],
        className="columns is-multiline",
    )
