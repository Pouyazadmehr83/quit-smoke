import client from './client'

export async function getGoals() {
  const { data } = await client.get('/goals/')
  return data
}

export async function createGoal(payload) {
  const { data } = await client.post('/goals/', payload)
  return data
}

export async function getActiveGoalProgress() {
  const { data } = await client.get('/goals/active/progress/')
  return data
}
