// Auto-generated from backend/labels.json
// Maps class folder names → display info

export const LABEL_MAP = {
  // ── Digits ─────────────────────────────────────────────────────────────
  digit_0: { display: "০", roman: "0",   name: "শূন্য", type: "digit" },
  digit_1: { display: "১", roman: "1",   name: "এক",    type: "digit" },
  digit_2: { display: "২", roman: "2",   name: "দুই",   type: "digit" },
  digit_3: { display: "৩", roman: "3",   name: "তিন",   type: "digit" },
  digit_4: { display: "৪", roman: "4",   name: "চার",   type: "digit" },
  digit_5: { display: "৫", roman: "5",   name: "পাঁচ",  type: "digit" },
  digit_6: { display: "৬", roman: "6",   name: "ছয়",   type: "digit" },
  digit_7: { display: "৭", roman: "7",   name: "সাত",   type: "digit" },
  digit_8: { display: "৮", roman: "8",   name: "আট",    type: "digit" },
  digit_9: { display: "৯", roman: "9",   name: "নয়",   type: "digit" },
  // ── Vowels (স্বরবর্ণ) ───────────────────────────────────────────────────
  alpha_00: { display: "অ", roman: "a",   name: "অ",  type: "vowel" },
  alpha_01: { display: "আ", roman: "aa",  name: "আ",  type: "vowel" },
  alpha_02: { display: "ই", roman: "i",   name: "ই",  type: "vowel" },
  alpha_03: { display: "ঈ", roman: "ii",  name: "ঈ",  type: "vowel" },
  alpha_04: { display: "উ", roman: "u",   name: "উ",  type: "vowel" },
  alpha_05: { display: "ঊ", roman: "uu",  name: "ঊ",  type: "vowel" },
  alpha_06: { display: "ঋ", roman: "ri",  name: "ঋ",  type: "vowel" },
  alpha_07: { display: "এ", roman: "e",   name: "এ",  type: "vowel" },
  alpha_08: { display: "ঐ", roman: "oi",  name: "ঐ",  type: "vowel" },
  alpha_09: { display: "ও", roman: "o",   name: "ও",  type: "vowel" },
  alpha_10: { display: "ঔ", roman: "ou",  name: "ঔ",  type: "vowel" },
  // ── Consonants (ব্যঞ্জনবর্ণ) ────────────────────────────────────────────
  alpha_11: { display: "ক", roman: "ko",   name: "ক", type: "consonant" },
  alpha_12: { display: "খ", roman: "kho",  name: "খ", type: "consonant" },
  alpha_13: { display: "গ", roman: "go",   name: "গ", type: "consonant" },
  alpha_14: { display: "ঘ", roman: "gho",  name: "ঘ", type: "consonant" },
  alpha_15: { display: "ঙ", roman: "ngo",  name: "ঙ", type: "consonant" },
  alpha_16: { display: "চ", roman: "cho",  name: "চ", type: "consonant" },
  alpha_17: { display: "ছ", roman: "chho", name: "ছ", type: "consonant" },
  alpha_18: { display: "জ", roman: "jo",   name: "জ", type: "consonant" },
  alpha_19: { display: "ঝ", roman: "jho",  name: "ঝ", type: "consonant" },
  alpha_20: { display: "ঞ", roman: "nyo",  name: "ঞ", type: "consonant" },
  alpha_21: { display: "ট", roman: "to",   name: "ট", type: "consonant" },
  alpha_22: { display: "ঠ", roman: "tho",  name: "ঠ", type: "consonant" },
  alpha_23: { display: "ড", roman: "do",   name: "ড", type: "consonant" },
  alpha_24: { display: "ঢ", roman: "dho",  name: "ঢ", type: "consonant" },
  alpha_25: { display: "ণ", roman: "no",   name: "ণ", type: "consonant" },
  alpha_26: { display: "ত", roman: "to2",  name: "ত", type: "consonant" },
  alpha_27: { display: "থ", roman: "tho2", name: "থ", type: "consonant" },
  alpha_28: { display: "দ", roman: "do2",  name: "দ", type: "consonant" },
  alpha_29: { display: "ধ", roman: "dho2", name: "ধ", type: "consonant" },
  alpha_30: { display: "ন", roman: "no2",  name: "ন", type: "consonant" },
  alpha_31: { display: "প", roman: "po",   name: "প", type: "consonant" },
  alpha_32: { display: "ফ", roman: "fo",   name: "ফ", type: "consonant" },
  alpha_33: { display: "ব", roman: "bo",   name: "ব", type: "consonant" },
  alpha_34: { display: "ভ", roman: "vho",  name: "ভ", type: "consonant" },
  alpha_35: { display: "ম", roman: "mo",   name: "ম", type: "consonant" },
  alpha_36: { display: "য", roman: "jo2",  name: "য", type: "consonant" },
}

export const DIGITS      = Object.entries(LABEL_MAP).filter(([,v]) => v.type === 'digit')
export const VOWELS      = Object.entries(LABEL_MAP).filter(([,v]) => v.type === 'vowel')
export const CONSONANTS  = Object.entries(LABEL_MAP).filter(([,v]) => v.type === 'consonant')

export const TYPE_COLOR = {
  digit:     '#f43f5e',
  vowel:     '#a855f7',
  consonant: '#db2777',
}
export const TYPE_BG = {
  digit:     'rgba(244,63,94,0.12)',
  vowel:     'rgba(168,85,247,0.12)',
  consonant: 'rgba(219,39,119,0.10)',
}
