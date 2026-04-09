# thread-post

Daily Threads post draft bot for Sebastian Ruder's NLP Newsletter.

## How it works

Each day the bot:
1. Reads `processed.json` to avoid duplicates
2. Fetches the latest issue of [NLP News](https://newsletter.ruder.io/) by Sebastian Ruder
3. Picks 3 new papers from the newsletter
4. Researches each paper via arXiv
5. Writes 4 Korean Threads post drafts per paper (12 total)
6. Saves drafts to `drafts/YYYY-MM-DD.md`
7. Updates `processed.json` with processed paper IDs

## Repo layout

- `drafts/` — one Markdown file per day with post drafts and webhook payload
- `processed.json` — array of already-covered papers (`{id, title, date}`)
- `README.md` — this file

## Post format

Each post targets the 500-character Threads limit, written in Korean with:
- A catchy hook title (emoji + Korean)
- 3–4 insight-driven listicle bullets
- An MLA-style citation

## Manual upload

Review drafts in `drafts/YYYY-MM-DD.md`, then trigger the n8n webhook manually using the payload at the bottom of each draft file.
