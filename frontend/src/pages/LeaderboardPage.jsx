import { useState, useEffect } from 'react'
import { getStreakLeaderboard, getSavingsLeaderboard } from '../api/leaderboard'
import BottomNav from '../components/BottomNav'

function formatToman(amount) {
  return new Intl.NumberFormat('fa-IR').format(Math.round(Number(amount)))
}

export default function LeaderboardPage() {
  const [tab, setTab] = useState('streak') // 'streak' | 'savings'
  const [entries, setEntries] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadEntries(tab)
  }, [tab])

  async function loadEntries(activeTab) {
    setLoading(true)
    try {
      const data = activeTab === 'streak'
        ? await getStreakLeaderboard()
        : await getSavingsLeaderboard()
      setEntries(data)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <div className="top-bar">
        <span className="brand">لیست برترها 🏆</span>
      </div>

      <div className="page">
        <div className="checkin-buttons" style={{ marginBottom: 20 }}>
          <button
            className={tab === 'streak' ? 'btn btn-success' : 'btn btn-primary-outline'}
            onClick={() => setTab('streak')}
          >
            بیشترین روز پاکی
          </button>
          <button
            className={tab === 'savings' ? 'btn btn-success' : 'btn btn-primary-outline'}
            onClick={() => setTab('savings')}
          >
            بیشترین پس‌انداز
          </button>
        </div>

        <div className="card">
          {loading ? (
            <p className="muted">در حال بارگذاری...</p>
          ) : entries.length === 0 ? (
            <p className="muted">هنوز کسی در این لیست نیست.</p>
          ) : (
            entries.map((entry) => (
              <div
                key={entry.rank}
                className={`leaderboard-row ${entry.is_current_user ? 'is-me' : ''}`}
              >
                <span className="leaderboard-rank">{entry.rank}</span>
                <span className="leaderboard-name">{entry.display_name}</span>
                <span className="leaderboard-value">
                  {tab === 'streak'
                    ? `${formatToman(entry.value)} روز`
                    : `${formatToman(entry.value)} تومان`}
                </span>
              </div>
            ))
          )}
        </div>
      </div>

      <BottomNav />
    </div>
  )
}
