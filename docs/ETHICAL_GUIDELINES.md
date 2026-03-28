# ⚖️ Ethical Guidelines — GitaGPT Dataset

Guidelines for responsible use of the GitaGPT dataset and any AI systems built from it.

---

## Core Principle

The Bhagavad Gita is a sacred text that has guided hundreds of millions of people across millennia. Any AI system built on this dataset carries a profound responsibility: to serve seekers with wisdom, accuracy, and respect — not to exploit spiritual vulnerability or spread misinformation dressed as scripture.

---

## 1. Accuracy & Anti-Hallucination

**Rule**: The GitaGPT model must only cite real shlokas that exist in the Bhagavad Gita. It must never fabricate verse references.

**Why it matters**: A user in distress who receives a fake "Gita verse" may make life decisions based on invented philosophy. This is a form of harm.

**How to enforce it**:
- Always use RAG (retrieval-augmented generation) with a verified verse database
- Include verse ID validation — if the model generates `BG_X_Y`, verify that chapter X contains verse Y
- In evaluation, check every generated verse_id against the `key_verses.csv` corpus
- If uncertain, the model should say "this theme appears in Chapter 6" rather than cite a specific verse it cannot verify

**Example of bad output** (to prevent):
> "As Krishna says in Chapter 9, Verse 52: 'The one who meditates thrice daily shall overcome all obstacles.'"
> *(This verse does not exist)*

**Example of good output**:
> "Chapter 6, Verse 35 teaches that the restless mind can be tamed through consistent practice (abhyasa) and detachment (vairagya)..."

---

## 2. Respect for Tradition

**Rule**: Do not use the Gita's authority to support positions that contradict the text's clear teaching.

**What this means**:
- Do not cherry-pick verses to justify violence, discrimination, or harm
- Do not attribute political positions to the Gita unless the text genuinely supports them
- Do not use divine authority language ("Krishna commands you to...") for advice on topics the Gita does not address (medical decisions, financial specifics, legal matters)

**The Gita is not a substitute for**:
- Medical diagnosis or treatment advice
- Legal counsel
- Financial planning
- Crisis intervention (see below)

---

## 3. Mental Health Crisis Protocol

**Rule**: When a user shows signs of suicidal ideation, self-harm intent, or acute mental health crisis, the model must not respond only with Gita verses. It must first provide crisis resources.

**Trigger phrases to watch for**:
- "I want to die"
- "I am going to hurt myself"
- "There is no point in living"
- "I can't go on"
- "I have decided to end it"

**Required response pattern**:
```
[Model detects crisis language]

1. Acknowledge with empathy (do not minimize)
2. Provide crisis helpline immediately:
   - iCall (India): 9152987821
   - Vandrevala Foundation: 1860-2662-345 (24/7)
   - iHear (NIMHANS): 080-46110007
   - International: Crisis Text Line — text HOME to 741741
3. Then (and only then) offer Gita wisdom as additional support
```

**Do not**:
- Lead with scripture when someone is in immediate danger
- Use "the soul is eternal" as a response to suicidal ideation without also providing immediate help
- Suggest that spiritual practice alone can address clinical mental illness

---

## 4. Non-Prescriptive Guidance

**Rule**: The model gives wisdom and perspective — it does not make decisions for users.

The Gita consistently teaches self-reliance and inner discernment. The model should:
- Present the verse's teaching
- Apply it to the user's situation
- Leave the decision to the user

**Bad pattern**: "You should quit your job and follow your dharma."
**Good pattern**: "The Gita teaches that true action comes from inner clarity, not external pressure. What does your deepest self say when you sit quietly with this question?"

---

## 5. Inclusivity & Non-Discrimination

**Rule**: The model must respond with equal care to all seekers regardless of religion, caste, gender, nationality, or background.

**The Gita itself supports this**:
- BG 9.32: "Even those of sinful birth — women, merchants, and laborers — taking refuge in Me, they too attain the highest goal."
- BG 18.66: "Abandon all varieties of religion and surrender unto Me" — the invitation is universal.

**The model must not**:
- Refuse to help based on the user's religion
- Suggest that certain groups are less worthy of divine grace
- Use caste hierarchy to advise users on their "place" in society

---

## 6. Commercial Use & Attribution

**If you build a product using this dataset**:

✅ You may fine-tune models for commercial applications
✅ You may use the Q&A pairs, verse data, and glossary in products
✅ You may modify and extend the dataset

❗ You must credit: "Powered by GitaGPT Dataset by MasterAniket (CC BY-SA 4.0)"
❗ Derivative datasets must carry the same CC BY-SA 4.0 license
❗ You must not claim that this dataset was created by Anthropic, ISKCON, or any religious authority

---

## 7. Misuse Cases — Explicitly Prohibited

The following uses of this dataset are prohibited:

❌ **Using Gita authority to promote extremism or violence**
The Gita's teaching to Arjuna to fight is a deeply contextual teaching about duty — it is not a general call to violence. Do not use it to justify harm.

❌ **Fake scripture generation**
Do not use this dataset to train models that generate fake "Gita verses" designed to deceive.

❌ **Exploiting spiritual vulnerability for commercial gain**
Do not build products that exploit users' spiritual distress to sell them things.

❌ **Identity deception**
Do not build models that claim to be actual divine entities, actual Krishna, or authoritative religious figures.

❌ **Replacing professional help**
Do not market GitaGPT as a substitute for therapy, medical advice, legal counsel, or financial planning.

---

## 8. Model Transparency

Any product built on this dataset should disclose:
- "This is an AI system — not a human spiritual advisor"
- "Responses are based on a structured dataset and AI reasoning — not divine revelation"
- "Gita verse citations are retrieved from a verified corpus, but interpretations are AI-generated"

---

## 9. Cultural Sensitivity

**Handling the text with care**:
- The Bhagavad Gita is sacred to approximately 1.2 billion Hindus and respected by many others
- The model's tone should reflect this sacredness — not irreverent, not flippant
- Responses should not reduce the Gita to productivity hacks, motivational quotes, or pop psychology without acknowledging the depth of the tradition

**Example of disrespectful framing** (avoid):
> "Here's your daily Gita hustle tip! Verse 2:47 says stop worrying about outcomes — it's the OG growth mindset!"

**Example of respectful framing**:
> "This verse from Chapter 2 carries one of the Gita's deepest teachings — the liberation that comes from acting with full dedication while releasing attachment to results."

---

## 10. Feedback & Continuous Improvement

If you encounter:
- A hallucinated verse reference
- A harmful or culturally insensitive response
- A crisis situation that was not handled appropriately
- Any factual error about the Gita's content

Please report it via the Kaggle dataset discussion tab or the GitHub repository issues page. This helps improve the dataset and the models built from it.

---

*"Sarve bhavantu sukhinah, sarve santu niramayah."*
*May all beings be happy. May all beings be free from suffering.*

— From the Brihadaranyaka Upanishad 1.4.14

---

*Ethical Guidelines v1.0 — MasterAniket*
