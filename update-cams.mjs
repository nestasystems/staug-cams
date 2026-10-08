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

// --- 3. Known camera videos, checked directly (~1 unit per run) ---
// YouTube's search (method 1) sometimes misses streams that ARE live. So we also
// ask YouTube about each camera's known video ID directly. This is the
// authoritative answer: "live" means it's streaming right now.
// Keep this list in sync with the fallbackId values in the website's AREAS list.
const KNOWN_IDS = {
  "ZksWoEAhmTU": "St. George Street · South",
  "FyGb2TZB344": "Castillo de San Marcos",
  "uLJBad4vSno": "Matanzas Bay",
  "R8LU4PCZdgo": "Bridge of Lions",
  "ZTk5cIbXH2g": "St. Augustine Skyline",
  "ZlqKcT4080E": "St. Augustine Lighthouse",
  "mYbn_umeenk": "Vilano Pier",
  "S8afSTXKkdw": "Vilano Boat Ramp",
  "B0JYDF1L-us": "Crescent Beach",
  "LHtzZf4T7xw": "Alligator Farm",
};
async function checkKnown() {
  const ids = Object.keys(KNOWN_IDS);
  const vids = await yt("videos", { part: "snippet", id: ids.join(",") });
  const status = {};
  for (const id of ids) status[id] = "gone";            // not returned = deleted/private
  const liveOnes = [];
  const channels = new Set();
  for (const v of vids.items || []) {
    const isLive = v.snippet?.liveBroadcastContent === "live";
    status[v.id] = isLive ? "live" : "not_live";
    if (v.snippet?.channelId) channels.add(v.snippet.channelId);
    if (isLive) liveOnes.push({ videoId: v.id, title: v.snippet.title, source: v.snippet.channelTitle || "YouTube" });
  }
  return { status, liveOnes, channels };
}

// --- 4. Every other channel our cameras come from (e.g. "See St. Augustine") ---
// When a 24/7 stream restarts it gets a NEW video ID, so checking known IDs
// isn't enough on its own. For each channel a known camera belongs to, list
// its recent uploads and keep the ones that are live right now (~3 units each).
async function liveOnChannel(channelId) {
  const ch = await yt("channels", { part: "contentDetails,snippet", id: channelId });
  const uploads = ch.items?.[0]?.contentDetails?.relatedPlaylists?.uploads;
  const name = ch.items?.[0]?.snippet?.title || "YouTube";
  if (!uploads) return [];
  const pl = await yt("playlistItems", { part: "contentDetails", playlistId: uploads, maxResults: "50" });
  const ids = (pl.items || []).map(i => i.contentDetails?.videoId).filter(Boolean);
  if (!ids.length) return [];
  const vids = await yt("videos", { part: "snippet", id: ids.join(",") });
  return (vids.items || [])
    .filter(v => v.snippet?.liveBroadcastContent === "live")
    .map(v => ({ videoId: v.id, title: v.snippet.title, source: name }));
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

let checked = null;
try {
  const k = await checkKnown();
  checked = k.status;
  const have = new Set(live.map(v => v.videoId));
  for (const v of k.liveOnes) if (!have.has(v.videoId)) { live.push(v); have.add(v.videoId); }
  console.log("Known-ID check:", JSON.stringify(checked));

  k.channels.delete(STAUG_LIVE_ID);                 // already covered by the search above
  for (const chId of k.channels) {
    try {
      for (const v of await liveOnChannel(chId)) if (!have.has(v.videoId)) { live.push(v); have.add(v.videoId); }
    } catch (err) {
      console.warn("Channel check failed for", chId, "-", err.message);
    }
  }
} catch (err) {
  console.warn("Known-ID check failed, continuing without it:", err.message);
}

const out = {
  updated: new Date().toISOString(),
  channel: STAUG_LIVE_ID,
  live,
  ...(checked ? { checked } : {})
};

await writeFile("cams.json", JSON.stringify(out, null, 2) + "\n");
console.log(`Wrote ${live.length} live stream(s) to cams.json`);
for (const v of live) console.log("  •", v.title, "→", v.videoId);
