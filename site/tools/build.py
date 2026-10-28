#!/usr/bin/env python3
"""Builds every Watch St. Augustine guide page from one template.
Run:  python3 build.py   -> writes HTML into ./pages/
To add a restaurant: add a dict to RESTAURANTS below and re-run."""
import json, html, os, datetime

SITE = "https://watchstaugustine.com"
BRAND = "Watch St. Augustine"
LOGO = "https://assets.cdn.filesafe.space/8yzojm3WV1TpigXrdMV6/media/6a3457d21c5d711b357049f3.png"
EMAIL = "hello@watchstaugustine.com"
TODAY = datetime.date.today().isoformat()
UTM = "utm_source=watchstaugustine&utm_medium=referral&utm_campaign={campaign}"

# Live cameras people can jump to from a listing (keys match the camera page's ?cam= feature)
CAMS = {
  "matanzas":  ("Matanzas Bay", "the bayfront and Bridge of Lions"),
  "george":    ("St. George Street", "the pedestrian lane downtown"),
  "skyline":   ("St. Augustine Skyline", "downtown rooftops"),
  "fort":      ("Castillo de San Marcos", "the fort and bayfront"),
  "pier":      ("St. Augustine Beach Pier", "the pier and surf"),
  "lighthouse":("St. Augustine Lighthouse", "Anastasia Island"),
}

