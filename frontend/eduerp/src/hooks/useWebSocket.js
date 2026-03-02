// frontend/src/hooks/useWebSocket.js
import { useEffect, useRef, useCallback } from 'react';
import { useSelector } from 'react-redux';

export const useWebSocket = (url, onMessage) => {
  const ws = useRef(null);
  const { tokens } = useSelector((state) => state.auth);

  const connect = useCallback(() => {
    if (!tokens?.access) return;

    try {
      ws.current = new WebSocket(`${url}?token=${tokens.access}`);
      
      ws.current.onopen = () => {
        console.log('WebSocket connected');
      };

      ws.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          onMessage(data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      ws.current.onclose = () => {
        console.log('WebSocket disconnected');
        // Reconnect after delay
        setTimeout(() => connect(), 3000);
      };

      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    } catch (error) {
      console.error('WebSocket connection failed:', error);
    }
  }, [tokens, url, onMessage]);

  const sendMessage = useCallback((message) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    }
  }, []);

  useEffect(() => {
    connect();

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [connect]);

  return { sendMessage };
};

export default useWebSocket;
