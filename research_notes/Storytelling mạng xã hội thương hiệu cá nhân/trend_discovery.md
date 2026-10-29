# Trend discovery for a Vietnam-focused creator (YouTube first, TikTok/Facebook second), as usable from a Claude Code agent

Tags: [OFFICIAL] = platform or government doc. [STUDY] = research. [PRACTITIONER] = blog, vendor, or creator guide. [BG] = background knowledge, not re-verified this session. [TESTED] = fetched this session (2026-10-29) with WebFetch or curl; the tag says which tool and what came back.

Test method: `curl -L` with a desktop Chrome User-Agent (records status, size, and whether the data sits in the raw HTML), plus WebFetch on the key pages. WebFetch turns the page into markdown and summarizes it. A page can carry data in inline JSON that curl sees but WebFetch drops. When the two tools disagree, the note says so.

---

## 1. Trend sources and their status (late 2026): what the agent can actually reach

### Takeaway
For WebFetch/curl with no login, the reliable Vietnam sources are: **Google Trends "Trending now" RSS** (`trends.google.com/trending/rss?geo=VN`), **Google News RSS (vi/VN)**, **news-site RSS** (VnExpress tin-xem-nhieu/tin-noi-bat, Tuổi Trẻ, Thanh Niên, Kenh14), the **Wikimedia top-pageviews API for vi.wikipedia**, the **Google/YouTube autocomplete endpoint**, and **trends24.in** for X. These were all server-rendered or JSON and returned data this session. YouTube's Trending page is gone (retired July 2025). YouTube Charts and TikTok Creative Center are JS shells, unusable without a browser. YouTube Studio Trends/Inspiration need login, so the user has to check them and paste results in.

### Access matrix (tested 2026-10-29)

