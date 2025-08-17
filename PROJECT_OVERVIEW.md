# Tuffy Hunt – Project Blueprint

## What It Is
A campus scavenger hunt played by teams on their phones. Each team has a private chat page with a “guardian” bot that speaks in riddles and drip-feeds hints. Teams physically find rubber ducks labeled with QR codes. Scanning the **next** correct duck advances their route and gives them points; scanning out of order returns “Not your duck.” The final duck is shared—first team to scan it wins, but everyone can finish. The bot never controls scoring or progression; the backend does. The bot only formats one hint at a time and resists prompt-injection tricks.

---

## Roles
- **Players**: open a secret URL, chat with the guardian, scan QR codes, race to the final.  
- **Guardian Bot (LLM)**: gives one riddle/hint per turn; never reveals names/IDs/routes; rejects repeat jailbreaks.  
- **Backend**: single source of truth (team progress, scoring, winner). Validates scans and decides what hint tier is allowed.  
- **Database**: stores stations, hint ladders, team routes, progress, scan/tap logs, and score events.  
- **Organizer**: seeds stations and hints, prints QRs, monitors leaderboard.  

---

## Tech Stack
- **Frontend**: Next.js + Tailwind (mobile-first). Pages: team chat, (optional) admin/seed, leaderboard view.  
- **Backend**: Next.js Route Handlers (REST). Endpoints: `/api/clue`, `/api/verify-scan`, `/api/chat`.  
- **Database + Realtime**: Supabase (Postgres + Realtime). Views for leaderboard; optional `pgvector` later for repeat-detection.  
- **LLM**: Grok via xAI API (system + developer prompts; backend-controlled hint tier).  
- **QR**: ordinary QR images encoding a `station_id` (or deep link with it in the query string).  
- **Hosting**: Vercel (app) + Supabase (db). Local dev first, then deploy.  

---

## Key Objects
- **Game**: name, final station, (winner once claimed).  
- **Team**: name + secret slug (the team’s private URL).  
- **Station (duck)**: ID, name, five-step hint ladder (H0 riddle → H1…H4).  
- **Path**: the station order for a team (last = shared final).  
- **Progress**: the index of the next expected station for a team.  
- **Tap (scan log)**: each attempt to scan a station; marks valid/invalid.  
- **Hint State**: per team+station, tracks attempts, last hint time, current tier.  
- **Score Event**: +10 for correct scans; optional small penalties/bonuses.  
- **Leaderboard View**: ranks by steps done, then score (live).  

---

## How The Loop Works
1. Team opens `/t/<slug>` (no login).  
2. Page shows the riddle (H0) for their **next** station.  
3. Players chat; the bot gives at most one stronger hint per turn.  
4. They find a duck and scan its QR.  
5. Frontend sends `{ team_slug, station_id }` to backend.  
6. Backend checks: is this the expected station?  
   - **Yes** → advance index, +10 points, log tap, unlock next station, push new riddle.  
   - **No** → reply “Not your duck,” log wrong tap (optional −1).  
7. Repeat until the shared final; first valid final scan sets the winner.  

---

## Guardrails
- **One-time progression**: only the next expected station advances.  
- **Bot blindfold**: bot never sees route or station IDs, only the single hint it is allowed to reveal.  
- **Anti-repeat**: repeating an earlier jailbreak gets “Old trick. Try a new angle.”  
- **Difficulty curve**: last three stations: leaders face tighter hint gates; trailers get slightly faster gates.  
- **Realtime nudge**: leaderboard updates live; a winner banner fires the moment someone claims the final.  

---

## Organizer Workflow
1. Write 5 short hints per station: **H0 riddle**, H1 concrete feature, H2 proximity/direction, H3 near-solution, H4 final nudge (never exact name).  
2. Pick the shared final station.  
3. Create teams and generate unique slugs.  
4. Generate each team’s path (shuffle stations + same final).  
5. Print team cards (their secret URL) and duck QRs (station IDs).  
6. Quick “hallway test” with two teams and two ducks.  

---

## Player UX
- A small chat window, a big **Scan** button, and a live leaderboard.  
- Bot messages are short (<35 words) and arrive one at a time.  
- Scanning shows a clear toast: **“Nice find!”** or **“Not your duck.”**  
- If they repeat a trick, they see **“Old trick. Try a new angle.”**  
- The final stretch feels tougher; still solvable with teamwork.  

---

## Build Order
**Phase 1 — Core Spine (no LLM yet)**  
1. Supabase project → add minimal tables for game, teams, stations, path+progress.  
2. Seed tiny demo (2 stations, 1 team).  
3. `/api/clue` → returns current station’s riddle (hardcoded text at first).  
4. `/api/verify-scan` → validates station_id, advances progress, awards points.  
5. Team page shows riddle + fake scan buttons for testing.  

**Phase 2 — Real Scans + Points**  
6. Swap fake buttons for QR-scan.  
7. Add score events.  
8. Build leaderboard view (subscribe to realtime updates).  

**Phase 3 — Guardian Bot**  
9. Add hint state per team+station.  
10. `/api/chat` → one hint per turn, cooldowns, block route dumps, detect repeats.  
11. Pass only the **single allowed hint** to Grok.  

**Phase 4 — Finish Logic + Polish**  
12. Shared final station → first scan sets winner.  
13. Difficulty curve for last three stations.  
14. UX polish and hallway playtest.  

**Phase 5 — Nice-to-Haves (optional)**  
15. Side quests (bonus points).  
16. Streak bonuses.  
17. Admin dashboard.  
18. Vector-based repeat detection.  

---

## Running The Event
- Put team cards (URL + QR) in envelopes.  
- Tape duck QRs at locations.  
- Start game → announce rules.  
- Watch leaderboard; give nudges if needed.  
- Show final leaderboard + stats after.  

---

## Grok (LLM) Notes
- **Chat access**: sometimes free with limits for consumers.  
- **API access**: pay-per-token, similar to ~$3 per 1M input and ~$15 per 1M output tokens.  
- **Free credits**: occasionally offered (e.g. $25/month promo).  
- **Bottom line**: not unlimited free. Budget-friendly if prompts are short.  

---

## Success Criteria
- Wrong duck → “Not your duck.”  
- Correct duck → +10 points, progress++, new riddle.  
- One team wins the final.  
- Leaderboard updates in real time.  
- Guardian bot: one hint per turn, rejects repeats, never leaks IDs/routes.  
- Two teams can play from start to finish with only their secret URLs.  

---

## Quick Glossary
- **Riddle (H0)**: first clue for a station.  
- **Hint Tier (H1–H4)**: increasingly specific breadcrumbs.  
- **One-time progression**: only next duck counts.  
- **Repeat detection**: blocking same jailbreak phrasing.  
- **Final duck**: shared end station; first scan wins.  
