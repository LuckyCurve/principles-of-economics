import hsi.monthly_change
import nasdaq.calculate_pe
import nasdaq.monthly_change
import sp500.calculate_pe
import sp500.monthly_change


def get_market_data():
    sp500.monthly_change.main()
    nasdaq.monthly_change.main()
    hsi.monthly_change.main()


def get_market_pe_data():
    sp500.calculate_pe.main()
    nasdaq.calculate_pe.main()


if __name__ == "__main__":
    get_market_data()
    get_market_pe_data()
