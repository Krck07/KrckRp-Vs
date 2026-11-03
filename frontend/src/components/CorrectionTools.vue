<template>
  <div class="correction-tools">
    <h2>Correction Tools</h2>

    <!-- Assistant Correction Interface -->
    <div class="correction-section">
      <h3>Assistant-Driven Correction</h3>

      <div class="assistant-interface">
        <div class="chat-history" ref="chatContainer">
          <div
            v-for="(message, index) in assistantMessages"
            :key="index"
            class="message"
            :class="{ 'user-message': message.role === 'user', 'assistant-message': message.role === 'assistant' }"
          >
            <div class="message-content">
              {{ message.content }}
            </div>
            <div class="message-timestamp">{{ formatTime(message.timestamp) }}</div>
          </div>
        </div>

        <div class="input-area">
          <textarea
            v-model="assistantInput"
            @keyup.enter.exact="submitAssistantCorrection"
            placeholder="Describe the correction you want to make (e.g. 'My sword should be in my inventory')..."
            :disabled="isSubmitting"
            class="correction-input"
          ></textarea>

          <button
            @click="submitAssistantCorrection"
            :disabled="!assistantInput.trim() || isSubmitting"
            class="submit-btn"
          >
            {{ isSubmitting ? 'Processing...' : 'Submit Correction' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Manual Data Editor -->
    <div class="correction-section">
      <h3>Manual Data Editor</h3>

      <div class="manual-editor">
        <div class="editor-form">
          <div class="form-group">
            <label for="editEntityType">Entity Type:</label>
            <select id="editEntityType" v-model="editForm.entityType">
              <option value="character">Character</option>
              <option value="location">Location</option>
              <option value="item">Item</option>
              <option value="quest">Quest</option>
              <option value="relationship">Relationship</option>
            </select>
          </div>

          <div class="form-group">
            <label for="editEntityId">Entity ID:</label>
            <input
              id="editEntityId"
              v-model="editForm.entityId"
              type="text"
              placeholder="Enter entity ID"
            />
          </div>

          <div class="form-group">
            <label for="editField">Field to Edit:</label>
            <input
              id="editField"
              v-model="editForm.field"
              type="text"
              placeholder="Enter field name (e.g. 'health', 'inventory')"
            />
          </div>

          <div class="form-group">
            <label for="editValue">New Value:</label>
            <textarea
              id="editValue"
              v-model="editForm.value"
              placeholder="Enter new value..."
              rows="3"
            ></textarea>
          </div>

          <button
            @click="submitManualCorrection"
            :disabled="isSubmitting"
            class="submit-btn manual-submit-btn"
          >
            {{ isSubmitting ? 'Applying...' : 'Apply Manual Correction' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'CorrectionTools',
  setup() {
    const assistantMessages = ref([
      {
        role: 'assistant',
        content: 'Hello! I can help you correct any issues in your game world. Please describe what needs to be fixed.',
        timestamp: new Date()
      }
    ])

    const assistantInput = ref('')
    const editForm = ref({
      entityType: 'character',
      entityId: '',
      field: '',
      value: ''
    })
    const isSubmitting = ref(false)

    const formatTime = (timestamp) => {
      if (!timestamp) return ''
      const date = new Date(timestamp)
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }

    const submitAssistantCorrection = async () => {
      if (!assistantInput.value.trim() || isSubmitting.value) return

      // Add user message
      assistantMessages.value.push({
        role: 'user',
        content: assistantInput.value,
        timestamp: new Date()
      })

      try {
        isSubmitting.value = true

        // In a real implementation, this would call the backend API
        // await apiService.correctGameState({ type: 'assistant', description: assistantInput.value })

        // Add AI response (mock)
        assistantMessages.value.push({
          role: 'assistant',
          content: "I've processed your correction request. The change has been logged as an event in the history.",
          timestamp: new Date()
        })

        assistantInput.value = ''

      } catch (error) {
        console.error('Error submitting assistant correction:', error)
        assistantMessages.value.push({
          role: 'assistant',
          content: "Sorry, I couldn't process your request. Please try again or use the manual editor.",
          timestamp: new Date()
        })
      } finally {
        isSubmitting.value = false
      }
    }

    const submitManualCorrection = async () => {
      if (isSubmitting.value) return

      try {
        isSubmitting.value = true

        // In a real implementation, this would call the backend API
        // await apiService.correctGameState({
        //   type: 'manual',
        //   data: editForm.value
        // })

        // Mock response
        alert(`Manual correction applied:\n${JSON.stringify(editForm.value, null, 2)}`)
        editForm.value = {
          entityType: 'character',
          entityId: '',
          field: '',
          value: ''
        }

      } catch (error) {
        console.error('Error submitting manual correction:', error)
        alert('Failed to apply manual correction. Please check your inputs.')
      } finally {
        isSubmitting.value = false
      }
    }

    return {
      assistantMessages,
      assistantInput,
      editForm,
      isSubmitting,
      formatTime,
      submitAssistantCorrection,
      submitManualCorrection
    }
  }
}
</script>

<style scoped>
.correction-tools {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.correction-section {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.correction-section h3 {
  margin-top: 0;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.chat-history {
  height: 200px;
  overflow-y: auto;
  background-color: white;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
}

.message {
  margin-bottom: 10px;
  padding: 8px 12px;
  border-radius: 16px;
  max-width: 80%;
}

.user-message {
  background-color: #e3f2fd;
  align-self: flex-end;
  margin-left: auto;
  border-bottom-right-radius: 4px;
}

.assistant-message {
  background-color: #f5f5f5;
  align-self: flex-start;
  margin-right: auto;
  border-bottom-left-radius: 4px;
}

.message-content {
  line-height: 1.4;
}

.message-timestamp {
  font-size: 0.7em;
  color: #666;
  text-align: right;
  margin-top: 5px;
}

.input-area {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.correction-input {
  flex-grow: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  resize: none;
  height: 80px;
}

.submit-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.submit-btn:hover:not(:disabled) {
  background-color: #45a049;
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.manual-editor .editor-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.manual-submit-btn {
  grid-column: span 2;
  width: 100%;
  padding: 15px;
}
</style>