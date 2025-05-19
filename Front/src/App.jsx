import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState('');
  const [conversations, setConversations] = useState([]);
  const [showDropdown, setShowDropdown] = useState(true);

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      const res = await fetch('http://localhost:8000/conversations');
      const data = await res.json();
      console.log('Conversaciones obtenidas:', data.conversation_ids);
      setConversations(data.conversation_ids);
    } catch (error) {
      console.error("Error fetching conversations", error);
    }
  };

  const createConversation = async () => {
    try {
      const res = await fetch('http://localhost:8000/conversations', { method: 'POST' });
      const data = await res.json();
      console.log('Nueva conversación creada automáticamente:', data);
      setConversationId(data.conversation_id);
      setHistory([]);
      fetchConversations();
      return data.conversation_id;
    } catch (error) {
      console.error('Error creando conversación automática', error);
      return null;
    }
  };

  const handleSend = async () => {
    if (!query.trim()) return;

    let activeConversationId = conversationId;

    if (!activeConversationId) {
      // Crear una conversación automáticamente
      activeConversationId = await createConversation();
      if (!activeConversationId) return; // Si falla la creación
    }

    setLoading(true);
    try {
      console.log('Enviando mensaje al backend con:', {
        query,
        conversation_id: activeConversationId
      });

      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, conversation_id: activeConversationId }),
      });

      const data = await res.json();
      console.log('Respuesta del backend:', data);

      setConversationId(data.conversation_id);
      setHistory([...history, { query, response: data.response }]);
      setQuery('');
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleCreateConversation = async () => {
    await createConversation();
  };

  const handleSelectConversation = async (id) => {
    setConversationId(id);
    console.log('Recuperando conversación:', id);

    try {
      const res = await fetch(`http://localhost:8000/conversations/${id}`);
      const data = await res.json();
      console.log('Historial recuperado:', data);

      if (Array.isArray(data.messages)) {
        const formatted = data.messages.map(([query, response]) => ({ query, response }));
        setHistory(formatted);
      } else {
        console.error('Formato de historial inesperado:', data.messages);
      }
    } catch (error) {
      console.error('Error fetching conversation history', error);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>🤖 AI Medicine Manager</h1>
      </header>

      {/* Botón para mostrar sidebar si está oculta */}
      {!showDropdown && (
        <button
          className="toggle-sidebar-button"
          onClick={() => setShowDropdown(true)}
        >
          Mostrar conversaciones
        </button>
      )}

      {/* Sidebar de conversaciones */}
      {showDropdown && (
        <div className="sidebar">
          <button onClick={() => setShowDropdown(false)}>Ocultar</button>
          <h3>Conversaciones</h3>
          <button onClick={handleCreateConversation}>Crear nueva conversación</button>
          <ul>
            {conversations.map((id) => (
              <li key={id}>
                <button onClick={() => handleSelectConversation(id)}>
                  {id === conversationId ? <strong>{id}</strong> : id}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      <main className="chat-container">
        {history.map((item, index) => (
          <div key={index} className="message-bubble">
            <div className="user-message">
              <p className="user">Tú</p>
              <p>{item.query}</p>
            </div>
            <div className="bot-message">
              <p className="bot">Bot</p>
              <p>{item.response}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="message-bubble loading">
            <div className="bot-message">
              <p className="bot">Bot</p>
              <p>Escribiendo...</p>
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <textarea
          className="input-box"
          rows="1"
          placeholder="Escribe tu mensaje..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button onClick={handleSend} disabled={loading} className="send-button">
          {loading ? 'Enviando...' : 'Enviar'}
        </button>
      </footer>
    </div>
  );
}

export default App;
