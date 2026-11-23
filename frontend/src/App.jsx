import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import LoginPage from './components/LoginPage';
import { api, getStoredToken, getStoredUser, setStoredToken, setStoredUser } from './services/api';

// Jawaban Dummy untuk simulasi presentasi / testing Minggu 1
const DUMMY_RESPONSES = [
  {
    trigger: ['loto', 'kunci', 'lockout'],
    answer: 'Prosedur Lockout/Tagout (LOTO) wajib diterapkan sebelum melakukan perawatan atau perbaikan mesin. Setiap teknisi wajib memasang gembok pribadi (padlock) dan tag peringatan pada sakelar pemutus energi utama. Pada pekerjaan kelompok, wajib menggunakan hasp pengunci multipel (Group Lockout Box).',
    sources: [
      {
        doc: 'SOP_LOTO_v1.pdf',
        page: 4,
        snippet: 'Bagian 4.2: Pada sistem Group Lockout, setiap pekerja berwenang harus menempelkan gembok pengaman pribadi ke kotak lockout kelompok sebelum memulai pekerjaan.',
      },
      {
        doc: 'SOP_LOTO_v1.pdf',
        page: 2,
        snippet: 'Bagian 2.1: Isolasi energi meliputi pemutusan daya listrik, pelepasan tekanan hidrolik/pneumatik, dan penguncian katup mekanis.',
      },
    ],
  },
  {
    trigger: ['apd', 'pelindung', 'helm', 'sarung tangan'],
    answer: 'Sesuai SOP APD Pabrik, teknisi yang bekerja di area kelistrikan dan mekanik wajib menggunakan: Helm keselamatan (Safety Helmet Standar ANSI), Kacamata pelindung (Safety Goggles), Sepatu safety bersol isolator 1000V, dan Sarung tangan tahan percikan/tegangan tinggi.',
    sources: [
      {
        doc: 'SOP_APD_v1.pdf',
        page: 3,
        snippet: 'Tabel 1: Matriks penggunaan APD wajib per area kerja operasional dan bengkel mekanik.',
      },
    ],
  },
  {
    trigger: ['kebakaran', 'api', 'apar', 'evakuasi'],
    answer: 'Jika terjadi kebakaran di area kerja, terapkan prosedur PASS pada APAR terdekat: Pull (Tarik pin), Aim (Arahkan corong ke dasar api), Squeeze (Tekan tuas), Sweep (Sapukan dari sisi ke sisi). Segera bunyikan alarm darurat dan ikuti jalur evakuasi menuju Titik Kumpul (Assembly Point) di halaman depan.',
    sources: [
      {
        doc: 'SOP_Kebakaran_v1.pdf',
        page: 5,
        snippet: 'Prosedur Tanggap Darurat Kebakaran: Hubungi posko keselamatan ext 112 dan jangan gunakan lift.',
      },
    ],
  },
];

