"""Text helpers: bag sizes, HTML stripping, and the origin/process/taste/roast classifiers."""
import html
import re
import unicodedata

SIZE_RE = re.compile(
    r"(\d+(?:[.,]\d+)?)\s*(kg|kilo|κιλ[όοά]|кг|g|gr|grams?|γρ|γραμ\w*|гр|г)(?![a-zα-ω])",
    re.IGNORECASE,
)

EXCLUDE_RE = re.compile(
    r"capsul|κάψουλ|καψουλ|капсул|\bpods?\b|drip ?bag|cold ?brew|\bml\b|t-?shirt|socks|\bmugs?\b|glass|"
    r"machine|grinder|kettle|dripper|\bkit\b|gift|bundle|subscription|συνδρομ|абонамент|advent|ticket|"
    r"\btea\b|matcha|milk|ελληνικός|ελληνικο|greek coffee|ibrik|\bese\b|дози|кутия|discovery|seasoning|"
    r"sample|tasting pack|\bset\b|\bbox\b|cascara|τσάι|σοκολάτ|choco drink|powder|paper filter|filters\b|tote|\btee\b|magazine|"
    r"drinking chocolate|\bdrink\b|reusable cup|ποτήρι|μπρελόκ|keychain|τσάντα|κανάτα|φίλτρα|εργαλείο|kalita|\bv60\b|"
    r"σεμινάρ|seminar|workshop|με γεύση|flavou?red",
    re.IGNORECASE,
)

COUNTRIES = {
    "Ethiopia": ["ethiopia", "αιθιοπ", "етиоп", "yirgacheffe", "sidama", "guji"],
    "Kenya": ["kenya", "κένυα", "κενυα", "кения", "kenia"],
    "Colombia": ["colombia", "κολομβ", "колумб"],
    "Brazil": ["brazil", "brasil", "βραζιλ", "бразил"],
    "Guatemala": ["guatemala", "γουατεμ", "гватем"],
    "Costa Rica": ["costa rica", "κόστα ρίκα", "κοστα ρικα", "коста рика"],
    "Honduras": ["honduras", "ονδούρ", "ονδουρ", "хондурас"],
    "El Salvador": ["el salvador", "salvador", "σαλβαδ", "салвадор"],
    "Nicaragua": ["nicaragua", "νικαράγ", "νικαραγ", "никарагуа"],
    "Panama": ["panama", "παναμ", "панама"],
    "Peru": ["peru", "περού", "περου", "перу"],
    "Rwanda": ["rwanda", "ρουάντ", "ρουαντ", "руанда"],
    "Burundi": ["burundi", "μπουρούντ", "бурунди"],
    "Uganda": ["uganda", "ουγκάντ", "уганда"],
    "Tanzania": ["tanzania", "τανζαν", "танзан"],
    "Indonesia": ["indonesia", "sumatra", "java", "ινδονησ", "индонез"],
    "Papua New Guinea": ["papua", "παπούα"],
    "Mexico": ["mexico", "μεξικ", "мексик"],
    "Ecuador": ["ecuador", "ισημεριν", "еквадор"],
    "Bolivia": ["bolivia", "βολιβ", "боливи"],
    "Yemen": ["yemen", "υεμέν", "йемен"],
    "India": ["india", "ινδία", "индия"],
    "Jamaica": ["jamaica", "τζαμάικ", "ямайка"],
    "China": ["yunnan", "china"],
}

BLEND_RE = re.compile(r"blend|χαρμάνι|χαρμανι|бленд", re.IGNORECASE)
DECAF_RE = re.compile(r"decaf|ντεκαφ|декаф|без кофеин", re.IGNORECASE)

PROCESSES = [
    ("Anaerobic", r"anaerob|αναερόβ|αναεροβ|анаероб|supernatural|thermal shock|ferment"),
    ("Carbonic maceration", r"carbonic"),
    ("Honey", r"honey process|\bhoney\b(?= ?(?:process|processed|\||$))|black honey|red honey|yellow honey|επεξεργασία μελιού"),
    ("Natural", r"\bnatural\b|φυσικ[ήη] επεξεργασ|sun[- ]dried|unwashed|натурал"),
    ("Pulped natural", r"pulped natural|semi[- ]washed"),
    ("Washed", r"\bwashed\b|πλυμέν|πλυμεν|μυτή επεξεργ|измит"),
]

NOTES_RE = re.compile(
    r"(?:tasting notes|cup notes|cupping notes|flavou?r notes|notes|cup profile|γευστικ[έεό]ς? (?:νότες|σημειώσεις|προφίλ)|νότες|"
    r"вкусов[иа]? (?:нотки|профил)|нотки)\s*[:\-–]\s*([^\n]{3,160})",
    re.IGNORECASE,
)

