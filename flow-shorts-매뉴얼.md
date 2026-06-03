# Flow 영상(쇼츠/인트로) 제작 매뉴얼 & 프롬프트 모음

> 책 『배움을 설계하는 기술의 역사』(유인식, UBION) 홍보 영상 제작용
> 도구: **Google Flow** (Veo 3 기반 AI 영상 생성) · labs.google/flow
> 용도: 유튜브 쇼츠 / 책 소개 인트로

---

## 0. 가장 중요한 원칙 (꼭 먼저 읽기)

1. **Flow는 한글·로고·텍스트를 거의 못 그린다.** 글자를 넣으면 깨지거나 가짜 글자가 생긴다.
   - → **"장면은 AI, 글자·로고·자막은 편집 단계에서"** 가 이 시리즈의 기본 전략.
   - → AI에는 글자 없이 깨끗한 장면만 뽑게 하고, 진짜 텍스트는 프리미어/캡컷에서 얹는다.
2. **프롬프트 1개 = 영상 1개.** 여러 장면은 각각 따로 생성한 뒤 Scene Builder로 이어붙인다.
3. **같은 프롬프트도 매번 다르게 나온다.** 마음에 드는 컷이 나올 때까지 2~3번 재생성.
4. **유튜브 업로드용 화면비**: 일반 영상 `16:9`, 쇼츠 `9:16`.

---

## 1. Flow 사용법 (단계별)

### 기본 흐름
1. **labs.google/flow** 접속 → 구글 계정 로그인 (Gemini 유료 플랜이면 크레딧 더 많음)
2. **New Project** 생성
3. 하단 입력창에서 생성 모드 선택
   - **Text to Video**: 이미지 없이 프롬프트만으로 생성 (분위기 샷 등)
   - **Frames to Video**: 시작 이미지 업로드 → 그 이미지가 움직이는 영상 (표지 등장 등)
4. 우측 설정: **Model = Veo 3**, **화면비 = 16:9 (쇼츠는 9:16)**, 길이 기본 8초
5. **Generate** → 마음에 드는 컷 채택
6. 여러 클립을 **Scene Builder**에서 순서대로 이어붙여 인트로 완성

### 모드 빠른 표

| 상황 | 모드 | 이미지 |
|---|---|---|
| 분위기/추상 도입 컷 | Text to Video | ❌ 없음 |
| 표지·사진을 움직이게 | Frames to Video | ✅ 업로드 |

---

## 2. 책 소개 인트로 프롬프트 (2클립 구성)

> ①과 ②는 **각각 따로** 생성하는 별개 클립. 한 창에 합쳐 넣지 말 것.
> 순서: ① 분위기 → ② 표지 등장 (Scene Builder로 연결)

### ① 도입부 — 표지 없는 분위기 컷 (0~3초, 광고 느낌 제거)
**모드: Text to Video**

```
A dark, elegant void slowly fills with tiny glowing orange particles
drifting and converging toward the center, forming a faint radiant
diamond of light. Cinematic, minimal, calm and contemplative mood.
Deep charcoal background, warm amber glow. Very slow, subtle camera
push-in. No text, no logos. 16:9.

Audio: a soft, clean J-pop inspired instrumental intro — gentle bright
piano with airy synth pads, light and hopeful, slowly building,
no vocals, no drums yet, calm and warm.
```

### ② 표지 등장 컷 (표지 이미지 업로드 + 아래 프롬프트)
**모드: Frames to Video** (표지 앞면만 크롭해서 업로드 추천)

```
The book cover gently emerges into focus from soft darkness.
The radiant starburst behind the title subtly shimmers and the
orange light pulses softly, like a heartbeat. Extremely slow,
elegant push-in. Keep all text crisp, stable and unchanged.
Cinematic, premium, quiet. 16:9.

Audio: a bright, clean J-pop style instrumental — sparkling piano
and airy synths with a light, uplifting melody, gentle soft beat
coming in, hopeful and refreshing, no vocals.
```

> 두 클립 음악이 자연스럽게 이어지도록 ①은 "no drums yet / building", ②는 "soft beat coming in"으로 흐름을 줬다.

---

## 3. 음악 (배경음악)

### Veo 3 자체 오디오 (1순위, 가장 간편)
- 프롬프트에 `Audio: ...` 라인으로 음악 지정 → **AI 생성 원본이라 저작권 문제 없음.**
- J-pop 맑은 느낌 키워드:
  - 더 맑게 → `crystalline, sparkling, glassy piano`
  - 더 잔잔하게 → `minimal, ambient, slow tempo`
  - 더 밝고 경쾌하게 → `upbeat, cheerful, City Pop vibe`  ← 일본 특유 산뜻함
- 마음에 드는 음악 나올 때까지 2~3번 재생성.

### 유튜브 오디오 보관함 (유튜브 업로드 시 가장 안전)
- 유튜브 스튜디오 → 좌측 **오디오 보관함** → 저작권 0, 수익화 OK
- 필터: ambient / cinematic / inspirational / city pop

### Suno (직접 작곡)
- suno.com → **Instrumental** 토글 ON
- 프롬프트 예: `Cinematic ambient piano with soft strings, contemplative and hopeful, slow build, minimal, warm and elegant, no drums, for a book trailer intro`
- ⚠️ **무료 플랜 곡은 상업/수익화 불가.** 유튜브(특히 수익화 채널)에 올리려면 **유료 플랜(Pro/Premier)** 필요.

### 구글 MusicFX (무료)
- labs.google/fx → **MusicFX** (Lyria 기반)
- 프롬프트 예: `calm cinematic ambient, soft piano and warm pads, reflective, slow tempo`
- 상업 이용 약관은 사용 시점에 확인.

