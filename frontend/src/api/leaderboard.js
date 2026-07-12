import client from './client'

export async function getStreakLeaderboard() {
  const { data } = await client.get('/leaderboard/streaks/')
  return data
}

export async function getSavingsLeaderboard() {
  const { data } = await client.get('/leaderboard/savings/')
  return data
}
