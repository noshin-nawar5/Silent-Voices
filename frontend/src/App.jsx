import { useState, useCallback, useRef } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'
import { motion, AnimatePresence } from 'framer-motion'
import { LABEL_MAP, DIGITS, VOWELS, CONSONANTS, TYPE_COLOR, TYPE_BG } from './labels.js'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

/* ── Floating petals ─────────────────────────────────────────── */
const PETALS = Array.from({ length: 16 }, (_, i) => ({
  id: i, size: 14 + Math.random() * 20,
  x: Math.random() * 100,
  delay: Math.random() * 10,
  dur: 12 + Math.random() * 14,
  opacity: 0.1 + Math.random() * 0.18,
}))
function Petals() {
  return (
    <div className="petals" aria-hidden>
      {PETALS.map(p => (
        <motion.div key={p.id} className="petal"
          style={{ left: `${p.x}%`, width: p.size, height: p.size, opacity: p.opacity }}
          animate={{ y: ['0vh', '108vh'], rotate: [0, 270] }}
          transition={{ duration: p.dur, delay: p.delay, repeat: Infinity, ease: 'linear' }} />
      ))}
    </div>
  )
}

/* ── Confidence bar chart ─────────────────────────────────────── */
function BarChart({ allScores }) {
  const entries = Object.entries(allScores)
    .sort((a, b) => b[1].confidence - a[1].confidence)
    .slice(0, 10)

  return (
    <div className="bar-chart">
      {entries.map(([cls, info], i) => (
        <motion.div key={cls} className="bar-row"
          initial={{ opacity: 0, x: -16 }} animate={{ opacity: 1, x: 0 }}
          transition={{ delay: i * 0.035 }}>
          <span className="bar-lbl" style={{ color: TYPE_COLOR[info.type] }}>
            {info.display}
          </span>
          <div className="bar-track">
            <motion.div className="bar-fill"
              style={{ '--c': i === 0 ? 'var(--rose)' : 'var(--violet)' }}
              initial={{ width: 0 }}
              animate={{ width: `${Math.min(info.confidence, 100)}%` }}
              transition={{ duration: 0.55, delay: i * 0.035, ease: 'easeOut' }} />
          </div>
          <span className="bar-pct">{info.confidence.toFixed(1)}%</span>
        </motion.div>
      ))}
    </div>
  )
}

/* ── Result card ─────────────────────────────────────────────── */
function ResultCard({ result }) {
  const { prediction, top5, all_scores } = result
  const typeColor = TYPE_COLOR[prediction.type] || '#f43f5e'
  const typeBg = TYPE_BG[prediction.type] || 'rgba(244,63,94,0.12)'

  const typeLabel = {
    digit: '🔢 Digit', vowel: '🌸 Vowel', consonant: '✦ Consonant'
  }[prediction.type] || prediction.type

  return (
    <motion.div className="result-card"
      initial={{ opacity: 0, scale: 0.88, y: 24 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ type: 'spring', stiffness: 200, damping: 20 }}>

      {/* Hero */}
      <div className="hero">
        <motion.div className="digit-orb"
          style={{ '--orb-color': typeColor }}
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ duration: 2.4, repeat: Infinity, ease: 'easeInOut' }}>
          <span className="orb-char">{prediction.display}</span>
          <span className="orb-roman">{prediction.roman}</span>
        </motion.div>
        <div className="hero-meta">
          <div className="type-badge" style={{ background: typeBg, color: typeColor }}>
            {typeLabel}
          </div>
          <p className="hero-name">{prediction.name}</p>
          <div className="conf-pill">✨ {prediction.confidence.toFixed(1)}% confident</div>
        </div>
      </div>

      <div className="hr" />

      {/* Top 5 */}
      <p className="sect-label">Top 5 Predictions</p>
      <div className="top5-row">
        {top5.map((t, i) => (
          <div key={i} className={`top5-chip rank-${i}`}
            style={{ '--c': TYPE_COLOR[t.type] }}>
            <span className="t5-char">{t.display}</span>
            <span className="t5-pct">{t.confidence.toFixed(0)}%</span>
          </div>
        ))}
      </div>

      <div className="hr" />

      {/* Bar chart */}
      <p className="sect-label">Score Breakdown (top 10)</p>
      <BarChart allScores={all_scores} />
    </motion.div>
  )
}

/* ── Reference panel ─────────────────────────────────────────── */
const REF_TABS = [
  { id: 'digit',     label: '০–৯ Digits',     entries: DIGITS,     color: TYPE_COLOR.digit },
  { id: 'vowel',     label: 'স্বরবর্ণ Vowels',   entries: VOWELS,     color: TYPE_COLOR.vowel },
  { id: 'consonant', label: 'ব্যঞ্জনবর্ণ Consonants', entries: CONSONANTS, color: TYPE_COLOR.consonant },
]

