<template>
  <div class="library-screen">
    <h1>World Library</h1>

    <div class="actions-bar">
      <button @click="createNewWorld" class="primary-btn">Create New World</button>
    </div>

    <div class="world-list">
      <div
        v-for="world in worlds"
        :key="world.id"
        class="world-card"
        @click="selectWorld(world)"
      >
        <h2>{{ world.name }}</h2>
        <p class="world-description">{{ world.description }}</p>
        <div class="world-meta">
          <span class="meta-item">Created: {{ formatDate(world.createdAt) }}</span>
          <span class="meta-item">Campaigns: {{ world.campaignCount }}</span>
        </div>
      </div>

      <!-- Placeholder when no worlds exist -->
      <div v-if="worlds.length === 0" class="empty-state">
        <p>No worlds created yet.</p>
        <button @click="createNewWorld" class="primary-btn">Create Your First World</button>
      </div>
    </div>

    <!-- Campaign List (if a world is selected) -->
    <div v-if="selectedWorld" class="campaign-section">
      <h2>Campaigns for {{ selectedWorld.name }}</h2>
      <div class="campaign-list">
        <div
          v-for="campaign in campaigns"
          :key="campaign.id"
          class="campaign-card"
        >
          <h3>{{ campaign.name }}</h3>
          <p>Started: {{ formatDate(campaign.startDate) }}</p>
          <button @click="loadCampaign(campaign)" class="secondary-btn">Load Campaign</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'LibraryScreen',
  setup() {
    const worlds = ref([])
    const campaigns = ref([])
    const selectedWorld = ref(null)

    // Mock data for demonstration
    const mockWorlds = [
      {
        id: 1,
        name: "Fantasy Realm",
        description: "A medieval fantasy world with magic and mythical creatures",
        createdAt: new Date('2023-01-15'),
        campaignCount: 2
      },
      {
        id: 2,
        name: "Cyberpunk City",
        description: "A dystopian future set in a neon-soaked metropolis",
        createdAt: new Date('2023-02-20'),
        campaignCount: 1
      }
    ]

    const mockCampaigns = [
      {
        id: 1,
        name: "The Lost Crown",
        worldId: 1,
        startDate: new Date('2023-01-20')
      },
      {
        id: 2,
        name: "Shadow Protocol",
        worldId: 1,
        startDate: new Date('2023-03-10')
      }
    ]

    const formatDate = (date) => {
      return date ? date.toLocaleDateString() : 'Unknown'
    }

    const loadWorlds = () => {
      // In a real implementation, this would fetch from the backend
      worlds.value = mockWorlds
    }

    const selectWorld = (world) => {
      selectedWorld.value = world
      campaigns.value = mockCampaigns.filter(campaign => campaign.worldId === world.id)
    }

    const createNewWorld = () => {
      // Placeholder for world creation functionality
      alert('World creation functionality would be implemented here')
    }

    const loadCampaign = (campaign) => {
      // Placeholder for loading a campaign
      alert(`Loading campaign: ${campaign.name}`)
    }

    onMounted(() => {
      loadWorlds()
    })

    return {
      worlds,
      campaigns,
      selectedWorld,
      formatDate,
      selectWorld,
      createNewWorld,
      loadCampaign
    }
  }
}
</script>

<style scoped>
.library-screen {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.actions-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.world-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.world-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: box-shadow 0.3s ease;
  background-color: white;
}

.world-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.world-card h2 {
  margin-top: 0;
  color: #333;
}

.world-description {
  color: #666;
  line-height: 1.5;
}

.world-meta {
  margin-top: 15px;
  display: flex;
  justify-content: space-between;
  font-size: 0.9em;
  color: #888;
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.primary-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.primary-btn:hover {
  background-color: #45a049;
}

.campaign-section {
  margin-top: 40px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.campaign-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
  margin-top: 20px;
}

.campaign-card {
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
}

.secondary-btn {
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.secondary-btn:hover {
  background-color: #1976D2;
}
</style>