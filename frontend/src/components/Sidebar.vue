<template>
  <div class="sidebar">
    <!-- Character Info -->
    <div class="sidebar-section">
      <h3>Character</h3>
      <div class="character-info">
        <div class="avatar-placeholder">[Avatar]</div>
        <div class="character-details">
          <h4>{{ character.name }}</h4>
          <p>{{ character.description }}</p>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="sidebar-section">
      <h3>Stats</h3>
      <div class="stats-grid">
        <div v-for="(stat, key) in character.stats" :key="key" class="stat-item">
          <span class="stat-name">{{ key }}:</span>
          <span class="stat-value">{{ stat }}</span>
        </div>
      </div>
    </div>

    <!-- Inventory -->
    <div class="sidebar-section">
      <h3>Inventory</h3>
      <div class="inventory-list">
        <div v-for="(item, index) in character.inventory" :key="index" class="inventory-item">
          {{ item.name }} - {{ item.description }}
        </div>
        <div v-if="character.inventory.length === 0" class="empty-state">
          No items
        </div>
      </div>
    </div>

    <!-- Location -->
    <div class="sidebar-section">
      <h3>Location</h3>
      <div class="location-info">
        <h4>{{ location.name }}</h4>
        <p v-html="formatDescription(location.description)"></p>
        <div class="nearby-entities">
          <h5>Nearby Characters:</h5>
          <div v-for="(npc, index) in nearbyCharacters" :key="index" class="npc-item">
            {{ npc.name }}
          </div>
          <div v-if="nearbyCharacters.length === 0" class="empty-state">None</div>
        </div>
      </div>
    </div>

    <!-- Active Quests -->
    <div class="sidebar-section">
      <h3>Active Quests</h3>
      <div class="quests-list">
        <div v-for="(quest, index) in activeQuests" :key="index" class="quest-item">
          <h4>{{ quest.title }}</h4>
          <p>{{ quest.summary }}</p>
          <span class="quest-status">{{ quest.state }}</span>
        </div>
        <div v-if="activeQuests.length === 0" class="empty-state">
          No active quests
        </div>
      </div>
    </div>

    <!-- Time -->
    <div class="sidebar-section time-info">
      <h3>Time</h3>
      <p>{{ currentTime }}</p>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'Sidebar',
  props: {
    campaignId: {
      type: Number,
      required: true
    },
    character: {
      type: Object,
      required: true
    },
    location: {
      type: Object,
      required: true
    },
    nearbyCharacters: {
      type: Array,
      default: () => []
    },
    activeQuests: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    const currentTime = computed(() => {
      // In a real implementation, this would come from the backend
      return new Date().toLocaleString()
    })

    const formatDescription = (description) => {
      if (!description) return ''
      return description.replace(/\n/g, '<br>')
    }

    return {
      currentTime,
      formatDescription
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 300px;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  height: calc(100vh - 180px);
  overflow-y: auto;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.sidebar-section {
  margin-bottom: 25px;
}

.sidebar-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
}

.character-info {
  display: flex;
  gap: 15px;
  align-items: flex-start;
}

.avatar-placeholder {
  width: 60px;
  height: 60px;
  background-color: #ddd;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #888;
}

.character-details h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.character-details p {
  margin: 0;
  color: #666;
  line-height: 1.4;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.stat-item {
  background-color: white;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.stat-name {
  display: block;
  font-size: 0.9em;
  color: #666;
  margin-bottom: 4px;
}

.stat-value {
  display: block;
  font-weight: bold;
  color: #333;
  font-size: 1.1em;
}

.inventory-list,
.quests-list {
  max-height: 200px;
  overflow-y: auto;
}

.inventory-item,
.quest-item {
  padding: 10px;
  margin-bottom: 8px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  font-size: 0.9em;
}

.quest-item h4 {
  margin-top: 0;
  margin-bottom: 5px;
  color: #333;
}

.quest-item p {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 0.9em;
  line-height: 1.4;
}

.quest-status {
  display: inline-block;
  padding: 2px 8px;
  background-color: #e3f2fd;
  color: #1976d2;
  border-radius: 12px;
  font-size: 0.8em;
}

.location-info h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
}

.nearby-entities h5 {
  margin-top: 0;
  margin-bottom: 8px;
  color: #666;
}

.npc-item {
  padding: 4px 0;
  border-bottom: 1px solid #f0f0f0;
}

.npc-item:last-child {
  border-bottom: none;
}

.empty-state {
  color: #999;
  font-style: italic;
  text-align: center;
  padding: 15px 0;
}

.time-info p {
  background-color: white;
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
</style>