RESTAURANTS = [
 dict(slug="ice-plant", name="The Ice Plant", short="Ice Plant", area="Riberia Street, downtown St. Augustine", photo_place="https://assets.cdn.filesafe.space/8yzojm3WV1TpigXrdMV6/media/6ae02da99c1511d5b9f5e8ff.png", photo_people="https://assets.cdn.filesafe.space/8yzojm3WV1TpigXrdMV6/media/6ae02e26d542268bb4586aeb.png", photo_people_caption="Inside The Ice Plant, in the restored 1905 ice house", title="The Ice Plant | Farm-to-Table and Cocktails in St. Augustine, FL", what="farm-to-table restaurant and cocktail bar", desc="The Ice Plant: farm-to-table food and craft cocktails in St. Augustine's historic 1905 ice plant, beside the St. Augustine Distillery. Hours and our story.", pick="farm to table and craft cocktails",
      cuisine="Farm-to-table American", kind="Restaurant and cocktail bar",
      address="110 Riberia St", city="St. Augustine", zip="32084", phone="(904) 829-6553",
      url="https://iceplantbar.com/", menu="https://iceplantbar.com/menu/", reserve=None,
      reserve_note="No reservations or call-ahead; walk in.",
      hours=["Mon–Thu 11:30 AM – 12:00 AM","Fri 11:30 AM – 2:00 AM","Sat 10:00 AM – 2:00 AM","Sun 10:00 AM – 12:00 AM"],
      hours_schema=["Mo-Th 11:30-24:00","Fr 11:30-02:00","Sa 10:00-02:00","Su 10:00-24:00"],
      social=["https://www.instagram.com/iceplantbar/","https://www.facebook.com/iceplantbar"],
      known=["Craft cocktails with house-pressed juices and a wide range of bitters","Farm-to-table lunch and dinner: grass-fed beef and burgers, local seafood, vegetarian options, daily specials","The historic Ice Plant: a 1905 power plant that became Florida's first commercial block-ice facility, making up to 125 tons of ice a day for the fishing fleets before closing in the 1950s","Restored from 2010 to 2012 with the St. Augustine Distillery downstairs and the restaurant upstairs, keeping the original overhead bridge crane and windows; listed on the National Register of Historic Places"],
      neighborhood="West of downtown, by the San Sebastian River", cam="george",
      geo=(29.8916,-81.3200),
      why='The Ice Plant is the one we tell people about first: a 1905 ice plant turned restaurant, cocktails made with real care, and a fresh farm-to-table menu that changes with the season.',
      story=["We found The Ice Plant by accident. A trolley ride pulled into the old ice plant building instead of driving past it, and that's how we learned the St. Augustine Distillery had opened there with a restaurant upstairs. We took the distillery tour, loved it, walked over to look at the restaurant, and decided on the spot to come back for dinner that night.", "That dinner is the reason it's on this list. The building alone is worth the trip. It started life as a power plant in 1905 and became Florida's first commercial block-ice plant, turning out up to 125 tons of ice a day for the shrimpers and fishing fleets. It sat empty for decades until a three-year restoration brought it back, and the dining room still has the overhead crane that once hoisted 325-pound blocks of ice. The cocktails are made with house-pressed juices and a wall of bitters, and you can tell someone cares about every one. The food is the real draw: a fresh farm-to-table menu that changes with the seasons, so there's always something new worth ordering.", "What stays with us is how seriously they take the craft of being a restaurant and a bar, right down to how a drink is built. That's what got us the first night, and it's what keeps us coming back."],
      faq_extra=[("What is the history of The Ice Plant building?","The Ice Plant at 110 Riberia Street began as a city power plant in 1905 and grew into Florida's first commercial block-ice facility, producing up to 125 tons of ice a day for local fishing fleets, farmers and residents. It closed in the 1950s, sat dormant for nearly 60 years, and was restored between 2010 and 2012. Today the St. Augustine Distillery occupies the lower level and the Ice Plant restaurant and bar the upper level. The building is listed on the National Register of Historic Places."),
                 ("Do I need a reservation at The Ice Plant?","No. The Ice Plant does not take reservations or call-ahead seating, so you walk in and wait for a table. Weekend evenings are the busiest."),
                 ("Is The Ice Plant open for lunch?","Yes. The Ice Plant opens at 11:30 AM Monday through Friday and at 10:00 AM on Saturday and Sunday, and serves both lunch and dinner.")]),
 dict(slug="17-king", name="17 King", short="17 King", area="downtown St. Augustine", what="wine-focused American bistro", desc="17 King: a wine-focused American bistro at King and Aviles in downtown St. Augustine, with live music nightly. Hours, menu, the chef, and our story.", pick="wine and bistro dining", photo_place="", photo_people="", photo_people_caption="",
      cuisine="American bistro, wine-focused", kind="Wine bar and bistro",
      address="17 King St", city="St. Augustine", zip="32084", phone="(904) 481-8546",
      url="https://www.17kingsta.com/", menu="https://www.17kingsta.com/dinnermenu", reserve="https://www.opentable.com/r/17-king-st-augustine", reserve_label="Reserve on OpenTable",
      reserve_note="Reservations recommended but not required; book on OpenTable or call.",
      hours=["Tue–Thu 4:30 PM – 9:00 PM","Fri–Sat 11:00 AM – 10:00 PM","Sun 11:00 AM – 9:00 PM","Mon: check their site"],
      hours_schema=["Tu-Th 16:30-21:00","Fr-Sa 11:00-22:00","Su 11:00-21:00"],
      social=["https://www.instagram.com/17kingstreet/","https://www.facebook.com/17KingStreet/"],
      known=["Opened May 1, 2026 by the team behind La Casa Studios, owner Gary McGeddy and partner Stephen Hutson, in the space that was The Harvest and Bourbon & Boards","A custom wine library at the center of the room that doubles as a retail wine shop and tasting bar","Chef Landry Wyatt, a graduate of the Auguste Escoffier School of Culinary Arts: duck pappardelle, grilled shrimp polenta, seared scallops with lemon risotto, charcuterie boards","Live music nightly, craft cocktails, and wine tastings at the King's Table, a custom magnolia-wood table","A different St. Augustine charity supported each month"],
      neighborhood="downtown at the corner of King St and Aviles St", cam="matanzas",
      geo=(29.8921,-81.3115),
      why="17 King is where we spent our 15th wedding anniversary, and it's where we now send everyone who wants a real night out downtown.",
      story=["We picked 17 King for our 15th wedding anniversary this October, and it turned into one of the best nights out we've had in St. Augustine.", "The room is warm and elegant without being stiff. There's live music every night, and it was outstanding. The service was tremendous from the first cocktail, which was poured perfectly and clearly made with care, to the last glass of wine. Matt had a filet mignon that was the best he's ever had, or close to it. Malena had the scallops over risotto, which were mind-blowing.", "We'd been curious about 17 King since we learned the team behind La Casa Studios, the beautiful event space a few doors down, was opening it. It arrived on May 1, 2026, built around a custom wine library that doubles as a wine shop, with chef Landry Wyatt running the kitchen. The answer to whether they could do it again is yes. We'll be sending everyone we know to go have the same night we did."],
      faq_extra=[("Who owns 17 King in St. Augustine?","17 King American Bistro opened on May 1, 2026 and was created by the team behind La Casa Studios, led by owner Gary McGeddy and business partner Stephen Hutson. It occupies the space at 17 King Street formerly home to The Harvest Restaurant and Bourbon & Boards, steps from the Plaza de la Constitución."),
                 ("Who is the chef at 17 King?","The kitchen is headed by chef Landry Wyatt, a graduate of the Auguste Escoffier School of Culinary Arts. Signature dishes include duck pappardelle, grilled shrimp polenta, seared scallops with lemon risotto, and charcuterie boards."),
                 ("Does 17 King take reservations?","Yes. Reservations are recommended but not required. You can book on OpenTable or call (904) 481-8546."),
                 ("Does 17 King have live music?","Yes. 17 King hosts live music nightly, according to its website, alongside its wine-focused dinner service.")]),
 dict(slug="the-floridian", name="The Floridian", short="The Floridian", title="The Floridian | Farm-to-Table Southern in St. Augustine, FL", what="farm-to-table Southern restaurant", desc="The Floridian: farm-to-table Southern cooking in a new custom-built home at 485 Old Beach Rd on Anastasia Island. Hours, menu and our story.", pick="Southern class with a modern menu", photo_place="", photo_people="", photo_people_caption="",
      cuisine="Farm-to-table Southern", kind="Restaurant",
      address="485 Old Beach Rd", city="St. Augustine", zip="32080", phone="(904) 829-0655",
      url="https://www.thefloridianstaug.com/", menu="https://www.thefloridianstaug.com/", reserve="https://resy.com/cities/st-augustine-fl/venues/the-floridian", reserve_label="Reserve on Resy",
      reserve_note="Reservations available on Resy.",
      hours=["Open Wednesday through Monday; closed Tuesday","Lunch 11 AM – 3 PM","Happy hour 3 – 5 PM","Dinner from 4:30 PM"],
      hours_schema=["We-Mo 11:00-15:00","We-Mo 16:30-21:00"],
      social=[],
      known=["Farm-to-table Southern cuisine from executive chef Genie McNally and Jeff McNally, who opened The Floridian downtown in 2010","Reopened June 5, 2026 in a brand-new, custom-built 4,000-square-foot home on Anastasia Island","Old Florida coastal cottage style: 120 seats, wraparound porch decks, a garden, a side patio with a bar, and free parking","A guiding motto: \"Food is Important!\""],
      neighborhood="Anastasia Island, near St. Augustine Beach", cam="pier",
      geo=(29.8540,-81.2760),
      why="The Floridian is where we send people for Southern food that's fresh, eclectic and made from what local farms have right now.",
      story=["The Floridian is one of those St. Augustine restaurants everyone told us about, and for a long time it stayed just out of reach. Years ago we tried to walk in at the old Spanish Street location and couldn't get a table. By the time we finally went, Genie and Jeff McNally had closed downtown and built their dream restaurant from the ground up on Anastasia Island, which happens to be a few blocks from our house.", "The new place is beautiful. It opened in June 2026, an Old Florida coastal cottage under the palmettos and live oaks, with wraparound porches, a garden, and a side patio with its own bar. Inside it has that classic old Southern look while feeling brand new and vibrant. We went for a late lunch, and the service was great and the food was outstanding.", "The menu is eclectic and fresh, built around what local farms and growers have in season, which means it's a little different every visit. It's one of the great restaurants in St. Augustine, and we'd tell anyone visiting to eat there."],
      faq_extra=[("Did The Floridian move?","Yes. The Floridian opened at 39 Cordova Street in 2010, moved to 72 Spanish Street in 2015, and closed that downtown location in July 2025. It reopened on June 5, 2026 in a new custom-built 4,000-square-foot restaurant at 485 Old Beach Road on Anastasia Island, with 120 seats, porch decks, a garden patio bar and free parking."),
                 ("Who owns The Floridian?","The Floridian is owned by husband-and-wife team Genie McNally, the executive chef, and Jeff McNally, who opened the restaurant in downtown St. Augustine in 2010."),
                 ("Is The Floridian open on Tuesdays?","No. The Floridian is open Wednesday through Monday and closed on Tuesday, according to its website."),
                 ("Does The Floridian have a happy hour?","Yes. The Floridian lists a happy hour from 3 PM to 5 PM between lunch and dinner service.")]),
 dict(slug="la-nouvelle", name="La Nouvelle", short="La Nouvelle", title="La Nouvelle | French Bistro in Lincolnville, St. Augustine, FL", what="French bistro", desc="La Nouvelle: a French bistro in the historic Jefferson House at 102 Bridge St in Lincolnville, St. Augustine. Dinner, hours and our story.", pick="charming French cuisine", photo_place="", photo_people="", photo_people_caption="",
      cuisine="French bistro", kind="French bistro",
      address="102 Bridge St", city="St. Augustine", zip="32084", phone="(904) 217-8551",
      url="https://www.lanousta.com/", menu="https://www.lanousta.com/dinnermenu", reserve="https://www.opentable.com/r/la-nouvelle-st-augustine", reserve_label="Reserve on OpenTable",
      reserve_note="Reservations available for guaranteed seating but not required; book on OpenTable, call, or email.",
      hours=["Tue–Thu 5:00 PM – 9:30 PM","Fri 5:00 PM – 10:00 PM","Sat 10:00 AM – 10:00 PM","Sun 10:00 AM – 9:30 PM","Mon closed"],
      hours_schema=["Tu-Th 17:00-21:30","Fr 17:00-22:00","Sa 10:00-22:00","Su 10:00-21:30"],
      social=["https://www.instagram.com/lanouvellesta/","https://www.facebook.com/LaNouvelleSTA/"],
      known=["French nouveau cuisine from chef Michael Lugo, with Matthieu Landillon of Marseille at the helm","Outdoor porch and courtyard seating, weather permitting","Housed in the Jefferson House, a two-story Victorian in Lincolnville and the original homesite of Maria Jefferson Eppes Shine, great-granddaughter of Thomas Jefferson"],
      neighborhood="Lincolnville, a few blocks south of downtown", cam="matanzas",
      geo=(29.8880,-81.3140),
      why='La Nouvelle is a French bistro in a restored Victorian home, grand and cozy at the same time, and where we celebrated our anniversary in 2025.',
      story=['We celebrated our wedding anniversary at La Nouvelle in 2025, and it was an amazing evening: ultra high quality food, wine, service and atmosphere, all of it.', "The room is the first thing you notice. The building is the Jefferson House, a two-story Victorian in Lincolnville that was the original homesite of Maria Jefferson Eppes Shine, Thomas Jefferson's great-granddaughter. Inside it's grand and beautiful while still feeling cozy, the kind of place you want to settle into for a while. That's exactly how they treat you: like you're there to spend the evening, not turn the table.", "A French dish made for you, a bottle of wine their sommelier can pair with it, and a porch or courtyard seat when the weather's right. We first spotted the building from the trolley and said we had to come back. We're glad we did, and it's the place we send people for a night that feels special."],
      faq_extra=[("What building is La Nouvelle in?","La Nouvelle is in the Jefferson House at 102 Bridge Street in the Lincolnville neighborhood of St. Augustine, a two-story Victorian that was the original homesite of Maria Jefferson Eppes Shine, great-granddaughter of President Thomas Jefferson, and her husband, Dr. William Shine."),
                 ("Do I need a reservation at La Nouvelle?","No. Reservations are available for guaranteed seating but are not required. You can book on OpenTable, call (904) 217-8551, or email hello@lanousta.com.")]),
]

