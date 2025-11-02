# Native Android Development Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Native Android Development Guide
**Focus:** Kotlin, Jetpack Compose, MVVM architecture

---

## 🤖 Jetpack Compose Fundamentals

### Basic Compose App

```kotlin
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController

@Composable
fun FeatureApp() {
    val navController = rememberNavController()
    
    NavHost(navController, startDestination = "features") {
        composable("features") {
            FeatureListScreen(
                onFeatureClick = { featureId ->
                    navController.navigate("feature/$featureId")
                }
            )
        }
        composable("feature/{featureId}") { backStackEntry ->
            val featureId = backStackEntry.arguments?.getString("featureId")!!
            FeatureDetailScreen(featureId = featureId)
        }
    }
}

// MVVM ViewModel
@HiltViewModel
class FeatureViewModel @Inject constructor(
    private val featureService: FeatureService
) : ViewModel() {
    
    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()
    
    private val _features = MutableStateFlow<List<Feature>>(emptyList())
    val features: StateFlow<List<Feature>> = _features.asStateFlow()
    
    init {
        loadFeatures()
    }
    
    fun loadFeatures() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            try {
                val features = featureService.getFeatures()
                _features.value = features
                _uiState.value = UiState.Success
            } catch (e: Exception) {
                _uiState.value = UiState.Error(e.message ?: "Unknown error")
            }
        }
    }
    
    fun createFeature(name: String, priority: Int) {
        viewModelScope.launch {
            try {
                val feature = featureService.createFeature(name, priority)
                _features.value += feature
            } catch (e: Exception) {
                _uiState.value = UiState.Error(e.message ?: "Failed to create")
            }
        }
    }
    
    fun deleteFeature(id: String) {
        viewModelScope.launch {
            try {
                featureService.deleteFeature(id)
                _features.value = _features.value.filter { it.id != id }
            } catch (e: Exception) {
                _uiState.value = UiState.Error(e.message ?: "Failed to delete")
            }
        }
    }
}

sealed class UiState {
    object Loading : UiState()
    object Success : UiState()
    data class Error(val message: String) : UiState()
}

// Feature List Screen
@Composable
fun FeatureListScreen(
    viewModel: FeatureViewModel = viewModel(),
    onFeatureClick: (String) -> Unit
) {
    val uiState by viewModel.uiState.collectAsState()
    val features by viewModel.features.collectAsState()
    
    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Features") })
        },
        floatingActionButton = {
            FloatingActionButton(onClick = { /* Show create dialog */ }) {
                Icon(Icons.Default.Add, contentDescription = "Add")
            }
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            when (uiState) {
                is UiState.Loading -> {
                    CircularProgressIndicator(
                        modifier = Modifier.align(Alignment.Center)
                    )
                }
                is UiState.Error -> {
                    Text(
                        text = (uiState as UiState.Error).message,
                        modifier = Modifier.align(Alignment.Center)
                    )
                }
                is UiState.Success -> {
                    if (features.isEmpty()) {
                        Text(
                            text = "No features",
                            modifier = Modifier.align(Alignment.Center)
                        )
                    } else {
                        LazyColumn {
                            items(features) { feature ->
                                FeatureItem(
                                    feature = feature,
                                    onClick = { onFeatureClick(feature.id) },
                                    onDelete = { viewModel.deleteFeature(feature.id) }
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun FeatureItem(
    feature: Feature,
    onClick: () -> Unit,
    onDelete: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
            .clickable(onClick = onClick)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(feature.name, style = MaterialTheme.typography.titleMedium)
            Text(
                "Priority: ${feature.priority}",
                style = MaterialTheme.typography.bodySmall
            )
            Button(
                onClick = onDelete,
                modifier = Modifier.align(Alignment.End)
            ) {
                Text("Delete")
            }
        }
    }
}
```

---

## 🔄 Coroutines & Flow

### Coroutine Patterns

```kotlin
// Service with suspend functions
interface FeatureService {
    suspend fun getFeatures(): List<Feature>
    suspend fun createFeature(name: String, priority: Int): Feature
    suspend fun deleteFeature(id: String)
}

// Implementation with Retrofit
class FeatureServiceImpl(
    private val apiService: FeatureApiService
) : FeatureService {
    
    override suspend fun getFeatures(): List<Feature> = withContext(Dispatchers.IO) {
        apiService.getFeatures()
    }
    
    override suspend fun createFeature(name: String, priority: Int): Feature {
        return withContext(Dispatchers.IO) {
            apiService.createFeature(CreateFeatureRequest(name, priority))
        }
    }
    
    override suspend fun deleteFeature(id: String) = withContext(Dispatchers.IO) {
        apiService.deleteFeature(id)
    }
}

// Repository pattern with Flow
class FeatureRepository(
    private val service: FeatureService,
    private val localDb: FeatureDatabase
) {
    
    fun getFeaturesFlow(): Flow<List<Feature>> = flow {
        try {
            // Try network first
            val features = service.getFeatures()
            
            // Save to local
            localDb.featureDao().insertAll(features)
            emit(features)
        } catch (e: Exception) {
            // Fall back to local
            emitAll(localDb.featureDao().getAllFlow())
        }
    }
    
    suspend fun createFeature(name: String, priority: Int) {
        val feature = service.createFeature(name, priority)
        localDb.featureDao().insert(feature)
    }
}

// ViewModel using Flow
@HiltViewModel
class FeatureViewModel @Inject constructor(
    private val repository: FeatureRepository
) : ViewModel() {
    
    val features: StateFlow<List<Feature>> = repository
        .getFeaturesFlow()
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )
    
    fun createFeature(name: String, priority: Int) {
        viewModelScope.launch {
            repository.createFeature(name, priority)
        }
    }
}
```

