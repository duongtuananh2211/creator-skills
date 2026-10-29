# TTS cho voiceover tiếng Việt: ElevenLabs và Vbee AIVoice (tình trạng cuối 2026)

Researched 2026-10-29. Tags: [OFFICIAL] = vendor docs/blog, [PRACTITIONER] = third-party guide/community, [BG] = my unverified background knowledge. WebFetch returns summarized/near-verbatim text, so quoted strings are close to but not guaranteed byte-exact.

**Big change since most training data:** ElevenLabs released **Eleven v4** (late Sept 2026). v3 is now labelled "previous generation" in the docs, and the old "Prompting Eleven v3 (alpha)" page (`/docs/best-practices/prompting`) now resolves to a consolidated "Best practices" page that leads with v4. Treat anything v3-specific from 2025 blogs as possibly outdated.

---

## Q1. Which ElevenLabs models support Vietnamese, and what are the character limits?

### Takeaway
Vietnamese (`vi`) works on Eleven v4, v4 Turbo, v3, v3 Conversational and Flash v2.5. It does **not** work on Multilingual v2 (29 languages, no `vi`). For expressive voiceover the choice is v4 (recommended, 10k chars) or v3 (5k chars). Flash v2.5 (40k chars) is the fallback when you need SSML `<break>` or long, flat narration.

