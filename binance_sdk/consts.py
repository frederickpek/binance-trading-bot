# API URL
SPOT_URL = "https://api.binance.com"
USDT_M_URL = "https://fapi.binance.com"
COIN_M_URL = "https://dapi.binance.com"
API_URL = "https://www.binance.com"
OPTION_URL = "https://vapi.binance.com"

# USDT-M market
FAPI_PING = "/fapi/v1/ping"
FAPI_TIME = "/fapi/v1/time"
FAPI_EXCHANGE_INFO = "/fapi/v1/exchangeInfo"
FAPI_DEPTH = "/fapi/v1/depth"
FAPI_TRADES = "/fapi/v1/trades"
FAPI_HISTORICAL_TRADES = "/fapi/v1/historicalTrades"

REST_SPOT_HISTORICAL_TRADE = "/api/v3/historicalTrades"

FAPI_AGGTRADE = "/fapi/v1/aggTrades"
FAPI_KLINES = "/fapi/v1/klines"
FAPI_CONT_KLINES = "/fapi/v1/continuousKlines"
FAPI_INDEX_KLINES = "/fapi/v1/indexPriceKlines"
FAPI_MARK_KLINES = "/fapi/v1/markPriceKlines"
FAPI_PREMIUM_INDEX = "/fapi/v1/premiumIndex"
FAPI_FUNDING_RATE = "/fapi/v1/fundingRate"
FAPI_TICKER_24H = "/fapi/v1/ticker/24hr"
FAPI_TICKER_PRICE = "/fapi/v1/ticker/price"
FAPI_BOOK_TICKER = "/fapi/v1/ticker/bookTicker"
FAPI_OPEN_INTEREST = "/futures/data/openInterestHist"
FAPI_TOP_LONG_SHORT_ACCT = "/futures/data/topLongShortAccountRatio"
FAPI_TOP_LONG_SHORT_POSN = "/futures/data/topLongShortPositionRatio"
FAPI_GLOBAL_LONG_SHORT_ACCT = "/futures/data/globalLongShortAccountRatio"
FAPI_TAKER_LONG_SHORT = "/futures/data/takerlongshortRatio"
FAPI_LVT_KLINES = "/fapi/v1/lvtKlines"
FAPI_INDEX_INFO = "/fapi/v1/indexInfo"

# Alternative data
BAPI_DUAL_INVESTMENT = "/bapi/earn/v4/friendly/pos/dc/project/list"  # DCD
BAPI_DUAL_INVESTMENT_UNDERLYINGS = (
    "/bapi/earn/v1/friendly/pos/dc/project/overview"  # DCD UNDERLYINGS
)
BAPI_ANNOUNCEMENT = (
    "/bapi/composite/v1/public/cms/article/list/query"  # All binance announcement
)
BAPI_ARTICLE = "/bapi/composite/v1/public/cms/article/all/query"  # All binance article for filtering keywords

SPOT = "SPOT"
SWAP = "PERPETUAL"
FUTURE = "FUTURE"

SPOT_API = "SAPI"
LINEAR_API = "FAPI"
INVERT_API = "DAPI"

EXCH_PERP = "PERP"

REST_ACCT_STATUS_PATH = "/sapi/v1/account/status"
SAPI_TIME_PATH = "/api/v3/time"
FAPI_TIME_PATH = "/fapi/v1/time"
DAPI_TIME_PATH = "/dapi/v1/time"

TIMESTAMP_KEY = "timestamp"
PAYLOAD_KEY = "payload"

RECV_WINDOW_KEY = "recvWindow"
RECV_WINDOW = "5000"

WS_SUB_BOOK = "%s@depth@100ms"

WS_SUB_TICKER = "%s@miniTicker"

WS_SUB_QUOTE_ARG_TEMPLATE = "%s@bookTicker"
WS_SUB_TRADE_ARG_TEMPLATE = "%s@trade"

WS_SUB_MARK_PRICE_ARG_TEMPLATE = "%s@markPrice@1s"
WS_SUB_INDEX_PRICE_ARG_TEMPLATE = "%s@indexPrice@1s"

