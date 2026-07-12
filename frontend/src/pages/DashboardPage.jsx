import { useState, useEffect } from 'react'
import { getTodayStatus, submitCheckIn } from '../api/tracking'
import BreathRing from '../components/BreathRing'
import BottomNav from '../components/BottomNav'

function formatToman(amount) {
  return new Intl.NumberFormat('fa-IR').format(Math.round(Number(amount)))
}

export default function DashboardPage() {
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [feedback, setFeedback] = useState(null)

  useEffect(() => {
    loadStatus()
  }, [])

  async function loadStatus() {
    setLoading(true)
    try {
      const data = await getTodayStatus()
      setStatus(data)
    } finally {
      setLoading(false)
    }
  }

  async function handleCheckIn(isSmokeFree) {
    setSubmitting(true)
    try {
      await submitCheckIn({ is_smoke_free: isSmokeFree })
      setFeedback(
        isSmokeFree
          ? 'عالیه! یک روز دیگه به پاکیت اضافه شد 🌿'
          : 'اشکالی نداره، فردا از نو شروع می‌کنیم. مهم اینه که ادامه بدی.'
      )
      await loadStatus()
    } catch (err) {
      setFeedback('برای امروز قبلا ثبت کردی.')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return <div className="page"><p className="muted">در حال بارگذاری...</p></div>
  }

  const summary = status?.streak_summary

  return (
    <div className="app-shell">
      <div className="top-bar">
        <span className="brand">ترک‌یار 🌿</span>
      </div>

      <div className="page">
        <BreathRing days={summary?.current_streak || 0} />

        <div className="savings-card">
          <div className="savings-label">پولی که تا الان پس‌انداز کردی</div>
          <div className="savings-amount">
            {formatToman(summary?.total_money_saved || 0)}
            <small>تومان</small>
          </div>
          <div className="savings-label" style={{ marginTop: 8 }}>
            بیشترین استریک: {summary?.longest_streak || 0} روز
          </div>
        </div>

        {!status?.already_checked_in_today ? (
          <div className="card checkin-question">
            <h2>امروز سیگار کشیدی؟</h2>
            <div className="checkin-buttons">
              <button
                className="btn btn-success"
                onClick={() => handleCheckIn(true)}
                disabled={submitting}
              >
                نه، پاک بودم ✅
              </button>
              <button
                className="btn btn-danger"
                onClick={() => handleCheckIn(false)}
                disabled={submitting}
              >
                آره، کشیدم
              </button>
            </div>
          </div>
        ) : (
          <div className="card" style={{ textAlign: 'center' }}>
            <p className="muted">برای امروز ثبت کردی. فردا دوباره میایم سراغت 👋</p>
          </div>
        )}

        {feedback && (
          <div className="card" style={{ textAlign: 'center' }}>
            <p style={{ margin: 0 }}>{feedback}</p>
          </div>
        )}
      </div>

      <BottomNav />
    </div>
  )
}
