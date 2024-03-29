# -*- coding: utf-8 -*-

ARABIC_CHARS = "دجحإﻹﻷأآﻵخهعغفقثصضذطكمنتالبيسشظزوةىﻻرؤءئ"
HARAKAT_MAIN = [
    "\u064b",  # Fathatan
    "\u064c",  # Dammatan
    "\u064d",  # Kasratan
    "\u064e",  # Fatha
    "\u064f",  # Damma
    "\u0650",  # Kasra
    "\u0651",  # Shadda
    "\u0652",  # Sukun
]
TANWEEN = HARAKAT_MAIN[0]
ALEF_CHARS = "إأٱآا" + "\u0670"  # Arabic Letter Superscript Alef
NORMAL_ALEF = "ا"
TAH_MARBOTA = "ة"
HA = "ه"
ALEF_MAKSORA = "ى"
YA = "ي"
HAMZA_CHARS = "ءؤئ" + "\u0655\u0656"  # Arabic Hamza Above and Below
NORMAL_HAMZA = "ء"
LAM_ALEF_COMBINED = [
    "\ufefb",  # Lam Alef
    "\ufef7",  # Lam Alef Hamza Above
    "\ufef9",  # Lam Alef Hamza Below
    "\ufef5",  # Lam Alef Madda Above
]
LAM_ALEF_NORMAL = "\u0644\u0627"  # ﻻ
HARAKAT_OTHERS = [
    "\u0653",  # Arabic Maddah Above
    "\u0654",  # Arabic Hamza Above
    "\u0655",  # Arabic Hamza Below
    "\u0656",  # Arabic Subscript Alef
    "\u0657",  # Arabic Inverted Damma
    "\u0658",  # Arabic Mark Noon Ghunna
    "\u0659",  # Arabic Zwarakay
    "\u065A",  # Arabic Vowel Sign Small V Above
    "\u065B",  # Arabic Vowel Sign Inverted Small V Above
    "\u065C",  # Arabic Vowel Sign Dot Below
    "\u065D",  # Arabic Reversed Damma
    "\u065E",  # Arabic Fatha With Two Dots
    "\u065F",  # Arabic Wavy Hamza Below
    "\u0670",  # Arabic Letter Superscript Alef
]
HARAKAT = HARAKAT_MAIN + HARAKAT_OTHERS
TATWEEL = "\u0640"  # ـ

QURANIC_ANNOTATION = [
    "\u0615",  # Arabic Small High Tah
    "\u0616",  # Arabic Small High Ligature Alef With Lam With Yeh
    "\u0617",  # Arabic Small High Zain
    "\u0618",  # Arabic Small Fatha
    "\u0619",  # Arabic Small Damma
    "\u061A",  # Arabic Small Kasra
    "\u06D6",  # Arabic Small High Ligature Sad With Lam With Alef Maksura
    "\u06D7",  # Arabic Small High Ligature Qaf With Lam With Alef Maksura
    "\u06D8",  # Arabic Small High Meem Initial Form
    "\u06D9",  # Arabic Small High Lam Alef
    "\u06DA",  # Arabic Small High Jeem
    "\u06DB",  # Arabic Small High Three Dots
    "\u06DC",  # Arabic Small High Seen
    "\u06DD",  # Arabic End Of Ayah
    "\u06DE",  # Arabic Start Of Rub El Hizb
    "\u06DF",  # Arabic Small High Rounded Zero
    "\u06E0",  # Arabic Small High Upright Rectangular Zero
    "\u06E1",  # Arabic Small High Dotless Head Of Khah
    "\u06E2",  # Arabic Small High Meem Isolated Form
    "\u06E3",  # Arabic Small Low Seen
    "\u06E4",  # Arabic Small High Madda
    "\u06E5",  # Arabic Small Waw
    "\u06E6",  # Arabic Small Yeh
    "\u06E7",  # Arabic Small High Yeh
    "\u06E8",  # Arabic Small High Noon
    "\u06E9",  # Arabic Place Of Sajdah
    "\u06EA",  # Arabic Empty Centre Low Stop
    "\u06EB",  # Arabic Empty Centre High Stop
    "\u06EC",  # Arabic Rounded High Stop With Filled Centre
    "\u06ED",  # Arabic Small Low Meem
]

HONORIFIC_SIGN = [
    "\u0610",  # Arabic Sign Sallallahou Alayhe Wa Sallam
    "\u0611",  # Arabic Sign Alayhe Assallam
    "\u0612",  # Arabic Sign Rahmatullah Alayhe
    "\u0613",  # Arabic Sign Radi Allahou Anhu
    "\u0614",  # Arabic Sign Takhallus
]
ENGLISH_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
PERSIAN_UNIQUE_CHARS = [
    '\u067E',
    '\u0686',
    '\u06AF',
    '\u0698'
]
ARABIC_NUM = "٠١٢٣٤٥٦٧٨٩"
ENGLISH_NUM = "0123456789"
FARISI_NUM = "۰۱۲۳۴۵۶۷۸۹"
ENGLISH_PUNCTUATION = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
ARABIC_PUNCTUATION = ':"؟!؛،,.؍,'