REST_ALL_LINEAR_DERIV_INST = "/fapi/v1/exchangeInfo"
REST_LINEAR_ORDER = "/fapi/v1/order"
REST_LINEAR_ORDER_TEST = "/fapi/v1/order/test"
REST_LINEAR_OPEN_ORDERS = "/fapi/v1/openOrders"
REST_LINEAR_CANCEL_OPEN_ORDERS = "/fapi/v1/allOpenOrders"
REST_LINEAR_USER_TRADES = "/fapi/v1/userTrades"

REST_LINEAR_ACCOUNT = "/fapi/v2/account"
REST_LINEAR_BALANCE = "/fapi/v2/balance"
REST_LINEAR_POSN_MODE = "/fapi/v1/positionSide/dual"
REST_LINEAR_POSN_RISK = "/fapi/v2/positionRisk"
REST_LINEAR_ACCT_POS = "/fapi/v2/account"
REST_LINEAR_TRADE_FEE = "/fapi/v1/commissionRate"
REST_LINEAR_LEVERAGE = "/fapi/v1/leverage"
REST_LINEAR_SYMBOL_CONFIG = "/fapi/v1/symbolConfig"
REST_LINEAR_TICKER_PRICE = "/fapi/v2/ticker/price"
REST_LINEAR_KLINES = "/fapi/v1/klines"
REST_LINEAR_POSN_RISK_V3 = "/fapi/v3/positionRisk"

REST_ALL_INVERT_DERIV_INST = "/dapi/v1/exchangeInfo"
REST_INVERT_ORDER = "/dapi/v1/order"
REST_INVERT_OPEN_ORDERS = "/dapi/v1/openOrders"
REST_INVERT_CANCEL_OPEN_ORDERS = "/dapi/v1/allOpenOrders"
REST_INVERT_USER_TRADES = "/dapi/v1/userTrades"
REST_INVERT_POSN_MODE = "/dapi/v1/positionSide/dual"
REST_INVERT_BALANCE = "/dapi/v1/balance"
REST_INVERT_ACCT_POS = "/dapi/v1/account"
REST_INVERT_POSN_RISK = "/dapi/v2/positionRisk"
REST_INVERT_TRADE_FEE = "/dapi/v1/commissionRate"
REST_INVERT_LEVERAGE = "/dapi/v1/leverage"

REST_SPOT_MGN_OPEN_ORDERS = "/sapi/v1/margin/openOrders"

REST_FUNDING_ACCOUNT = "/sapi/v1/asset/get-funding-asset"
REST_FUNDING_TRANSFER_HIST = "/sapi/v1/asset/transfer"
REST_FUNDING_DEPO_HIST = "/sapi/v1/capital/deposit/hisrec"
REST_FUNDING_WITH_HIST = "/sapi/v1/capital/withdraw/history"
REST_FUNDING_WITH = "/sapi/v1/capital/withdraw/apply"
REST_SUB_TRANS_HIST = "/sapi/v1/sub-account/transfer/subUserHistory"
REST_PARENT_TRANS_HIST = "/sapi/v1/sub-account/universalTransfer"
REST_TRADE_FEE = "/sapi/v1/asset/tradeFee"
REST_MGMT_SUB_TRANS = "/sapi/v1/managed-subaccount/query-trans-log"
REST_API_RESTRICTIONS = "/sapi/v1/account/apiRestrictions"

REST_ALL_SPOT_INST = "/api/v3/exchangeInfo"
REST_SPOT_ACCOUNT = "/api/v3/account"
REST_SPOT_MGN_ACCOUNT = "/sapi/v1/margin/account"

REST_SPOT_TICKER = "/api/v3/ticker/24hr?symbol=%s"
REST_ALL_SPOT_TICKER = "/api/v3/ticker/24hr"
REST_SPOT_ALL_TICKER = "/api/v3/ticker/price"
REST_SWAP_TICKER = "/fapi/v1/ticker/24hr?symbol=%s"
REST_ALL_SWAP_TICKER = "/fapi/v1/ticker/24hr"
REST_ALL_LINEAR_24HR = "/fapi/v1/ticker/24hr"
REST_ALL_INVERT_24HR = "/dapi/v1/ticker/24hr"

REST_SPOT_QUOTE = "/api/v3/ticker/bookTicker?symbol=%s"
REST_SWAP_QUOTE = "/fapi/v1/ticker/bookTicker?symbol=%s"