# ---------------------------------------------------------------- shared pieces
CSS = """
:root{--sand:#FCF7EE;--shell:#fff;--shell-2:#FFFDF8;--foam:#E8F5F4;--hairline:#EAE0CF;--ink:#0F3A45;--slate:#3A565C;--coral:#FF6F59;--coral-deep:#E2553C;--aqua:#10B4C8;--aqua-deep:#0A6270;--sun:#FFC23C;--radius:18px;--maxw:1480px}
*{box-sizing:border-box}
/* Full-bleed: break out of the site builder's centered box, same as the camera page */
html,body{margin:0 !important;padding:0 !important}
body *:has(> .pagewrap), body *:has(.pagewrap){max-width:none !important;width:auto !important;padding:0 !important;margin:0 !important;background:transparent !important}
.pagewrap{width:100vw;max-width:100vw;margin-left:calc(50% - 50vw);margin-right:calc(50% - 50vw);overflow-x:clip;min-height:100vh;display:flex;flex-direction:column}
.pagewrap main{flex:1 0 auto}
body{margin:0;background:radial-gradient(1100px 560px at 82% -8%,rgba(255,205,80,.30),transparent 60%),radial-gradient(900px 520px at -8% 8%,rgba(16,180,200,.12),transparent 55%),var(--sand);color:var(--ink);font-family:"Inter",system-ui,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.5}
a{color:var(--aqua-deep)} a:focus-visible,button:focus-visible{outline:2px solid var(--coral);outline-offset:3px}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 clamp(16px,4vw,40px)}
header.top{position:sticky;top:0;z-index:20;background:rgba(252,247,238,.9);backdrop-filter:blur(10px);border-bottom:1px solid var(--hairline)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-top:12px;padding-bottom:12px}
.brand{text-decoration:none;color:var(--ink);font-weight:800;font-size:19px;letter-spacing:-.02em}.brand em{color:var(--coral);font-style:normal}
.brand small{display:block;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--aqua-deep)}
nav.main ul{list-style:none;margin:0;padding:0;display:flex;gap:4px;flex-wrap:wrap}
nav.main a{display:inline-block;padding:8px 12px;border-radius:999px;text-decoration:none;font-weight:600;font-size:14px;color:var(--ink)}
nav.main a:hover,nav.main a[aria-current]{background:var(--foam);color:var(--aqua-deep)}
.hero{padding:clamp(28px,5vw,56px) 0 10px}
.eyebrow{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--aqua-deep);margin:0 0 12px}
h1{font-weight:800;font-size:clamp(30px,4.3vw,52px);line-height:1.02;letter-spacing:-.025em;margin:0 0 14px}
h1 em{font-style:normal;color:var(--coral)}
h2{font-weight:700;font-size:clamp(22px,2.8vw,30px);letter-spacing:-.02em;margin:34px 0 12px}
h3{font-weight:700;font-size:17px;margin:18px 0 6px}
.lede{max-width:60ch;color:var(--slate);font-size:clamp(15px,1.25vw,18px);margin:0}
.aeo-summary{background:var(--shell);border:1px solid var(--hairline);border-left:4px solid var(--aqua);border-radius:0 14px 14px 0;padding:16px 20px;margin:18px 0 26px;font-size:16px;line-height:1.65}
.aeo-summary strong{color:var(--ink)}
.freeline{display:flex;align-items:center;gap:8px;font-size:14px;font-weight:600;margin:14px 0 0}
.freeline svg{width:16px;height:16px;fill:none;stroke:var(--aqua-deep);stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px;margin:22px 0}
.card{cursor:pointer;background:var(--shell);border:2px solid var(--coral);border-radius:var(--radius);padding:20px;display:flex;flex-direction:column;gap:8px;box-shadow:0 12px 30px -20px rgba(15,58,69,.28);transition:transform .2s,box-shadow .2s}
.card:hover{transform:translateY(-3px);border-color:var(--coral-deep);box-shadow:0 20px 40px -22px rgba(255,111,89,.5)}
.card h3{margin:0;font-size:20px}.card h3 a{color:var(--ink);text-decoration:none}.card h3 a:hover{color:var(--coral-deep)}
.card .kind{font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--aqua-deep)}
.card p{margin:0;color:var(--slate);font-size:15px}
.card .meta{font-size:13px;color:var(--slate)}
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;border-radius:999px;background:var(--coral);color:#fff;font-weight:700;text-decoration:none;font-size:14px;border:0;cursor:pointer}
.btn:hover{filter:brightness(1.06)} .btn.ghost{background:var(--foam);color:var(--aqua-deep)}
.btnrow{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:18px 0}
.fact{background:var(--shell);border:1px solid var(--aqua);border-radius:14px;padding:14px 16px}
.fact b{display:block;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--aqua-deep);margin-bottom:4px}
.fact ul{margin:0;padding-left:18px;color:var(--slate);font-size:14px}
.cambox{display:flex;gap:16px;align-items:center;background:linear-gradient(135deg,#E8F5F4,#FFF8E6);border:1px solid var(--hairline);border-radius:var(--radius);padding:18px 20px;margin:26px 0}
.cambox .dot{width:12px;height:12px;border-radius:50%;background:#FF5247;flex:none;animation:pulse 1.6s ease-in-out infinite}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(255,82,71,.5)}50%{box-shadow:0 0 0 8px rgba(255,82,71,0)}}
.cambox p{margin:0;font-size:15px}.cambox b{display:block;font-size:16px}
.about-split{display:grid;grid-template-columns:minmax(0,1fr) 520px;gap:40px;align-items:start;margin:34px 0 10px}
.about-text .lede{margin:0 0 16px}
.about-photo{display:block;width:100%;max-width:520px;height:auto;border-radius:var(--radius);border:1px solid var(--hairline);box-shadow:0 20px 40px -22px rgba(15,58,69,.4);position:sticky;top:90px}
@media(max-width:980px){.about-split{grid-template-columns:1fr}.about-photo{position:static;margin:0 auto}}
.pickline{margin:4px 0 14px;font-size:15px;color:var(--slate)}.pickline b{color:var(--coral-deep)}
.photos{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin:6px 0 20px}
.photos img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:var(--radius);border:1px solid var(--hairline)}
.photos figure{margin:0}.photos figcaption{font-size:13px;color:var(--slate);margin-top:6px}
.why{background:var(--shell);border:1px solid var(--hairline);border-radius:var(--radius);padding:20px 22px;margin:22px 0}
.why .by{font-size:13px;color:var(--slate);margin-top:8px}
.faq-item{background:var(--shell);border:1px solid var(--hairline);border-radius:14px;margin:10px 0;overflow:hidden}
.faq-question{width:100%;text-align:left;background:none;border:0;padding:16px 18px;font:600 16px/1.4 "Inter",system-ui,sans-serif;color:var(--ink);display:flex;justify-content:space-between;gap:14px;cursor:pointer}
.faq-toggle{color:var(--coral);font-size:20px;line-height:1}
.faq-answer{display:none;padding:0 18px 16px;color:var(--slate);font-size:15px;line-height:1.65}
.faq-item.open .faq-answer{display:block}.faq-item.open .faq-toggle{transform:rotate(45deg)}
.sitefoot{background:var(--ink);color:#CFE6E6;margin-top:54px;padding:46px 0 34px;font-size:14px}
.sitefoot a{color:#CFE6E6}.sitefoot .cols{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:26px 40px}
.sitefoot h4{margin:0 0 8px;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#9FB6B6}
.sitefoot ul{list-style:none;margin:0;padding:0}.sitefoot li{margin:4px 0}
.sf-base{border-top:1px solid rgba(255,255,255,.12);margin-top:26px;padding-top:18px;font-size:13px;color:#9FB6B6;display:flex;flex-wrap:wrap;gap:6px 14px}
.sf-base .credit{color:#fff;font-weight:600}.sf-base .credit a{color:#fff}
@media(max-width:680px){.sitefoot .cols{grid-template-columns:1fr}header.top .wrap{flex-direction:column;align-items:flex-start}}
"""

