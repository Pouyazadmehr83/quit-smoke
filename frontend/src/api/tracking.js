import client from './client'

export async function getTodayStatus() {
  const { data } = await client.get('/tracking/today/')
  return data
}

export async function submitCheckIn({ is_smoke_free, note = '' }) {
  const { data } = await client.post('/tracking/checkin/', { is_smoke_free, note })
  return data
}

export async function getCheckInHistory() {
  const { data } = await client.get('/tracking/checkin/')
  return data
}
