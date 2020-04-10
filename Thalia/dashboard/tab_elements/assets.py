import dash_html_components as html
import dash_table


def table_title(portfolio_name, id):
    return html.Div(
        html.Div(
            portfolio_name,
            id=f"assets-portfolio-name-{id}",
            className="level-item title",
        ),
        className="level",
    )


def table(id, data):
    return dash_table.DataTable(
        id=f"asset-contributions-{id}",
        style_table={"width": "100%"},
        columns=[
            {"name": "AssetTicker", "id": "AssetTicker", "type": "text"},
            {"name": "Name", "id": "Name", "type": "text"},
            {"name": "Category", "id": "Category", "type": "text"},
            {"name": "Allocation", "id": "Allocation", "type": "numeric"},
        ],
        row_deletable=False,
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"},
        ],
        style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
        style_cell_conditional=[{"textAlign": "left"}],
        data=data,
    )


def asset_contributions_table_element(portfolio_name, id, data):
    return html.Div(
        [
            table_title(portfolio_name, id),
            html.Div(
                [
                    html.Div(table(id, data), className="column is-8"),
                    html.Div(className="column is-4"),
                ],
                className="columns",
            ),
        ],
        className="column is-12",
    )