---

## 💾 Room Database

### Data Persistence

```kotlin
import androidx.room.*
import kotlinx.coroutines.flow.Flow

// Entity
@Entity(tableName = "features")
data class FeatureEntity(
    @PrimaryKey val id: String,
    val name: String,
    val priority: Int,
    val createdAt: Long
)

// DAO
@Dao
interface FeatureDao {
    
    @Query("SELECT * FROM features ORDER BY priority DESC")
    fun getAllFlow(): Flow<List<FeatureEntity>>
    
    @Query("SELECT * FROM features WHERE id = :id")
    suspend fun getFeatureById(id: String): FeatureEntity
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(feature: FeatureEntity)
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(features: List<FeatureEntity>)
    
    @Update
    suspend fun update(feature: FeatureEntity)
    
    @Delete
    suspend fun delete(feature: FeatureEntity)
    
    @Query("DELETE FROM features WHERE id = :id")
    suspend fun deleteById(id: String)
}

// Database
@Database(entities = [FeatureEntity::class], version = 1)
abstract class FeatureDatabase : RoomDatabase() {
    
    abstract fun featureDao(): FeatureDao
    
    companion object {
        private var instance: FeatureDatabase? = null
        
        fun getInstance(context: Context): FeatureDatabase {
            return instance ?: synchronized(this) {
                Room.databaseBuilder(
                    context.applicationContext,
                    FeatureDatabase::class.java,
                    "feature_database"
                )
                    .build()
                    .also { instance = it }
            }
        }
    }
}
```

---

## 🔐 Security

### Encrypted SharedPreferences

```kotlin
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

class SecurePreferences(context: Context) {
    
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()
    
    private val encryptedSharedPreferences = EncryptedSharedPreferences.create(
        context,
        "secure_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )
    
    fun saveToken(token: String) {
        encryptedSharedPreferences.edit()
            .putString("auth_token", token)
            .apply()
    }
    
    fun getToken(): String? {
        return encryptedSharedPreferences.getString("auth_token", null)
    }
    
    fun clearToken() {
        encryptedSharedPreferences.edit()
            .remove("auth_token")
            .apply()
    }
}

// Biometric authentication
class BiometricAuth(context: Context) {
    
    private val biometricPrompt = BiometricPrompt(
        context as FragmentActivity,
        executor,
        object : BiometricPrompt.AuthenticationCallback() {
            override fun onAuthenticationSucceeded(
                result: BiometricPrompt.AuthenticationResult
            ) {
                super.onAuthenticationSucceeded(result)
                // Authentication succeeded
            }
            
            override fun onAuthenticationError(
                errorCode: Int,
                errString: CharSequence
            ) {
                super.onAuthenticationError(errorCode, errString)
                // Handle error
            }
        }
    )
    
    fun authenticate() {
        val promptInfo = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Authenticate")
            .setNegativeButtonText("Cancel")
            .build()
        
        biometricPrompt.authenticate(promptInfo)
    }
}
```

---

## 🎬 Animations

### Compose Animations

```kotlin
@Composable
fun AnimatedFeatureItem(feature: Feature) {
    var expanded by remember { mutableStateOf(false) }
    
    val animatedHeight by animateDpAsState(
        targetValue = if (expanded) 200.dp else 100.dp,
        animationSpec = spring(dampingRatio = 0.7f)
    )
    
    Box(
        modifier = Modifier
            .height(animatedHeight)
            .clickable { expanded = !expanded }
            .background(Color.Blue)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(feature.name)
            if (expanded) {
                Spacer(modifier = Modifier.height(8.dp))
                Text("Priority: ${feature.priority}")
            }
        }
    }
}

// Cross-fade animation
@Composable
fun AnimatedVisibility(feature: Feature) {
    var visible by remember { mutableStateOf(true) }
    
    Column {
        AnimatedVisibility(
            visible = visible,
            enter = fadeIn() + expandVertically(),
            exit = fadeOut() + shrinkVertically()
        ) {
            Text(feature.name)
        }
        
        Button(onClick = { visible = !visible }) {
            Text("Toggle")
        }
    }
}
```

---

## 📚 Related Documents

- Native iOS (native_ios.md)
- Mobile Development (mobile_development.md)
- Cross-Platform Strategies (cross_platform.md)
- App Distribution (app_distribution.md)

---

**END OF NATIVE ANDROID DEVELOPMENT DOCUMENT**
