import { MOCK_STUDENTS, MOCK_TEACHERS } from './useMocks'

// Initialisation du store global dans le localStorage
const initDb = () => {
  if (process.client) {
    if (!localStorage.getItem('db_etudiants')) {
      localStorage.setItem('db_etudiants', JSON.stringify(MOCK_STUDENTS))
    }
    if (!localStorage.getItem('db_enseignants')) {
      localStorage.setItem('db_enseignants', JSON.stringify(MOCK_TEACHERS))
    }
    if (!localStorage.getItem('db_matieres')) {
      localStorage.setItem('db_matieres', JSON.stringify([
        { id: 'M1', libelle: 'Architecture Réseaux', coefficient: 3, credits: 4, ue_id: 'UE1' },
        { id: 'M2', libelle: 'Protocoles IP', coefficient: 2, credits: 3, ue_id: 'UE1' },
        { id: 'M3', libelle: 'Vue.js', coefficient: 3, credits: 4, ue_id: 'UE2' }
      ]))
    }
    if (!localStorage.getItem('db_ues')) {
      localStorage.setItem('db_ues', JSON.stringify([
        { id: 'UE1', code: 'UE5-1', libelle: 'Réseaux', semestre: 5 },
        { id: 'UE2', code: 'UE5-2', libelle: 'Développement', semestre: 5 }
      ]))
    }
    if (!localStorage.getItem('db_notes')) {
      localStorage.setItem('db_notes', JSON.stringify([]))
    }
  }
}

export const useMockDb = () => {
  initDb()

  const getCollection = (collectionName) => {
    if (process.client) {
      const data = localStorage.getItem(`db_${collectionName}`)
      return data ? JSON.parse(data) : []
    }
    return []
  }

  const setCollection = (collectionName, data) => {
    if (process.client) {
      localStorage.setItem(`db_${collectionName}`, JSON.stringify(data))
    }
  }

  const addDoc = (collectionName, doc) => {
    const data = getCollection(collectionName)
    const newDoc = { ...doc, id: Math.random().toString(36).substring(2, 9) }
    data.push(newDoc)
    setCollection(collectionName, data)
    return newDoc
  }

  const updateDoc = (collectionName, id, updates) => {
    const data = getCollection(collectionName)
    const index = data.findIndex(item => item.id === id)
    if (index !== -1) {
      data[index] = { ...data[index], ...updates }
      setCollection(collectionName, data)
      return data[index]
    }
    return null
  }

  const deleteDoc = (collectionName, id) => {
    const data = getCollection(collectionName)
    const filtered = data.filter(item => item.id !== id)
    setCollection(collectionName, filtered)
  }
  
  // Fonction de login simulée
  const authenticate = (username, password, role) => {
    if (role === 'etudiant') {
      const etudiants = getCollection('etudiants')
      // Login = prenom (insensible à la casse), Password = matricule
      const user = etudiants.find(e => 
        e.prenom.toLowerCase() === username.toLowerCase() && 
        e.matricule === password
      )
      if (user) return { ...user, role: 'etudiant', name: `${user.nom} ${user.prenom}` }
    } else if (role === 'enseignant') {
      const enseignants = getCollection('enseignants')
      const user = enseignants.find(e => 
        e.prenom.toLowerCase() === username.toLowerCase() && 
        e.matricule === password
      )
      if (user) return { ...user, role: 'enseignant', name: `${user.nom} ${user.prenom}` }
    } else if (role === 'secretariat' || role === 'admin') {
      // Hardcodé pour admin/secretariat pour les tests
      if (username === 'admin' && password === 'admin') {
         return { id: 'A1', prenom: 'Admin', nom: 'System', email: 'admin@system.com', role: role, name: 'Admin System' }
      }
    }
    return null
  }

  return {
    getCollection,
    addDoc,
    updateDoc,
    deleteDoc,
    authenticate
  }
}
