import json, os, urllib.request, urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path
from svg_utils import PALETTE, svg_open, text, finish, atomic_write

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"generated"
def api(query, variables):
    token=os.environ.get("GITHUB_TOKEN")
    if not token: raise RuntimeError("GITHUB_TOKEN is required for statistics generation")
    req=urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query":query,"variables":variables}).encode(), headers={"Authorization":f"bearer {token}","Content-Type":"application/json","User-Agent":"profile-generator"})
    with urllib.request.urlopen(req, timeout=30) as r: payload=json.load(r)
    if payload.get("errors"): raise RuntimeError(payload["errors"][0].get("message","GitHub GraphQL error"))
    return payload["data"]
def client_data(login):
    end=datetime.now(timezone.utc).date(); start=end-timedelta(days=364)
    q='''query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){name contributionsCollection(from:$from,to:$to){contributionCalendar{totalContributions weeks{contributionDays{contributionCount date}}} } repositories(first:100,ownerAffiliations:OWNER,privacy:PUBLIC,orderBy:{field:PUSHED_AT,direction:DESC}){nodes{name url primaryLanguage{name color} languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}}}'''
    return api(q,{"login":login,"from":f"{start}T00:00:00Z","to":f"{end}T23:59:59Z"})["user"]
def make(login, data):
    cal=data["contributionsCollection"]["contributionCalendar"]; days=[d for w in cal["weeks"] for d in w["contributionDays"]]; total=cal["totalContributions"]
    lines=svg_open(760,170,"GitHub contribution overview",f"{total} contributions in the last year")
    lines += [text(28,42,"ACTIVITY / 365",12,PALETTE["muted"],"700"), text(28,86,total,38,PALETTE["accent"],"700"), text(28,112,"public contributions",12,PALETTE["muted"]), '<line x1="220" y1="30" x2="220" y2="140" stroke="#263341"/>']
    recent=days[-52:]; maxv=max([d["contributionCount"] for d in recent] or [1])
    for i,d in enumerate(recent):
        h=round(88*d["contributionCount"]/maxv); x=242+i*9; lines.append(f'<rect x="{x}" y="{130-h}" width="5" height="{max(h,2)}" rx="2" fill="{PALETTE["accent"]}" opacity="{.25+.75*d["contributionCount"]/maxv:.2f}"/>')
    atomic_write(OUT/"stats.svg",finish(lines)); return days
def main():
    login=os.environ.get("GITHUB_USERNAME") or os.environ.get("GH_LOGIN")
    if not login: raise SystemExit("Set GITHUB_USERNAME (or GH_LOGIN in Actions)")
    days=make(login,client_data(login)); return days
if __name__=="__main__": main()
