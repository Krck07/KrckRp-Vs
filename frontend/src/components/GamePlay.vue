<template>
  <div class="game-play-screen">
    <h1>{{ campaign.name }} - Playing as {{ character.name }}</h1>

    <div class="game-container">
      <!-- Sidebar -->
      <div class="sidebar-container">
        <Sidebar
          :campaign-id="campaign.id"
          :character="character"
          :location="currentLocation"
          :nearby-characters="nearbyCharacters"
          :active-quests="activeQuests"
        />
      </div>

      <!-- Chat Pane -->
      <div class="chat-container">
        <ChatPane :campaign-id="campaign.id" />
      </div>
    </div>

    <div class="game-controls">
      <button @click="$emit('back-to-library')" class="control-btn back-btn">
        Back to Library
      </button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import Sidebar from './Sidebar.vue'
import ChatPane from './ChatPane.vue'

export default {
  name: 'GamePlayScreen',
  components: {
    Sidebar,
    ChatPane
  },
  props: {
    campaign: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    // Mock data for demonstration - in a real app this would come from API calls
    const character = ref({
      name: "Hero",
      description: "A brave adventurer on a quest",
      stats: {
        strength: 12,
        dexterity: 10,
        intelligence: 8,
        health: 30,
        mana: 15
      },
      inventory: [
        { name: "Iron Sword", description: "A reliable blade" },
        { name: "Health Potion", description: "Restores health" }
      ]
    })

    const currentLocation = ref({
      name: "Forest Clearing",
      description: "A peaceful clearing surrounded by tall trees with a small stream running through it."
    })

    const nearbyCharacters = ref([
      { name: "Old Man", role: "Town Guide" },
      { name: "Wolf", role: "Wild Animal" }
    ])

    const activeQuests = ref([
      {
        title: "Find the Lost Artifact",
        summary: "Retrieve the ancient artifact from the ruins.",
        state: "active"
      },
      {
        title: "Help the Village",
        summary: "Assist the villagers with their problems.",
        state: "completed"
      }
    ])

    return {
      character,
      currentLocation,
      nearbyCharacters,
      activeQuests
    }
  }
}
</script>

<style scoped>
.game-play-screen {
  max-width: 1400px;
  margin: 0 auto;
}

.game-play-screen h1 {
  margin-bottom: 20px;
  color: #333;
}

.game-container {
  display: flex;
  gap: 20px;
  height: calc(100vh - 180px);
}

.sidebar-container {
  flex: 0 0 300px;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.game-controls {
  margin-top: 20px;
  text-align: center;
}

.control-btn {
  padding: 10px 20px;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.control-btn:hover {
  background-color: #555;
}
</style>