function ReferencePanel() {
  const [tab, setTab] = useState('digit')
  const active = REF_TABS.find(t => t.id === tab)

  return (
    <section className="ref-section">
      <h3 className="ref-title playfair">Sign Reference</h3>
      <p className="ref-sub">47 classes total — 10 digits · 11 vowels · 26 consonants</p>

      <div className="tab-row">
        {REF_TABS.map(t => (
          <button key={t.id} className={`tab-btn ${tab === t.id ? 'active' : ''}`}
            style={{ '--tc': t.color }}
            onClick={() => setTab(t.id)}>
            {t.label}
          </button>
        ))}
      </div>

      <AnimatePresence mode="wait">
        <motion.div key={tab} className="chip-grid"
          initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }} transition={{ duration: 0.2 }}>
          {active.entries.map(([cls, info]) => (
            <div key={cls} className="ref-chip" style={{ '--rc': active.color }}>
              <span className="rc-char">{info.display}</span>
              <span className="rc-roman">{info.roman}</span>
            </div>
          ))}
        </motion.div>
      </AnimatePresence>
    </section>
  )
}

/* ── Main App ─────────────────────────────────────────────────── */
export default function App() {
  const [preview, setPreview] = useState(null)
  const [file,    setFile]    = useState(null)
  const [result,  setResult]  = useState(null)
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState(null)

  const onDrop = useCallback(accepted => {
    if (!accepted.length) return
    const f = accepted[0]
    setFile(f); setResult(null); setError(null)
    setPreview(URL.createObjectURL(f))
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, accept: { 'image/*': [] }, maxFiles: 1,
  })

  const handlePredict = async () => {
    if (!file) return
    setLoading(true); setError(null)
    try {
      const fd = new FormData()
      fd.append('file', file)
      const res = await axios.post(`${API_URL}/predict`, fd)
      setResult(res.data)
    } catch (e) {
      setError(e.response?.data?.error || 'Could not reach the API. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  const reset = () => { setFile(null); setPreview(null); setResult(null); setError(null) }

  return (
    <div className="app">
      <Petals />

      {/* Header */}
      <header className="header">
        <motion.div initial={{ opacity: 0, y: -24 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}>
          <div className="logo-row">
            <span className="logo-icon">🤙</span>
            <span className="logo-text playfair">হস্তচিহ্ন</span>
          </div>
          <h1 className="hero-h1 playfair">
            Bangla Sign Language <em>Recognizer</em>
          </h1>
          <p className="hero-sub">Digits · Vowels · Consonants — 47 signs, one model</p>
          <div className="stat-chips">
            <span style={{ '--sc': TYPE_COLOR.digit }}>🔢 10 Digits</span>
            <span style={{ '--sc': TYPE_COLOR.vowel }}>🌸 11 Vowels</span>
            <span style={{ '--sc': TYPE_COLOR.consonant }}>✦ 26 Consonants</span>
          </div>
        </motion.div>
      </header>

      <main className="main">
        <div className="two-col">
          {/* Upload */}
          <motion.div className="panel" initial={{ opacity: 0, x: -28 }}
            animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }}>
            <h2 className="panel-title playfair">Upload Sign</h2>

            <div {...getRootProps()}
              className={`dropzone ${isDragActive ? 'drag' : ''} ${preview ? 'has-img' : ''}`}>
              <input {...getInputProps()} />
              {preview ? (
                <div className="prev-wrap">
                  <img src={preview} alt="preview" className="prev-img" />
                  <div className="prev-overlay">Click or drop to change</div>
                </div>
              ) : (
                <div className="drop-empty">
                  <motion.span className="drop-icon"
                    animate={{ y: [0, -7, 0] }}
                    transition={{ duration: 1.8, repeat: Infinity, ease: 'easeInOut' }}>
                    🖐️
                  </motion.span>
                  <p className="drop-text">
                    {isDragActive ? 'Drop here! 🌸' : 'Drag & drop or click to upload'}
                  </p>
                  <p className="drop-hint">JPG or PNG · Any Bangla hand sign</p>
                </div>
              )}
            </div>

            <div className="btn-row">
              <button className="btn btn-main" onClick={handlePredict}
                disabled={!file || loading}>
                {loading ? <><span className="spinner" /> Recognizing…</> : '✨ Recognize Sign'}
              </button>
              {preview && (
                <button className="btn btn-ghost" onClick={reset}>Reset</button>
              )}
            </div>

            <AnimatePresence>
              {error && (
                <motion.div className="err-box"
                  initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
                  ⚠️ {error}
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>

          {/* Result */}
          <motion.div className="panel" initial={{ opacity: 0, x: 28 }}
            animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }}>
            <h2 className="panel-title playfair">Result</h2>

            <AnimatePresence mode="wait">
              {result ? (
                <ResultCard key="res" result={result} />
              ) : (
                <motion.div key="empty" className="empty-state"
                  initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                  <div className="empty-chars">
                    {['অ','আ','ক','খ','০','১','গ','ঘ','ই','ঈ'].map((c, i) => (
                      <motion.span key={i} className="empty-char"
                        animate={{ opacity: [0.15, 0.7, 0.15] }}
                        transition={{ duration: 2.8, delay: i * 0.28, repeat: Infinity }}>
                        {c}
                      </motion.span>
                    ))}
                  </div>
                  <p className="empty-hint">Upload a hand-sign image<br />to see the prediction</p>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </div>

        <ReferencePanel />
      </main>

      <footer className="footer">
        <p>Built with 💗 · MobileNetV2 Transfer Learning · Bangla Sign Language Dataset · 47 classes</p>
      </footer>
    </div>
  )
}