| Source | URL | Result this session | Usable by agent? |
|---|---|---|---|
| Google Trends Trending-now RSS | `https://trends.google.com/trending/rss?geo=VN` | [TESTED curl] 200, `text/xml`, **10 items**, each with `<title>`, `<ht:approx_traffic>` (e.g. "200+", "100+"), `<pubDate>`, `<ht:picture>`, and 1–3 `<ht:news_item>` (title, url, source). Sample items: "adelaide utd đấu với lion city", "chôn cất", "gian lận", "nhà thầu", "hồ văn cường", "mùa đông", "liverpool vs chelsea carabao cup" | **YES, primary source** |
| Old Google Trends daily RSS | `https://trends.google.com/trends/trendingsearches/daily/rss?geo=VN` | [TESTED curl] **404**, deprecated | NO, don't use |
| Google Trends "Trending now" page | `https://trends.google.com/trending?geo=VN` | [TESTED WebFetch] only nav + title "Trending Now - Google Trends"; WebFetch reported a JS shell. [TESTED curl] 200, 1.26 MB, and the raw HTML **does** hold the data in inline JS arrays, e.g. `"hồ văn cường",null,"VN",[1793252400],null,null,200,null,500,...` (term, geo, start timestamp, then fields that look like volume 200 and +500% growth; that reading of the fields is my inference) | Partly: curl + parsing only. Prefer the RSS |
| Google Trends Explore (compare terms, 0–100 over time) | `https://trends.google.com/trends/explore?geo=VN&q=...` | Not tested. [BG] Charts come from JS widgets behind a token API. The unofficial pytrends library is often rate-limited (429) | NO via WebFetch; user checks it by hand |
| Google Trends Year in Search | `https://trends.withgoogle.com/year-in-search/` (per-country pages) | Not tested [BG]. Annual lists, released around December | Seasonal planning only |
| YouTube Trending page | `https://www.youtube.com/feed/trending?gl=VN` | [TESTED curl] 200, but the payload only holds `browseId":"FEwhat_to_watch"` (the home feed). No trending list, which matches the retirement | **DEPRECATED** |
| YouTube Charts | `https://charts.youtube.com/charts/TrendingVideos/vn`, `/charts/TopVideos/vn/weekly`, `/podcasts` | [TESTED curl] 200, about 68 KB, title " YouTube music charts ", body is only `ytcsi` bootstrap JS. [TESTED WebFetch] returned only the heading "YouTube music charts", no entries | NO (JS shell). Not checked: whether a VN chart exists for each category |
| YouTube Gaming Explore | `https://www.youtube.com/gaming` | [TESTED curl] 200, 1 MB, contents not parsed | Unverified |
| YouTube / Google autocomplete | `https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=vi&gl=VN&q=<seed>` | [TESTED curl] 200, clean JSON. `q=giá vàng` gave "giá vàng hôm nay", "giá vàng ngày 29 tháng 10", "giá vàng trực tiếp"… `client=youtube` returns JSONP `window.google.ac.h([...])` | **YES**, for demand validation and title wording. [BG] Undocumented, unofficial endpoint, could change |
| TikTok Creative Center, Trends > Hashtags | `https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en?region=VN` | [TESTED curl] 200, 21 KB. Page title is now **"TikTok One Creative Suite"**. The HTML has the header ("Top Ads, Trends, Creative Tools… Log in") and a React-Router `loaderData` stub with `"tt4bUID":"0"`. **No hashtag names in the HTML**, so the data loads client-side | NO (JS-rendered). User checks it in a browser |
| Google News RSS (VN) | `https://news.google.com/rss?hl=vi&gl=VN&ceid=VN:vi` | [TESTED curl] 200, 82 KB XML. Top stories from Thanh Niên, Lao Động, Tiền Phong, VietNamNet… | **YES** |
| VnExpress most-read | `https://vnexpress.net/tin-xem-nhieu` (HTML) and `https://vnexpress.net/rss/tin-xem-nhieu.rss` | [TESTED curl] both 200 (the first attempt timed out and a retry worked, so expect slowness). RSS title "Tin xem nhiều - VnExpress RSS" | **YES**. The most-read RSS is the best Vietnamese "what people actually read" signal |
| VnExpress featured | `https://vnexpress.net/rss/tin-noi-bat.rss` | [TESTED curl] 200 | YES |
| Tuổi Trẻ | `https://tuoitre.vn/rss/tin-moi-nhat.rss` | [TESTED curl] 200, 41 KB XML (titles in CDATA) | YES (latest news, not most-read) |
| Thanh Niên | `https://thanhnien.vn/rss/home.rss` | [TESTED curl] 200, 70 KB | YES (latest) |
| Kenh14 (youth/showbiz) | `https://kenh14.vn/rss/home.rss` | [TESTED curl] 200, 69 KB. `kenh14.vn/home.rss` → 404 | YES. Good for Gen Z, showbiz, viral |
| Znews | `https://znews.vn/xem-nhieu-nhat.html` | [TESTED curl] **404**. Homepage `znews.vn` 200 | Homepage only. Most-read URL not found |
| Wikipedia top pageviews (vi) | `https://wikimedia.org/api/rest_v1/metrics/pageviews/top/vi.wikipedia/all-access/{YYYY}/{MM}/{DD}`; month: `.../{YYYY}/{MM}/all-days` | [TESTED curl] 200 JSON for 2026/10/27 (data lags about 1 day; use D-1 or D-2). Rank 1 "Hồ_Hoàn_Kiếm" 22,747 views… plus "BigBang_(nhóm_nhạc)", "Harry_Kane", "Quả_bóng_vàng_châu_Âu", "ChatGPT". `2026/09/all-days` → 200 | **YES**. Free, absolute counts. **Filter out** "Trang_Chính", "Đặc_biệt:*", and bot or NSFW anomalies (rank 4 that day was an NSFW article, almost certainly bot or crawler traffic). Send a descriptive User-Agent [BG: Wikimedia API etiquette] |
| X/Twitter trends for VN (third-party) | `https://trends24.in/vietnam/` | [TESTED curl] 200, server-rendered `class=trend-link`. Items: "NIVEA THIAMIDOL WITH LINGLING", "#NIVEASuperGlowXLingling", "$SPHERE"… | Yes, but **low value for VN**: dominated by K-pop/T-pop fandom and brand hashtag campaigns, not general Vietnamese interest |
| Reddit r/VietNam JSON | `https://www.reddit.com/r/VietNam/top.json?t=day` | [TESTED curl] **403** | NO |
| Threads search | `https://www.threads.com/search?q=...` | [TESTED curl] 200, title "Threads", contents not checked (likely a login wall or JS) | Assume NO |
| Facebook trending | — | Not tested. [BG] No public trending surface. Graph API needs app review; CrowdTangle shut down Aug 2024 | NO. User reports by hand |
| Exploding Topics | `https://explodingtopics.com/` | [TESTED curl] 200, 465 KB homepage, contents not parsed. [BG] Paid vendor, US/English-centric, little VN coverage | Low value for VN |
| AnswerThePublic | `https://answerthepublic.com/` | [TESTED curl] 200 homepage. [BG] Searches need an account and are capped on the free tier | NO for automation. The autocomplete endpoint above covers the same need |
| Glimpse | — | Not tested. [BG] Paid Chrome extension/API that adds absolute volumes to Google Trends | NO |

