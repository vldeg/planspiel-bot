import os
from dotenv import load_dotenv

load_dotenv()

PORTFOLIO_ID = os.getenv("PORTFOLIO_ID")

sp500_tickers = [
    "A", "AAPL", "ABBV", "ABNB", "ABT", "ACGL", "ACN", "ADBE", "ADI", "ADM",
    "ADP", "ADSK", "AEE", "AEP", "AES", "AFL", "AIG", "AIZ", "AJG", "AKAM",
    "ALB", "ALGN", "ALLE", "ALL", "AMAT", "AMCR", "AMD", "AME", "AMGN", "AMP",
    "AMT", "AMZN", "ANET", "AON", "AOS", "APA", "APD", "APH", "APO", "APP",
    "APTV", "ARE", "ARES", "ATO", "AVGO", "AVY", "AWK", "AXP", "AXON", "AZO",
    "BA", "BAC", "BALL", "BAX", "BBY", "BDX", "BE", "BEN", "BF-B", "BG",
    "BIIB", "BKNG", "BLK", "BMY", "BNY", "BR", "BRK-B", "BRO", "BSX",
    "BXP", "C", "CAG", "CAH", "CARR", "CAT", "CASY", "CB", "CBOE", "CBRE",
    "CCI", "CCL", "CDNS", "CDW", "CEG", "CF", "CFG", "CHD", "CHRW", "CHTR",
    "CI", "CIEN", "CINF", "CL", "CLX", "CMA", "CMCSA", "CME", "CMG", "CMI",
    "CMS", "CNC", "CNP", "COF", "COHR", "COIN", "COP", "COR", "COST", "CPAY",
    "CPB", "CPRT", "CRH", "CRL", "CRM", "CRWD", "CSCO", "CSGP", "CSX", "CTAS",
    "CTSH", "CTVA", "CVNA", "CVS", "CVX", "D", "DAL", "DASH", "DD", "DDOG",
    "DE", "DECK", "DELL", "DG", "DGX", "DHI", "DHR", "DIS", "DLR", "DLTR",
    "DOC", "DOV", "DOW", "DPZ", "DRI", "DTE", "DUK", "DVN", "DXCM", "EA",
    "EBAY", "ECHO", "ECL", "ED", "EFX", "EG", "EIX", "EL", "ELV", "EME",
    "EMR", "EOG", "EPAM", "EQIX", "EQR", "EQT", "ERIE", "ES", "ESS", "ETN",
    "ETR", "EVRG", "EW", "EXC", "EXE", "EXPD", "EXPE", "EXR", "F", "FANG",
    "FAST", "FBIN", "FCX", "FDX", "FDXF", "FE", "FERG", "FFIV", "FICO", "FIS",
    "FISV", "FITB", "FLEX", "FLS", "FMC", "FOX", "FOXA", "FRT", "FSLR", "FTNT",
    "FTV", "GD", "GDDY", "GE", "GEHC", "GEN", "GEV", "GILD", "GIS", "GL",
    "GLW", "GM", "GNRC", "GOOG", "GOOGL", "GPC", "GPN", "GRMN", "GS", "GWW",
    "HAL", "HAS", "HBAN", "HCA", "HD", "HIG", "HII", "HLT", "HON",
    "HONA", "HOOD", "HPQ", "HRL", "HSIC", "HST", "HSY", "HUBB", "HUM", "HWM",
    "IBM", "IBKR", "ICE", "IEX", "IFF", "ILMN", "INCY", "INTC", "INTU", "INVH",
    "IP", "IQV", "IR", "IRM", "ISRG", "IT", "ITW", "IVZ", "J", "JBHT",
    "JBL", "JCI", "JKHY", "JNJ", "JPM", "KDP", "KEY", "KEYS", "KHC",
    "KIM", "KKR", "KLAC", "KMB", "KMI", "KO", "KR", "L", "LDOS", "LEN",
    "LH", "LHX", "LII", "LIN", "LITE", "LLY", "LMT", "LOW", "LULU", "LUV",
    "LYB", "LYV", "MA", "MAA", "MAR", "MAS", "MCD", "MCHP", "MCK", "MCO",
    "MDLZ", "MDT", "MET", "META", "MGM", "MKC", "MLM", "MMM", "MNST",
    "MO", "MOS", "MPC", "MPWR", "MRK", "MRNA", "MRSH", "MS", "MSCI", "MSFT",
    "MSI", "MTB", "MTD", "MU", "NCLH", "NDAQ", "NDSN", "NEE", "NEM", "NFLX",
    "NI", "NKE", "NOC", "NOW", "NRG", "NSC", "NTAP", "NTRS", "NUE", "NVDA",
    "NVR", "NWS", "NWSA", "NXPI", "O", "ODFL", "OKE", "OKTA", "OMC", "ON",
    "ORCL", "ORLY", "OTIS", "OXY", "P", "PANW", "PAYX", "PCAR", "PCG", "PEG",
    "PEP", "PFE", "PFG", "PG", "PGR", "PH", "PHM", "PKG", "PLD", "PLTR",
    "PM", "PNC", "PNR", "PNW", "POOL", "PPG", "PPL", "PRU", "PSA", "PSKY",
    "PSX", "PTC", "PWR", "PYPL", "Q", "QCOM", "RCL", "RDDT", "REG", "REGN",
    "RF", "RJF", "RL", "RMD", "ROK", "ROL", "ROP", "ROST", "RSG", "RTX",
    "RVTY", "SATS", "SBAC", "SBUX", "SCHW", "SHW", "SJM", "SLB", "SMCI",
    "SNA", "SNPS", "SO", "SOLV", "SPG", "SPGI", "STLD", "STT", "STX", "STZ",
    "SW", "SWK", "SWKS", "SYF", "SYK", "SYY", "T", "TAP", "TDG", "TDY",
    "TECH", "TEL", "TER", "TFC", "TGT", "TJX", "TMO", "TMUS", "TPL", "TPR",
    "TRGP", "TRMB", "TROW", "TRV", "TSCO", "TSLA", "TSN", "TT", "TTWO",
    "TXN", "TXT", "TYL", "UAL", "UBER", "UDR", "ULTA", "UNH", "UNP", "UPS",
    "URI", "USB", "V", "VEEV", "VICI", "VLTO", "VMC", "VRSK", "VRSN", "VRTX",
    "VST", "VTR", "VTRS", "VZ", "WAB", "WAT", "WDAY", "WDC", "WEC", "WELL",
    "WM", "WMB", "WMT", "WRB", "WSM", "WTW", "WY", "XEL", "XOM", "XYL",
    "YUM", "ZBH", "ZBRA", "ZTS"
]
nasdaq100_tickers = [
    "AAPL", "ABNB", "ADBE", "ADI", "ADP",
    "ADSK", "AEP", "ALAB", "ALNY", "AMAT",
    "AMD", "AMGN", "AMZN", "APP", "ARM",
    "ASML", "AVGO", "AXON", "BKNG", "BKR",
    "CCEP", "CDNS", "CEG", "CHTR", "CMCSA",
    "COST", "CPRT", "CRWD", "CRWV", "CSCO",
    "CSX", "CTAS", "DASH", "DDOG", "DXCM",
    "EXC", "FANG", "FAST", "FER", "FTNT",
    "GEHC", "GILD", "GOOG", "GOOGL", "HON",
    "IDXX", "INTC", "INTU", "ISRG", "KDP",
    "KHC", "KLAC", "LIN", "LRCX", "LULU",
    "MAR", "MCHP", "MDLZ", "MELI", "META",
    "MNST", "MPWR", "MRVL", "MSFT", "MSTR",
    "MU", "NFLX", "NVDA", "NXPI", "ODFL",
    "ON", "ORLY", "PANW", "PAYX", "PCAR",
    "PDD", "PEP", "PLTR", "PYPL", "QCOM",
    "REGN", "ROP", "ROST", "SBUX", "SHOP",
    "SNPS", "TEAM", "TMUS", "TSLA", "TTD",
    "TTWO", "TXN", "VRSK", "VRTX", "WBD",
    "WDAY", "XEL", "ZS"
]

TICKERS = sorted(set(sp500_tickers + nasdaq100_tickers))

MIN_CASH_RESERVE = 10000
RISK_PER_TRADE = 0.01
ATR_FACTOR = 0.15

FEE_PERCENTAGE = 0.003
MIN_FEE = 15.0

API_BASE_URL = os.getenv("API_BASE_URL")
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")
