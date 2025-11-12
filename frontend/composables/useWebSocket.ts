/**
 * WebSocket composable for real-time ticket updates
 * 
 * Provides reactive WebSocket connection management with:
 * - Auto-reconnection with exponential backoff
 * - Event-based message handling
 * - Connection status tracking
 * - Agent presence updates
 */

import { ref, onMounted, onUnmounted, computed } from 'vue'

interface WebSocketMessage {
  type: string
  [key: string]: any
}

type MessageHandler = (data: any) => void

export const useWebSocket = (agentId?: string) => {
  const ws = ref<WebSocket | null>(null)
  const isConnected = ref(false)
  const connectionId = ref<string | null>(null)
  const reconnectAttempts = ref(0)
  const maxReconnectAttempts = 10
  const reconnectTimeout = ref<ReturnType<typeof setTimeout> | null>(null)
  
  // Message handlers
  const messageHandlers = new Map<string, Set<MessageHandler>>()
  
  /**
   * Register a message handler for a specific message type
   */
  const on = (type: string, handler: MessageHandler) => {
    if (!messageHandlers.has(type)) {
      messageHandlers.set(type, new Set())
    }
    messageHandlers.get(type)!.add(handler)
    
    // Return unsubscribe function
    return () => {
      messageHandlers.get(type)?.delete(handler)
    }
  }
  
  /**
   * Emit a message to all registered handlers
   */
  const emit = (type: string, data: any) => {
    const handlers = messageHandlers.get(type)
    if (handlers) {
      handlers.forEach(handler => handler(data))
    }
  }
  
  /**
   * Calculate reconnect delay with exponential backoff
   */
  const getReconnectDelay = () => {
    const baseDelay = 1000 // 1 second
    const maxDelay = 30000 // 30 seconds
    const delay = Math.min(baseDelay * Math.pow(2, reconnectAttempts.value), maxDelay)
    return delay
  }
  
  /**
   * Connect to WebSocket server
   */
  const connect = () => {
    try {
      const wsUrl = `ws://localhost:8000/ws/tickets${agentId ? `?agent_id=${agentId}` : ''}`
      ws.value = new WebSocket(wsUrl)
      
      ws.value.onopen = () => {
        console.log('✅ WebSocket connected')
        isConnected.value = true
        reconnectAttempts.value = 0
        
        // Start ping interval to keep connection alive
        startPingInterval()
      }
      
      ws.value.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          console.log('📨 WebSocket message:', message.type)
          
          // Handle connection establishment
          if (message.type === 'connection_established') {
            connectionId.value = message.connection_id
          }
          
          // Emit to registered handlers
          emit(message.type, message)
          emit('*', message) // Wildcard for all messages
          
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }
      
      ws.value.onerror = (error) => {
        console.error('❌ WebSocket error:', error)
      }
      
      ws.value.onclose = () => {
        console.log('🔌 WebSocket disconnected')
        isConnected.value = false
        connectionId.value = null
        stopPingInterval()
        
        // Attempt to reconnect
        if (reconnectAttempts.value < maxReconnectAttempts) {
          const delay = getReconnectDelay()
          console.log(`🔄 Reconnecting in ${delay}ms... (attempt ${reconnectAttempts.value + 1}/${maxReconnectAttempts})`)
          reconnectAttempts.value++
          reconnectTimeout.value = setTimeout(connect, delay)
        } else {
          console.error('⚠️ Max reconnection attempts reached')
        }
      }
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error)
    }
  }
  
  /**
   * Disconnect from WebSocket server
   */
  const disconnect = () => {
    if (reconnectTimeout.value) {
      clearTimeout(reconnectTimeout.value)
      reconnectTimeout.value = null
    }
    stopPingInterval()
    
    if (ws.value) {
      ws.value.close()
      ws.value = null
    }
  }
  
  /**
   * Send a message to the server
   */
  const send = (message: WebSocketMessage) => {
    if (ws.value && isConnected.value) {
      ws.value.send(JSON.stringify(message))
    } else {
      console.warn('Cannot send message: WebSocket not connected')
    }
  }
  
  /**
   * Send ping to keep connection alive
   */
  let pingInterval: ReturnType<typeof setInterval> | null = null
  
  const startPingInterval = () => {
    pingInterval = setInterval(() => {
      send({ type: 'ping' })
    }, 30000) // Ping every 30 seconds
  }
  
  const stopPingInterval = () => {
    if (pingInterval) {
      clearInterval(pingInterval)
      pingInterval = null
    }
  }
  
  /**
   * Update agent presence status
   */
  const updatePresence = (status: 'online' | 'away' | 'offline') => {
    send({
      type: 'presence_update',
      status
    })
  }
  
  // Auto-connect on mount
  onMounted(() => {
    connect()
  })
  
  // Cleanup on unmount
  onUnmounted(() => {
    disconnect()
  })
  
  return {
    isConnected: computed(() => isConnected.value),
    connectionId: computed(() => connectionId.value),
    reconnectAttempts: computed(() => reconnectAttempts.value),
    on,
    send,
    updatePresence,
    connect,
    disconnect
  }
}