OTHER_PUNCTUATION = [
    "\xa1",
    "\xa7",
    "\xab",
    "\xb6",
    "\xb7",
    "\xbb",
    "\xbf",
    "\u037e",
    "\u0387",
    "\u055a",
    "\u055b",
    "\u055c",
    "\u055d",
    "\u055e",
    "\u055f",
    "\u0589",
    "\u058a",
    "\u05be",
    "\u05c0",
    "\u05c3",
    "\u05c6",
    "\u05f3",
    "\u05f4",
    "\u0609",
    "\u060a",
    "\u061e",
    "\u066a",
    "\u066b",
    "\u066c",
    "\u066d",
    "\u06d4",
    "\u0700",
    "\u0701",
    "\u0702",
    "\u0703",
    "\u0704",
    "\u0705",
    "\u0706",
    "\u0707",
    "\u0708",
    "\u0709",
    "\u070a",
    "\u070b",
    "\u070c",
    "\u070d",
    "\u07f7",
    "\u07f8",
    "\u07f9",
    "\u0830",
    "\u0831",
    "\u0832",
    "\u0833",
    "\u0834",
    "\u0835",
    "\u0836",
    "\u0837",
    "\u0838",
    "\u0839",
    "\u083a",
    "\u083b",
    "\u083c",
    "\u083d",
    "\u083e",
    "\u085e",
    "\u0964",
    "\u0965",
    "\u0970",
    "\u09fd",
    "\u0a76",
    "\u0af0",
    "\u0c77",
    "\u0c84",
    "\u0df4",
    "\u0e4f",
    "\u0e5a",
    "\u0e5b",
    "\u0f04",
    "\u0f05",
    "\u0f06",
    "\u0f07",
    "\u0f08",
    "\u0f09",
    "\u0f0a",
    "\u0f0b",
    "\u0f0c",
    "\u0f0d",
    "\u0f0e",
    "\u0f0f",
    "\u0f10",
    "\u0f11",
    "\u0f12",
    "\u0f14",
    "\u0f3a",
    "\u0f3b",
    "\u0f3c",
    "\u0f3d",
    "\u0f85",
    "\u0fd0",
    "\u0fd1",
    "\u0fd2",
    "\u0fd3",
    "\u0fd4",
    "\u0fd9",
    "\u0fda",
    "\u104a",
    "\u104b",
    "\u104c",
    "\u104d",
    "\u104e",
    "\u104f",
    "\u10fb",
    "\u1360",
    "\u1361",
    "\u1362",
    "\u1363",
    "\u1364",
    "\u1365",
    "\u1366",
    "\u1367",
    "\u1368",
    "\u1400",
    "\u166e",
    "\u169b",
    "\u169c",
    "\u16eb",
    "\u16ec",
    "\u16ed",
    "\u1735",
    "\u1736",
    "\u17d4",
    "\u17d5",
    "\u17d6",
    "\u17d8",
    "\u17d9",
    "\u17da",
    "\u1800",
    "\u1801",
    "\u1802",
    "\u1803",
    "\u1804",
    "\u1805",
    "\u1806",
    "\u1807",
    "\u1808",
    "\u1809",
    "\u180a",
    "\u1944",
    "\u1945",
    "\u1a1e",
    "\u1a1f",
    "\u1aa0",
    "\u1aa1",
    "\u1aa2",
    "\u1aa3",
    "\u1aa4",
    "\u1aa5",
    "\u1aa6",
    "\u1aa8",
    "\u1aa9",
    "\u1aaa",
    "\u1aab",
    "\u1aac",
    "\u1aad",
    "\u1b5a",
    "\u1b5b",
    "\u1b5c",
    "\u1b5d",
    "\u1b5e",
    "\u1b5f",
    "\u1b60",
    "\u1bfc",
    "\u1bfd",
    "\u1bfe",
    "\u1bff",
    "\u1c3b",
    "\u1c3c",
    "\u1c3d",
    "\u1c3e",
    "\u1c3f",
    "\u1c7e",
    "\u1c7f",
    "\u1cc0",
    "\u1cc1",
    "\u1cc2",
    "\u1cc3",
    "\u1cc4",
    "\u1cc5",
    "\u1cc6",
    "\u1cc7",
    "\u1cd3",
    "\u2010",
    "\u2011",
    "\u2012",
    "\u2013",
    "\u2014",
    "\u2015",
    "\u2016",
    "\u2017",
    "\u2018",
    "\u2019",
    "\u201a",
    "\u201b",
    "\u201c",
    "\u201d",
    "\u201e",
    "\u201f",
    "\u2020",
    "\u2021",
    "\u2022",
    "\u2023",
    "\u2024",
    "\u2025",
    "\u2026",
    "\u2027",
    "\u2030",
    "\u2031",
    "\u2032",
    "\u2033",
    "\u2034",
    "\u2035",
    "\u2036",
    "\u2037",
    "\u2038",
    "\u2039",
    "\u203a",
    "\u203b",
    "\u203c",
    "\u203d",
    "\u203e",
    "\u203f",
    "\u2040",
    "\u2041",
    "\u2042",
    "\u2043",
    "\u2045",
    "\u2046",
    "\u2047",
    "\u2048",
    "\u2049",
    "\u204a",
    "\u204b",
    "\u204c",
    "\u204d",
    "\u204e",
    "\u204f",
    "\u2050",
    "\u2051",
    "\u2053",
    "\u2054",
    "\u2055",
    "\u2056",
    "\u2057",
    "\u2058",
    "\u2059",
    "\u205a",
    "\u205b",
    "\u205c",
    "\u205d",
    "\u205e",
    "\u207d",
    "\u207e",
    "\u208d",
    "\u208e",
    "\u2308",
    "\u2309",
    "\u230a",
    "\u230b",
    "\u2329",
    "\u232a",
    "\u2768",
    "\u2769",
    "\u276a",
    "\u276b",
    "\u276c",
    "\u276d",
    "\u276e",
    "\u276f",
    "\u2770",
    "\u2771",
    "\u2772",
    "\u2773",
    "\u2774",
    "\u2775",
    "\u27c5",
    "\u27c6",
    "\u27e6",
    "\u27e7",
    "\u27e8",
    "\u27e9",
    "\u27ea",
    "\u27eb",
    "\u27ec",
    "\u27ed",
    "\u27ee",
    "\u27ef",
    "\u2983",
    "\u2984",
    "\u2985",
    "\u2986",
    "\u2987",
    "\u2988",
    "\u2989",
    "\u298a",
    "\u298b",
    "\u298c",
    "\u298d",
    "\u298e",
    "\u298f",
    "\u2990",
    "\u2991",
    "\u2992",
    "\u2993",
    "\u2994",
    "\u2995",
    "\u2996",
    "\u2997",
    "\u2998",
    "\u29d8",
    "\u29d9",
    "\u29da",
    "\u29db",
    "\u29fc",
    "\u29fd",
    "\u2cf9",
    "\u2cfa",
    "\u2cfb",
    "\u2cfc",
    "\u2cfe",
    "\u2cff",
    "\u2d70",
    "\u2e00",
    "\u2e01",
    "\u2e02",
    "\u2e03",
    "\u2e04",
    "\u2e05",
    "\u2e06",
    "\u2e07",
    "\u2e08",
    "\u2e09",
    "\u2e0a",
    "\u2e0b",
    "\u2e0c",
    "\u2e0d",
    "\u2e0e",
    "\u2e0f",
    "\u2e10",
    "\u2e11",
    "\u2e12",
    "\u2e13",
    "\u2e14",
    "\u2e15",
    "\u2e16",
    "\u2e17",
    "\u2e18",
    "\u2e19",
    "\u2e1a",
    "\u2e1b",
    "\u2e1c",
    "\u2e1d",
    "\u2e1e",
    "\u2e1f",
    "\u2e20",
    "\u2e21",
    "\u2e22",
    "\u2e23",
    "\u2e24",
    "\u2e25",
    "\u2e26",
    "\u2e27",
    "\u2e28",
    "\u2e29",
    "\u2e2a",
    "\u2e2b",
    "\u2e2c",
    "\u2e2d",
    "\u2e2e",
    "\u2e30",
    "\u2e31",
    "\u2e32",
    "\u2e33",
    "\u2e34",
    "\u2e35",
    "\u2e36",
    "\u2e37",
    "\u2e38",
    "\u2e39",
    "\u2e3a",
    "\u2e3b",
    "\u2e3c",
    "\u2e3d",
    "\u2e3e",
    "\u2e3f",
    "\u2e40",
    "\u2e41",
    "\u2e42",
    "\u2e43",
    "\u2e44",
    "\u2e45",
    "\u2e46",
    "\u2e47",
    "\u2e48",
    "\u2e49",
    "\u2e4a",
    "\u2e4b",
    "\u2e4c",
    "\u2e4d",
    "\u2e4e",
    "\u2e4f",
    "\u3001",
    "\u3002",
    "\u3003",
    "\u3008",
    "\u3009",
    "\u300a",
    "\u300b",
    "\u300c",
    "\u300d",
    "\u300e",
    "\u300f",
    "\u3010",
    "\u3011",
    "\u3014",
    "\u3015",
    "\u3016",
    "\u3017",
    "\u3018",
    "\u3019",
    "\u301a",
    "\u301b",
    "\u301c",
    "\u301d",
    "\u301e",
    "\u301f",
    "\u3030",
    "\u303d",
    "\u30a0",
    "\u30fb",
    "\ua4fe",
    "\ua4ff",
    "\ua60d",
    "\ua60e",
    "\ua60f",
    "\ua673",
    "\ua67e",
    "\ua6f2",
    "\ua6f3",
    "\ua6f4",
    "\ua6f5",
    "\ua6f6",
    "\ua6f7",
    "\ua874",
    "\ua875",
    "\ua876",
    "\ua877",
    "\ua8ce",
    "\ua8cf",
    "\ua8f8",
    "\ua8f9",
    "\ua8fa",
    "\ua8fc",
    "\ua92e",
    "\ua92f",
    "\ua95f",
    "\ua9c1",
    "\ua9c2",
    "\ua9c3",
    "\ua9c4",
    "\ua9c5",
    "\ua9c6",
    "\ua9c7",
    "\ua9c8",
    "\ua9c9",
    "\ua9ca",
    "\ua9cb",
    "\ua9cc",
    "\ua9cd",
    "\ua9de",
    "\ua9df",
    "\uaa5c",
    "\uaa5d",
    "\uaa5e",
    "\uaa5f",
    "\uaade",
    "\uaadf",
    "\uaaf0",
    "\uaaf1",
    "\uabeb",
    "\ufd3e",
    "\ufd3f",
    "\ufe10",
    "\ufe11",
    "\ufe12",
    "\ufe13",
    "\ufe14",
    "\ufe15",
    "\ufe16",
    "\ufe17",
    "\ufe18",
    "\ufe19",
    "\ufe30",
    "\ufe31",
    "\ufe32",
    "\ufe33",
    "\ufe34",
    "\ufe35",
    "\ufe36",
    "\ufe37",
    "\ufe38",
    "\ufe39",
    "\ufe3a",
    "\ufe3b",
    "\ufe3c",
    "\ufe3d",
    "\ufe3e",
    "\ufe3f",
    "\ufe40",
    "\ufe41",
    "\ufe42",
    "\ufe43",
    "\ufe44",
    "\ufe45",
    "\ufe46",
    "\ufe47",
    "\ufe48",
    "\ufe49",
    "\ufe4a",
    "\ufe4b",
    "\ufe4c",
    "\ufe4d",
    "\ufe4e",
    "\ufe4f",
    "\ufe50",
    "\ufe51",
    "\ufe52",
    "\ufe54",
    "\ufe55",
    "\ufe56",
    "\ufe57",
    "\ufe58",
    "\ufe59",
    "\ufe5a",
    "\ufe5b",
    "\ufe5c",
    "\ufe5d",
    "\ufe5e",
    "\ufe5f",
    "\ufe60",
    "\ufe61",
    "\ufe63",
    "\ufe68",
    "\ufe6a",
    "\ufe6b",
    "\uff01",
    "\uff02",
    "\uff03",
    "\uff05",
    "\uff06",
    "\uff07",
    "\uff08",
    "\uff09",
    "\uff0a",
    "\uff0c",
    "\uff0d",
    "\uff0e",
    "\uff0f",
    "\uff1a",
    "\uff1b",
    "\uff1f",
    "\uff20",
    "\uff3b",
    "\uff3c",
    "\uff3d",
    "\uff3f",
    "\uff5b",
    "\uff5d",
    "\uff5f",
    "\uff60",
    "\uff61",
    "\uff62",
    "\uff63",
    "\uff64",
    "\uff65",
]
PUNCTUATION = list(ENGLISH_PUNCTUATION) + \
    list(ARABIC_PUNCTUATION) + OTHER_PUNCTUATION


BUCKWALTER_TRANSLITERATION = {
    'ا': 'A',
    'ب': 'b',
    'ة': 'p',
    'ت': 't',
    'ث': 'v',
    'ج': 'j',
    'ح': 'H',
    'خ': 'x',
    'د': 'd',
    'ذ': '*',
    'ر': 'r',
    'ز': 'z',
    'س': 's',
    'ش': '$',
    'ص': 'S',
    'ض': 'D',
    'ط': 'T',
    'ظ': 'Z',
    'ع': 'E',
    'غ': 'g',
    'ف': 'f',
    'ق': 'q',
    'ك': 'k',
    'ل': 'l',
    'م': 'm',
    'ن': 'n',
    'ه': 'h',
    'و': 'w',
    'ی': 'Y',
    'ي': 'y',
    'ً': 'F',
    'ٌ': 'N',
    'ٍ': 'K',
    'َ': 'a',
    'ُ': 'u',
    'ِ': 'i',
    'ّ': '~',
}
