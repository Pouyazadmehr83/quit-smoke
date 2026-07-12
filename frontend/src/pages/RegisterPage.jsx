import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { register, login, getMe } from '../api/auth'
import { useAuth } from '../context/AuthContext'

export default function RegisterPage() {
  const [email, setEmail] = useState('')
  const [displayName, setDisplayName] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { setUser } = useAuth()

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await register({ email, password, display_name: displayName })
      await login({ email, password })
      const me = await getMe()
      setUser(me)
      navigate('/onboarding')
    } catch (err) {
      const detail = err.response?.data
      setError(detail?.email?.[0] || detail?.password?.[0] || 'خطایی رخ داد. دوباره تلاش کن.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="center-page">
      <h1 className="auth-title">شروع پاکی 🌿</h1>
      <p className="auth-subtitle">اولین قدم برای دیدن پس‌اندازت</p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">نام نمایشی</label>
          <input
            type="text"
            className="form-input"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            placeholder="مثلا علی"
            required
          />
        </div>
        <div className="form-group">
          <label className="form-label">ایمیل</label>
          <input
            type="email"
            className="form-input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label className="form-label">رمز عبور</label>
          <input
            type="password"
            className="form-input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            minLength={8}
            required
          />
        </div>
        {error && <p className="error-text">{error}</p>}
        <button type="submit" className="btn btn-success btn-full" disabled={loading}>
          {loading ? 'در حال ساخت حساب...' : 'ثبت‌نام'}
        </button>
      </form>

      <p style={{ textAlign: 'center', marginTop: 20 }} className="muted">
        حساب داری؟ <Link to="/login" className="link-button">وارد شو</Link>
      </p>
    </div>
  )
}