### Cited findings
- YouTube announced in July 2025 that it would retire the Trending page and the "Trending Now" list, with removal around **21–22 July 2025**. The stated reason was a steady fall in visits over five years, since viewers now find trends through recommendations, search, Shorts, comments, and communities. [OFFICIAL, reported] — [9to5Google](https://9to5google.com/2025/07/10/youtube-trending-page-removal/); [Android Authority](https://www.androidauthority.com/youtube-trending-removed-3576664); [PPC Land](https://ppc.land/youtube-closes-trending-page-after-a-decade-of-operation/); [Storyboard18](https://www.storyboard18.com/brand-marketing/youtube-retires-trending-page-after-nearly-a-decade-75844.htm)
- The replacement is **category-specific YouTube Charts**. At launch these were Trending Music Videos, Weekly Top Podcast Shows, and Trending Movie Trailers, with "more categories over time". The **Gaming Explore page** stays the home for trending gaming. Non-personalized browsing remains in the Explore menu. [OFFICIAL, reported] — [Gigazine](https://gigazine.net/gsc_news/en/20250711-youtube-rids-of-trends-page); [BetaNews](https://betanews.com/2025/07/11/youtube-is-dropping-the-trending-page-as-it-shakes-up-content-discovery/)
- **YouTube Studio > Analytics > Trends tab** (login required). Cards: **Top searches** (from your audience and saves, last 28 days), **Breakout videos** (well-performing videos from creators similar to your channel), **Recent videos** (topics your audience watched, last 28 days), **Content gaps for Shorts**. Topic search shows **Audience interest** from "very low" to "very high", based on videos watched >1,000 times/week over the last 28 days. A **content gap** = "viewers can't find enough quality search results for a specific search" (no results, no exact match, or old/low-quality results). Some insights are limited by country, language, and device. A Studio redesign rolling out from July 2026 may change the layout. [OFFICIAL] [TESTED WebFetch] — [YouTube Help: Explore trends on YouTube](https://support.google.com/youtube/answer/11962757)
- **YouTube Studio Inspiration tab**: reached through Content > "Get inspired". It gives AI-generated ideas, titles, thumbnails, outlines, and hooks, and is **desktop-only and English-only**. Earlier it was the renamed "Research" tab under Analytics. At launch it was unavailable in the EU, UK, Switzerland, and India. [OFFICIAL via search snippet, page not fetched] — [YouTube Help: Inspiration tab](https://support.google.com/youtube/answer/15575509?hl=en); [Social Media Today](https://www.socialmediatoday.com/news/youtube-adds-ai-assistance-tools-creators/718024/)
- **What Google Trends measures**: each data point is divided by total searches for that place and time, then scaled 0–100. It shows **relative interest, not volume**. Two regions with the same score can have different absolute volumes. The data is a **sample**. Low-volume terms show as 0. Repeat searches by one person, and queries with apostrophes or special characters, are removed. **Searches from Google's AI Mode and AI Overviews are excluded.** Noise is added for privacy, so spikes on low-interest terms may be noise. Google advises comparing against common reference terms to judge size, and treating Trends as "one data point among others". Time zone is UTC for ranges ≥30 days and local for ≤7 days. [OFFICIAL] [TESTED WebFetch] — [Google Trends Help: FAQ about Trends data](https://support.google.com/trends/answer/4365533?hl=en)
- Google Trends RSS at `/trending/rss?geo=VN` works and carries `ht:approx_traffic` buckets plus linked news articles. The old `/trends/trendingsearches/daily/rss` path returns 404. [TESTED curl] — https://trends.google.com/trending/rss?geo=VN
- TikTok's help center (updated July 2026) describes Creative Center as a free, public resource. "Trends" shows trending hashtags. Logging in adds a Personal Profile (My Collections, Material Library). [OFFICIAL via search snippet] — [TikTok Ads Help: About Creative Center](https://ads.tiktok.com/help/article/creative-center?lang=en-GB). Social Champ says login is required to use features, which conflicts with this [PRACTITIONER] — [Social Champ](https://www.socialchamp.com/blog/tiktok-creative-center). Novo Ads says hashtag data has been **narrowed to ranked lists by industry** and free-text hashtag search may not work as older guides describe [PRACTITIONER, unverified] — [Novo Ads](https://novoads.ai/en/blog/tiktok-creative-center)
- The TikTok Creative Center page now carries the title "TikTok One Creative Suite", and the trend data is not in the server HTML. [TESTED curl] — https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en?region=VN

### Inferences
- **Recommended agent pipeline, in priority order:** (1) Google Trends RSS VN, for search spikes with linked news. (2) VnExpress `tin-xem-nhieu.rss` + Google News RSS, for what people read and why. (3) Kenh14 RSS for youth, showbiz, and viral topics. (4) Wikimedia top vi.wikipedia for D-1 plus the monthly list, which catches explainer-worthy entities (people, places, concepts) and evergreen interest. (5) Autocomplete with `ds=yt&gl=VN&hl=vi`, run on each candidate to check YouTube demand and harvest title wording. (6) Ask the user to paste their **YouTube Studio Trends tab** (Top searches, Breakout videos, Content gaps) and **TikTok Creative Center** hashtags/songs for VN. Only the user can see these, and the Studio data is audience-specific, so it is the highest-fit signal.
- The RSS returns only about 10 items, mostly sports fixtures, crime/court news, and celebrity names. For most niches, the agent should use it as a **seed list and connector to news**, not as a list of ideas.
- `approx_traffic` buckets like "200+" are small for Vietnam, which suggests the RSS surfaces breakouts of any size. Pair it with Wikipedia absolute pageviews and autocomplete presence before calling something big.
- Autocomplete strings that include today's date (e.g. "giá vàng ngày 29 tháng 10") mark a **daily recurring query**: big volume, near-zero shelf life, served better by news sites than by a creator.

### Gaps
- Could not confirm whether YouTube Charts publishes Trending Videos/Trailers/Podcasts **for Vietnam**: the page is a JS shell. The internal `youtubei` browse API behind charts.youtube.com was not tested.
- Could not confirm by testing what Creative Center shows for VN without login, or whether a JSON endpoint is reachable. Sources conflict on login.
- Google announced an official Google Trends API (alpha, 2025) [BG]. Its 2026 availability and VN coverage were not verified.
- Facebook/Threads trending: no public machine-readable source found or tested successfully.
- Spotify Charts VN (`charts.spotify.com`) and podcast charts were not tested. [BG] Spotify Charts now needs login for full data.

---

## 2. How to judge a trend for a specific channel

### Takeaway
Score each candidate on **fit (niche/pillar/audience) × timing (spike vs rising vs seasonal vs evergreen) × competition (content gap) × angle (what only this channel can say) × production time vs half-life**. Spikes in news-driven searches usually die before a researched long-form YouTube video can ship. They suit Shorts/TikTok reactions, or a long-form "why it keeps happening" video built on the underlying mechanism.

### Cited findings
- Google Trends values are relative and sampled, and spikes on low-interest terms can be privacy noise. Google says to benchmark against common terms and not treat Trends as a popularity poll. [OFFICIAL] — [Google Trends Help](https://support.google.com/trends/answer/4365533?hl=en)
- YouTube's own model for "is there room for my video": a **content gap** is when viewers find no results, no exact match, or only old/low-quality videos. "Audience interest" in the Trends tab measures watch activity (videos >1,000 views/week, last 28 days), scoped to **your** audience. [OFFICIAL] — [YouTube Help 11962757](https://support.google.com/youtube/answer/11962757)
- YouTube says viewers now find trends mostly through **personalized recommendations, search, Shorts, comments**, not a global trending list. [OFFICIAL, reported] — [9to5Google](https://9to5google.com/2025/07/10/youtube-trending-page-removal/)
- "Breakout videos from creators similar to your channel" is YouTube's built-in "what's working in my niche now" signal. [OFFICIAL] — [YouTube Help 11962757](https://support.google.com/youtube/answer/11962757)

### Inferences (scoring rubric for the skill; my synthesis, not an official framework)
- **Fit gate (pass/fail first):** Does the topic map to at least one channel pillar? Would the channel's stated audience search for or click it? If the only link is "it's popular", reject it. Off-niche viral topics bring in viewers who don't come back, which muddies recommendation signals [BG].
- **Lifespan classes** (judge from Trends RSS pubDate, news volume, and autocomplete):
  - *Spike* (match result, scandal, celebrity death or arrest, viral clip): half-life of hours to about 2 days. Short-form only, or skip.
  - *Rising* (new AI tool, new regulation taking effect, new product): weeks. Long-form fits if the video can ship in 3–7 days.
  - *Seasonal/calendar* (Tết, Trung thu, thi THPT, Black Friday, mùa mưa bão, World Cup): predictable, so **pre-produce**. Use Year in Search and last year's monthly Wikipedia tops to plan.
  - *Evergreen with a news hook* (personal finance after a gold-price spike, health after an outbreak story): best ROI for long-form, since the hook expires but the core keeps getting searched.
- **Competition check (agent-doable):** use autocomplete with `ds=yt`. If many long-tail variants show up, demand is real. WebSearch `site:youtube.com <topic>` gives a rough count of recent videos; if top results are from big VN news channels (VTV, VnExpress, Thanh Niên), a creator can't win "the news", only the explanation or a personal angle.
- **Production-time vs half-life rule:** if estimated production days exceed about half the remaining interest window, change format (Shorts/TikTok take, Community post) or change angle to the evergreen mechanism.
- **Angle test ("content tilt"):** state in one sentence what this channel can say that a news site can't: expertise, lived experience, a local or Vietnamese perspective on a global story, a data comparison, a how-to. No sentence means no video.
- Fit to scale for a VN creator: a VN-specific topic in Vietnamese beats an English global trend, since Vietnamese-language supply is thinner [BG/inference].

### Gaps
- Found no official YouTube guidance with numbers on how long "timely" videos keep getting traffic, and no study measuring trend half-life for VN audiences.
- Found no rigorous study (only practitioner opinion) on whether off-niche trend videos hurt channel-level recommendations.

---

## 3. Newsjacking ethics and policy risks

### Takeaway
The biggest risks are: (a) cashing in on tragedies or disasters, (b) misinformation on breaking events before facts settle, (c) titles or thumbnails that promise more than the video gives (YouTube's "malicious clickbait"), (d) reusing broadcaster or news footage (Content ID claims), and (e) Vietnam's legal regime on online content, including Decree 147/2024 account rules and penalties for false or "harmful" information. The skill should hard-flag these categories and push them toward careful explainer framing or skipping.

### Cited findings
- YouTube's spam, deceptive practices and scams policy bans "content, metadata, or behavior designed to take advantage of the YouTube community". It covers thumbnails and applies to unlisted and private content too. Example of **malicious clickbait**: "maliciously misleading titles, thumbnails, descriptions, or imagery" that trick viewers into clicking something that doesn't deliver what was promised, e.g. a title promising a full sports match when the video is only a clip. [OFFICIAL] [TESTED WebFetch] — [YouTube Help: Spam, deceptive practices & scams policies](https://support.google.com/youtube/answer/2801973?hl=en)
- **Decree 147/2024/NĐ-CP** (internet services and online information management) **took effect 25/12/2024**. Social-network accounts must be **verified with a Vietnamese mobile number** (Art. 23(3)(e), Art. 27(3)(b)). Foreign platforms may use a personal ID number only if the user has no VN phone number. **Only verified accounts may post, comment, livestream, or share**. Accounts livestreaming **for commerce** must verify with a personal ID number. Existing accounts had **90 days** to comply (the window closed around late March 2025). One source says accounts suspended **3+ times** for illegal content get permanently locked. [OFFICIAL, via secondary summaries; the decree text was not fetched] — [hatinh.gov.vn](https://hatinh.gov.vn/vi/bai-viet/xac-thuc-tai-khoan-mang-xa-hoi-bang-so-dien-thoai-di-dong); [Thư viện Pháp luật](https://thuvienphapluat.vn/hoi-dap-phap-luat/huong-dan-xac-thuc-tai-khoan-mang-xa-hoi-tu-25122024-138041193.html); [LSVN: livestream](https://lsvn.vn/chi-duoc-livestream-khi-da-xac-thuc-tai-khoan-mang-xa-hoi-a149868.html); [LSVN: 90 ngày](https://lsvn.vn/tai-khoan-mang-xa-hoi-phai-xac-thuc-trong-90-ngay-a152520.html). Sources differ slightly on which clauses cover the transition (Art. 82(10)–(11) is cited). Check against vanbanphapluat.gov.vn.
- [BG] YouTube's misinformation policies (https://support.google.com/youtube/answer/10834785) ban content contradicting authorities on specific harm areas (medical, elections, manipulated media). For breaking news, YouTube shows authoritative sources and info panels. Not re-fetched this session.
- [BG] Vietnam's 2018 Cybersecurity Law and Decree 15/2020 (amended by Decree 14/2022) set administrative fines for posting false or distorted information online. Police routinely fine individuals for posting false information about disasters, epidemics, and accidents. Not re-verified this session. A newer consolidated cybersecurity law (2025) may change this; status not verified.
- [BG] Footage from VTV and other broadcasters, and from news-agency video, is commonly registered in Content ID. Vietnamese IP law has no US-style "fair use" doctrine, only narrower exceptions for quotation and news reporting. Not verified this session.

### Inferences (red-flag list for the skill)
- **Hard-flag topics:** deaths, accidents, disasters (storms and floods are frequent in VN Sept–Nov), crimes involving named private people, child victims, suicides, ongoing court cases, epidemics, politics, leaders, sovereignty or border issues, religion, ethnicity. The skill should either refuse the "trend-ride" framing or suggest a service angle (how to stay safe, how to help, how the system works) with no monetized hook. Tone: no glee, no "SHOCKING". Check facts against at least two established outlets before scripting.
- **Names in trending queries** (e.g. a person's name with "chôn cất", "gian lận", "nhà thầu" seen in today's RSS) are often crime, scandal, or funeral stories about real people. Default to skip unless the channel is a news or legal explainer, and never speculate on guilt.
- **Title rule from YouTube policy:** the title and thumbnail must describe what the video actually contains. Curiosity gaps are fine. A promise the video doesn't deliver is not.
- **Footage:** use your own visuals, licensed stock, screenshots of headlines with attribution (low risk, not zero), or narration over graphics. Avoid re-uploading TV clips.
- **Deliverability for VN creators:** publishing accounts must be Decree-147-verified. Commercial livestreams need ID verification.

### Gaps
- The Decree 147 text, and any 2025–2026 amendments or the new Cybersecurity Law's content provisions, were not fetched from an official legal database.
- YouTube's 2024–2025 "egregious clickbait" enforcement push (first announced for India) was not verified for Vietnam.

---

## 4. Turning a trend into a video idea and title in the channel's style

### Takeaway
Use **Trend × Pillar × Angle × Format**. Take the trend's underlying question ("why", "how", "what does it mean for me"), pass it through one channel pillar, apply the channel's unique angle, then pick the format by half-life (Short/TikTok now, long-form for the evergreen mechanism). Write the title in the channel's voice, using real search wording from autocomplete.

### Cited findings
- YouTube's own idea surfaces are built on audience-specific signals: top searches, breakout videos from similar channels, and content gaps where quality results are missing. The Inspiration tab generates ideas, titles, outlines, and hooks, but only in English. [OFFICIAL] — [YouTube Help 11962757](https://support.google.com/youtube/answer/11962757); [YouTube Help 15575509](https://support.google.com/youtube/answer/15575509?hl=en)
- Autocomplete returns real query phrasings in Vietnamese (e.g. "giá vàng hôm nay bao nhiêu", "giá vàng trực tiếp"), which can feed title wording directly. [TESTED curl] — `suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=vi&gl=VN&q=...`
- The Wikipedia top list surfaces *entities* behind trends (e.g. Quả bóng vàng châu Âu, BigBang, ChatGPT, Văn Miếu on 2026-10-27), which are natural starting points for explainers. [TESTED curl] — https://wikimedia.org/api/rest_v1/metrics/pageviews/top/vi.wikipedia/all-access/2026/10/27

### Inferences (procedure for the skill)
1. **Collect:** pull the sources from §1 into 20–40 raw candidates, each with source, timestamp, and linked headline.
2. **Cluster and name the underlying question:** "gold price up" → "Why does Vietnamese gold cost more than world gold?" "Storm hits central VN" → "Why do floods in Central Vietnam keep getting worse?" The **evergreen conversion** asks: why does X keep happening, what does X mean for [audience], how does X actually work, what did people get wrong about X.
3. **Fit filter:** map to a pillar; drop anything with no pillar or a red flag (§3).
4. **Angle:** apply one tilt from the channel profile: expertise ("as an accountant…"), experience (personal story), local lens (global story → Vietnamese consequences), data (compare numbers), contrarian-but-true, or practical (what to do now).
5. **Format by half-life:** spike → Shorts/TikTok within 24h (or a Community/Facebook post). Rising → long-form within a week. Seasonal → scheduled. Evergreen-with-hook → long-form whose hook names the trend and whose body is the mechanism, so the hook can be swapped when the next spike comes.
6. **Title:** match the channel's voice (formal/casual, pronouns *mình/tôi/bạn/anh em*, emoji use, number style). Include the autocomplete phrase people actually type. Make a specific promise the video keeps. Give 3 variants: curiosity, benefit, and search-literal.
7. **Output per idea:** trend + source link + timestamp, lifespan class, pillar, angle sentence, format + deadline, 3 titles, risk flags, and "verify with" (which Studio Trends/Creative Center check the user should run).

### Gaps
- Found no official or study-backed framework for "trend × pillar × angle". It is practitioner synthesis. No evidence gathered this session on how well evergreen-converted trend videos perform compared with pure news reaction.
- Not researched: Vietnamese title conventions in specific niches (e.g. capitalization, "[Giải thích]" prefixes). The sibling notes (youtube_long.md, hooks_and_review.md) may cover them.
