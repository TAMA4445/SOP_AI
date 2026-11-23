// API service helper untuk SOP-GPT Backend
const API_BASE = '/api';

export function getStoredToken() {
  return localStorage.getItem('sop_token');
}

export function setStoredToken(token) {
  if (token) {
    localStorage.setItem('sop_token', token);
  } else {
    localStorage.removeItem('sop_token');
  }
}

export function getStoredUser() {
  const user = localStorage.getItem('sop_user');
  return user ? JSON.parse(user) : null;
}

export function setStoredUser(user) {
  if (user) {
    localStorage.setItem('sop_user', JSON.stringify(user));
  } else {
    localStorage.removeItem('sop_user');
  }
}

async function request(endpoint, options = {}) {
  const token = getStoredToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers || {}),
  };

  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data.error || `HTTP error ${res.status}`);
    }
    return { data, error: null };
  } catch (err) {
    return { data: null, error: err.message || 'Gagal menghubungi server' };
  }
}

export const api = {
  // 1. Auth
  async login(username, password) {
    return request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  },

  async getMe() {
    return request('/auth/me');
  },

  // 2. Chat
  async sendMessage(question, sessionId = null) {
    return request('/chat', {
      method: 'POST',
      body: JSON.stringify({ question, session_id: sessionId }),
    });
  },

  async getSessions() {
    return request('/chat/sessions');
  },

  async getHistory(sessionId) {
    return request(`/chat/history?session_id=${encodeURIComponent(sessionId)}`);
  },

  // 3. Feedback
  async sendFeedback(messageId, rating, comment = '') {
    return request('/feedback', {
      method: 'POST',
      body: JSON.stringify({ message_id: messageId, rating, comment }),
    });
  },

  // 4. Dokumen & Stats (Admin)
  async getDocuments() {
    return request('/documents');
  },

  async getStats() {
    return request('/stats');
  },
};
