import os
import argparse
from pathlib import Path
from urllib.parse import urlencode
import qrcode
from qrcode.constants import ERROR_CORRECT_H

from db import supabase

DEFAULT_BASE = os.getenv("APP_BASE_URL", "http://localhost:8501/")

def ensure_trailing_slash(url: str) -> str:
    return url if url.endswith("/") else url + "/"

def fetch_all_teams():
    res = supabase.table("teams").select("id, slug, name").execute()
    return res.data or []

def fetch_path(team_id: str):
    res = supabase.table("paths").select("station_order").eq("team_id", team_id).single().execute()
    return res.data or {}

def fetch_stations_map(station_ids):
    if not station_ids:
        return {}
    # bulk fetch names for filenames/manifest
    res = supabase.table("stations").select("id, name").in_("id", list(station_ids)).execute()
    rows = res.data or []
    return {r["id"]: r.get("name") or "" for r in rows}

def qr_png(data_url: str, out_path: Path, box_size=10, border=2):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=box_size, border=border)
    qr.add_data(data_url)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(out_path)

def build_scan_url(base: str, team_slug: str, station_id: str) -> str:
    base = ensure_trailing_slash(base)
    qs = urlencode({"team": team_slug, "station": station_id, "scan": "1"})
    return f"{base}?{qs}"

def generate_for_team(team_slug: str, base_url: str, out_dir: Path):
    # find the team
    team = supabase.table("teams").select("id, slug, name").eq("slug", team_slug).single().execute().data
    if not team:
        print(f"[!] Team not found: {team_slug}")
        return 0

    path = fetch_path(team["id"])
    order = (path or {}).get("station_order") or []
    if not order:
        print(f"[!] No station_order for team {team_slug}")
        return 0

    # bulk fetch station names for nicer filenames + manifest
    stations_map = fetch_stations_map(set(order))

    team_dir = out_dir / team_slug
    team_dir.mkdir(parents=True, exist_ok=True)

    manifest_lines = ["team_slug,team_name,station_id,station_name,file_name,url"]
    count = 0
    for idx, sid in enumerate(order, start=1):
        station_name = stations_map.get(sid, "")
        url = build_scan_url(base_url, team_slug, sid)
        safe_station = station_name.replace(" ", "_") or "station"
        fname = f"{idx:02d}_{safe_station}_{sid[:8]}.png"
        out_path = team_dir / fname
        qr_png(url, out_path)
        manifest_lines.append(f'{team_slug},"{team["name"]}",{sid},"{station_name}",{fname},{url}')
        count += 1

    # write a manifest CSV per team to make printing easy
    (team_dir / "manifest.csv").write_text("\n".join(manifest_lines), encoding="utf-8")
    print(f"[ ok ] {team_slug}: saved {count} QR(s) to {team_dir}")
    return count

def generate_all(base_url: str, out_dir: Path):
    teams = fetch_all_teams()
    if not teams:
        print("[!] No teams found.")
        return 0
    out_dir.mkdir(parents=True, exist_ok=True)
    # prefetch all station names for all teams (optional); we do per team for simplicity
    total = 0
    for t in teams:
        total += generate_for_team(t["slug"], base_url, out_dir)
    print(f"[ done ] Saved {total} QR(s) to {out_dir}")
    return total

def main():
    parser = argparse.ArgumentParser(description="Generate Tuffy Hunt QR codes.")
    parser.add_argument("--base-url", default=DEFAULT_BASE, help="App base URL (default from APP_BASE_URL or http://localhost:8501/)")
    parser.add_argument("--team", help="Generate QRs for a single team slug")
    parser.add_argument("--out", default="qr_out", help="Output directory")
    args = parser.parse_args()

    out_dir = Path(args.out)
    base_url = args.base_url

    if args.team:
        generate_for_team(args.team, base_url, out_dir)
    else:
        generate_all(base_url, out_dir)

if __name__ == "__main__":
    main()