FRUITY = r"berr|fruit|cherry|strawberr|raspberr|blueberr|blackberr|currant|grape|mango|pineapple|papaya|peach|apricot|nectarine|plum|prune|lemon|lime|orange|citrus|tangerine|mandarin|grapefruit|bergamot|melon|guava|lychee|passion|apple|pear|banana|jasmine|floral|flower|blossom|rose|violet|lavender|lilac|magnolia|hibiscus|chamomile|lotus|wine|tropical|pomegranate|tamarind|raisin|tea|lemongrass|coconut|gooseberr|persimmon|cola|muscat|kiwi|fig"
CHOC = r"chocolate|cocoa|cacao|nut|hazelnut|almond|walnut|cashew|pecan|praline|caramel|toffee|butterscotch|molasses|brown sugar|sugar ?cane|honey|vanilla|butter|carob|maple|fudge|spice|nutmeg|clove|cinnamon|biscuit"


def strip_html(value):
    if not value:
        return ""
    text = re.sub(r"<(br|/p|/li|/div|/h\d)[^>]*>", "\n", value, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(html.unescape(text))
    text = re.sub(r"[ \t\xa0]+", " ", text)
    return re.sub(r"\n\s*", "\n", text).strip()


def parse_size_g(*texts):
    """Return the bag size in grams from the first text that names one, else None."""
    for text in texts:
        if not text:
            continue
        for amount, unit in SIZE_RE.findall(str(text)):
            value = float(amount.replace(",", "."))
            unit = unit.lower()
            grams = value * 1000 if unit.startswith(("kg", "kilo", "κιλ", "кг")) else value
            if 30 <= grams <= 5000:
                return int(round(grams))
    return None


def is_excluded(name, extra=""):
    return bool(EXCLUDE_RE.search(name)) or bool(EXCLUDE_RE.search(extra or ""))


def _fold(text):
    text = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def find_origin(name, text=""):
    if BLEND_RE.search(name):
        return "Blend"
    for haystack in (name, text[:600]):
        folded = _fold(haystack)
        for country, keys in COUNTRIES.items():
            if any(_fold(k) in folded for k in keys):
                return country
    return ""


def find_type(name, origin, process):
    if DECAF_RE.search(name) or DECAF_RE.search(process or ""):
        return "Decaf"
    if origin == "Blend" or BLEND_RE.search(name):
        return "Blend"
    return "Single origin"


def find_process(name, text=""):
    explicit = re.search(r"(?:process(?:ing)?|επεξεργασία|обработка)\s*[:\-–]\s*([^\n]{2,60})", text, re.IGNORECASE)
    for haystack in ([explicit.group(1)] if explicit else []) + [name, text]:
        for label, pattern in PROCESSES:
            if re.search(pattern, haystack, re.IGNORECASE):
                return label
    return ""


def find_notes(text):
    match = NOTES_RE.search(text or "")
    if not match:
        return ""
    return match.group(1).strip(" .;|")[:160]


def taste_group(notes):
    n = (notes or "").lower()
    if not n:
        return "Not stated"
    fruity = len(re.findall(FRUITY, n))
    choc = len(re.findall(CHOC, n))
    if fruity >= choc + 2:
        return "Fruity / floral"
    if choc >= fruity + 1:
        return "Chocolate / nutty"
    return "Balanced"


def roast_level(raw, name="", text=""):
    """Return (level, basis). Explicit roast words win; espresso/filter only gives an inferred level."""
    for source in (raw or "", name, text[:800]):
        s = source.lower()
        if re.search(r"medium[- ]light|μέτριο[- ]ανοιχτό", s):
            return "Medium-light", "Stated"
        if re.search(r"light roast|extra light|\blight\b(?= roast)|ανοιχτό ψήσιμο|светло", s) or s.strip() == "light":
            return "Light", "Stated"
        if re.search(r"medium[- ]dark", s):
            return "Medium-dark", "Stated"
        if re.search(r"medium roast|μέτριο ψήσιμο|средно", s) or s.strip() == "medium":
            return "Medium", "Stated"
        if re.search(r"dark roast|σκούρο ψήσιμο|тъмно", s) or s.strip() == "dark":
            return "Dark", "Stated"
    raw_l = (raw or "").lower()
    if "espresso or filter" in raw_l or "omni" in raw_l:
        return "Light or Medium", "Omni roast or you choose"
    use = (raw_l + " " + name.lower())
    if "filter" in use or "φίλτρ" in use:
        return "Light", "Inferred: filter roast"
    if "espresso" in use:
        return "Medium", "Inferred: espresso roast"
    return "Not stated", ""
