import { useState, useEffect } from 'react'
import { getActiveGoalProgress, createGoal } from '../api/goals'
import BottomNav from '../components/BottomNav'

function formatToman(amount) {
  return new Intl.NumberFormat('fa-IR').format(Math.round(Number(amount)))
}

export default function GoalPage() {
  const [progress, setProgress] = useState(null)
  const [hasGoal, setHasGoal] = useState(true)
  const [loading, setLoading] = useState(true)

  // فرم ساخت هدف جدید
  const [title, setTitle] = useState('')
  const [amount, setAmount] = useState('')
  const [creating, setCreating] = useState(false)

  useEffect(() => {
    loadProgress()
  }, [])

  async function loadProgress() {
    setLoading(true)
    try {
      const data = await getActiveGoalProgress()
      setProgress(data)
      setHasGoal(true)
    } catch (err) {
      if (err.response?.status === 404) {
        setHasGoal(false)
      }
    } finally {
      setLoading(false)
    }
  }

  async function handleCreateGoal(e) {
    e.preventDefault()
    setCreating(true)
    try {
      await createGoal({ title, target_amount_toman: Number(amount), is_active: true })
      await loadProgress()
    } finally {
      setCreating(false)
    }
  }

  if (loading) {
    return <div className="page"><p className="muted">در حال بارگذاری...</p></div>
  }

  return (
    <div className="app-shell">
      <div className="top-bar">
        <span className="brand">هدف من 🎯</span>
      </div>

      <div className="page">
        {hasGoal && progress ? (
          <div className="card">
            <div className="goal-title">{progress.title}</div>
            <div className="goal-progress-bar">
              <div
                className="goal-progress-fill"
                style={{ width: `${progress.progress_percent}%` }}
              />
            </div>
            <p className="muted">
              {formatToman(progress.current_saved_toman)} از {formatToman(progress.target_amount_toman)} تومان
              ({progress.progress_percent}%)
            </p>

            {progress.is_achieved ? (
              <p style={{ color: 'var(--color-accent-gold)', fontWeight: 700, marginTop: 12 }}>
                🎉 به هدفت رسیدی! وقتشه بخریش.
              </p>
            ) : progress.estimated_days_remaining !== null ? (
              <p className="goal-eta">
                با همین روند، حدود {progress.estimated_days_remaining} روز دیگر به هدفت می‌رسی.
              </p>
            ) : (
              <p className="goal-eta">
                برای تخمین روزهای باقی‌مانده، ابتدا پروفایل سیگارت را تکمیل کن.
              </p>
            )}
          </div>
        ) : (
          <div className="card">
            <div className="card-title">یک هدف برای پولت تعریف کن</div>
            <p className="muted" style={{ marginBottom: 16 }}>
              مثلا خرید موتور، گوشی جدید یا یک سفر. هر روز پاکی، یک قدم نزدیک‌ترت می‌کند.
            </p>
            <form onSubmit={handleCreateGoal}>
              <div className="form-group">
                <label className="form-label">عنوان هدف</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="مثلا خرید موتور هوندا"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">هزینه‌ی تقریبی (تومان)</label>
                <input
                  type="number"
                  className="form-input"
                  placeholder="50000000"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  min={1000}
                  required
                />
              </div>
              <button type="submit" className="btn btn-success btn-full" disabled={creating}>
                {creating ? 'در حال ذخیره...' : 'ثبت هدف'}
              </button>
            </form>
          </div>
        )}
      </div>

      <BottomNav />
    </div>
  )
}
