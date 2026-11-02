<template>
  <div class="world-creation-screen">
    <h1>Create New World</h1>

    <div class="form-container">
      <div class="form-section">
        <h2>Basic Information</h2>

        <div class="form-group">
          <label for="worldName">World Name *</label>
          <input
            id="worldName"
            v-model="worldForm.name"
            type="text"
            placeholder="Enter a name for your world"
            required
          />
        </div>

        <div class="form-group">
          <label for="worldDescription">Description</label>
          <textarea
            id="worldDescription"
            v-model="worldForm.description"
            placeholder="Describe your world's setting, tone and themes..."
            rows="4"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="genre">Genre/Tone *</label>
          <select id="genre" v-model="worldForm.genre" required>
            <option value="">Select a genre</option>
            <option value="fantasy">Fantasy</option>
            <option value="sci-fi">Science Fiction</option>
            <option value="horror">Horror</option>
            <option value="mystery">Mystery/Thriller</option>
            <option value="historical">Historical</option>
            <option value="slice-of-life">Slice of Life</option>
          </select>
        </div>

        <div class="form-group">
          <label for="narrationStyle">Narration Style</label>
          <select id="narrationStyle" v-model="worldForm.narrationStyle">
            <option value="cinematic">Cinematic</option>
            <option value="epic">Epic</option>
            <option value="intimate">Intimate</option>
            <option value="mysterious">Mysterious</option>
          </select>
        </div>
      </div>

      <div class="form-section">
        <h2>World Settings</h2>

        <div class="form-group">
          <label for="combatStyle">Combat Style</label>
          <select id="combatStyle" v-model="worldForm.combatStyle">
            <option value="lethal">Lethal (characters can die)</option>
            <option value="forgiving">Forgiving (no permanent death)</option>
            <option value="abstract">Abstract (detailed combat mechanics optional)</option>
          </select>
        </div>

        <div class="form-group">
          <label for="progressionStyle">Progression Style</label>
          <select id="progressionStyle" v-model="worldForm.progressionStyle">
            <option value="levels">Level-based</option>
            <option value="milestones">Milestone-based</option>
            <option value="narrative">Narrative growth</option>
          </select>
        </div>

        <div class="form-group">
          <label>Content Settings</label>
          <div class="checkbox-group">
            <label>
              <input type="checkbox" v-model="worldForm.contentSettings.graphicViolence">
              Allow graphic violence
            </label>
            <label>
              <input type="checkbox" v-model="worldForm.contentSettings.explicitContent">
              Allow explicit content
            </label>
          </div>
        </div>
      </div>

      <div class="form-actions">
        <button @click="saveWorld" :disabled="!isFormValid" class="primary-btn">Save World</button>
        <button @click="cancelCreation" class="secondary-btn">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'WorldCreationScreen',
  setup(props, { emit }) {
    const worldForm = ref({
      name: '',
      description: '',
      genre: '',
      narrationStyle: 'cinematic',
      combatStyle: 'lethal',
      progressionStyle: 'levels',
      contentSettings: {
        graphicViolence: false,
        explicitContent: false
      }
    })

    const isFormValid = computed(() => {
      return worldForm.value.name && worldForm.value.genre
    })

    const saveWorld = () => {
      // In a real implementation, this would submit to the backend
      console.log('Saving world:', worldForm.value)
      alert(`World "${worldForm.value.name}" created successfully!`)

      // Reset form and emit event back to parent component
      worldForm.value = {
        name: '',
        description: '',
        genre: '',
        narrationStyle: 'cinematic',
        combatStyle: 'lethal',
        progressionStyle: 'levels',
        contentSettings: {
          graphicViolence: false,
          explicitContent: false
        }
      }
      emit('world-created')
    }

    const cancelCreation = () => {
      emit('cancel')
    }

    return {
      worldForm,
      isFormValid,
      saveWorld,
      cancelCreation
    }
  }
}
</script>

<style scoped>
.world-creation-screen {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.form-container {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.form-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.form-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.form-section h2 {
  margin-top: 0;
  color: #333;
  font-size: 1.4em;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #555;
}

input[type="text"],
textarea,
select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
}

textarea {
  resize: vertical;
  min-height: 80px;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.checkbox-group label {
  font-weight: normal;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 30px;
}

.primary-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
}

.primary-btn:hover:not(:disabled) {
  background-color: #45a049;
}

.primary-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.secondary-btn {
  background-color: #f1f1f1;
  color: #333;
  border: 1px solid #ddd;
  padding: 12px 30px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.secondary-btn:hover {
  background-color: #e0e0e0;
}
</style>