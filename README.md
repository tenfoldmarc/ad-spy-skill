# Ad Spy
### A Claude Code Skill by [@tenfoldmarc](https://www.instagram.com/tenfoldmarc)

Give Claude your competitors' Meta Ad Library links once. Then every time you run `/ad-spy`, it pulls their active ads, downloads the images and videos, transcribes the videos (spoken hook, on-screen text, full script), finds the ads that have been running longest, flags the ones that look like retargeting, and hands you 3 to 5 proven angles adapted to your own offer. Say the word and it builds them with `/ad-copy`, `/ad-image-gen`, or `/video-ad-copy`.

---

## What It Does

1. First run: the same short business interview the other ad skills use (skipped if you've done it), then "who are your competitors?" Paste Ad Library links or just names.
2. Every run: opens each competitor's Ad Library page, grabs every active ad, and downloads the media. Only new ads get processed, so refreshes are fast.
3. Video ads get transcribed and frame-grabbed so you get the spoken hook, the on-screen hook, and the whole script.
4. Ranks by run length (longest running = probably profitable) and by newest (what they're testing now).
5. Checks each long-running ad for retargeting signals and tells you when a "winner" is probably just a retargeting ad.
6. Writes a short summary per competitor: what they sell, their top 3 proven ads, their go-to format, their mechanism, their proof, and the gap they leave open.
7. Recommends 3 to 5 angles adapted to your offer and voice, each with a suggested hook and format. Pick some, and it builds the ads.

---

## Commands

| Type this | What it does |
|---|---|
| `/ad-spy` | Refresh all competitors and recommend angles |
| `/ad-spy Hormozi` | Refresh one |
| `/ad-spy add [link or name]` | Save a competitor |
| `/ad-spy list` | See who's saved and when they were last pulled |
| `/ad-spy angles` | Re-read what's saved and recommend angles without scraping |

---

## Requirements

- A Mac or Linux computer (Windows works with WSL)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- Node.js (for the browser tool; the skill uses `npx agent-browser`)
- ffmpeg (`brew install ffmpeg`) for pulling audio and frames from video ads
- For video transcripts, one of: local Whisper (`pip3 install openai-whisper`, free) or an OpenAI API key

The skill checks all of this on first run and tells you the exact command for anything missing. Without a transcription tool it still pulls image ads and ad text, just no spoken transcripts.

---

## Install

No terminal needed.

### Step 1: Open Claude

Open the Claude Desktop app (or Claude Code, if you already use it).

### Step 2: Paste this message

```
Install this skill for me: https://github.com/tenfoldmarc/ad-spy-skill
```

### Step 3: Run the skill

```
/ad-spy
```

<details>
<summary>Prefer the terminal? Manual install</summary>

```bash
git clone https://github.com/tenfoldmarc/ad-spy-skill ~/.claude/skills/ad-spy
```

Then type `claude` and run `/ad-spy`.
</details>

---

## Usage

**Add a competitor**
```
/ad-spy add https://www.facebook.com/ads/library/?...&view_all_page_id=116482854782233
```

**Refresh and get angles**
```
/ad-spy
```
You get: "[Competitor]: 34 active ads, 6 new. Top proven ad: 'Most entrepreneurs don't realize they're the bottleneck' running 56 days, talking head, founder-to-camera. Angle 1 for you: ..."

**Build from an angle**
```
Build angles 1 and 3, copy and image.
```

---

## What's Inside

- `SKILL.md`: the skill
- `scrape.sh`: pulls ads and media from an Ad Library page
- `transcribe.py`: audio to text plus frame grabs (local Whisper or OpenAI API)

Your profile, competitor list, and everything pulled live on your machine at `~/.claude/ad-profiles/` and your output folder. Shared with [ad-copy](https://github.com/tenfoldmarc/ad-copy-skill), [video-ad-copy](https://github.com/tenfoldmarc/video-ad-copy-skill), and [ad-image-gen](https://github.com/tenfoldmarc/ad-image-gen-skill).

---

## Updating

Paste this into Claude:

```
Update the ad-spy skill from https://github.com/tenfoldmarc/ad-spy-skill
```

---

## Built By

[@tenfoldmarc](https://www.instagram.com/tenfoldmarc). Follow for daily AI automation walkthroughs. Real systems, not theory.
