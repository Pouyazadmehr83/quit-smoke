import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createSmokingProfile } from '../api/auth'

export default function OnboardingPage() {
  const [brandName, setBrandName] = useState('')
  const [packPrice, setPackPrice] = useState('')
  const [cigarettesPerPack, setCigarettesPerPack] = useState(20)
  const [cigarettesPerDay, setCigarettesPerDay] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await createSmokingProfile({
        brand_name: brandName,
        pack_price_toman: Number(packPrice),
        cigarettes_per_pack: Number(cigarettesPerPack),
        cigarettes_per_day: Number(cigarettesPerDay),
      })
      navigate('/')
    } catch (err) {
      setError('لطفا مقادیر را بررسی کن.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <h2 style={{ color: 'var(--color-primary-deep)', marginBottom: 4 }}>چی می‌کشیدی؟</h2>
      <p className="muted" style={{ marginBottom: 24 }}>
        این اطلاعات فقط برای محاسبه‌ی دقیق پس‌اندازت استفاده می‌شود.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">برند سیگار</label>
          <input
            type="text"
            className="form-input"
            placeholder="مثلا وینستون اولترا"
            value={brandName}
            onChange={(e) => setBrandName(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">قیمت یک پاکت (تومان)</label>
          <input
            type="number"
            className="form-input"
            placeholder="150000"
            value={packPrice}
            onChange={(e) => setPackPrice(e.target.value)}
            min={1000}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">تعداد سیگار در هر پاکت</label>
          <input
            type="number"
            className="form-input"
            value={cigarettesPerPack}
            onChange={(e) => setCigarettesPerPack(e.target.value)}
            min={1}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">چند تا در روز می‌کشیدی؟</label>
          <input
            type="number"
            className="form-input"
            placeholder="10"
            value={cigarettesPerDay}
            onChange={(e) => setCigarettesPerDay(e.target.value)}
            min={1}
            required
          />
        </div>

        {error && <p className="error-text">{error}</p>}

        <button type="submit" className="btn btn-success btn-full" disabled={loading}>
          {loading ? 'در حال ذخیره...' : 'شروع کن'}
        </button>
      </form>
    </div>
  )
}