CRAWLERS = """<meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large" />
<meta name="bingbot" content="index, follow" />
<meta name="GPTBot" content="index, follow" />
<meta name="ChatGPT-User" content="index, follow" />
<meta name="Google-Extended" content="index, follow" />
<meta name="PerplexityBot" content="index, follow" />
<meta name="ClaudeBot" content="index, follow" />
<meta name="anthropic-ai" content="index, follow" />"""

FAQ_JS = """<script>
document.querySelectorAll(".card[data-href]").forEach(c=>c.addEventListener("click",e=>{ if(e.target.closest("a")) return; location.href=c.dataset.href; }));
document.querySelectorAll(".faq-question").forEach(b=>b.addEventListener("click",()=>{const it=b.closest(".faq-item");const open=it.classList.toggle("open");b.setAttribute("aria-expanded",open?"true":"false");}));
</script>"""

def esc(t): return html.escape(t, quote=True)
def utm(url, campaign):
    sep = "&" if "?" in url else "?"
    return url + sep + UTM.format(campaign=campaign)

def org_nodes():
    return [
      {"@type":"Organization","@id":f"{SITE}/#organization","name":BRAND,"alternateName":"WatchStAugustine","url":f"{SITE}/",
       "logo":{"@type":"ImageObject","url":LOGO},"description":"Watch St. Augustine is an independent guide that gathers free, public live cameras of St. Augustine, Florida into one page, plus local recommendations from Nesta Systems.",
       "foundingDate":"2026","contactPoint":{"@type":"ContactPoint","email":EMAIL,"contactType":"customer service","availableLanguage":"English"},
       "areaServed":{"@type":"City","name":"St. Augustine, Florida"}},
      {"@type":"Organization","@id":"https://nestasystems.com/#organization","name":"Nesta Systems","alternateName":"Nestasystems.com","url":"https://nestasystems.com/",
       "description":"Nesta Systems is a small business consulting company in St. Augustine, Florida that helps local businesses win more repeat customers and referrals. It built and maintains watchstaugustine.com.",
       "address":{"@type":"PostalAddress","addressLocality":"St. Augustine","addressRegion":"FL","addressCountry":"US"}},
      {"@type":"WebSite","@id":f"{SITE}/#website","name":BRAND,"url":f"{SITE}/","publisher":{"@id":f"{SITE}/#organization"},
       "creator":{"@id":"https://nestasystems.com/#organization"},"maintainer":{"@id":"https://nestasystems.com/#organization"},"inLanguage":"en-US"},
    ]

