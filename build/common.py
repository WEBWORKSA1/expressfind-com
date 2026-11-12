"""Shared helpers and constants for the generator."""
import json, os
from html import escape

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEWED = "November 2026"

SERVICES = [
    ("Plumbing", "drop"), ("Water damage", "home"), ("Heating / furnace", "flame"), ("Air conditioning", "fan"),
    ("Electrical", "bolt"), ("Roofing", "roof"), ("Locksmith", "key"), ("Garage door", "garage"),
    ("Drain & sewer", "pipe"), ("Mold remediation", "spore"), ("Tree service", "tree"), ("Appliance repair", "fridge"),
    ("Handyman", "hammer"), ("Other", "wrench"),
]

CATS = [("all", "All"), ("plumbing", "Plumbing"), ("hvac", "Heating & cooling"), ("restoration", "Water & mold"),
        ("roofing", "Roofing"), ("electrical", "Electrical"), ("security", "Locks & doors"), ("exterior", "Trees & exterior"), ("appliances", "Appliances")]

VIDEOS = [
    dict(id="VLrku55gWr4", title="How To Turn Off The Main Water Valve", ch="Ace Hardware", cat="water", note="Find your main shutoff and close it before a leak becomes a flood.", link="emergency/burst-pipe.html"),
    dict(id="_WPsK5O0hKQ", title="How To Thaw Frozen Pipes", ch="Ace Hardware", cat="water", note="Safe ways to thaw exposed pipes and pipes behind walls.", link="emergency/frozen-pipes.html"),
    dict(id="-vN-ayzIJuU", title="How To Snake A Clogged Drain", ch="The Home Depot", cat="water", note="Clear a simple clog with a hand auger before paying for a service call.", link="costs/drain-cleaning.html"),
    dict(id="dIHHDXGongA", title="Furnace Troubleshooting: 5 Things to Try Before Calling a Technician", ch="Any Hour Services", cat="hvac", note="Thermostat, filter, switch and other no-heat checks.", link="emergency/no-heat.html"),
    dict(id="ARvCJRKIEOo", title="Air Conditioning Not Cooling Easy Fix", ch="Rc Jr", cat="hvac", note="Filter, breaker and thermostat checks for a no-cool AC.", link="emergency/ac-not-cooling.html"),
    dict(id="Lb2UhcnK7n8", title="How To Identify and Reset a Tripped Circuit Breaker", ch="StevesVids", cat="electrical", note="Spot a tripped breaker and reset it the right way.", link="emergency/electrical-outage.html"),
    dict(id="GYFdV23l5JU", title="Natural Gas: Stay Safe in Your Home", ch="NIPSCO", cat="safety", note="What a gas leak smells like and what to do.", link="emergency/gas-smell.html"),
    dict(id="kiXqIjwyV5w", title="PASS Technique for Fire Extinguisher Use", ch="Petroleum library", cat="safety", note="Pull, Aim, Squeeze, Sweep — for small, contained fires only.", link="tools/emergency-kit.html"),
    dict(id="GVBamXXVD30", title="How to Use a Fire Extinguisher", ch="WebstaurantStore", cat="safety", note="A second walkthrough of extinguisher basics.", link="tools/emergency-kit.html"),
    dict(id="vXWMj_TbDp4", title="How To Tarp A Roof | Severe Weather Guide", ch="Lowe's Home Improvement", cat="roofing", note="Temporary storm protection. Only attempt in dry, calm weather.", link="emergency/roof-leak.html"),
    dict(id="57CeGJR_Xow", title="How to Vet a Contractor | Ask This Old House", ch="This Old House", cat="hiring", note="How pros vet the people they hire.", link="tools/license-lookup.html"),
    dict(id="Qj_Yu0shx8A", title="BBB's Tips for Hiring a Contractor", ch="WBRC 6 News", cat="hiring", note="Red flags and homework before you sign.", link="tools/quote-checker.html"),
]
VCATS = [("all", "All"), ("water", "Water & plumbing"), ("hvac", "Heating & cooling"), ("electrical", "Electrical"), ("safety", "Safety"), ("roofing", "Roofing"), ("hiring", "Hiring a pro")]


def load_cpi():
    p = os.path.join(ROOT_DIR, "data", "cpi.json")
    try:
        with open(p) as f:
            d = json.load(f)
    except Exception:
        d = {}
    d.setdefault("factor", 1.0)
    d.setdefault("label", REVIEWED)
    return d


def rnd(n):
    if n < 100:
        return int(round(n / 5.0) * 5)
    if n < 1000:
        return int(round(n / 10.0) * 10)
    return int(round(n / 50.0) * 50)


def money(n):
    return "$" + f"{int(n):,}"


def adj(n, factor, unit=""):
    if unit == "sqft":
        v = round(n * factor * 20) / 20.0
        return f"${v:,.2f}"
    return money(rnd(n * factor))


def e(s):
    return escape(s, quote=True)
