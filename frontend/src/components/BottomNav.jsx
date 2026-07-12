import { useNavigate, useLocation } from 'react-router-dom'

const items = [
  { path: '/', label: 'خانه', icon: '🏠' },
  { path: '/goal', label: 'هدف', icon: '🎯' },
  { path: '/leaderboard', label: 'برترها', icon: '🏆' },
  { path: '/profile', label: 'پروفایل', icon: '👤' },
]

export default function BottomNav() {
  const navigate = useNavigate()
  const location = useLocation()

  return (
    <nav className="bottom-nav">
      {items.map((item) => (
        <button
          key={item.path}
          className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
          onClick={() => navigate(item.path)}
        >
          <span>{item.icon}</span>
          <span>{item.label}</span>
        </button>
      ))}
    </nav>
  )
}