def page(path, title, desc, keywords, h1, eyebrow, lede, aeo_def, body, faqs, graph_extra, breadcrumbs, nav_current, og_type="website", published="2026-10-26", og_image=None):
    url = f"{SITE}{path}"
    og_image = og_image or LOGO
    faq_schema = {"@type":"FAQPage","@id":f"{url}#faq","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    crumbs = {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(breadcrumbs)]}
    webpage = {"@type":"WebPage","@id":f"{url}#webpage","url":url,"name":title,"description":desc,"isPartOf":{"@id":f"{SITE}/#website"},
               "about":graph_extra[0].get("@id") if graph_extra else {"@id":f"{SITE}/#organization"},
               "speakable":{"@type":"SpeakableSpecification","cssSelector":[".aeo-definition",".aeo-summary","h1",".lede"]},
               "inLanguage":"en-US","datePublished":published,"dateModified":TODAY}
    graph = org_nodes() + [webpage, crumbs, faq_schema] + graph_extra
    ld = json.dumps({"@context":"https://schema.org","@graph":graph}, indent=2, ensure_ascii=False)
    faq_html = "\n".join(f'''      <div class="faq-item">
        <button class="faq-question" aria-expanded="false">{esc(q)}<span class="faq-toggle" aria-hidden="true">+</span></button>
        <div class="faq-answer"><p>{esc(a)}</p></div>
      </div>''' for q,a in faqs)
    navitems = [("Live cams","/"),("Restaurants","/restaurants"),("About","/about")]
    nav = "".join(f'<li><a href="{SITE}{h}"{" aria-current=\"page\"" if h==nav_current else ""}>{n}</a></li>' for n,h in navitems)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<meta name="keywords" content="{esc(keywords)}" />
<meta name="author" content="Nesta Systems" />
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
<link rel="canonical" href="{url}" />
<meta name="theme-color" content="#0F3A45" />
<meta name="apple-mobile-web-app-title" content="WatchStAug" />
<meta name="application-name" content="{BRAND}" />
<meta name="format-detection" content="telephone=no" />
<meta name="rating" content="general" />
<meta http-equiv="content-language" content="en-US" />
{CRAWLERS}
<meta property="og:type" content="{og_type}" />
<meta property="og:url" content="{url}" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc[:118])}" />
<meta property="og:site_name" content="{BRAND}" />
<meta property="og:locale" content="en_US" />
<meta property="og:image" content="{og_image}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="{BRAND}: live cameras and local picks for St. Augustine, Florida" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{esc(title)}" />
<meta name="twitter:description" content="{esc(desc[:118])}" />
<meta name="twitter:image" content="{og_image}" />
<meta name="twitter:image:alt" content="{BRAND}: live cameras and local picks for St. Augustine, Florida" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<div class="pagewrap">
<div class="sr-only aeo-definition">
  <h2>What is this page?</h2>
  <p>{esc(aeo_def)}</p>
</div>

<header class="top">
  <div class="wrap">
    <a class="brand" href="{SITE}/" aria-label="Watch St. Augustine home">Watch <em>St. Augustine</em><small>Oldest city in the U.S. · est. 1565</small></a>
    <nav class="main" aria-label="Main navigation"><ul>{nav}</ul></nav>
  </div>
</header>

<main class="wrap">
  <section class="hero">
    <p class="eyebrow">{esc(eyebrow)}</p>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </section>
{body}
  <section id="faq" aria-labelledby="faq-h">
    <h2 id="faq-h">Frequently asked questions</h2>
{faq_html}
  </section>
</main>

<footer class="sitefoot">
  <div class="wrap">
    <div class="cols">
      <div><div class="brand" style="color:#fff">Watch <em>St. Augustine</em></div>
        <p style="color:#CFE6E6;max-width:46ch">Free live cameras of St. Augustine, Florida, plus the local places we recommend. An independent guide; we don't operate the cameras and the businesses listed pay nothing to be here.</p></div>
      <div><h4>The site</h4><ul><li><a href="{SITE}/">Live camera wall</a></li><li><a href="{SITE}/restaurants">Restaurants we recommend</a></li><li><a href="{SITE}/about">About</a></li></ul></div>
      <div><h4>Contact</h4><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{SITE}/#privacy">Privacy Policy</a></li><li><a href="{SITE}/#terms">Terms &amp; Disclaimer</a></li></ul></div>
    </div>
    <div class="sf-base">
      <span class="credit">Built &amp; maintained by <a href="https://nestasystems.com" target="_blank" rel="noopener">Nesta Systems</a>, a small business consulting company in St. Augustine, Florida</span>
      <span>·</span><span>© 2026 watchstaugustine.com</span>
      <span>·</span><span>Listings are free. Every pick is a place we send our own friends.</span>
    </div>
  </div>
