# Native iOS Development Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Native iOS Development Guide
**Focus:** Swift, SwiftUI, and iOS patterns

---

## 🍎 SwiftUI Fundamentals

### Basic App Structure

```swift
import SwiftUI

@main
struct FeatureApp: App {
    @StateObject private var viewModel = FeatureViewModel()
    
    var body: some Scene {
        WindowGroup {
            NavigationStack {
                FeatureListView()
                    .environmentObject(viewModel)
            }
        }
    }
}

// View Model
@MainActor
class FeatureViewModel: ObservableObject {
    @Published var features: [Feature] = []
    @Published var isLoading = false
    @Published var error: Error?
    
    private let service: FeatureService
    
    init(service: FeatureService = .shared) {
        self.service = service
    }
    
    func loadFeatures() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            features = try await service.getFeatures()
        } catch {
            self.error = error
        }
    }
    
    func createFeature(_ name: String, priority: Int) async {
        do {
            let feature = try await service.createFeature(
                name: name,
                priority: priority
            )
            features.append(feature)
        } catch {
            self.error = error
        }
    }
}

// Feature List View
struct FeatureListView: View {
    @EnvironmentObject var viewModel: FeatureViewModel
    @State private var showingCreateSheet = false
    
    var body: some View {
        ZStack {
            if viewModel.isLoading {
                ProgressView()
            } else if viewModel.features.isEmpty {
                Text("No features")
                    .foregroundColor(.gray)
            } else {
                List {
                    ForEach(viewModel.features) { feature in
                        NavigationLink(destination: FeatureDetailView(feature: feature)) {
                            VStack(alignment: .leading) {
                                Text(feature.name)
                                    .font(.headline)
                                Text("Priority: \(feature.priority)")
                                    .font(.caption)
                                    .foregroundColor(.gray)
                            }
                        }
                    }
                }
            }
        }
        .navigationTitle("Features")
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button(action: { showingCreateSheet = true }) {
                    Image(systemName: "plus")
                }
            }
        }
        .sheet(isPresented: $showingCreateSheet) {
            CreateFeatureSheet(viewModel: viewModel)
        }
        .task {
            await viewModel.loadFeatures()
        }
    }
}

// Create Feature Sheet
struct CreateFeatureSheet: View {
    @Environment(\.dismiss) var dismiss
    @ObservedObject var viewModel: FeatureViewModel
    
    @State private var name = ""
    @State private var priority = 5
    
    var body: some View {
        NavigationStack {
            Form {
                TextField("Name", text: $name)
                Stepper("Priority: \(priority)", value: $priority, in: 1...13)
            }
            .navigationTitle("Create Feature")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Create") {
                        Task {
                            await viewModel.createFeature(name, priority: priority)
                            dismiss()
                        }
                    }
                    .disabled(name.isEmpty)
                }
            }
        }
    }
}

// Feature Detail View
struct FeatureDetailView: View {
    let feature: Feature
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text(feature.name)
                    .font(.title)
                
                HStack {
                    Label("Priority", systemImage: "flag.fill")
                    Spacer()
                    Text("\(feature.priority)")
                }
                .padding()
                .background(Color(.systemGray6))
                .cornerRadius(8)
                
                HStack {
                    Label("Created", systemImage: "calendar")
                    Spacer()
                    Text(feature.createdAt.formatted())
                }
                .padding()
                .background(Color(.systemGray6))
                .cornerRadius(8)
            }
            .padding()
        }
        .navigationTitle(feature.name)
    }
}
```

---

## 🔄 Concurrency with async/await

### Async Patterns

```swift
// Service with async/await
class FeatureService {
    static let shared = FeatureService()
    
    private let session: URLSession
    
    init(session: URLSession = .shared) {
        self.session = session
    }
    
    func getFeatures() async throws -> [Feature] {
        let url = URL(string: "https://api.example.com/features")!
        let (data, response) = try await session.data(from: url)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw NetworkError.invalidResponse
        }
        
        return try JSONDecoder().decode([Feature].self, from: data)
    }
    
    func createFeature(name: String, priority: Int) async throws -> Feature {
        let url = URL(string: "https://api.example.com/features")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = ["name": name, "priority": priority] as [String: Any]
        request.httpBody = try JSONSerialization.data(withJSONObject: body)
        
        let (data, _) = try await session.data(for: request)
        return try JSONDecoder().decode(Feature.self, from: data)
    }
}

enum NetworkError: LocalizedError {
    case invalidResponse
    case decodingError
}

// Using with Task
struct FeatureView: View {
    @State private var features: [Feature] = []
    
    var body: some View {
        List(features) { feature in
            Text(feature.name)
        }
        .task {
            do {
                features = try await FeatureService.shared.getFeatures()
            } catch {
                print("Error: \(error)")
            }
        }
    }
}
```