export default function App() {
  const [user, setUser] = useState(null);
  const [isDummyMode, setIsDummyMode] = useState(false);
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Cek token tersimpan saat load
  useEffect(() => {
    const savedUser = getStoredUser();
    const token = getStoredToken();
    if (savedUser && token) {
      setUser(savedUser);
      loadSessions();
    }
  }, []);

  const loadSessions = async () => {
    const res = await api.getSessions();
    if (res.data && res.data.sessions) {
      setSessions(res.data.sessions);
      if (res.data.sessions.length > 0 && !activeSessionId) {
        loadHistory(res.data.sessions[0].session_id);
      }
    }
  };

  const loadHistory = async (sessionId) => {
    setActiveSessionId(sessionId);
    const res = await api.getHistory(sessionId);
    if (res.data && res.data.messages) {
      const formatted = [];
      res.data.messages.forEach((m) => {
        formatted.push({ role: 'user', text: m.question, timestamp: m.created_at });
        formatted.push({
          role: 'assistant',
          answer: m.answer,
          sources: m.sources,
          message_id: m.message_id,
          feedback: m.feedback,
          timestamp: m.created_at,
        });
      });
      setMessages(formatted);
    }
  };

  const handleLoginSuccess = (userData, isDummy = false) => {
    setUser(userData);
    setIsDummyMode(isDummy);
    if (!isDummy) {
      loadSessions();
    }
  };

  const handleUseDummy = () => {
    const dummyUser = {
      username: 'teknisi_demo',
      role: 'teknisi',
      full_name: 'Teknisi Demo (Simulasi)',
    };
    setUser(dummyUser);
    setIsDummyMode(true);
    setSessions([
      { session_id: 'demo-1', title: 'Tanya Prosedur LOTO Mesin' },
      { session_id: 'demo-2', title: 'Standar APD Bengkel' },
    ]);
  };

  const handleLogout = () => {
    setStoredToken(null);
    setStoredUser(null);
    setUser(null);
    setSessions([]);
    setMessages([]);
    setActiveSessionId(null);
  };

  const handleNewChat = () => {
    setActiveSessionId(null);
    setMessages([]);
  };

  const handleSelectSession = (sessionId) => {
    if (isDummyMode) {
      setActiveSessionId(sessionId);
      if (sessionId === 'demo-1') {
        setMessages([
          { role: 'user', text: 'Bagaimana prosedur LOTO untuk mesin press?' },
          {
            role: 'assistant',
            answer: DUMMY_RESPONSES[0].answer,
            sources: DUMMY_RESPONSES[0].sources,
          },
        ]);
      } else {
        setMessages([
          { role: 'user', text: 'Apa APD wajib untuk teknisi las?' },
          {
            role: 'assistant',
            answer: DUMMY_RESPONSES[1].answer,
            sources: DUMMY_RESPONSES[1].sources,
          },
        ]);
      }
      return;
    }
    loadHistory(sessionId);
  };

  const handleSendMessage = async (text) => {
    const userMsg = { role: 'user', text, timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    // 1. Jika dalam mode Dummy (Demo Frontend)
    if (isDummyMode) {
      setTimeout(() => {
        const lower = text.toLowerCase();
        const matched = DUMMY_RESPONSES.find((item) =>
          item.trigger.some((t) => lower.includes(t))
        );

        const botReply = matched
          ? {
              role: 'assistant',
              answer: matched.answer,
              sources: matched.sources,
              timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            }
          : {
              role: 'assistant',
              answer:
                'Informasi mengenai "' +
                text +
                '" telah diverifikasi terhadap basis dokumen SOP. Untuk keselamatan operasional, selalu patuhi pedoman K3 yang tertera pada manual masing-masing unit mesin.',
              sources: [
                {
                  doc: 'SOP_Standar_Operasional_Umum.pdf',
                  page: 1,
                  snippet: 'Semua personil diwajibkan mematuhi rambu-rambu bahaya di area pabrik.',
                },
              ],
              timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            };

        setMessages((prev) => [...prev, botReply]);
        setLoading(false);

        if (!activeSessionId) {
          const newId = 'session-' + Date.now();
          setActiveSessionId(newId);
          setSessions((prev) => [{ session_id: newId, title: text.slice(0, 28) + '...' }, ...prev]);
        }
      }, 700);
      return;
    }

    // 2. Jika dalam mode Backend Asli (Menghubungkan ke Flask API)
    const res = await api.sendMessage(text, activeSessionId);
    setLoading(false);

    if (res.data) {
      const botReply = {
        role: 'assistant',
        answer: res.data.answer,
        sources: res.data.sources || [],
        message_id: res.data.message_id,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, botReply]);

      if (!activeSessionId && res.data.session_id) {
        setActiveSessionId(res.data.session_id);
        setSessions((prev) => [
          { session_id: res.data.session_id, title: text.slice(0, 28) + '...' },
          ...prev,
        ]);
      }
    } else {
      // Jika backend gagal diakses
      const errorReply = {
        role: 'assistant',
        answer:
          '⚠️ Maaf, server backend tidak dapat dihubungi (' +
          (res.error || 'Connection Refused') +
          '). Pastikan backend Flask di port 5000 sudah berjalan, atau gunakan tombol "Mode Dummy" di sidebar untuk melihat demo UI.',
        sources: [],
      };
      setMessages((prev) => [...prev, errorReply]);
    }
  };

  // Tampilkan halaman Login jika belum ada user
  if (!user) {
    return (
      <LoginPage
        onLoginSuccess={handleLoginSuccess}
        onUseDummy={handleUseDummy}
      />
    );
  }

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-900 text-slate-100 font-sans">
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onSelectSession={handleSelectSession}
        onNewChat={handleNewChat}
        currentUser={user}
        onLogout={handleLogout}
        isDummyMode={isDummyMode}
        onToggleDummy={() => setIsDummyMode(!isDummyMode)}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      <ChatArea
        messages={messages}
        onSendMessage={handleSendMessage}
        loading={loading}
        isDummyMode={isDummyMode}
        onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
      />
    </div>
  );
}