---

## 4. 글자·로고 깨짐 대응 (핵심 노하우)

Flow는 한글/로고를 거의 못 그린다. 대응 전략:

### 전략 A — 글자를 통째로 비우기 (가장 깔끔)
프롬프트에 강제 구문 삽입:
```
STRICT: no text, no letters, no numbers, no Korean characters, no
logos, no emblems, no captions, no signage anywhere. All surfaces
are completely blank. Do not generate any garbled or fake text or
fake logos.
```

### 전략 B — 로고 1개만 예외 허용 (예: EBS)
```
Behind him is a simple banner showing ONLY the blue "EBS" logo —
nothing else. The podium front is completely blank with absolutely
no writing.
STRICT: no Korean text, no letters, no numbers, no captions, no
signage anywhere except the single clean "EBS" logo. Do not generate
any garbled or fake text.
```

### 전략 C — 깨지던 영역만 비우고 나머지 유지
- "화면 하단의 대학 로고 줄"처럼 특정 영역만 문제면, 그 영역을 명시적으로 비운다:
```
STRICT: the lower part of the screen is clean and blank — do NOT
place any university logos, crests, shields, or names there.
```

### 전략 D — 글자는 편집에서 (가장 정확)
- 글자 없는 깨끗한 장면을 뽑고 → 프리미어/캡컷에서 진짜 자막·로고·교명을 직접 얹는다.
- AI 가짜 글자보다 100배 깨끗하고, 정보도 정확하다.

---

## 5. 본문 장면 프롬프트 모음 (정리본)

> 모두 글자/로고 깨짐 방지 구문 포함. 인물 직접 묘사보다 상징적 구성을 우선(초상권·얼굴깨짐 회피).

### 2004 EBS / 교육방송 기자회견 (단독 장면)
```
An April 2004 Korean government press conference in Seoul. A male
Minister of Education stands at a wooden podium speaking to the press.
A crowd of journalists fills the room, holding professional cameras
and taking photos, with bright press flashes firing.
Behind him is a simple banner showing ONLY the blue "EBS" logo —
nothing else. The podium front is completely blank, smooth and plain
with absolutely no writing. The walls are completely blank.
STRICT: no Korean text, no letters, no numbers, no captions, no
signage anywhere except the single clean "EBS" logo. All surfaces
are plain and empty. Do not generate any garbled or fake text.
Modern high-definition photography, clean cinematic color grading,
documentary style, cinematic quality. 16:9.
```

### 2011 팟캐스트(청취형 학습) — 인물 없이 상징적
```
A symbolic scene representing the rise of podcast-based listening
culture in Korea around 2011. A dim, intimate small home recording
studio at night: several vintage broadcast microphones clustered
together on a simple wooden desk, soft warm desk lamp light, a laptop
glowing faintly, headphones resting nearby, a few tangled cables.
No people in the room. The empty microphones suggest voices that just
spoke. Quiet, grassroots, slightly rebellious DIY atmosphere.
Subtle slow camera push-in toward the microphones. Warm amber and
deep shadow tones, shallow depth of field, cinematic documentary
style, high-definition, film grain.
STRICT: no text, no letters, no numbers, no logos, no captions, no
signage anywhere. All surfaces blank. Do not generate any garbled
or fake text. 16:9.
```
- 듣는 사람 한 컷 추가하고 싶을 때:
```
Alternative: a single young person at night wearing earphones,
looking at a glowing smartphone on a quiet subway, contemplative,
one person only, no text on screen.
```

### 2015 K-MOOC 출범식 (대학 로고/교명만 제거, 나머지 유지)
```
A 2015 K-MOOC launch ceremony in Seoul Korea. A stage with a long
overhead banner and the National Institute for Lifelong Education
branding. Ten Korean university representatives in dark suits stand
in a row across the stage, one speaking at a central wooden podium.
Behind them a large illuminated presentation screen shows a clean
title 'K-MOOC Year One' and a bold number counter '27 Courses', set
over a soft blue gradient — with NO university crests, NO emblems,
and NO university names of any kind. A seated audience fills the
foreground. Soft warm event lighting.
STRICT: the lower part of the screen is clean and blank — do NOT
place any university logos, crests, shields, or Korean/English
university names there. Do not generate any garbled or fake logos.
Keep only the simple 'K-MOOC Year One' title and '27 Courses' number.
Modern high-definition photography, clean cinematic color grading,
wide medium shot, documentary style, cinematic quality. 16:9.
```

---

## 6. 쇼츠(9:16) 만들 때 추가 팁

- 모든 프롬프트의 끝 `16:9` → **`9:16`(세로)** 로 변경.
- 구도 키워드 추가: `vertical composition, centered subject, mobile-first framing`.
- 길이: 쇼츠는 보통 **15~60초**. Flow 클립(8초) 2~4개를 이어붙여 구성.
- 도입 3초가 승부 → 가장 강한 비주얼/움직임을 맨 앞에.
- 자막은 편집 단계에서 **큰 글씨 + 화면 중앙 안전영역**에 배치 (모바일 가독성).

---

## 7. 추천 작업 순서 (요약)

1. 표지 앞면 크롭 → 인트로 ①(Text) + ②(Frames) 생성 → Scene Builder 연결
2. 본문 장면들은 5장 프롬프트로 각각 생성 (글자 없이)
3. 음악은 Veo 자체 오디오 or 유튜브 오디오 보관함
4. 글자·로고·자막·교명은 **편집 단계에서** 진짜 텍스트로 입력
5. 유튜브 업로드 (일반 16:9 / 쇼츠 9:16)

---

*작성: 2026-06-04 · 회사 PC 작업용 휴대 매뉴얼*