### Cited Findings
- [OFFICIAL] **Eleven v4** (`eleven_v4`): 10,000 character limit (~10 min audio), "90+" languages including `vi` — [Models](https://elevenlabs.io/docs/overview/models)
- [OFFICIAL] **Eleven v4 Turbo** (`eleven_v4_turbo`): includes `vi`, ~100 ms median inference latency, character limit not stated — [Models](https://elevenlabs.io/docs/overview/models)
- [OFFICIAL] **Eleven v3** (`eleven_v3`): "5,000 character limit" (~5 min), 70+ languages including `vi`, labelled "previous generation" — [Models](https://elevenlabs.io/docs/overview/models)
- [OFFICIAL] **Eleven v3 Conversational** (`eleven_v3_conversational`): `vi`, ~280 ms, realtime-oriented — [Models](https://elevenlabs.io/docs/overview/models)
- [OFFICIAL] **Multilingual v2** (`eleven_multilingual_v2`): 10,000 chars, "29 languages supported". **Vietnamese is not in its list** — [Models](https://elevenlabs.io/docs/overview/models)
- [OFFICIAL] **Flash v2.5** (`eleven_flash_v2_5`): 40,000 chars (~40 min), 32 languages = "All `eleven_multilingual_v2` languages plus: `hu`, `no`, `vi`", ~75 ms — [Models](https://elevenlabs.io/docs/overview/models)
- [OFFICIAL] **Turbo v2.5** is deprecated and "functionally equivalent" to Flash v2.5. Use Flash "in all use cases" — [Models](https://elevenlabs.io/docs/overview/models)
- [OFFICIAL] v4 is "our latest and most advanced Text to Speech model, and the first in a new generation". It "may sound substantially different from Eleven v3", so retest content — [Eleven v4](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4)
- [OFFICIAL] The Text to Speech app allows up to 10,000 characters per generation (v4 blog) — [Introducing Eleven v4 / audio tags list](https://elevenlabs.io/blog/elevenlabs-audio-tags-list)
- [PRACTITIONER] A guide dates the v4 release to September 28, 2026. The official page only shows a "3x credits on Creator+ until October 12" promo — [The Rundown guide](https://app.therundown.ai/guides/elevenlabs-audio-tags-guide); [ElevenLabs blog](https://elevenlabs.io/blog/elevenlabs-audio-tags-list)
- [OFFICIAL, self-reported] ElevenLabs claims v4 leads its TTS leaderboard (1319 Elo) and Artificial Analysis Speech Arena (Sept 2026) — [ElevenLabs blog](https://elevenlabs.io/blog/elevenlabs-audio-tags-list)
- **Conflict:** the v4 capability page says Vietnamese plus "about 70 others", while the Models page and blog say "90+" — [Eleven v4](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4) vs [Models](https://elevenlabs.io/docs/overview/models)
- [PRACTITIONER, unclear] A Runware page says its Eleven v3 endpoint "is deprecated and will be deactivated on June 18, 2026". This may only apply to Runware's hosting, since ElevenLabs' own Models page still lists v3 with no deprecation note — [Runware](https://runware.ai/docs/models/elevenlabs-v3/guides/directing-with-audio-tags)

### Inferences
- The skill should default to **v4** for tone-driven voiceover and keep a **v3** profile, since both use the same audio-tag syntax. Add a "Flash v2.5 / no-tags" profile for users who want SSML breaks or very long scripts.
- Chunking rule: keep each generation ≤ 5,000 chars for v3 and ≤ 10,000 for v4. A 60–90 s short-video script (~800–1,500 Vietnamese chars) fits easily.
- Never route Vietnamese to Multilingual v2, even though older tutorials recommend it for normalization quality.

### Gaps
- No official statement on how *well* each model handles Vietnamese tones (dấu thanh). The v4 page only says "some languages are handled more fluently than others".
- v4 Turbo and v3 Conversational character limits are not stated.

---

## Q2. Eleven v3/v4 audio tags: syntax, official list, voice interaction, Vietnamese, pitfalls

### Takeaway
Audio tags are short English instructions in **square brackets**, placed right before the words they affect. v3 and v4 use the same tags. The list is open-ended: you can write free-form, comma-combined tags. Pause tags exist (`[pause]`, `[long pause]`). Tags work best when the voice already "has" that delivery in its training data. Parentheses or braces cause tags to be read aloud.

### Cited Findings
- [OFFICIAL] "Wrap a short instruction in square brackets and place it in the text where the delivery should change." v4 and v3 use the same tags. v4 Turbo also supports them — [How do audio tags work with Eleven v3 and v4](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-do-audio-tags-work-with-eleven-v3-and-v4)
- [OFFICIAL] Tags "must use square brackets. Parentheses or curly braces can cause the tag to be read aloud." Scripts written for v3 should work in v4 — [Eleven v4 audio tags list](https://elevenlabs.io/blog/elevenlabs-audio-tags-list)
- [OFFICIAL] **v4 official tag categories** — [Eleven v4 audio tags list](https://elevenlabs.io/blog/elevenlabs-audio-tags-list):
  - Emotions, high energy: excited, playful, amazed, powerful, proud, optimistic, startled
  - Heated: mad, aggressive, bitter, critical, repelled
  - Tense: anxious, stressed, scared, threatened, vulnerable, confused, busy
  - Low energy: tired, bored, distant, despair, let down
  - Calm/reflective: peaceful, content, curious, thoughtful, trusting
  - Delivery/volume: whispers, shouts, softly, quietly, low threatening, hushed, barely audible, booming, disbelief
  - **Pacing: slowly, rushed, pause, drawn out, long pause, snappy, speedy**
  - Reactions: laughs, sighs, gasps, clears throat, crying, starts crying, gulp
  - Accents/characters: British accent, French accent, Australian accent, Irish accent, pirate voice
  - SFX: thunder rumbling, footsteps, door creaking, clapping, owl hooting, twig snapping, zipper opening, dog barking
- [OFFICIAL] Custom tags: combine with commas (`[whispering, fearful]`). Describe manner, situation, character or shift. "One tag per clause, and add a new tag where the emotion changes." Start from a preset and add detail — [Eleven v4 audio tags list](https://elevenlabs.io/blog/elevenlabs-audio-tags-list)
- [OFFICIAL] Best-practices list (shown under v4 and stated to apply to v3): `[laughs]`, `[laughs harder]`, `[starts laughing]`, `[wheezing]`, `[whispers]`, `[sighs]`, `[exhales]`, `[sarcastic]`, `[curious]`, `[excited]`, `[crying]`, `[snorts]`, `[mischievously]`; SFX `[gunshot]`, `[applause]`, `[clapping]`, `[explosion]`, `[swallows]`, `[gulps]`; experimental `[strong X accent]`, `[sings]`, `[woo]`, `[fart]`. Example: `[whispers] I never knew it could be this way, but I'm glad we're here.` — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] Tag placement (from the official "Enhance" LLM prompt): "place audio tags strategically to maximize impact, typically immediately before the dialogue segment they modify". The Enhance prompt must not alter the original words — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] Voice interaction: "A serious, professional voice may not respond well to playful tags like `[giggles]`." "Tags land more readily when the delivery is already in the voice's training data." "Some experimental tags may be less consistent across different voices." — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] Pitfall: since the model is also trained on SFX, a tag "can occasionally be interpreted as a request for a sound effect rather than a delivery instruction". Descriptive tags like `[low, gravelly voice]` help — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] Tags are "not perfect yet", and instruction-following is still being improved — [Eleven v4](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4)
- [OFFICIAL] Emotion via text: "Explicit dialogue tags yield more predictable results than relying solely on context." Narrative delivery guides written as prose (e.g. "she said excitedly") **will be spoken aloud** and must be cut in post — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] PVCs "are not fully optimized for Eleven v3, resulting in potentially lower clone quality". In v4, PVCs are fully supported (Clone Strength slider, start at 0%), and IVCs need only 1–2 min of clean audio. "Voice Design voices may not be as performative" in v4 — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices); [Eleven v4](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4)
- [OFFICIAL] Cross-language: when output language differs from the reference voice's language, v4 aims for fluent target-language speech. Tags may guide accent but "results may vary" — [Eleven v4](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4)
- [BG] Earlier v3 guidance (2025) said very short prompts (<~250 chars) give inconsistent results and recommended longer text. I could not re-verify this on the current consolidated page.

### Inferences
- **Vietnamese text + English tags** is the safe pattern. Every official example uses English tags, and no doc says Vietnamese-language tags (`[thì thầm]`) are understood. The skill should always emit English tags.
- Suggested voicing → tag map (built from the official vocabulary):
  - vui vẻ → `[cheerful]`/`[playful]`, `[laughs]` sparingly
  - trầm lắng/xúc động → `[softly]`, `[thoughtful]`, `[sighs]`, `[let down]`, `[pause]`
  - hào hứng → `[excited]`, `[amazed]`, `[snappy]`
  - thủ thỉ/tâm sự → `[softly]`, `[quietly]`, `[whispers]`, `[trusting]`
  - nghiêm túc → `[serious]` (custom), `[powerful]`, `[slowly]`
  - hài hước → `[playful]`, `[sarcastic]`, `[mischievously]`, `[laughs]`
  - hồi hộp/bí ẩn → `[hushed]`, `[low threatening]`, `[anxious]`, `[long pause]`
  - kể chuyện → `[thoughtful]`, `[curious]`, `[slowly]`/`[pause]` at turns
  - `cheerful` and `serious` are not in the official list. They are plausible as custom tags but untested.
- Density rule for the skill: one tag per clause at an emotion change, not on every sentence. Warn that the voice must fit the tone (e.g. don't put `[laughs]` on a news-anchor voice).
- Avoid SFX tags in voiceover scripts unless asked, since they may insert actual sounds.

### Gaps
- No official statement that tags work with Vietnamese text specifically. Compatibility is implied (tags are model-level, and v4/v3 support `vi`) but unverified for quality. Testing is needed.
- No official numeric guidance on maximum tags per generation.

---

## Q3. Pauses: `<break>` support, limits, alternatives

### Takeaway
`<break time="x.xs" />` (max 3 s) works only on the older models (Flash v2.5 / v2 / Multilingual v2 family). **Eleven v3 and v4 do not support SSML break tags.** On v3/v4, use `[pause]`/`[long pause]` tags, ellipses, dashes and paragraph structure.

### Cited Findings
- [OFFICIAL] Syntax `<break time="x.xs" />` for "natural pauses up to 3 seconds" — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] "Eleven v4 and Eleven v3 do not support SSML break tags." In v4/v3, use "audio tags, punctuation (ellipses), and text structure to control pauses and pacing." — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] "SSML is not supported" in v4 — [Eleven v4](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4)
- [OFFICIAL] "Using too many break tags in a single generation can cause instability": the AI may speed up or add noises/artifacts. Voices trained with filler sounds may handle pauses differently — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] Alternatives: dashes (`-` or `--`) for short pauses and ellipses (`...`) for hesitant tones, described as "less consistent" — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] Official v4 pacing tags: `pause`, `long pause`, `slowly`, `drawn out`, `rushed`, `snappy`, `speedy` — [Eleven v4 audio tags list](https://elevenlabs.io/blog/elevenlabs-audio-tags-list)
- [BG] `[short pause]` was commonly cited in 2025 v3 materials. It is not in the current official v4 list, but custom tags are allowed.

### Inferences
- The skill needs **two pause dialects**:
  - v3/v4: `...`, `—`, line breaks, `[pause]`, `[long pause]`
  - Flash v2.5: `<break time="0.8s" />`, ≤ 3 s, used sparingly (e.g. ≤ 1 per ~2–3 sentences)
- Do not emit `<break>` for v3/v4. It may be ignored or read aloud (not officially stated which).

### Gaps
- No official max count of breaks. Only "too many" is stated.
- Whether `<break>` is read aloud or silently dropped on v3/v4 is not documented.

---

## Q4. Emphasis (CAPS, punctuation, quotes)

### Takeaway
Officially: CAPS increase emphasis, ellipses add pause and weight, and standard punctuation gives rhythm. "Punctuation significantly affects delivery in v4". Nothing official on quotes.

### Cited Findings
- [OFFICIAL] "Capitalization increases emphasis", "Ellipses (...) add pauses and weight", standard punctuation gives natural rhythm. Example: `It was a VERY long day [sigh] … nobody listens anymore.` — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] "Punctuation significantly affects delivery in v4" — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)

### Inferences
- For Vietnamese, CAPS on a word with diacritics (e.g. "RẤT", "KHÔNG") keeps the diacritics, so emphasis via CAPS should be safe. This is untested. Use it for 1–2 words per paragraph at most. Fully capitalized acronyms could be confused with emphasis, so expand acronyms (see Q6).
- `!` and `?` drive intonation strongly in Vietnamese too. Rhetorical questions are a useful hook-delivery tool.

### Gaps
- No official guidance on quotation marks, bold or italics. No Vietnamese-specific emphasis guidance.

---

## Q5. Voice settings: stability, similarity, style, speed, speaker boost; v3 stability modes

### Takeaway
Speed is 0.7–1.2 (default 1.0) on models that support it. **v4 has no Style or Speed slider.** v3 historically exposed Stability as three presets: Creative (most expressive, can hallucinate), Natural (closest to the original voice), and Robust (most stable, less responsive to tags). Lower stability gives more expressive, varied delivery.

### Cited Findings
- [OFFICIAL] Speed: default 1.0, min 0.7, max 1.2. "Extreme values may affect quality." Available in website, API, Studio, Agents — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] v4: "The Style and Speed sliders aren't offered in Eleven v4." Stability controls consistency across generations: lower = more expressive/varied, higher = closer to baseline — [Eleven v4](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4)
- [OFFICIAL, archived page; possibly outdated] v3 Stability presets: **Creative** = most expressive, with higher hallucination risk. **Natural** = closest to the original recording. **Robust** = most stable, v2-like, with "reduced responsiveness to directional prompts". Creative/Natural are recommended for maximum tag expressiveness — [Prompting Eleven v3 (alpha)](https://elevenlabs.io/docs/best-practices/prompting) (as indexed by search; the URL now serves the consolidated Best-practices page, which no longer contains this text)
- [PRACTITIONER] Workflow: start with Creative/Natural for expressive work, test short sections, and regenerate when a direction doesn't land — [techbloat guide](https://www.techbloat.com/how-to-use-elevenlabs-v3-for-emotional-ai-voice-synthesis.html)
- [OFFICIAL] If results are inconsistent, "generating more than once and selecting the best result" is suggested — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [BG] API `voice_settings` for v2/Flash models: `stability` 0–1, `similarity_boost` 0–1, `style` 0–1 (style exaggeration; higher costs latency and stability), `use_speaker_boost` boolean, `speed` 0.7–1.2. Typical narration starting point: stability ~0.5, similarity ~0.75, style 0–0.3. v3 maps the Creative/Natural/Robust presets onto stability values (≈0.0 / 0.5 / 1.0). Unverified this session.

### Inferences
- Per-voicing settings suggestions for the skill:
  - Expressive tones (hào hứng, hài hước, hồi hộp, xúc động): v3 Creative/Natural or v4 lower stability.
  - Nghiêm túc / kể chuyện dài: Natural/Robust or higher stability for consistency.
  - Speed adjustments are only available on v3/Flash. On v4, carry pace with tags (`[slowly]`, `[rushed]`) and sentence length.

### Gaps
- Current official API reference for `voice_settings` ranges was not fetched (not visible in the docs index portion I read).
- Whether v4 exposes Similarity / Speaker Boost is not stated.

---

## Q6. Pronunciation, numbers, abbreviations, English words in Vietnamese; text normalization

### Takeaway
For Vietnamese, the reliable path is to **write everything out in Vietnamese words** before sending: numbers, dates, times, units, acronyms. Use `language_code: "vi"` and `apply_text_normalization` on the API. Pronunciation dictionaries support alias rules on all models. Phoneme (IPA/CMU) rules work only on v4, v4 Turbo, v3 and Flash v2, and **non-English IPA requires v4/v4 Turbo**. v4 also accepts inline IPA between slashes.

### Cited Findings
- [OFFICIAL] Normalization is enabled by default for all TTS models, but quality differs by model. Example: "$1,000,000" is read correctly by Multilingual v2 but as "one thousand thousand dollars" by Flash v2.5 — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] Problem items: phone numbers, currencies, dates, times, addresses, URLs, unit abbreviations. Mitigations: expand abbreviations, write numbers as words, normalize alphanumerics ("100%" → "one hundred percent"), and tell the LLM that writes TTS text to normalize. Date/time formats are locale-dependent — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] "we recommend writing numbers, acronyms, dates and symbols fully, in words." `language_code` (ISO 639-1) "ensures the normalizer applies that language's rules", which helps with short/ambiguous text. `apply_text_normalization`: `on` / `off` / `auto`, and it adds latency. "11" can be read in the wrong language — [Why are numbers… not properly pronounced](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/why-are-numbers-dates-symbols-and-acronyms-not-properly-pronounced-or-spoken-in-the-correct-language)
- [OFFICIAL] "Pronunciation dictionary phoneme tags only work with eleven_v4, eleven_v4_turbo, eleven_flash_v2 and eleven_v3 models." Other models skip phoneme rules, so use alias rules instead. "If you want to use IPA and CMU pronunciations in languages other than English, you will have to switch" to eleven_v4/v4_turbo. PLS files are case sensitive — [Pronunciation dictionaries](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/pronunciation-dictionaries)
- [OFFICIAL] Dictionaries: TXT or .PLS, phoneme or alias only, case-sensitive, first match wins, available in Studio / Dubbing Studio / API. Alias example: `<grapheme>UN</grapheme>` → `<alias>United Nations</alias>`. For models without phoneme support, respell phonetically — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] v4 reads IPA inline wrapped in slashes (`/ˌbaɪoʊˈkemɪstri/`) with no XML tag needed. Apply it selectively and include stress marks — [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)

### Inferences
- The skill should pre-normalize Vietnamese itself and not rely on ElevenLabs' normalizer, which is English-centric in all examples:
  - "1,8 triệu" → "một phẩy tám triệu"
  - "23h47" → "hai mươi ba giờ bốn mươi bảy phút"
  - "KPI" → "kê-pê-i" or "chỉ số KPI" spelled out as "ca-pi-ai"; pick one convention and keep it consistent
- For English loanwords inside Vietnamese, leave common brand/tech words in English (multilingual voices usually handle code-switching), or respell Vietnamese-style for v3/Flash. This is [BG] and needs testing.

### Gaps
- No official Vietnamese normalization examples. It is unknown whether `language_code: "vi"` correctly expands "1.800.000đ" or Vietnamese date formats.
- Vietnamese IPA via inline slashes on v4 is untested.

---

## Q7. Vbee AIVoice: product, voices, regions, emotions, speed/pitch/volume

### Takeaway
Vbee AIVoice (web studio, mobile app, REST API) has roughly 20 native Vietnamese voices with region codes in the voice ID: `hn_` = Bắc, `hue_` = Trung (Huế), `sg_` = Nam. There are **no emotion tags or emotion variants**. Expressiveness comes from choosing the right voice (including "nhấn nhá" 2.0 voices with an `emphasisIntensity` 0–100 API param), speed (0.25–1.9), pauses and punctuation. Pitch and volume are post-processing tools in the "Hiệu chỉnh âm thanh" editor, not prosody controls.

### Cited Findings
- [OFFICIAL] "Hiện tại Vbee AIVoice hỗ trợ 20 giọng đọc Tiếng Việt và 591 giọng đọc Quốc tế." Other FAQ pages say "Hơn 50 ngôn ngữ và 400+ giọng nói AI" and "hơn 40 ngôn ngữ", which is a conflicting count — [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt)
- [OFFICIAL] Voice filters: Tên giọng, Giới tính, Loại giọng, Ngôn ngữ, **Vùng miền**, Lĩnh vực. Each voice has a sample. You can copy the "mã giọng" for API use. Default voice is "HN-Ngọc Huyền" — [Chọn giọng đọc](https://help.vbee.vn/huong-dan-su-dung/chuyen-van-ban/giao-dien-may-tinh/chon-giong-doc)
- [OFFICIAL] Voice code examples: `hn_female_ngochuyen_full_48k-fhg`, `hn_female_maiphuong_vdts_48k-fhg`, `sg_female_lantrinh_vdts_48k-fhg`, `hue_female_huonggiang_full_48k-fhg`, `sg_male_trungkien_vdts_48k-fhg`, `hn_male_thanhlong_talk_48k-fhg` — [Vbee API docs](https://api-docs.vbee.vn/llms-full.txt)
- [OFFICIAL] Voices named in changelogs: Ngọc Huyền, Lan Trinh, Tường Vy, Thảo Trinh, Mạnh Dũng, Phú Thăng, Anh Khôi, Ngọc Lan, Hà Chi, Việt Bách (child), Mai Phương — [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt)
- [OFFICIAL] Emphasis voices: Ngọc Huyền 2.0 "với khả năng nhấn nhá" (v3.85.0, 12/11/2025), Mạnh Dũng 2.0 "có hỗ trợ nhấn nhá" (v3.132.0, 27/03/2026), Thảo Trinh nhấn nhá, Mạnh Dũng nhấn nhá Beta. Marketing says voices simulate "ngữ điệu, cảm xúc và cách nhấn nhá". **No list of emotions/styles is documented** — [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt)
- [OFFICIAL] API `emphasisIntensity` (new) / `emphasis_intensity` (legacy): integer 0–100 in steps of 10, "only works with voices that support emphasis" (`has_emphasis`) — [Vbee API docs](https://api-docs.vbee.vn/llms-full.txt)
- [OFFICIAL] Speed: API `speed` 0.25–1.9 (default 1.0). Legacy `speed_rate` 0.1–1.9, one decimal place. Changelog v1.2.0: "Giới hạn tốc độ của tất cả các giọng từ 0.25-1.9". UI has 7 presets "rất chậm" → "rất nhanh" plus a custom value. **Conflict:** one FAQ says "từ 0.25x - 0.9x", likely a typo — [Vbee API docs](https://api-docs.vbee.vn/llms-full.txt); [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt); [Tham số (mobile)](https://help.vbee.vn/huong-dan-su-dung/chuyen-van-ban/giao-dien-dien-thoai/tham-so)
- [OFFICIAL] "Hiệu chỉnh âm thanh" editor: volume (Gain; "không vượt qua vạch đỏ để âm thanh không bị rè"), Fade In/Out, speed, pitch, background music. No numeric pitch range given — [Hiệu chỉnh âm thanh](https://help.vbee.vn/huong-dan-su-dung/chuyen-van-ban/giao-dien-may-tinh/tinh-nang-ho-tro/hieu-chinh-am-thanh)
- [OFFICIAL] API: Realtime (sync) mode supports only HN-Ngọc Huyền, SG-Tường Vy, HN-Mai Phương, SG-Lan Trinh, SG-Thảo Trinh — [Vbee API docs](https://api-docs.vbee.vn/llms-full.txt)
- [OFFICIAL] Voice cloning: fast clone needs 10–30 s and professional clone needs ≥5 min. Vietnamese only. Fast clones have "tỷ lệ lỗi đọc cao hơn" — [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt)

### Inferences
- In the skill, voicing for Vbee ≈ **voice recommendation + speed + pause density + punctuation + (optional) emphasisIntensity**. For example:
  - thủ thỉ/tâm sự / trầm lắng: speed 0.85–0.95, longer pauses
  - hào hứng / hài hước: speed 1.05–1.15, short sentences, "!"
  - nghiêm túc: speed 1.0, a "talk"/news-style voice
- The script text itself must carry the emotion through word choice and rhythm, since there are no tags.

### Gaps
- No official mapping of which voice suits which mood. No pitch range.
- I could not confirm whether any Vbee voice has explicit emotional variants (e.g. "vui", "buồn"). None is documented.
- The exact count of Bắc/Trung/Nam voices was not found.

---

## Q8. Vbee pause/break syntax, SSML, emphasis

### Takeaway
In the studio, pauses are inserted through a UI "Thêm khoảng nghỉ" breaktime element (presets ngắn/vừa/dài, or a custom 0–60 s). Punctuation-based pauses are automatic and configurable. In the API, **no inline SSML/`<break>` syntax is documented**. Pause control is via the `clientPause` object (sentence/major/medium/paragraph break durations).

### Cited Findings
- [OFFICIAL] Breaktime tag: choose "Thêm khoảng nghỉ", place it in the sentence, then pick short/medium/long or type 0–60 s and press Enter. "Vbee hỗ trợ nhập tùy chỉnh ngắt nghỉ từ 0 - 60s" — [Tạo ngắt nghỉ](https://help.vbee.vn/huong-dan-su-dung/ung-dung-vbee-ai-voice/chuyen-van-ban/tinh-nang-ho-tro/tao-ngat-nghi); [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt)
- [OFFICIAL] Mobile presets: 0.5 s, 1 s, 2 s, 3 s, or a custom value with a dot decimal (0.3) — [Tham số (mobile)](https://help.vbee.vn/huong-dan-su-dung/chuyen-van-ban/giao-dien-dien-thoai/tham-so)
- [OFFICIAL] Automatic punctuation pauses after `.` `,` `;` and line breaks. Defaults are editable and can be reset with "Đặt mặc định" ("Thiết lập ngắt nghỉ dấu câu", v1.3.16) — [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt)
- [OFFICIAL] Changelog v3.68.0 (26/09/2025): "Cấu hình ngắt nghỉ theo khối văn bản" (per-block pause config) — [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt)
- [OFFICIAL] Studio: insert silence via "S" (Shift+N): "Insert silence at beginning / at current cursor" in the audio editor — [Hiệu chỉnh âm thanh](https://help.vbee.vn/huong-dan-su-dung/chuyen-van-ban/giao-dien-may-tinh/tinh-nang-ho-tro/hieu-chinh-am-thanh)
- [OFFICIAL] API `clientPause`: `sentenceBreak` (default 0.45, 0.1–10 s), `majorBreak` (0.3, 0.1–10), `mediumBreak` (0.25, 0.1–10), `paragraphBreak` (0.6, 0–10). The docs show no SSML or `<break>` syntax — [Vbee API docs](https://api-docs.vbee.vn/llms-full.txt)

### Inferences
- In the Vbee output format, the skill should:
  - mark pauses as human-readable markers for the user to insert in the studio (e.g. `[nghỉ 1s]` with an instruction to replace it with a Breaktime element), not as SSML
  - rely on punctuation and paragraph breaks, since Vbee maps `.` `,` `;` and newlines to configurable pauses
  - for API users, recommend `clientPause` values per voicing (e.g. trầm lắng: sentenceBreak 0.7, paragraphBreak 1.2)
- Likely mapping: `majorBreak` = ";" or ":", `mediumBreak` = "," [BG; the doc doesn't define which punctuation each maps to].

### Gaps
- Whether inline `<break time="…"/>` inside API `text` works is undocumented. I found no evidence either way.
- How the UI breaktime element serializes (e.g. into exported text) was not found.
- Emphasis markup: none documented. Only voice-level `emphasisIntensity`.

---

## Q9. Vbee pronunciation dictionary ("Cách đọc"), numbers, abbreviations, English; limits and writing tips

### Takeaway
Vbee has a personal pronunciation feature (renamed from "Từ điển" to "Cách đọc" in v2.28.0), plus an AI "Kiểm tra cách đọc" tool that scans for words needing custom readings. Readings are written as **Vietnamese respellings**, with official rules for English (e.g. "bad" → "bát-đ", "resort" → "ri-xót"). **Unknown acronyms are spelled letter by letter.** Number/date normalization exists but has had bugs. Rules aren't documented, so pre-normalize. Limits: 1,000 chars per block, 100,000 per batch API request, 300 per realtime request, 1,500-char preview.

### Cited Findings
- [OFFICIAL] "Tùy chỉnh cách đọc": enter an abbreviation or foreign word, enter a reading, listen, then "Thêm từ". Rows can be edited and deleted. Renamed "Từ điển" → "Cách đọc" in v2.28.0 — [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt) (pages "Tùy chỉnh cách đọc", "Hướng dẫn sử dụng trên web")
- [OFFICIAL] "Hướng dẫn viết cách đọc": two word types, abbreviations ("QL4H" → "Quốc lộ 4-hát") and foreign words ("Bad" → "bát-đ"). Read the context, look up when unsure, refer to mainstream newspapers. Words not in the dictionary are spelled letter by letter — [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt)
- [OFFICIAL] "Kiểm tra cách đọc" (AI Biên tập): scans the text, suggests readings with a phonetic table. "Áp dụng tất cả" applies a reading to all occurrences and "Thêm vào từ điển" saves it. Example: "VHVN" is read "vê hát vê nờ" unless added as "văn hóa Việt Nam". Transliteration rules: s/x → "x"; sh, -tion → "s"; d/z → "d"; gi/j → "gi"; clusters keep the first consonant ("brain" → "b-rên"); "six" → "xích-x" — [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt)
- [OFFICIAL] "Tìm kiếm và Thay thế" swaps a word throughout the text — [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt)
- [OFFICIAL] Normalization bugs fixed historically: misreading "năm 10.000 tỷ đồng" and "0 giờ 0 phút 0 giây" (v2.33.0), and failing to read "°C" (v2.8.1). This shows auto-normalization exists but is imperfect — [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt)
- [OFFICIAL] Limits:
  - Preview: "Nghe thử tối đa 1.500 ký tự/1 lần". An older note says 1,000, so the figures conflict.
  - Per conversion: 100,000 points on paid plans, 3,000 on free.
  - Points: 1 char = 1 point for basic voices; ×2 for advanced and fast-clone voices; ×3 for premium; foreign voices ×2.
  - A bug fix references ">1000 ký tự trong mỗi block", which implies a 1,000-char block limit.
  - API: Batch `text` ≤ 100,000 chars; Realtime ≤ 300 chars.

  Sources: [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt); [Vbee API docs](https://api-docs.vbee.vn/llms-full.txt)
- [OFFICIAL] Writing tips:
  - Text imported from files/links can have spelling or sentence-break errors, so check before converting ("Nhập văn bản").
  - Highlight a passage and preview it to check pronunciation ("Nghe thử").
  - Offensive or prohibited words trigger "Văn bản không hợp lệ".

  Source: [Vbee Help Center (llms-full)](https://help.vbee.vn/llms-full.txt)
- [OFFICIAL] API docs document no normalization. The only preprocessing is whitespace trimming — [Vbee API docs](https://api-docs.vbee.vn/llms-full.txt)

### Inferences
- For Vbee, the skill should:
  - expand all acronyms into readable Vietnamese (KPI → "kê-pê-i" or "chỉ số đánh giá hiệu quả")
  - write numbers and times in words ("1,8 triệu" → "một phẩy tám triệu", "23h47" → "hai mươi ba giờ bốn mươi bảy")
  - respell English loanwords using Vbee's official transliteration rules ("deadline" → "đét-lai"), or output a separate "Cách đọc cần thêm" table for the user to paste into the dictionary
- Keep paragraphs under ~1,000 chars (block limit) and use clear sentence-final punctuation.

### Gaps
- Whether Vbee auto-reads "1,8 triệu", "23h47" or "KPI" correctly today is not documented. Only past bug fixes are known. Testing is needed.
- Part of the help center (~chars 200k–293k of llms-full) was only partially extracted. A dedicated "writing tips for natural TTS" page was not found.

---

## Q10. General best practices for writing Vietnamese TTS text

### Takeaway
Vendor docs from both companies converge on a few rules: normalize numbers, dates and acronyms into words, use punctuation as the prosody control, keep sentences short, and preview and regenerate. Vietnamese-specific concerns (correct dấu, Unicode, homographs) come mostly from background knowledge and need testing.

### Cited Findings
- [OFFICIAL] Write numbers, acronyms, dates and symbols fully in words. If an LLM writes the text, instruct it to do so — [ElevenLabs help](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/why-are-numbers-dates-symbols-and-acronyms-not-properly-pronounced-or-spoken-in-the-correct-language); [ElevenLabs Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] Punctuation drives pauses: Vbee maps `.` `,` `;` and newlines to pauses, and in ElevenLabs v4 "Punctuation significantly affects delivery" — [Vbee Help Center](https://help.vbee.vn/llms-full.txt); [ElevenLabs Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [OFFICIAL] Vbee: unknown acronyms are spelled letter by letter, and foreign words should be respelled in Vietnamese phonetics — [Vbee Help Center](https://help.vbee.vn/llms-full.txt)
- [BG] Use precomposed Unicode (NFC) Vietnamese. Mixed NFD from some editors, or old TCVN3/VNI encodings, can cause mispronunciation or dropped diacritics.
- [BG] Keep tone-mark placement consistent (old-style "hoà" vs new-style "hòa"). Most modern engines accept both, but consistency helps dictionary matching, which is case- and string-sensitive in both tools.
- [BG] Homographs and ambiguous readings:
  - "1/2" can be a date or a fraction
  - "2-3" can be "hai đến ba" or "hai trừ ba"
  - "15/10": write "ngày mười lăm tháng mười"
  - "%": write "phần trăm"
  - "k" / "tr" / "đ": write "nghìn" / "triệu" / "đồng"
  - "h": write "giờ"
  - Roman numerals ("thế kỷ XXI"): write "thế kỷ hai mươi mốt"
  - Decimal comma vs thousands dot (Vietnamese convention): spell out to avoid "1.800" being read as "một chấm tám trăm"
- [BG] Avoid emoji, hashtags, URLs, @handles, slashes and bracketed stage directions in TTS text. Turn on-screen text cues ("(chèn B-roll)") into separate non-spoken notes.
- [BG] Short sentences of ~10–20 words per breath group with one idea each sound more natural. Very long comma chains flatten intonation.

### Inferences
- The skill's pipeline:
  1. Strip non-spoken elements (B-roll notes, emoji, hashtags).
  2. Normalize numbers, dates, units and acronyms into Vietnamese words.
  3. Re-break sentences for breath.
  4. Apply tool-specific prosody markup: ElevenLabs v3/v4 English bracket tags + ellipses/CAPS; Flash `<break>`; Vbee punctuation + `[nghỉ Xs]` markers + a settings block (voice, speed, emphasisIntensity, clientPause).
  5. Output a pronunciation table (ElevenLabs alias/PLS, Vbee "Cách đọc") for recurring terms.

### Gaps
- I found no authoritative Vietnamese-language style guide for TTS script writing from either vendor or academia in this session. The Q10 BG items should be validated by listening tests.
