import pathlib

APPROVED_SEUQUENCE_1_ID = 2610101
APPROVED_SEUQUENCE_2_ID = 2614361
APPROVED_SEUQUENCE_3_ID = 2614384
APPROVED_SEUQUENCE_4_ID = 2614399
APPROVED_SEUQUENCE_5_ID = 2614410

APPROVED_SEUQUENCE_EMAIL_1_ID = 9348296
APPROVED_SEUQUENCE_EMAIL_2_ID = 9362853
APPROVED_SEUQUENCE_EMAIL_3_ID = 9362951
APPROVED_SEUQUENCE_EMAIL_4_ID = 9363004
APPROVED_SEUQUENCE_EMAIL_5_ID = 9363055


FOMO_SEQUENCE_ID = 2612710
FOMO_SEQUENCE_EMAIL_1_ID = 9357348
FOMO_SEQUENCE_EMAIL_2_ID = 9357349
FOMO_SEQUENCE_EMAIL_3_ID = 9357350
FOMO_SEQUENCE_EMAIL_4_ID = 9357351
FOMO_SEQUENCE_EMAIL_5_ID = 9357352
FOMO_SEQUENCE_EMAIL_6_ID = 9357353
FOMO_SEQUENCE_EMAIL_7_ID = 9357354




def get_kit_cookies():
    BASE_DIR = pathlib.Path(__file__).parent.parent

    with open(BASE_DIR.joinpath("cookies.txt"), "r") as f:
        content = f.read()

    return content

REQUESTS_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': "en-SG,en;q=0.9",
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0',
    'Cookie': get_kit_cookies()
}

