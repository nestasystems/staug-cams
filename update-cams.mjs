// update-cams.mjs
// Fetches currently-live streams from the St. Augustine cam channels and writes cams.json.
// Run by the GitHub Action on a schedule. Requires Node 18+ (built-in fetch).
//
// Needs an environment variable:  YT_API_KEY  (a YouTube Data API v3 key)
//
// Channels:
//   1. St. Augustine Live — uses the search endpoint (100 quota units per run).
//   2. Beachcomber St. Augustine — uses the cheap uploads-playlist method (~3 units per run).
//      Its stream titles are prefixed with "Beachcomber" if needed, so the page can
//      always match it with  match: ["beachcomber"]  even if the restaurant renames the stream.
//
// If the Beachcomber lookup fails, the St. Augustine Live results are still written.

import { writeFile } from "node:fs/promises";

const API = "https://www.googleapis.com/youtube/v3/";
const KEY = process.env.YT_API_KEY;

const STAUG_LIVE_ID = "UCznXKvxj3U1dEQDprXBmlQA"; // St. Augustine Live
const BEACHCOMBER_HANDLE = "@BeachcomberStAugustine";  // Beachcomber St. Augustine

if (!KEY) {
  console.error("Missing YT_API_KEY environment variable.");
  process.exit(1);
}

async function yt(endpoint, params) {
  const qs = new URLSearchParams({ ...params, key: KEY });
  const res = await fetch(API + endpoint + "?" + qs);
  if (!res.ok) throw new Error(`YouTube API error ${res.status} on ${endpoint}: ${await res.text()}`);
  return res.json();
}

// --- 1. St. Augustine Live (unchanged method) ---
async function getStAugLive() {
  const data = await yt("search", {
    part: "snippet",
    channelId: STAUG_LIVE_ID,
    eventType: "live",
    type: "video",
    maxResults: "50"
  });
  return (data.items || [])
    .filter(i => i.id && i.id.videoId)
    .map(i => ({ videoId: i.id.videoId, title: i.snippet.title, source: "St. Augustine Live" }));
}

// --- 2. Beachcomber (cheap method: uploads playlist -> check which are live) ---
async function getBeachcomber() {
  const ch = await yt("channels", { part: "contentDetails", forHandle: BEACHCOMBER_HANDLE });
  const uploads = ch.items?.[0]?.contentDetails?.relatedPlaylists?.uploads;
  if (!uploads) throw new Error("Could not find Beachcomber channel uploads playlist");

  const pl = await yt("playlistItems", { part: "contentDetails", playlistId: uploads, maxResults: "50" });
  const ids = (pl.items || []).map(i => i.contentDetails?.videoId).filter(Boolean);
  if (!ids.length) return [];

  const vids = await yt("videos", { part: "snippet", id: ids.join(",") });
  return (vids.items || [])
    .filter(v => v.snippet?.liveBroadcastContent === "live")
    .map(v => {
      const t = v.snippet.title;
      const title = /beachcomber/i.test(t) ? t : "Beachcomber · " + t;
      return { videoId: v.id, title, source: "Beachcomber St. Augustine" };
    });
}

// --- Run ---
let live;
try {
  live = await getStAugLive();
} catch (err) {
  console.error(err.message);
  process.exit(1); // main channel failed: don't overwrite cams.json with a partial list
}

try {
  live.push(...await getBeachcomber());
} catch (err) {
  console.warn("Beachcomber lookup failed, continuing without it:", err.message);
}

const out = {
  updated: new Date().toISOString(),
  channel: STAUG_LIVE_ID,
  live
};

await writeFile("cams.json", JSON.stringify(out, null, 2) + "\n");
console.log(`Wrote ${live.length} live stream(s) to cams.json`);
for (const v of live) console.log("  •", v.title, "→", v.videoId);
