# Experience team competency

The competency framework for the GHN Experience team (Product Designers and User Researchers): **5 domains, 19 skills, rated 1 to 5**, rendered as an interactive radar dashboard.

## How this works (source of truth)

Content is **authored in Notion** and generated into the dashboard. Nothing about the wording is hand-edited in the HTML.

```
Notion (Skills DB)  ->  data/skills.json  ->  scripts/build.py  ->  dist/index.html
   author here          mirrored content       build step            what you open/deploy
```

- `data/skills.json` mirrors the Notion **Skills** database: each skill has a definition, a plain self-check, a track, and 5 levels written as a sentence plus a concrete GHN example (stored as `"sentence|example"`).
- `data/profiles.json` holds the illustrative per Role and Level shapes (not real ratings).
- `scripts/build.py` bakes both into a single self-contained `dist/index.html`.

## Run it

Open `dist/index.html` in any browser. No build step or server needed to view.

To regenerate after editing the data:

```bash
python3 scripts/build.py
```

## Update the content

1. Edit the skill in Notion (the Skills database).
2. Update the matching row in `data/skills.json`.
3. Run `python3 scripts/build.py` and commit `dist/index.html`.

(The Notion-to-JSON step is currently manual/assisted. A scripted pull is a later option, see Roadmap.)

## The dashboard

- Filter by **Role** and **Level** (levels with no profile are hidden).
- **Hover** a skill for a quick popover (rising bar to current level, one-line summary).
- **Click** to select a skill and see its full detail below; **double-click** to clear.
- Domains are grouped by an outer colour band and named in the legend.

## Deploy (optional)

`.github/workflows/pages.yml` publishes `dist/` to GitHub Pages.

> **Privacy note:** on GitHub Free/Pro, a Pages site built from a private repo is still **publicly reachable**. Private-visibility Pages require GitHub Enterprise Cloud. This dashboard contains the rubric and illustrative shapes only (no named people), but confirm that is acceptable before enabling Pages, or just share `dist/index.html` directly.

## Roadmap

- **Ratings layer:** a Skill Snapshot (one row per person per quarter) and per Role and Level benchmark shapes, related to a Team Management database in Notion.
- **Scripted Notion pull:** replace the manual mirror step with a script that reads the Notion Skills DB via the API.
