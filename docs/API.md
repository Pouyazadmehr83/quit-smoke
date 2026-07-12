# مستند API

> **توجه**: علاوه بر این سند، یک رابط Swagger زنده و تعاملی در آدرس
> `http://localhost:8000/api/docs/` بعد از بالا آمدن پروژه در دسترس است.

تمام پاسخ‌ها JSON هستند. تمام endpoint های زیر «احراز هویت» (`POST
/auth/register/` و `/auth/login/`) به استثنای رجیستر و لاگین، نیاز به
هدر زیر دارند:

```
Authorization: Bearer <access_token>
```

---

## احراز هویت (`/api/auth/`)

### `POST /api/auth/register/`
ثبت‌نام کاربر جدید.

**ورودی:**
```json
{
  "email": "ali@example.com",
  "password": "رمزعبور۸کاراکتری",
  "display_name": "علی"
}
```

**خروجی (201):**
```json
{ "id": 1, "email": "ali@example.com", "display_name": "علی" }
```

### `POST /api/auth/login/`
ورود و دریافت توکن.

**ورودی:**
```json
{ "email": "ali@example.com", "password": "رمزعبور۸کاراکتری" }
```

**خروجی (200):**
```json
{ "access": "eyJ...", "refresh": "eyJ..." }
```

### `POST /api/auth/refresh/`
گرفتن `access` token جدید با `refresh` token.

**ورودی:** `{ "refresh": "eyJ..." }`
**خروجی:** `{ "access": "eyJ..." }`

### `GET /api/auth/me/`
اطلاعات کاربر فعلی.

**خروجی:**
```json
{ "id": 1, "email": "ali@example.com", "display_name": "علی", "date_joined": "..." }
```

### `GET /api/auth/smoking-profile/`
دریافت پروفایل سیگار کاربر فعلی. اگر هنوز ثبت نشده باشد: `404`.

### `POST /api/auth/smoking-profile/`
ساخت پروفایل سیگار (فقط یک‌بار - اگر از قبل وجود داشته باشد `400`).

**ورودی:**
```json
{
  "brand_name": "وینستون اولترا",
  "pack_price_toman": 150000,
  "cigarettes_per_pack": 20,
  "cigarettes_per_day": 10
}
```

**خروجی (201):**
```json
{
  "id": 1,
  "brand_name": "وینستون اولترا",
  "pack_price_toman": 150000,
  "cigarettes_per_pack": 20,
  "cigarettes_per_day": 10,
  "quit_start_date": "2026-06-20",
  "price_per_cigarette": 7500.0,
  "daily_saving_amount": 75000.0,
  "created_at": "...",
  "updated_at": "..."
}
```

### `PUT /api/auth/smoking-profile/`
ویرایش پروفایل سیگار موجود (مثلاً تغییر برند).

---

## پیگیری روزانه (`/api/tracking/`)

### `GET /api/tracking/today/`
**مهم‌ترین endpoint داشبورد.** وضعیت امروز کاربر + خلاصه‌ی کامل استریک
و پس‌انداز.

**خروجی:**
```json
{
  "already_checked_in_today": false,
  "streak_summary": {
    "current_streak": 5,
    "longest_streak": 12,
    "total_smoke_free_days": 30,
    "total_money_saved": "2250000",
    "last_relapse_date": "2026-06-01",
    "last_checkin_date": "2026-06-19",
    "updated_at": "..."
  }
}
```

### `POST /api/tracking/checkin/`
ثبت وضعیت روزانه (سوال «امروز سیگار کشیدی؟»).

**ورودی:**
```json
{ "is_smoke_free": true, "note": "روز سختی بود ولی موفق شدم" }
```
- `date` اختیاری است (پیش‌فرض: امروز).
- `note` اختیاری است.

**خروجی (201):** رکورد چک‌این ساخته‌شده.
**خطا (400):** اگر برای آن تاریخ قبلاً چک‌این ثبت شده باشد.

### `GET /api/tracking/checkin/`
تاریخچه‌ی ۳۰ چک‌این آخر کاربر.

### `GET /api/tracking/summary/`
فقط خلاصه‌ی استریک (بدون اطلاع «آیا امروز چک‌این کرده»)، برای جایی که
صرفاً آمار لازم است.

---

## هدف‌گذاری مالی (`/api/goals/`)

### `GET /api/goals/`
لیست تمام هدف‌های کاربر.

### `POST /api/goals/`
ساخت هدف جدید.

**ورودی:**
```json
{ "title": "خرید موتور هوندا", "target_amount_toman": 50000000, "is_active": true }
```

> اگر `is_active: true` باشد، سایر هدف‌های قبلی کاربر به‌صورت خودکار
> `is_active: false` می‌شوند (فقط یک هدف اصلی در داشبورد نمایش داده می‌شود).

### `GET /api/goals/<id>/`
جزئیات یک هدف.

### `PATCH /api/goals/<id>/`
ویرایش هدف (مثلاً تغییر عنوان یا مقدار).

### `DELETE /api/goals/<id>/`
حذف هدف.

### `GET /api/goals/active/progress/`
**مهم‌ترین endpoint صفحه‌ی هدف.** پیشرفت هدف فعال (اصلی) کاربر.

**خروجی:**
```json
{
  "goal_id": 3,
  "title": "خرید موتور هوندا",
  "target_amount_toman": 50000000,
  "current_saved_toman": "2250000",
  "remaining_amount_toman": "47750000",
  "progress_percent": 4.5,
  "estimated_days_remaining": 637,
  "is_achieved": false
}
```
اگر هدف فعالی وجود نداشته باشد: `404`.

### `GET /api/goals/<id>/progress/`
پیشرفت یک هدف مشخص (با همان فرمت بالا).

---

## لیست برترها (`/api/leaderboard/`)

### `GET /api/leaderboard/streaks/`
۲۰ نفر برتر بر اساس بیشترین استریک فعلی (روزهای پاکی متوالی).

### `GET /api/leaderboard/savings/`
۲۰ نفر برتر بر اساس بیشترین پول پس‌انداز شده.

**خروجی (هر دو، فرمت یکسان):**
```json
[
  { "rank": 1, "display_name": "علی", "value": "12", "is_current_user": true },
  { "rank": 2, "display_name": "مریم", "value": "8", "is_current_user": false }
]
```
> توجه: هیچ‌وقت ایمیل کاربران در لیدربورد نمایش داده نمی‌شود.

---

## کدهای خطای رایج

| کد | معنی |
|---|---|
| 400 | ورودی نامعتبر یا عملیات تکراری (مثلاً چک‌این دوباره برای یک روز) |
| 401 | توکن نامعتبر یا منقضی شده |
| 404 | رکورد یافت نشد (مثلاً هدف فعال یا پروفایل سیگار ثبت نشده) |