REST_SPOT_DEPTH = "/api/v3/depth?symbol=%s&limit=%s"
REST_LINEAR_DERIV_DEPTH = "/fapi/v1/depth?symbol=%s&limit=%s"
REST_INVERT_DERIV_DEPTH = "/dapi/v1/depth?symbol=%s&limit=%s"

REST_SPOT_AGGTRADES = "/api/v3/aggTrades?symbol=%s&startTime=%s&endTime=%&limit=%s"
REST_SWAP_AGGTRADES = "/fapi/v1/aggTrades?symbol=%s&startTime=%s&endTime=%&limit=%s"

REST_SPOT_TRADES = "/api/v3/trades?symbol=%s&limit=%s"
REST_SWAP_TRADES = "/fapi/v1/trades?symbol=%s&limit=%s"

REST_SPOT_KLINES = (
    "/api/v3/klines?symbol=%s&interval=%s&startTime=%s&endTime=%s&limit=%s"
)
REST_SWAP_KLINES = (
    "/fapi/v1/klines?symbol=%s&interval=%s&startTime=%s&endTime=%s&limit=%s"
)

X_MBX_APIKEY = "X-MBX-APIKEY"
CONTENT_TYPE_NAME = "Content-Type"
CONTENT_TYPE_VALUE = "application/x-www-form-urlencoded"
SWAP_SUFFIX = "-SWAP"
PERP_SUFFIX = "_PERP"
COIN_INVERT_SWAP = "CoinInvertSWAP"
COIN_SWAP = "SWAP"

REST_SPOT_LISTEN_KEY = "/api/v3/userDataStream"
REST_MGN_SPOT_LISTEN_KEY = "/sapi/v1/userDataStream"
REST_LINEAR_DERIV_LISTEN_KEY = "/fapi/v1/listenKey"
REST_INVERT_DERIV_LISTEN_KEY = "/dapi/v1/listenKey"

REST_SPOT_ACCT = "/api/v3/account"

REST_SPOT_ORDER = "/api/v3/order"
REST_SPOT_ORDER_TEST = "/api/v3/order/test"
REST_SPOT_OPEN_ORDERS = "/api/v3/openOrders"
REST_SPOT_ALL_ORDERS = "/api/v3/allOrders"
REST_SPOT_USER_TRADES = "/api/v3/myTrades"

ORD_CLI_ORD_ID = "newClientOrderId"
ORD_ORIG_CLI_ORD_ID = "origClientOrderId"
ORD_EXCH_ORD_ID = "orderId"
ORD_TIME_IN_FORCE = "timeInForce"
ORD_INST_ID = "symbol"
ORD_SIDE = "side"
ORD_PRICE = "price"
ORD_SIZE = "quantity"
ORD_TYPE = "type"
ORD_RESP_TYPE = "newOrderRespType"

PRICE_INDEX = 0
QTY_INDEX = 1

WS_SUB_PUBLIC_METHOD = "SUBSCRIBE"
WS_UNSUB_PUBLIC_METHOD = "UNSUBSCRIBE"
WS_LISTSUB_PUBLIC_METHOD = "LIST_SUBSCRIPTIONS"

# Market Data (v3)
MRT_DATA_24HR_TICK = "/api/v3/ticker/24hr"

# Options
LATEST_MARK_PRICE = "/vapi/v1/mark"

LINEAR_MARK_PRICE = "/fapi/v1/premiumIndex"
INVERT_MARK_PRICE = "/dapi/v1/premiumIndex"

LINEAR_MULTI_ASSET_MARGIN = "/fapi/v1/multiAssetsMargin"
INVERT_TICKER_PRICE = "/dapi/v1/ticker/price"
INVERT_24HR_TICKER = "/dapi/v1/ticker/24hr"
INVERT_BOOK_TICKER = "/dapi/v1/ticker/bookTicker"

# sub to sub
REST_SUB_TO_SUB = "/sapi/v1/sub-account/transfer/subToSub"

# managed subaccount
REST_DEPOSIT_MANAGED_SUB = "/sapi/v1/managed-subaccount/deposit"
REST_WITHDRAW_MANAGED_SUB = "/sapi/v1/managed-subaccount/withdraw"
REST_MANAGED_SUB_LIST = "/sapi/v1/managed-subaccount/info"
