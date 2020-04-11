import dash_table


def asset_contributions_table(id):
    return dash_table.DataTable(
        id=f"asset-contributions-{id}",
        style_table={"width": "100%",},
        css=[{"selector": f"asset-contributions-{id}", "rule": "width: 100%;"}],
        columns=[
            {"name": "AssetTicker", "id": "AssetTicker", "type": "text"},
            {"name": "Name", "id": "Name", "type": "text"},
            {"name": "Category", "id": "Category", "type": "text"},
            {"name": "Allocation", "id": "Allocation", "type": "numeric"},
            {"name": "Contribution", "id": "Contribution", "type": "numeric"},
        ],
        row_deletable=False,
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)",},
        ],
        style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold",},
        style_cell_conditional=[{"textAlign": "left"}],
    )
