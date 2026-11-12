#!/usr/bin/env python3
"""Weekly data refresh: pulls U.S. CPI data from the BLS public API (v1, no key needed),
records a baseline on first success, and writes the inflation factor and year-over-year
changes to data/cpi.json. Any failure leaves the existing data untouched (exit code 0)."""
import json, os, sys, urllib.request, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "cpi.json")
SERIES = {"all": "CUUR0000SA0", "repair": "CUUR0000SEHP04"}  # CPI-U all items; repair of household items
API = "https://api.bls.gov/publicAPI/v1/timeseries/data/"


def fetch(sid):
    req = urllib.request.Request(API + sid, headers={"User-Agent": "ExpressFind-data-refresh/1.0 (+https://expressfind.com/methodology.html)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        js = json.load(r)
    if js.get("status") != "REQUEST_SUCCEEDED":
        raise RuntimeError(js.get("message") or js.get("status"))
    rows = [d for d in js["Results"]["series"][0]["data"] if d.get("period", "").startswith("M") and d["period"] != "M13"]
    rows.sort(key=lambda d: (int(d["year"]), int(d["period"][1:])), reverse=True)
    return rows


def yoy(rows):
    if not rows:
        return None
    cur = rows[0]
    prev = next((d for d in rows if int(d["year"]) == int(cur["year"]) - 1 and d["period"] == cur["period"]), None)
    if not prev:
        return None
    return round((float(cur["value"]) / float(prev["value"]) - 1) * 100, 1)


def main():
    try:
        with open(PATH) as f:
            data = json.load(f)
    except Exception:
        data = {}
    try:
        all_rows = fetch(SERIES["all"])
        latest = all_rows[0]
        val = float(latest["value"])
        if not data.get("baseline"):
            data["baseline"] = {"value": val, "year": latest["year"], "period": latest["period"]}
        base = float(data["baseline"]["value"])
        factor = max(0.9, min(1.5, val / base))
        data["factor"] = round(factor, 4)
        data["latest"] = {"value": val, "year": latest["year"], "period": latest["period"]}
        data["data_label"] = f'{latest["periodName"]} {latest["year"]}'
        data["label"] = data["data_label"]
        data["yoy_all"] = yoy(all_rows)
        try:
            data["yoy_repair"] = yoy(fetch(SERIES["repair"]))
        except Exception as ex:
            print("repair series unavailable:", ex)
        data["checked"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ")
    except Exception as ex:
        print("CPI refresh skipped, keeping previous data:", ex)
        return 0
    with open(PATH, "w") as f:
        json.dump(data, f, indent=2)
    print("CPI updated:", data["label"], "factor", data["factor"], "yoy", data.get("yoy_all"), data.get("yoy_repair"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
