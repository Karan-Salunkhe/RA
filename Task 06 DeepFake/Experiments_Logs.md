# Experiments Log – Task 06 (AI Deep Fake Interview)

This folder documents all experiments, trials, and alternative approaches explored while creating the AI-generated deep fake interview for **Research Task 06**.  

---

### 🔎 Approach 1: ChatGPT  
- **Tool Used:** ChatGPT  
- **Goal:** Draft a dataset-driven Q&A interview between a reporter and Sachin Tendulkar.  
- **Process:** Used IPL 2025 stats (from Task 05) to generate both factual and scenario-based questions.  
- **Result:** A polished interview script blending stats (strike rates, overs bowled, runs, wickets) with opinions and coaching scenarios.  
- **Status:** ✅ Successful (script creation only, not audio/video).  

---

### 🔎 Approach 2: D-ID (AI Talking Head)  
- **Tool Used:** [D-ID](https://studio.d-id.com)  
- **Goal:** Generate a lip-synced video interview with avatars for Reporter & Sachin.  
- **Result:** Free trial was too limited (few seconds of video, watermark, no multi-speaker conversation).  
- **Status:** ❌ Abandoned due to restrictions.  

---

### 🔎 Approach 3: HeyGen (AI Avatars)  
- **Tool Used:** [HeyGen](https://www.heygen.com)  
- **Goal:** Create a two-avatar interview (Reporter vs. Sachin).  
- **Process:** Uploaded dialogue lines separately, tried switching avatars.  
- **Result:** Free plan only allows 1 minute per day, not suitable for full multi-question interview.  
- **Status:** ❌ Abandoned due to time limits.  

---

### 🔎 Approach 4: CapCut / Canva (Manual Video Editing)  
- **Tools Used:** [CapCut](https://www.capcut.com), [Canva](https://www.canva.com)  
- **Goal:** Create a TV-style interview video by overlaying stock cricket footage with TTS audio.  
- **Process:** Tested uploading generated TTS clips, aligning them with visuals.  
- **Result:** Feasible, but required too much manual syncing and lacked a realistic “interview” feel.  
- **Status:** ❌ Not pursued further.  

---

### 🔎 Approach 5: Descript (Final Solution)  
- **Tool Used:** [Descript](https://www.descript.com)  
- **Goal:** Generate a realistic video interview with distinct AI voices for Reporter & Sachin.  
- **Process:**  
  1. Imported the full interview script.  
  2. Assigned one AI voice to the Reporter, another to Sachin.  
  3. Generated dialogue tracks, aligned them as a conversation.  
  4. Exported final deep fake video as `.mp4`.  
- **Result:** Smooth, believable audio + video interview, free of paywall restrictions.  
- **Status:** ✅ Final working solution.  

---

## 📊 Summary  
- Multiple tools were tested: ChatGPT (script), D-ID, HeyGen, CapCut, Descript.  
- Free trial limits and watermarks made D-ID & HeyGen impractical.  
- CapCut/Canva offered editing flexibility but lacked realism.  
- **Descript provided the most practical workflow** for free/student use: *Script → Voices → Video Export*.  

This iterative process highlights both **technical challenges** (tool limits, paywalls) and **problem-solving** (pivoting to Descript as the best free solution).

