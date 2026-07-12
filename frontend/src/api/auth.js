import client from './client'

export async function register({ email, password, display_name }) {
  const { data } = await client.post('/auth/register/', { email, password, display_name })
  return data
}

export async function login({ email, password }) {
  const { data } = await client.post('/auth/login/', { email, password })
  localStorage.setItem('access_token', data.access)
  localStorage.setItem('refresh_token', data.refresh)
  return data
}

export function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

export async function getMe() {
  const { data } = await client.get('/auth/me/')
  return data
}

export async function getSmokingProfile() {
  const { data } = await client.get('/auth/smoking-profile/')
  return data
}

export async function createSmokingProfile(payload) {
  const { data } = await client.post('/auth/smoking-profile/', payload)
  return data
}

export async function updateSmokingProfile(payload) {
  const { data } = await client.put('/auth/smoking-profile/', payload)
  return data
}