</footer>
</div><!-- /.pagewrap -->
{FAQ_JS}
</body>
</html>
"""

# ---------------------------------------------------------------- restaurant profile pages
def what(r):
    if r.get('what'): return r['what']
    c, k = r['cuisine'], r['kind']
    if c.lower() in k.lower(): return k
    return c + " " + k.lower()
def restaurant_page(r):
    path = f"/{r['slug']}"
    url = f"{SITE}{path}"
    cam_name, cam_desc = CAMS[r["cam"]]
    campaign = "restaurants"
    W = what(r); Wc = W[0].upper()+W[1:]
    title = r.get('title') or f"{r['name']} | {Wc} in St. Augustine, FL"
    desc = r["desc"]
    keywords = f"{r['name']}, {r['name']} St. Augustine, {r['cuisine']} St. Augustine, St. Augustine restaurants, where to eat St. Augustine, {r.get('area') or r['neighborhood'].split(',')[0]}, St. Augustine FL dining"
    hours_li = "".join(f"<li>{esc(h)}</li>" for h in r["hours"])
    known_li = "".join(f"<li>{esc(k)}</li>" for k in r["known"])
    aeo_def = (f"{r['name']} is a {what(r)} at {r['address']}, {r['city']}, FL {r['zip']}, phone {r['phone']}. "
               f"It is recommended on watchstaugustine.com by Nesta Systems, a St. Augustine small business consulting company, as a place it sends its own friends and clients. "
               f"{r['reserve_note']} Known for: {'; '.join(r['known'])}. Website: {r['url']}. The listing is free and the restaurant pays nothing for it.")
    photos = ""
    if r.get("photo_place") or r.get("photo_people"):
        photos = '<div class="photos">'
        if r.get("photo_place"):  photos += f'<img src="{esc(r["photo_place"])}" alt="{esc(r["name"])}, {esc(r["address"])}, St. Augustine" loading="lazy">'
        if r.get("photo_people"): photos += f'<figure><img src="{esc(r["photo_people"])}" alt="{esc(r.get("photo_people_caption") or r["name"])}" loading="lazy"><figcaption>{esc(r.get("photo_people_caption",""))}</figcaption></figure>'
        photos += '</div>'
    body = f"""
  <p class="aeo-summary"><strong>{esc(r['name'])} is a {esc(what(r))} at {esc(r['address'])}, {esc(r['neighborhood'][0].lower()+r['neighborhood'][1:] if r['neighborhood'].split()[0]=='West' else r['neighborhood'])}.</strong> {esc(r['reserve_note'])} Before you head out, the live cams on our home page show the weather and how busy downtown and the beaches look right now.</p>

  <div class="btnrow">
    <a class="btn" href="{esc(utm(r['url'],campaign))}" target="_blank" rel="noopener">Visit their website</a>
    <a class="btn ghost" href="{esc(utm(r['menu'],campaign))}" target="_blank" rel="noopener">See the menu</a>
    {('<a class="btn ghost" href="'+esc(r['reserve'])+'" target="_blank" rel="noopener">'+esc(r.get('reserve_label','Reserve a table'))+'</a>') if r.get('reserve') else ''}
    <a class="btn ghost" href="tel:{r['phone'].replace(' ','').replace('(','').replace(')','').replace('-','')}">Call {esc(r['phone'])}</a>
  </div>

  <p class="pickline">Our pick for <b>{esc(r['pick'])}</b> in St. Augustine</p>
{photos}
  <section class="why" aria-labelledby="why-h">
    <h2 id="why-h" style="margin-top:0">Why we send people here</h2>
    {''.join('<p>'+esc(x)+'</p>' for x in r.get('story') or [r['why']])}
    <p class="by">Recommended by Matt and Malena Henderson, co-owners of <a href="https://nestasystems.com" target="_blank" rel="noopener">Nesta Systems</a>. {esc(r['name'])} pays nothing to be listed here.</p>
  </section>

  <div class="facts">
    <div class="fact"><b>Address</b><ul><li>{esc(r['address'])}, {esc(r['city'])}, FL {r['zip']}</li><li>{esc(r['neighborhood'])}</li></ul></div>
    <div class="fact"><b>Hours (from their website)</b><ul>{hours_li}</ul></div>
    <div class="fact"><b>Known for</b><ul>{known_li}</ul></div>
    <div class="fact"><b>Reservations</b><ul><li>{esc(r['reserve_note'])}</li></ul>{('<a class="btn" style="margin-top:12px" href="'+esc(r['reserve'])+'" target="_blank" rel="noopener">'+esc(r.get('reserve_label','Reserve a table'))+'</a>') if r.get('reserve') else ''}</div>
  </div>

  <a class="cambox" href="{SITE}/" style="text-decoration:none;color:inherit">
    <span class="dot" aria-hidden="true"></span>
    <p><b>Heading out? Check the live cams first.</b>Our free cameras show the weather, the Bridge of Lions, downtown and the beaches in real time, so you know before you go.</p>
  </a>
