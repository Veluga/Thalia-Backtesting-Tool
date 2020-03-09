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
            graph_box("Graph1", figure={}, id="graph-1", size=6),
            graph_box("Graph2", figure={}, id="graph-2", size=6),
            graph_box("Graph3", figure={}, id="graph-3", size=6),
            graph_box("Graph4", figure={}, id="graph-4", size=6),
            graph_box("Graph5", figure={}, id="graph-5", size=6),
        ],
        className="columns is-multiline",
    )
