/**
 * حلقه‌ی نفَس: استعاره‌ی بصری از نفس کشیدن آرام به‌جای دود کردن سیگار.
 * هرچه روزهای پاکی بیشتر شود، حلقه پُرتر می‌شود (تا یک سقف بصری 60 روزه که بعد از آن کامل می‌ماند).
 */
export default function BreathRing({ days }) {
  const radius = 80
  const circumference = 2 * Math.PI * radius
  const visualCap = 60
  const progress = Math.min(days / visualCap, 1)
  const offset = circumference * (1 - progress)

  return (
    <div className="breath-ring-wrap">
      <svg className="breath-ring-svg" viewBox="0 0 180 180">
        <circle className="breath-ring-bg" cx="90" cy="90" r={radius} />
        <circle
          className="breath-ring-progress"
          cx="90"
          cy="90"
          r={radius}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
        />
      </svg>
      <div className="breath-ring-center">
        <span className="breath-ring-days">{days}</span>
        <span className="breath-ring-sub">روز پاکی</span>
      </div>
    </div>
  )
}