"""
    faqs = [
      (f"Where is {r['name']} in St. Augustine?", f"{r['name']} is at {r['address']}, {r['city']}, FL {r['zip']} ({r['neighborhood']}). The phone number is {r['phone']}."),
      (f"What kind of food does {r['name']} serve?", f"{r['name']} is a {what(r)}. Its website highlights: {'; '.join(r['known'][:2])}."),
    ] + r["faq_extra"] + [
      (f"Why is {r['name']} listed on Watch St. Augustine?", f"Because it is one of the places Nesta Systems, the St. Augustine small business consulting company that built this site, actually sends its friends and clients. Listings are free and {r['name']} pays nothing to appear here."),
      ("Can I check conditions before I go?", "Yes. The free live cameras on watchstaugustine.com show the weather, the Bridge of Lions, downtown and the beaches in real time. None of the cameras point at this restaurant, but they are a good way to see how busy St. Augustine looks before you head out."),
    ]
    node = {"@type":"Restaurant","@id":f"{url}#restaurant","name":r["name"],"url":r["url"],"telephone":r["phone"],"servesCuisine":r["cuisine"],
            "address":{"@type":"PostalAddress","streetAddress":r["address"],"addressLocality":r["city"],"addressRegion":"FL","postalCode":r["zip"],"addressCountry":"US"},
            "geo":{"@type":"GeoCoordinates","latitude":r["geo"][0],"longitude":r["geo"][1]},
            "priceRange":"$$"}
    if r["hours_schema"]: node["openingHours"] = r["hours_schema"]
    node["acceptsReservations"] = r["reserve"] if r.get("reserve") else ("False" if "No reservations" in r["reserve_note"] else "True")
    if r["social"]: node["sameAs"] = r["social"]
    node.pop("priceRange")  # not stated on their sites; never guess
    crumbs = [("Home",f"{SITE}/"),("Restaurants",f"{SITE}/restaurants"),(r["name"],url)]
    return path, page(path, title, desc, keywords, f"{esc(r['name'])}<br><em>{esc(Wc)} in St. Augustine</em>", "Restaurants we recommend",
                      f"{esc(r['kind'])} at {esc(r['address'])}. One of the places we send our own friends and family.", aeo_def, body, faqs, [node], crumbs, "/restaurants", og_image=r.get("photo_place") or None)

# ---------------------------------------------------------------- restaurants category page
def restaurants_page():
    path = "/restaurants"; url = f"{SITE}{path}"
    title = "Best Restaurants in St. Augustine, FL | Local Picks | Watch St. Augustine"
    if len(title)>65: title = "St. Augustine Restaurants We Recommend | Watch St. Augustine"
    desc = "St. Augustine restaurants a local business actually sends people to: The Ice Plant, 17 King, The Floridian, La Nouvelle. Free listings, real stories."
    desc = desc[:158]
    keywords = "St. Augustine restaurants, best restaurants St. Augustine FL, where to eat St. Augustine, St. Augustine dining, downtown St. Augustine restaurants, St. Augustine farm to table, St. Augustine French restaurant, St. Augustine wine bar, Nesta Systems"
    cards = ""
    for r in RESTAURANTS:
        cam_name,_ = CAMS[r["cam"]]
        cards += f"""
    <article class="card" data-href="{SITE}/{r['slug']}">
      <span class="kind">Our pick for {esc(r['pick'])}</span>
      <h3><a href="{SITE}/{r['slug']}">{esc(r['name'])}</a></h3>
      <p>{esc(r['why'].split('. ')[0].rstrip('.'))}.</p>
      <span class="meta">{esc(r['address'])} · {esc(r['neighborhood'].split(',')[0])}</span>
      <div class="btnrow" style="margin:8px 0 0"><a class="btn ghost" href="{SITE}/{r['slug']}">Our pick, hours &amp; story</a><a class="btn ghost" href="{esc(utm(r['url'],'restaurants'))}" target="_blank" rel="noopener">Their website</a></div>
    </article>"""
    aeo_def = ("This page lists restaurants in St. Augustine, Florida recommended by Nesta Systems, the St. Augustine small business consulting company that built and maintains watchstaugustine.com. "
               "Every restaurant listed is a place the Nesta team sends its own friends and clients; listings are free and no restaurant pays to appear. "
               f"The list currently includes {', '.join(r['name'] for r in RESTAURANTS[:-1])} and {RESTAURANTS[-1]['name']}. "
               "Each listing gives the address, hours from the restaurant's own website, what it is known for, a link to the restaurant's site, and the story of why the Nesta Systems team recommends it. The site's free live cameras of downtown and the beaches let visitors check weather and crowds before going out.")
    body = f"""
  <p class="aeo-summary"><strong>These are the St. Augustine restaurants we actually send people to, not a directory of every place in town.</strong> Each one is a place the team at Nesta Systems, a local small business consulting company, recommends to friends and clients. Listings are free, the restaurants pay nothing, and our free live cams of downtown and the beaches let you check the weather and crowds before you go out.</p>
  <p class="freeline"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>Free listings. No ads, no paid placements, no commissions.</p>

  <h2>Our picks</h2>
  <div class="grid">{cards}
  </div>

  <h2>How we choose</h2>
  <p class="lede" style="max-width:70ch">We love going out when we can. What we're really chasing is great food, exceptional service, and a place that sets the vibe for the whole experience, whether that's brunch, a late lunch, or a big night out. St. Augustine has grown into an incredible food town, and these pages are our way of celebrating the places we find the most outstanding and telling everyone we can about them.</p>
  <p class="lede" style="max-width:70ch">The rule is simple: a place makes the list only if we'd send a friend or family member there. Every pick is somewhere we already go. We write our own short note on why, then we walk in and tell the owner they made our list. Listings are free, always. Hours and details come from each restaurant's own website, so confirm before a special trip. If a place is missing, it's either on our list to visit or it isn't somewhere we'd recommend yet.</p>