---

## 📱 Core Data

### Data Persistence

```swift
import CoreData

// Model
@Entity
final class FeatureCoreData {
    @Attribute(.unique) var id: String
    var name: String
    var priority: Int
    var createdAt: Date
}

// Repository
class FeatureCoreDataRepository {
    let container: NSPersistentContainer
    
    init() {
        container = NSPersistentContainer(name: "Features")
        container.loadPersistentStores { _, error in
            if let error = error {
                fatalError("Error loading Core Data: \(error)")
            }
        }
    }
    
    func fetch() -> [Feature] {
        let request = NSFetchRequest<FeatureCoreData>(entityName: "Feature")
        request.sortDescriptors = [NSSortDescriptor(keyPath: \FeatureCoreData.priority, ascending: false)]
        
        do {
            let results = try container.viewContext.fetch(request)
            return results.map { Feature(from: $0) }
        } catch {
            return []
        }
    }
    
    func save(_ feature: Feature) {
        let entity = FeatureCoreData(context: container.viewContext)
        entity.id = feature.id
        entity.name = feature.name
        entity.priority = feature.priority
        entity.createdAt = feature.createdAt
        
        do {
            try container.viewContext.save()
        } catch {
            print("Error saving: \(error)")
        }
    }
    
    func delete(_ id: String) {
        let request = NSFetchRequest<FeatureCoreData>(entityName: "Feature")
        request.predicate = NSPredicate(format: "id == %@", id)
        
        do {
            let results = try container.viewContext.fetch(request)
            results.forEach { container.viewContext.delete($0) }
            try container.viewContext.save()
        } catch {
            print("Error deleting: \(error)")
        }
    }
}
```

---

## 🎬 Navigation

### Navigation Stack

```swift
@main
struct FeatureApp: App {
    var body: some Scene {
        WindowGroup {
            NavigationStack {
                HomeView()
            }
        }
    }
}

struct HomeView: View {
    @State private var path: [NavigationDestination] = []
    
    var body: some View {
        NavigationStack(path: $path) {
            List {
                NavigationLink("Features", value: NavigationDestination.features)
                NavigationLink("Deployments", value: NavigationDestination.deployments)
            }
            .navigationDestination(for: NavigationDestination.self) { destination in
                destinationView(for: destination)
            }
            .navigationTitle("Home")
        }
    }
    
    @ViewBuilder
    func destinationView(for destination: NavigationDestination) -> some View {
        switch destination {
        case .features:
            FeatureListView()
        case .deployments:
            DeploymentListView()
        case let .featureDetail(id):
            FeatureDetailView(featureId: id)
        }
    }
}

enum NavigationDestination: Hashable {
    case features
    case deployments
    case featureDetail(id: String)
}
```

---

## 🔐 Security & Keychain

```swift
import Security

class KeychainManager {
    static let shared = KeychainManager()
    
    func save(token: String, forKey key: String) {
        let data = token.data(using: .utf8)!
        
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        ]
        
        SecItemDelete(query as CFDictionary)
        SecItemAdd(query as CFDictionary, nil)
    }
    
    func retrieve(forKey key: String) -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true
        ]
        
        var result: AnyObject?
        SecItemCopyMatching(query as CFDictionary, &result)
        
        if let data = result as? Data,
           let token = String(data: data, encoding: .utf8) {
            return token
        }
        
        return nil
    }
    
    func delete(forKey key: String) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key
        ]
        
        SecItemDelete(query as CFDictionary)
    }
}

// Usage
let token = "secure-token"
KeychainManager.shared.save(token: token, forKey: "authToken")

if let retrievedToken = KeychainManager.shared.retrieve(forKey: "authToken") {
    print("Token: \(retrievedToken)")
}
```

---

## 📚 Related Documents

- Native Android (native_android.md)
- Mobile Development (mobile_development.md)
- Cross-Platform Strategies (cross_platform.md)
- App Distribution (app_distribution.md)

---

**END OF NATIVE iOS DEVELOPMENT DOCUMENT**
