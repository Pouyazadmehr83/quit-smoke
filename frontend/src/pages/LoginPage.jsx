import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { login } from '../api/auth'
import { useAuth } from '../context/AuthContext'
import { getMe } from '../api/auth'

export default function LoginPage() {
  const [email, setEmail] = useState('')
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
      await login({ email, password })
      const me = await getMe()
      setUser(me)
      navigate('/')
    } catch (err) {
      setError('ایمیل یا رمز عبور نادرست است.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="center-page">
      <h1 className="auth-title">ترک‌یار 🌿</h1>
      <p className="auth-subtitle">پس‌انداز هر روزِ پاکی‌ات را ببین</p>

      <form onSubmit={handleSubmit}>
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
            required
          />
        </div>
        {error && <p className="error-text">{error}</p>}
        <button type="submit" className="btn btn-success btn-full" disabled={loading}>
          {loading ? 'در حال ورود...' : 'ورود'}
        </button>
      </form>

      <p style={{ textAlign: 'center', marginTop: 20 }} className="muted">
        حساب نداری؟ <Link to="/register" className="link-button">ثبت‌نام کن</Link>
      </p>
    </div>
  )
}
