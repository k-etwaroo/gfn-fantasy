"""
GFN Owner Mapping — GUID Based
Maps Yahoo manager GUIDs to consistent owner identities across all seasons.
"""

# GUID → Display Name
GUID_TO_OWNER = {
    "KPLDDOE75HRHOKHP7D4DLJ3YRE": "Lee",
    "DDLJVOXLB3TBCFW2FBQI4KSYSQ": "Edward",
    "MSH745OA5MRJ6ODN7W4URFPIKE": "Steve L",       # left after 2012
    "M45RSWGHYMA7MNU7DISCAOIEBE": "Hidden",         # 2011 only
    "GA2A2CNRUWQHL4CROE6XYLBW5A": "Kevin",
    "RXICUQGFSZDLSOLDXZPBGWMO5U": "Kenneth",
    "X7JNYHBHM5RFSN7G3UBGBNINQA": "Steve M",        # left after 2012
    "6UGHYQ44WGFQM7IMMFU3BPP3ZU": "Kevin2",         # second Kevin, left 2020
    "--":                           "Hidden2",       # hidden account
    "M6GO4RD7WXBMO227RA6QPG7SXI": "Scott",          # left after 2019
    "AUQPV6VO46IPNFKFDXFDHIZG3E": "Jeff",
    "BOPP2W4BZXTGWKI2HFXSA4J7XQ": "Chris D",
    "W62MGNWU6PEOVGSZXR73G6O5DU": "Chris M",        # 2011 only
    "VGRITQ2V6WVUIQUROZCD5ZEX2U": "Peter",
    "BFY67B6XCNFKOAE4ZPJ2PI6NUM": "Tim",            # left after 2013
    "3B7LCASSQJCVRTTSMJMRIHFORI": "Chad",
    "WVV244VHQOZLXAW3V7XTH7IVXA": "Tom",            # left after 2015
    "YN7YQQNWNDV25OIZS5FVWPNELE": "Steph",          # left after 2023
    "IAAOSELPIEFJXKB3UILBKNSFYA": "Mike",
    "OG6GL5AOKECVCEIF7L5CTEOEQA": "Chris",          # 2016 only
    "MPYLO3KABC6M4EZHTVOD5S4VOI": "Brian",
    "ETCIM4DSHDIAJAKTR5AT6BFIWY": "Tony",
    "GTU3SQECGX3WTJIMVO5VUOOGNY": "Christian",      # 2019-2020 only
    "UTRAVJ74I3XSTYRO3UZUNFW3PA": "Joshua",
    "NB2LPJVUM4XNNPYQZC42NZUYNE": "Christopher",
}

# Current active owners (2025 roster)
ACTIVE_OWNERS = [
    "Lee", "Edward", "Kevin", "Kenneth", "Jeff",
    "Chris D", "Peter", "Mike", "Brian", "Tony",
    "Joshua", "Christopher",
]

