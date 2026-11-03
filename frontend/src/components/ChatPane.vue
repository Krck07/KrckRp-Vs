<template>
  <div class="chat-pane">
    <!-- Chat History -->
    <div class="chat-history" ref="chatContainer">
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="message"
        :class="{ 'player-message': message.type === 'player', 'narrator-message': message.type === 'narrator' }"
      >
        <div class="message-content">
          <div v-html="formatMessage(message.content)"></div>
        </div>
        <div class="message-timestamp">{{ formatTime(message.timestamp) }}</div>
      </div>

      <!-- Loading indicator -->
      <div v-if="isLoading" class="loading-indicator">
        <span class="typing-indicator">AI is typing...</span>
      </div>
    </div>

    <!-- Input Area -->
    <div class="input-area">
      <textarea
        v-model="playerInput"
        @keyup.enter.exact="submitPlayerAction"
        placeholder="Enter your action (e.g. 'I walk to the forest')..."
        :disabled="isLoading"
        class="action-input"
      ></textarea>

      <div class="turn-controls">
        <button
          @click="regenerateLastResponse"
          :disabled="!lastNarratorMessage || isLoading"
          class="control-btn regenerate-btn"
        >
          Regenerate
        </button>
        <button
          @click="undoLastTurn"
          :disabled="!canUndo || isLoading"
          class="control-btn undo-btn"
        >
          Undo Last Turn
        </button>
        <button
          @click="submitPlayerAction"
          :disabled="!playerInput.trim() || isLoading"
          class="control-btn submit-btn"
        >
          Submit Action
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, nextTick } from 'vue'
import apiService from '../api.js'

export default {
  name: 'ChatPane',
  props: {
    campaignId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const messages = ref([])
    const playerInput = ref('')
    const isLoading = ref(false)
    const canUndo = ref(false)
    const lastNarratorMessage = ref(null)

    // Scroll to bottom when new messages arrive
    watch(messages, () => {
      nextTick(() => {
        scrollToBottom()
      })
    })

    const formatMessage = (content) => {
      // Simple formatting - in a real app this might be more sophisticated
      return content.replace(/\n/g, '<br>')
    }

    const formatTime = (timestamp) => {
      if (!timestamp) return ''
      const date = new Date(timestamp)
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }

    const scrollToBottom = () => {
      const container = document.querySelector('.chat-history')
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    }

    const loadGameHistory = async () => {
      try {
        isLoading.value = true
        const history = await apiService.getGameHistory(props.campaignId)

        messages.value = history.map(turn => ({
          type: 'player',
          content: turn.player_input,
          timestamp: turn.timestamp
        })).concat(history.map(turn => ({
          type: 'narrator',
          content: turn.narration,
          timestamp: turn.timestamp
        })))

        // Find last narrator message for regeneration
        const narratorMessages = messages.value.filter(msg => msg.type === 'narrator')
        if (narratorMessages.length > 0) {
          lastNarratorMessage.value = narratorMessages[narratorMessages.length - 1]
        }

      } catch (error) {
        console.error('Failed to load game history:', error)
        messages.value = [
          { type: 'narrator', content: 'Error loading game history. Please try again.', timestamp: new Date() }
        ]
      } finally {
        isLoading.value = false
      }
    }

    const submitPlayerAction = async () => {
      if (!playerInput.value.trim() || isLoading.value) return

      // Add player message to chat immediately
      const playerMessage = {
        type: 'player',
        content: playerInput.value,
        timestamp: new Date()
      }

      messages.value.push(playerMessage)
      playerInput.value = ''

      try {
        isLoading.value = true

        // Send action to backend
        await apiService.getPlayerTurn({
          campaign_id: props.campaignId,
          input_text: playerMessage.content
        })

        // Reload chat history after successful submission
        await loadGameHistory()

      } catch (error) {
        console.error('Error submitting player action:', error)
        messages.value.push({
          type: 'narrator',
          content: `Error processing your request. Please try again.`,
          timestamp: new Date()
        })
      } finally {
        isLoading.value = false
      }
    }

    const regenerateLastResponse = async () => {
      if (!lastNarratorMessage.value || isLoading.value) return

      try {
        isLoading.value = true
        // In a real implementation, this would trigger regeneration of the last response
        await loadGameHistory()
      } catch (error) {
        console.error('Error regenerating response:', error)
      } finally {
        isLoading.value = false
      }
    }

    const undoLastTurn = async () => {
      if (!canUndo.value || isLoading.value) return

      try {
        isLoading.value = true
        // In a real implementation, this would call the backend to undo last turn
        await apiService.undoTurn(props.campaignId, null)

        // Reload chat history after undo
        await loadGameHistory()
      } catch (error) {
        console.error('Error undoing last turn:', error)
      } finally {
        isLoading.value = false
      }
    }

    onMounted(() => {
      scrollToBottom()
      loadGameHistory()
    })

    return {
      messages,
      playerInput,
      isLoading,
      canUndo,
      lastNarratorMessage,
      formatMessage,
      formatTime,
      submitPlayerAction,
      regenerateLastResponse,
      undoLastTurn
    }
  }
}
</script>

<style scoped>
.chat-pane {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 180px);
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  background-color: white;
}

.chat-history {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.message {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 18px;
  line-height: 1.4;
  position: relative;
}

.player-message {
  align-self: flex-end;
  background-color: #e3f2fd;
  border-bottom-right-radius: 4px;
}

.narrator-message {
  align-self: flex-start;
  background-color: #f5f5f5;
  border-bottom-left-radius: 4px;
}

.message-content {
  margin-bottom: 8px;
}

.message-timestamp {
  font-size: 0.7em;
  color: #666;
  text-align: right;
}

.input-area {
  padding: 15px;
  border-top: 1px solid #eee;
  background-color: #fafafa;
}

.action-input {
  width: 100%;
  height: 80px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  resize: none;
  margin-bottom: 10px;
}

.turn-controls {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.control-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.regenerate-btn {
  background-color: #2196F3;
  color: white;
}

.regenerate-btn:hover:not(:disabled) {
  background-color: #1976D2;
}

.regenerate-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.undo-btn {
  background-color: #ff9800;
  color: white;
}

.undo-btn:hover:not(:disabled) {
  background-color: #f57c00;
}

.undo-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-btn {
  background-color: #4CAF50;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background-color: #45a049;
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-indicator {
  text-align: center;
  padding: 10px;
  color: #666;
}

.typing-indicator::after {
  content: '.';
  animation: dots 1.5s infinite;
}

@keyframes dots {
  0%, 20% { content: '.'; }
  40% { content: '..'; }
  60%, 100% { content: '...'; }
}
</style>