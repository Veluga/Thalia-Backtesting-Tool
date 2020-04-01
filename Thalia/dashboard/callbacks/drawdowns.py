from analyse_data import analyse_data as anda


def get_drawdowns_tables(total_returns):
    drawdowns = anda.drawdowns(total_returns)
    drawdowns_summary = anda.drawdown_summary(drawdowns)
