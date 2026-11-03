<template>
  <div class="settings-screen">
    <h1>Settings</h1>

    <!-- Model Configuration -->
    <div class="settings-section">
      <h2>Model Configuration</h2>

      <div class="form-group">
        <label for="narratorEndpoint">Narrator Model Endpoint:</label>
        <input
          id="narratorEndpoint"
          v-model="settings.narratorEndpoint"
          type="text"
          placeholder="http://localhost:5001"
        />
      </div>

      <div class="form-group">
        <label for="extractorEndpoint">Extractor Model Endpoint:</label>
        <input
          id="extractorEndpoint"
          v-model="settings.extractorEndpoint"
          type="text"
          placeholder="http://localhost:5002"
        />
      </div>

      <div class="form-group">
        <label for="assistantEndpoint">Assistant Model Endpoint:</label>
        <input
          id="assistantEndpoint"
          v-model="settings.assistantEndpoint"
          type="text"
          placeholder="http://localhost:5003"
        />
      </div>
    </div>

    <!-- Context and Token Settings -->
    <div class="settings-section">
      <h2>Context & Token Settings</h2>

      <div class="form-group">
        <label for="maxTokens">Max Tokens (Narrator):</label>
        <input
          id="maxTokens"
          v-model.number="settings.maxTokens"
          type="number"
          min="100"
          max="8000"
        />
      </div>

      <div class="form-group">
        <label for="contextWindow">Context Window Size:</label>
        <input
          id="contextWindow"
          v-model.number="settings.contextWindow"
          type="number"
          min="100"
          max="32000"
        />
      </div>

      <div class="form-group">
        <label for="temperature">Temperature:</label>
        <input
          id="temperature"
          v-model.number="settings.temperature"
          type="range"
          min="0"
          max="1"
          step="0.01"
        />
        <span>{{ settings.temperature }}</span>
      </div>
    </div>

    <!-- Content and Tone Settings -->
    <div class="settings-section">
      <h2>Content & Tone Settings</h2>

      <div class="form-group">
        <label for="narrationStyle">Narration Style:</label>
        <select id="narrationStyle" v-model="settings.narrationStyle">
          <option value="cinematic">Cinematic</option>
          <option value="epic">Epic</option>
          <option value="intimate">Intimate</option>
          <option value="mysterious">Mysterious</option>
        </select>
      </div>

      <div class="form-group">
        <label for="contentSettings">Content Settings:</label>
        <div class="checkbox-group">
          <label>
            <input type="checkbox" v-model="settings.contentSettings.graphicViolence">
            Allow graphic violence
          </label>
          <label>
            <input type="checkbox" v-model="settings.contentSettings.explicitContent">
            Allow explicit content
          </label>
          <label>
            <input type="checkbox" v-model="settings.contentSettings.sensitiveTopics">
            Allow sensitive topics
          </label>
        </div>
      </div>
    </div>

    <!-- Save Button -->
    <div class="save-section">
      <button @click="saveSettings" :disabled="isSaving" class="save-btn">
        {{ isSaving ? 'Saving...' : 'Save Settings' }}
      </button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'SettingsScreen',
  setup(props, { emit }) {
    // Default settings
    const settings = ref({
      narratorEndpoint: 'http://localhost:5001',
      extractorEndpoint: 'http://localhost:5002',
      assistantEndpoint: 'http://localhost:5003',
      maxTokens: 1000,
      contextWindow: 4096,
      temperature: 0.7,
      narrationStyle: 'cinematic',
      contentSettings: {
        graphicViolence: false,
        explicitContent: false,
        sensitiveTopics: false
      }
    })

    const isSaving = ref(false)

    const saveSettings = async () => {
      try {
        isSaving.value = true

        // In a real implementation, this would call the backend to save settings
        // await apiService.saveSettings(settings.value)

        console.log('Saving settings:', settings.value)
        alert('Settings saved successfully!')

      } catch (error) {
        console.error('Error saving settings:', error)
        alert('Failed to save settings. Please try again.')
      } finally {
        isSaving.value = false
      }
    }

    return {
      settings,
      isSaving,
      saveSettings
    }
  }
}
</script>

<style scoped>
.settings-screen {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.settings-section {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.settings-section h2 {
  margin-top: 0;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #555;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.checkbox-group label {
  font-weight: normal;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.save-section {
  text-align: center;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.save-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.save-btn:hover:not(:disabled) {
  background-color: #45a049;
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>