# Team name → GUID lookup (built from Yahoo data)
TEAM_TO_GUID = {
    # Lee
    "FLIGHT BOYZ":                    "KPLDDOE75HRHOKHP7D4DLJ3YRE",
    "TE-BOWNED":                      "KPLDDOE75HRHOKHP7D4DLJ3YRE",
    "Buttfumblers":                   "KPLDDOE75HRHOKHP7D4DLJ3YRE",
    "Genocologist":                   "KPLDDOE75HRHOKHP7D4DLJ3YRE",
    "Finding Geno":                   "KPLDDOE75HRHOKHP7D4DLJ3YRE",
    "Fitzmagic":                      "KPLDDOE75HRHOKHP7D4DLJ3YRE",
    "mCLOWN n HACKnberg":             "KPLDDOE75HRHOKHP7D4DLJ3YRE",
    "Hey dArnold!":                   "KPLDDOE75HRHOKHP7D4DLJ3YRE",
    "Darn'old Jets":                  "KPLDDOE75HRHOKHP7D4DLJ3YRE",
    "Green Jets & Sam":               "KPLDDOE75HRHOKHP7D4DLJ3YRE",
    "Stairway to Tevin":              "KPLDDOE75HRHOKHP7D4DLJ3YRE",
    "Sauce'n on you":                 "KPLDDOE75HRHOKHP7D4DLJ3YRE",
    "A Kill Lee\u2019s Tendon":       "KPLDDOE75HRHOKHP7D4DLJ3YRE",
    "A Kill Lee's Tendon":            "KPLDDOE75HRHOKHP7D4DLJ3YRE",
    "Armed Rodgery":                  "KPLDDOE75HRHOKHP7D4DLJ3YRE",
    "Dr. Fields Good":                "KPLDDOE75HRHOKHP7D4DLJ3YRE",

    # Edward
    "Hail the Skins":                 "DDLJVOXLB3TBCFW2FBQI4KSYSQ",
    "MyJimShwartzAreDirty":           "DDLJVOXLB3TBCFW2FBQI4KSYSQ",
    "No LUCK Needed 4 RG3":           "DDLJVOXLB3TBCFW2FBQI4KSYSQ",
    "Ya-Ya Smalls":                   "DDLJVOXLB3TBCFW2FBQI4KSYSQ",
    "Who?..Matt Jones":               "DDLJVOXLB3TBCFW2FBQI4KSYSQ",
    "My Cousin Kirk":                 "DDLJVOXLB3TBCFW2FBQI4KSYSQ",
    "NE Clam Crowder":                "DDLJVOXLB3TBCFW2FBQI4KSYSQ",
    "DC Janitah":                     "DDLJVOXLB3TBCFW2FBQI4KSYSQ",
    "Haskins N Robbins":              "DDLJVOXLB3TBCFW2FBQI4KSYSQ",
    "Fitz n Chips":                   "DDLJVOXLB3TBCFW2FBQI4KSYSQ",
    "The Hurts Locker":               "DDLJVOXLB3TBCFW2FBQI4KSYSQ",
    "HOWELLitzer TANK":               "DDLJVOXLB3TBCFW2FBQI4KSYSQ",
    "The Hibernators":                "DDLJVOXLB3TBCFW2FBQI4KSYSQ",
    "The Warren Brothers":            "DDLJVOXLB3TBCFW2FBQI4KSYSQ",

    # Steve L
    "#sanchizeSWAG":                  "MSH745OA5MRJ6ODN7W4URFPIKE",

    # Kevin
    "ManningHAM n' Cheese":          "GA2A2CNRUWQHL4CROE6XYLBW5A",
    "ManningHam N' Cheese":          "GA2A2CNRUWQHL4CROE6XYLBW5A",
    "StartedFromDAbottom":           "GA2A2CNRUWQHL4CROE6XYLBW5A",

    # Kenneth
    "CremeOfSomeYoungGuy":           "RXICUQGFSZDLSOLDXZPBGWMO5U",
    "HappyTissues":                  "RXICUQGFSZDLSOLDXZPBGWMO5U",
    "BlameObama":                    "RXICUQGFSZDLSOLDXZPBGWMO5U",
    "Tears of Boston":               "RXICUQGFSZDLSOLDXZPBGWMO5U",
    "Watch the Throne \U0001f440":   "RXICUQGFSZDLSOLDXZPBGWMO5U",
    "Watch the Throne 👀":           "RXICUQGFSZDLSOLDXZPBGWMO5U",
    "FIGJAM":                        "RXICUQGFSZDLSOLDXZPBGWMO5U",
    "Brolo&Cholo":                   "RXICUQGFSZDLSOLDXZPBGWMO5U",
    "NoCholoImSolo":                 "RXICUQGFSZDLSOLDXZPBGWMO5U",
    "Ed Money May Be Right":         "RXICUQGFSZDLSOLDXZPBGWMO5U",
    "James Conner Who?":             "RXICUQGFSZDLSOLDXZPBGWMO5U",
    "Deep Dish Flavor":              "RXICUQGFSZDLSOLDXZPBGWMO5U",
    "Koo and the Gang":              "RXICUQGFSZDLSOLDXZPBGWMO5U",

    # Steve M
    "Titsburgh Feelers":             "X7JNYHBHM5RFSN7G3UBGBNINQA",

    # Kevin2 / Chad (both used "THE TAMPA 2" — keyed by GUID in fetch)
    "GMEN":                          "6UGHYQ44WGFQM7IMMFU3BPP3ZU",
    "THE TAMPA 2":                   "6UGHYQ44WGFQM7IMMFU3BPP3ZU",  # fallback

    # Scott
    "Team Kellz":                    "M6GO4RD7WXBMO227RA6QPG7SXI",
    "BroSwithZsameHoe":              "M6GO4RD7WXBMO227RA6QPG7SXI",
    "SingleBroFucknHoes":            "M6GO4RD7WXBMO227RA6QPG7SXI",
    "Who?ScottyKellz":               "M6GO4RD7WXBMO227RA6QPG7SXI",

    # Jeff
    "Team Bush":                     "AUQPV6VO46IPNFKFDXFDHIZG3E",
    "Gangnam Style":                 "AUQPV6VO46IPNFKFDXFDHIZG3E",
    "Jeffrey Football":              "AUQPV6VO46IPNFKFDXFDHIZG3E",
    "Upset City":                    "AUQPV6VO46IPNFKFDXFDHIZG3E",
    "Boom Squad":                    "AUQPV6VO46IPNFKFDXFDHIZG3E",

    # Chris D
    "Swearing at Fans":              "BOPP2W4BZXTGWKI2HFXSA4J7XQ",
    "Gang Green":                    "BOPP2W4BZXTGWKI2HFXSA4J7XQ",
    "Noodle Knee III":               "BOPP2W4BZXTGWKI2HFXSA4J7XQ",
    "D'Brick House":                 "BOPP2W4BZXTGWKI2HFXSA4J7XQ",
    "Zeke-a Virus":                  "BOPP2W4BZXTGWKI2HFXSA4J7XQ",
    "Petes nOTT Good":               "BOPP2W4BZXTGWKI2HFXSA4J7XQ",
    "New Jack City":                 "BOPP2W4BZXTGWKI2HFXSA4J7XQ",
    "Got a Chubb-ie":                "BOPP2W4BZXTGWKI2HFXSA4J7XQ",
    "Rodgers Hurts":                 "BOPP2W4BZXTGWKI2HFXSA4J7XQ",
    "LaPorta Potty":                 "BOPP2W4BZXTGWKI2HFXSA4J7XQ",
    "Shambles":                      "BOPP2W4BZXTGWKI2HFXSA4J7XQ",

    # Peter
    "Rolle Tide":                    "VGRITQ2V6WVUIQUROZCD5ZEX2U",
    "Kaep N Krunch":                 "VGRITQ2V6WVUIQUROZCD5ZEX2U",
    "DaMaryius Targaryen":           "VGRITQ2V6WVUIQUROZCD5ZEX2U",
    "Abdullah Oblongata":            "VGRITQ2V6WVUIQUROZCD5ZEX2U",
    "Ya down with O.T.T":            "VGRITQ2V6WVUIQUROZCD5ZEX2U",
    "Ottoman Empire":                "VGRITQ2V6WVUIQUROZCD5ZEX2U",

    # Tim
    "Stop Drop N Rolle":             "BFY67B6XCNFKOAE4ZPJ2PI6NUM",

    # Chad
    # THE TAMPA 2 shared with Kevin2 — resolved via GUID in fetch

    # Tom
    "Brown":                         "WVV244VHQOZLXAW3V7XTH7IVXA",

    # Steph
    "TRUMPDOZER":                    "YN7YQQNWNDV25OIZS5FVWPNELE",
    "HurtInaCarr CallWilliamMattar": "YN7YQQNWNDV25OIZS5FVWPNELE",
    "Ex Sucks but my Younghoe Koo":  "YN7YQQNWNDV25OIZS5FVWPNELE",
    "Hee Hee Rhamondra!":            "YN7YQQNWNDV25OIZS5FVWPNELE",

    # Mike
    "AnnexationPuertoRico":          "IAAOSELPIEFJXKB3UILBKNSFYA",
    "Just-End-The-Season":           "IAAOSELPIEFJXKB3UILBKNSFYA",

    # Brian
    "Flutie n da Blowfish":          "MPYLO3KABC6M4EZHTVOD5S4VOI",
    "Flutie and the Blowfish":       "MPYLO3KABC6M4EZHTVOD5S4VOI",
    "PSquared*":                     "MPYLO3KABC6M4EZHTVOD5S4VOI",

    # Tony
    "Dow Jones iA 33":               "ETCIM4DSHDIAJAKTR5AT6BFIWY",
    "Dow Jones I A 33":              "ETCIM4DSHDIAJAKTR5AT6BFIWY",
    "Twas da nite Alvin ruined Xmas":"ETCIM4DSHDIAJAKTR5AT6BFIWY",
    "Just-in Fields is HIM":         "ETCIM4DSHDIAJAKTR5AT6BFIWY",
    "FDIC Crew":                     "ETCIM4DSHDIAJAKTR5AT6BFIWY",

    # Christian
    "Brolo&Cholo":                   "GTU3SQECGX3WTJIMVO5VUOOGNY",  # 2020 only

    # Joshua
    "I have Staff":                  "UTRAVJ74I3XSTYRO3UZUNFW3PA",
    "Jeff Driskel isn\u2019t a Tight End": "UTRAVJ74I3XSTYRO3UZUNFW3PA",
    "Jeff Driskel isn't a Tight End":"UTRAVJ74I3XSTYRO3UZUNFW3PA",
    "JD":                            "UTRAVJ74I3XSTYRO3UZUNFW3PA",
    "Cooper Kupp my Balls":          "UTRAVJ74I3XSTYRO3UZUNFW3PA",
    "Nacua Matata":                  "UTRAVJ74I3XSTYRO3UZUNFW3PA",

    # Christopher
    "Hayes Brigade":                 "NB2LPJVUM4XNNPYQZC42NZUYNE",
}


def get_owner_from_guid(guid):
    """Return owner display name from GUID."""
    return GUID_TO_OWNER.get(guid, f"Unknown ({guid[:8]})")


def get_guid_from_team(team_name):
    """Fallback: look up GUID from team name."""
    return TEAM_TO_GUID.get(team_name)


def get_owner(team_name=None, guid=None):
    """
    Return owner display name.
    Prefer GUID lookup; fall back to team name lookup.
    """
    if guid and guid in GUID_TO_OWNER:
        return guid, GUID_TO_OWNER[guid]
    if team_name:
        g = TEAM_TO_GUID.get(team_name)
        if g:
            return g, GUID_TO_OWNER.get(g, team_name)
    return None, team_name
