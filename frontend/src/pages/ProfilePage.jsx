import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getSmokingProfile, updateSmokingProfile, logout } from '../api/auth'
import { useAuth } from '../context/AuthContext'
import BottomNav from '../components/BottomNav'

export default function ProfilePage() {
  const { user, setUser } = useAuth()
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    getSmokingProfile()
      .then(setProfile)
      .catch(() => setProfile(null))
      .finally(() => setLoading(false))
  }, [])

  function handleLogout() {
    logout()
    setUser(null)
    navigate('/login')
  }

  async function handleSave(e) {
    e.preventDefault()
    const form = new FormData(e.target)
    const updated = await updateSmokingProfile({
      brand_name: form.get('brand_name'),
      pack_price_toman: Number(form.get('pack_price_toman')),
      cigarettes_per_pack: Number(form.get('cigarettes_per_pack')),
      cigarettes_per_day: Number(form.get('cigarettes_per_day')),
    })
    setProfile(updated)
    setEditing(false)
  }

  return (
    <div className="app-shell">
      <div className="top-bar">
        <span className="brand">پروفایل 👤</span>
      </div>

      <div className="page">
        <div className="card">
          <div className="card-title">{user?.display_name || user?.email}</div>
          <p className="muted">{user?.email}</p>
        </div>

        {loading ? (
          <p className="muted">در حال بارگذاری...</p>
        ) : profile && !editing ? (
          <div className="card">
            <div className="card-title">اطلاعات سیگار</div>
            <p><strong>برند:</strong> {profile.brand_name}</p>
            <p><strong>قیمت پاکت:</strong> {profile.pack_price_toman.toLocaleString('fa-IR')} تومان</p>
            <p><strong>تعداد روزانه:</strong> {profile.cigarettes_per_day} عدد</p>
            <button className="btn btn-primary-outline btn-full" onClick={() => setEditing(true)}>
              ویرایش اطلاعات
            </button>
          </div>
        ) : profile && editing ? (
          <form className="card" onSubmit={handleSave}>
            <div className="form-group">
              <label className="form-label">برند سیگار</label>
              <input name="brand_name" className="form-input" defaultValue={profile.brand_name} required />
            </div>
            <div className="form-group">
              <label className="form-label">قیمت پاکت (تومان)</label>
              <input name="pack_price_toman" type="number" className="form-input" defaultValue={profile.pack_price_toman} required />
            </div>
            <div className="form-group">
              <label className="form-label">تعداد در پاکت</label>
              <input name="cigarettes_per_pack" type="number" className="form-input" defaultValue={profile.cigarettes_per_pack} required />
            </div>
            <div className="form-group">
              <label className="form-label">تعداد روزانه (قبل از ترک)</label>
              <input name="cigarettes_per_day" type="number" className="form-input" defaultValue={profile.cigarettes_per_day} required />
            </div>
            <button type="submit" className="btn btn-success btn-full">ذخیره</button>
          </form>
        ) : (
          <div className="card">
            <p className="muted">هنوز پروفایل سیگار ثبت نکردی.</p>
            <button className="btn btn-success btn-full" onClick={() => navigate('/onboarding')}>
              تکمیل پروفایل
            </button>
          </div>
        )}

        <button className="btn btn-danger btn-full" onClick={handleLogout} style={{ marginTop: 8 }}>
          خروج از حساب
        </button>
      </div>

      <BottomNav />
    </div>
  )
}