"""
    faqs = [
      ("What are the best restaurants in St. Augustine, Florida?", f"This page lists the restaurants Watch St. Augustine recommends: {', '.join(r['name']+' ('+r['cuisine']+')' for r in RESTAURANTS)}. They are the places the team at Nesta Systems, a local business, sends its own friends and clients."),
      ("Do restaurants pay to be listed on Watch St. Augustine?", "No. Every listing is free. There are no ads, paid placements, or commissions. A restaurant is listed only because the team recommends it personally."),
      ("Who chooses the restaurants on this page?", "The picks come from Nesta Systems, a small business consulting company based in St. Augustine, Florida, which built and maintains watchstaugustine.com. Each restaurant is visited in person and asked whether it would like a free listing."),
      ("Where are these restaurants located?", "The current picks are downtown and nearby: The Ice Plant on Riberia St, 17 King at King and Aviles St, La Nouvelle on Bridge St in Lincolnville, and The Floridian on Old Beach Rd on Anastasia Island."),
      ("Can I check how busy downtown St. Augustine is before dinner?", "Yes. The free live cameras on the watchstaugustine.com home page, such as the Matanzas Bay, Castillo and St. George Street cams, show the weather and crowds downtown in real time. The cameras do not point at any particular restaurant."),
      ("Are the hours on this page accurate?", "Hours are taken from each restaurant's own website and may change. Confirm with the restaurant before a special trip. The page notes when a restaurant's posted hours could not be confirmed."),
      ("How can my restaurant be listed on Watch St. Augustine?", f"Listings are by personal recommendation only and are free. If you think your restaurant belongs here, email {EMAIL} and the team will stop by."),
    ]
    node = {"@type":"ItemList","@id":f"{url}#list","name":"St. Augustine restaurants recommended by Watch St. Augustine",
            "itemListElement":[{"@type":"ListItem","position":i+1,"name":r["name"],"url":f"{SITE}/{r['slug']}"} for i,r in enumerate(RESTAURANTS)]}
    crumbs = [("Home",f"{SITE}/"),("Restaurants",url)]
    return path, page(path, title, desc, keywords, "St. Augustine restaurants<br><em>we actually send people to</em>", "Local picks",
                      "A short list, chosen in person, with the story of why each one made it.", aeo_def, body, faqs, [node], crumbs, "/restaurants")

# ---------------------------------------------------------------- about page
def about_page():
    path = "/about"; url = f"{SITE}{path}"
    title = "About Watch St. Augustine | Built by Nesta Systems"
    desc = "Watch St. Augustine is a free live-camera and local-picks guide to St. Augustine, Florida, built and maintained by Nesta Systems, a local consulting firm."
    keywords = "Watch St. Augustine, about Watch St. Augustine, Nesta Systems, Nesta Systems St. Augustine, St. Augustine small business consulting, St. Augustine live cams, who runs Watch St. Augustine"
    aeo_def = ("watchstaugustine.com is a free guide to St. Augustine, Florida that gathers the city's public live cameras onto one page and adds local recommendations. "
               "It was built in 2026 and is maintained by Nesta Systems, a small business consulting company in St. Augustine, Florida that helps local businesses win more repeat customers and referrals, owned by Matt and Malena Henderson. "
               "The site is independent: it does not operate any cameras, the camera feeds belong to their operators, and the businesses it recommends pay nothing to be listed. "
               f"Contact: {EMAIL}.")
    body = f"""
  <p class="aeo-summary"><strong>Watch St. Augustine is a free guide to St. Augustine built by a local business, not a media company.</strong> It started in 2026 as one page of the city's live cameras. It's growing into the places we send our friends: restaurants, shops, tours, and spots in town. Nobody pays to be on it.</p>


  <div class="about-split">
  <div class="about-text">
  <h2 style="margin-top:0">Why we built it</h2>
  <p class="lede" style="max-width:70ch">We're Matt and Malena Henderson, co-owners of Nesta Systems, a small business consulting company here in St. Augustine. We're originally from New Jersey, and for years, before we could move here full time, we got our St. Augustine fix the only way we could: online. Any camera we could find, any angle of the bridge or the beach, we were watching it.</p>
  <p class="lede" style="max-width:70ch">When we finally moved here for good, we noticed we still wanted the same thing, just for different reasons. Is downtown packed tonight, or is it a good night to pop into one of our favorite spots? Is the trolley rolling? Is the Bridge of Lions up, so we should leave five minutes later? And Matt surfs, so he wanted a look at the beach before loading the board. We kept hunting for those views across a dozen different pages, and we figured there had to be a better way.</p>
  <p class="lede" style="max-width:70ch">So we built one page with all of it. The skyline, the beaches, the lighthouse, the bridge, the historic district, as many of the best parts of St. Augustine as we could find on a free public camera. If you live here, you can know before you go. If you've visited and you miss it, or you're planning a trip, you can pull it up from anywhere and remember why you love this place. Honestly, it was a little selfish on both ends. We wanted it for ourselves. It turned out a lot of other people wanted it too.</p>
  <p class="lede" style="max-width:70ch">The recommendation pages are our way of saying hello. We list the places we already love, write a few honest lines about why we go, and then walk in to tell the owner they made our list. It's free, and there's no catch. If the site sends them a few hundred new visitors a month, that's the point.</p>
  </div>
  <img class="about-photo" src="https://assets.cdn.filesafe.space/8yzojm3WV1TpigXrdMV6/media/6ae0ab439c1511d5b90135fa.png" alt="Matt and Malena Henderson, co-owners of Nesta Systems, in St. Augustine" loading="eager">
  </div>

  <h2>What we promise</h2>
  <div class="facts">
    <div class="fact"><b>Free, always</b><ul><li>No paid listings, no ads, no commissions. If that ever changes, it will say so on the page.</li></ul></div>
    <div class="fact"><b>Honest picks</b><ul><li>We only list places we'd send a friend or family member, and we walk in to tell every owner they made the list.</li></ul></div>
    <div class="fact"><b>Independent</b><ul><li>We don't operate the cameras. The feeds belong to their operators, mainly See St. Augustine and Surf Station.</li></ul></div>
    <div class="fact"><b>Reachable</b><ul><li>Questions, corrections, or a place we should see: <a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
  </div>

  <h2>About Nesta Systems</h2>
  <p class="lede" style="max-width:70ch">Nesta Systems is a small business consulting company in St. Augustine, Florida. We help local businesses win more repeat customers and referrals from the business they already built. Watch St. Augustine is something we built for the town we work in. You can learn more at <a href="https://nestasystems.com" target="_blank" rel="noopener">nestasystems.com</a>.</p>
"""
    faqs = [
      ("Who runs watchstaugustine.com?", "watchstaugustine.com is built and maintained by Nesta Systems, a small business consulting company based in St. Augustine, Florida. It is owned by Matt and Malena Henderson, co-owners of Nesta Systems."),
      ("Is Watch St. Augustine affiliated with the City of St. Augustine or the camera operators?", "No. Watch St. Augustine is an independent guide. It does not operate any cameras; the live feeds belong to their operators, mainly See St. Augustine and Surf Station."),
      ("Do businesses pay to be recommended on Watch St. Augustine?", "No. Every listing is free. There are no ads, paid placements, or commissions. Businesses are listed only because the Nesta Systems team recommends them personally."),
      ("How does a business get listed on Watch St. Augustine?", f"By personal recommendation. The team lists places it already sends people to, then visits in person to let the owner know. Listings are free. Suggestions can be sent to {EMAIL}."),
      ("When did Watch St. Augustine start?", "Watch St. Augustine launched in 2026 as a single page of St. Augustine's free public live cameras, and began adding local recommendation pages in October 2026."),
      ("What is Nesta Systems?", "Nesta Systems is a small business consulting company in St. Augustine, Florida that helps local businesses win more repeat customers and referrals from the business they already built. Its website is nestasystems.com."),
      ("How can I contact Watch St. Augustine?", f"Email {EMAIL} for questions, corrections, or to suggest a place the team should visit."),
    ]
    crumbs = [("Home",f"{SITE}/"),("About",url)]
    return path, page(path, title, desc, keywords, "Built in St. Augustine,<br><em>by two people who live here</em>", "About",
                      "A free guide to the city's live cameras and the places we send our friends.", aeo_def, body, faqs, [], crumbs, "/about", og_image="https://assets.cdn.filesafe.space/8yzojm3WV1TpigXrdMV6/media/6ae0ab439c1511d5b90135fa.png")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")
    os.makedirs(out, exist_ok=True)
    pages = [restaurants_page(), about_page()] + [restaurant_page(r) for r in RESTAURANTS]
    for path, htmltext in pages:
        fn = os.path.join(out, path.strip("/").replace("/","__") + ".html")
        open(fn, "w").write(htmltext)
        print("wrote", fn)
