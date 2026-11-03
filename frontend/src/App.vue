<template>
  <div id="app">
    <!-- Navigation -->
    <nav class="navbar">
      <h1>KrckRP - AI Narrative RPG</h1>
      <div class="nav-buttons">
        <button @click="currentView = 'library'" :class="{ active: currentView === 'library' }">Library</button>
        <button @click="currentView = 'create-world'" :class="{ active: currentView === 'create-world' }">Create World</button>
        <button @click="currentView = 'settings'" :class="{ active: currentView === 'settings' }">Settings</button>
      </div>
    </nav>

    <!-- View Content -->
    <main class="main-content">
      <LibraryScreen
        v-if="currentView === 'library'"
        @world-selected="handleWorldSelected"
        @campaign-loaded="handleCampaignLoaded"
      />

      <WorldCreationScreen
        v-else-if="currentView === 'create-world'"
        @world-created="handleWorldCreated"
        @cancel="currentView = 'library'"
      />

      <GamePlayScreen
        v-else-if="currentView === 'game-play' && selectedCampaign"
        :campaign="selectedCampaign"
        @back-to-library="currentView = 'library'"
      />

      <SettingsScreen
        v-else-if="currentView === 'settings'"
        @save-settings="handleSaveSettings"
      />
    </main>
  </div>
</template>

<script>
import { ref } from 'vue'
import LibraryScreen from './components/Library.vue'
import WorldCreationScreen from './components/WorldBuilder.vue'
import GamePlayScreen from './components/GamePlay.vue'
import SettingsScreen from './components/Settings.vue'

export default {
  name: 'App',
  components: {
    LibraryScreen,
    WorldCreationScreen,
    GamePlayScreen,
    SettingsScreen
  },
  setup() {
    const currentView = ref('library')
    const selectedCampaign = ref(null)

    const handleWorldSelected = (world) => {
      // Switch to library view after world selection
      currentView.value = 'library'
    }

    const handleCampaignLoaded = (campaign) => {
      selectedCampaign.value = campaign
      currentView.value = 'game-play'
    }

    const handleWorldCreated = () => {
      // Switch to library view after world creation
      currentView.value = 'library'
    }

    const handleSaveSettings = () => {
      // Handle settings save if needed
      alert('Settings saved successfully!')
    }

    return {
      currentView,
      selectedCampaign,
      handleWorldSelected,
      handleCampaignLoaded,
      handleWorldCreated,
      handleSaveSettings
    }
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.navbar {
  background-color: #333;
  color: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar h1 {
  margin: 0;
  font-size: 1.5em;
}

.nav-buttons {
  display: flex;
  gap: 10px;
}

.nav-buttons button {
  background-color: #555;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.nav-buttons button:hover,
.nav-buttons button.active {
  background-color: #777;
}

.main-content {
  padding: 20px;
}
</style>