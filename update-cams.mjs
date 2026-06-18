// update-cams.mjs
// Fetches the St. Augustine Live channel's currently-live streams and writes cams.json.
// Run by the GitHub Action on a schedule. Requires Node 18+ (built-in fetch).
//
// Needs an environment variable:  YT_API_KEY  (a YouTube Data API v3 key)

import { writeFile } from "node:fs/promises";

const CHANNEL_ID = "UCznXKvxj3U1dEQDprXBmlQA"; // St. Augustine Live
const KEY = process.env.YT_API_KEY;

if (!KEY) {
  console.error("Missing YT_API_KEY environment variable.");
  process.exit(1);
}

const url = "https://www.googleapis.com/youtube/v3/search"
  + "?part=snippet"
  + "&channelId=" + CHANNEL_ID
  + "&eventType=live"
  + "&type=video"
  + "&maxResults=50"
  + "&key=" + KEY;

const res = await fetch(url);
if (!res.ok) {
  console.error("YouTube API error", res.status, await res.text());
  process.exit(1);
}

const data = await res.json();
const live = (data.items || [])
  .filter(i => i.id && i.id.videoId)
  .map(i => ({ videoId: i.id.videoId, title: i.snippet.title }));

const out = {
  updated: new Date().toISOString(),
  channel: CHANNEL_ID,
  live
};

await writeFile("cams.json", JSON.stringify(out, null, 2) + "\n");
console.log(`Wrote ${live.length} live stream(s) to cams.json`);
for (const v of live) console.log("  •", v.title, "→", v.videoId);
