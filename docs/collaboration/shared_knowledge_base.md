# Shared Knowledge Base System

## Overview

The shared knowledge base enables agents to store, retrieve, and collaborate on information within the Advanced AI Agent System. This document covers knowledge representation, storage patterns, retrieval mechanisms, and best practices for effective knowledge sharing.

---

## 1. Knowledge Base Architecture

### 1.1 Knowledge Layers

```
┌─────────────────────────────────┐
│   Knowledge Presentation Layer   │  APIs, Query interfaces
├─────────────────────────────────┤
│   Knowledge Processing Layer     │  Indexing, caching, reasoning
├─────────────────────────────────┤
│   Knowledge Storage Layer        │  Databases, indexes, caches
├─────────────────────────────────┤
│   Knowledge Ingestion Layer      │  Parsing, extraction, validation
└─────────────────────────────────┘
```

### 1.2 Knowledge Types

**Factual Knowledge**
```javascript
{
  type: 'FACT',
  id: 'fact_001',
  domain: 'product_inventory',
  content: {
    productId: 'prod_abc',
    name: 'Product ABC',
    stock: 150,
    price: 99.99
  },
  sourceAgent: 'inventory_agent',
  timestamp: Date.now(),
  confidence: 0.95,
  ttl: 86400000 // 24 hours
}
```

**Procedural Knowledge**
```javascript
{
  type: 'PROCEDURE',
  id: 'proc_002',
  domain: 'data_processing',
  name: 'Data Validation Pipeline',
  steps: [
    { step: 1, action: 'validate_schema', params: {} },
    { step: 2, action: 'check_duplicates', params: {} },
    { step: 3, action: 'clean_data', params: {} }
  ],
  sourceAgent: 'data_processor',
  timestamp: Date.now(),
  version: '1.0'
}
```

**Contextual Knowledge**
```javascript
{
  type: 'CONTEXT',
  id: 'ctx_003',
  domain: 'customer_service',
  context: {
    customerId: 'cust_123',
    sessionId: 'sess_456',
    history: ['order_placed', 'payment_confirmed', 'shipped'],
    currentIssue: 'delivery_delayed'
  },
  sourceAgent: 'customer_agent',
  timestamp: Date.now()
}
```

**Decision Knowledge**
```javascript
{
  type: 'DECISION',
  id: 'dec_004',
  domain: 'resource_allocation',
  decision: 'ALLOCATE_RESOURCE',
  reasoning: 'High priority task with tight deadline',
  parameters: { resource: 'compute_node_5', duration: 3600 },
  sourceAgent: 'orchestrator',
  approvers: ['admin_agent'],
  timestamp: Date.now()
}
```

---

## 2. Knowledge Storage Systems

### 2.1 Multi-Tier Storage Strategy

```javascript
class KnowledgeStorageManager {
  constructor() {
    this.tiers = {
      L1: new Map(),              // In-memory cache
      L2: new LRUCache(10000),    // Process memory
      L3: new RedisCache(),       // Distributed cache
      L4: new PostgreSQL(),       // Persistent database
      L5: new DocumentStore()     // Archive storage
    };
    
    this.policies = new Map();
  }
  
  async storeKnowledge(knowledge, storagePolicy = 'auto') {
    const policy = this.policies.get(storagePolicy) || this.getDefaultPolicy(knowledge);
    
    for (const tier of policy.tiers) {
      try {
        await this.tiers[tier].set(knowledge.id, knowledge);
      } catch (error) {
        console.error(`Failed to store in tier ${tier}:`, error);
      }
    }
    
    return {
      id: knowledge.id,
      storedAt: policy.tiers,
      timestamp: Date.now()
    };
  }
  
  async retrieveKnowledge(id, preferredTier = 'L1') {
    // Try to retrieve from preferred tier first
    if (preferredTier !== 'L1') {
      try {
        const knowledge = await this.tiers[preferredTier].get(id);
        if (knowledge) {
          // Replicate to faster tiers
          await this.promoteToFasterTier(id, knowledge, preferredTier);
          return knowledge;
        }
      } catch (error) {
        console.error(`Failed to retrieve from ${preferredTier}:`, error);
      }
    }
    
    // Fall back to searching through tiers
    const tierOrder = ['L1', 'L2', 'L3', 'L4', 'L5'];
    const startIndex = tierOrder.indexOf(preferredTier);
    
    for (let i = startIndex; i < tierOrder.length; i++) {
      try {
        const knowledge = await this.tiers[tierOrder[i]].get(id);
        if (knowledge) {
          await this.promoteToFasterTier(id, knowledge, tierOrder[i]);
          return knowledge;
        }
      } catch (error) {
        continue;
      }
    }
    
    throw new Error(`Knowledge not found: ${id}`);
  }
  
  async promoteToFasterTier(id, knowledge, fromTier) {
    const tierOrder = ['L1', 'L2', 'L3', 'L4', 'L5'];
    const fromIndex = tierOrder.indexOf(fromTier);
    
    for (let i = 0; i < fromIndex; i++) {
      try {
        await this.tiers[tierOrder[i]].set(id, knowledge);
      } catch (error) {
        console.error(`Failed to promote to ${tierOrder[i]}:`, error);
      }
    }
  }
  
  getDefaultPolicy(knowledge) {
    const frequency = knowledge.accessFrequency || 'low';
    const ttl = knowledge.ttl || 3600000;
    
    if (frequency === 'high' && ttl > 86400000) {
      return { tiers: ['L1', 'L2', 'L3', 'L4'] };
    } else if (frequency === 'medium') {
      return { tiers: ['L2', 'L3', 'L4'] };
    } else {
      return { tiers: ['L3', 'L4'] };
    }
  }
}
```

### 2.2 Knowledge Graph Database

```javascript
class KnowledgeGraph {
  constructor() {
    this.nodes = new Map();
    this.edges = new Map();
    this.indexes = {
      byType: new Map(),
      byDomain: new Map(),
      byAgent: new Map()
    };
  }
  
  addNode(knowledge) {
    this.nodes.set(knowledge.id, {
      ...knowledge,
      relationships: []
    });
    
    // Index by multiple dimensions
    this.indexNode(knowledge);
  }
  
  indexNode(knowledge) {
    // Index by type
    if (!this.indexes.byType.has(knowledge.type)) {
      this.indexes.byType.set(knowledge.type, []);
    }
    this.indexes.byType.get(knowledge.type).push(knowledge.id);
    
    // Index by domain
    if (!this.indexes.byDomain.has(knowledge.domain)) {
      this.indexes.byDomain.set(knowledge.domain, []);
    }
    this.indexes.byDomain.get(knowledge.domain).push(knowledge.id);
    
    // Index by source agent
    if (!this.indexes.byAgent.has(knowledge.sourceAgent)) {
      this.indexes.byAgent.set(knowledge.sourceAgent, []);
    }
    this.indexes.byAgent.get(knowledge.sourceAgent).push(knowledge.id);
  }
  
  addRelationship(fromId, toId, relationType, metadata = {}) {
    const edge = {
      id: `edge_${fromId}_${toId}`,
      from: fromId,
      to: toId,
      type: relationType,
      metadata,
      timestamp: Date.now()
    };
    
    this.edges.set(edge.id, edge);
    
    // Update node relationships
    const fromNode = this.nodes.get(fromId);
    if (fromNode) {
      fromNode.relationships.push(edge.id);
    }
  }
  
  queryByPattern(pattern) {
    const results = [];
    
    for (const [id, node] of this.nodes) {
      if (this.matchesPattern(node, pattern)) {
        results.push(node);
      }
    }
    
    return results;
  }
  
  matchesPattern(node, pattern) {
    for (const [key, value] of Object.entries(pattern)) {
      if (key === 'domain' || key === 'type') {
        if (node[key] !== value) return false;
      } else if (key === 'content') {
        if (!this.matchesContent(node.content, value)) return false;
      }
    }
    return true;
  }
  
  matchesContent(content, pattern) {
    for (const [key, value] of Object.entries(pattern)) {
      if (content[key] !== value) return false;
    }
    return true;
  }
  
  traverse(startId, depth = 2) {
    const visited = new Set();
    const result = [];
    
    this.traverseHelper(startId, depth, visited, result);
    
    return result;
  }
  
  traverseHelper(nodeId, depth, visited, result) {
    if (depth === 0 || visited.has(nodeId)) return;
    
    visited.add(nodeId);
    const node = this.nodes.get(nodeId);
    result.push(node);
    
    for (const edgeId of node.relationships) {
      const edge = this.edges.get(edgeId);
      if (edge) {
        this.traverseHelper(edge.to, depth - 1, visited, result);
      }
    }
  }
}
```

---

## 3. Knowledge Retrieval and Querying

### 3.1 Query Engine

```javascript
class KnowledgeQueryEngine {
  constructor(storageManager, knowledgeGraph) {
    this.storageManager = storageManager;
    this.graph = knowledgeGraph;
    this.queryParsers = new Map();
    this.queryCache = new Map();
  }
  
  async query(queryString, options = {}) {
    // Check cache first
    const cacheKey = `${queryString}_${JSON.stringify(options)}`;
    if (this.queryCache.has(cacheKey)) {
      return this.queryCache.get(cacheKey);
    }
    
    // Parse query
    const parsedQuery = this.parseQuery(queryString);
    
    // Execute query
    let results = [];
    
    switch (parsedQuery.type) {
      case 'keyword':
        results = await this.keywordSearch(parsedQuery);
        break;
      case 'pattern':
        results = await this.patternSearch(parsedQuery);
        break;
      case 'graph':
        results = await this.graphSearch(parsedQuery);
        break;
      case 'semantic':
        results = await this.semanticSearch(parsedQuery);
        break;
      default:
        throw new Error(`Unknown query type: ${parsedQuery.type}`);
    }
    
    // Apply filters
    if (options.filters) {
      results = this.applyFilters(results, options.filters);
    }
    
    // Sort results
    if (options.sort) {
      results = this.sortResults(results, options.sort);
    }
    
    // Limit results
    if (options.limit) {
      results = results.slice(0, options.limit);
    }
    
    this.queryCache.set(cacheKey, results);
    return results;
  }
  
  parseQuery(queryString) {
    // Parse query to determine type and extract parameters
    if (queryString.startsWith('MATCH')) {
      return { type: 'graph', query: queryString };
    } else if (queryString.includes('?')) {
      return { type: 'pattern', query: queryString };
    } else if (queryString.includes('semantic')) {
      return { type: 'semantic', query: queryString };
    } else {
      return { type: 'keyword', query: queryString };
    }
  }
  
  async keywordSearch(query) {
    const keywords = query.query.split(' ');
    const results = [];
    
    for (const [id, node] of this.graph.nodes) {
      const score = this.calculateRelevance(node, keywords);
      if (score > 0) {
        results.push({ node, score });
      }
    }
    
    return results.sort((a, b) => b.score - a.score);
  }
  
  calculateRelevance(node, keywords) {
    let score = 0;
    const nodeStr = JSON.stringify(node).toLowerCase();
    
    for (const keyword of keywords) {
      if (nodeStr.includes(keyword.toLowerCase())) {
        score += 1;
      }
    }
    
    return score;
  }
  
  async patternSearch(query) {
    // Extract pattern from query
    const pattern = this.extractPattern(query.query);
    return this.graph.queryByPattern(pattern);
  }
  
  extractPattern(queryString) {
    // Parse pattern query format
    const pattern = {};
    const parts = queryString.split('?');
    
    for (const part of parts) {
      const [key, value] = part.split('=').map(s => s.trim());
      if (key && value) {
        pattern[key] = value;
      }
    }
    
    return pattern;
  }
  
  async graphSearch(query) {
    // Execute graph query (MATCH syntax)
    const traversalDepth = this.extractDepth(query.query) || 2;
    
    // Extract start node pattern
    const startPattern = this.extractStartPattern(query.query);
    const startNodes = this.graph.queryByPattern(startPattern);
    
    const results = [];
    for (const node of startNodes) {
      const traversed = this.graph.traverse(node.id, traversalDepth);
      results.push(...traversed);
    }
    
    return [...new Map(results.map(r => [r.id, r])).values()];
  }
  
  async semanticSearch(query) {
    // Use semantic similarity to find related knowledge
    const embedding = await this.getEmbedding(query.query);
    const results = [];
    
    for (const [id, node] of this.graph.nodes) {
      const nodeEmbedding = await this.getEmbedding(
        JSON.stringify(node.content)
      );
      const similarity = this.cosineSimilarity(embedding, nodeEmbedding);
      
      if (similarity > 0.7) {
        results.push({ node, similarity });
      }
    }
    
    return results.sort((a, b) => b.similarity - a.similarity);
  }
  
  applyFilters(results, filters) {
    return results.filter(result => {
      const node = result.node || result;
      
      for (const [key, value] of Object.entries(filters)) {
        if (node[key] !== value) return false;
      }
      
      return true;
    });
  }
  
  sortResults(results, sortCriteria) {
    return results.sort((a, b) => {
      const nodeA = a.node || a;
      const nodeB = b.node || b;
      
      const valueA = nodeA[sortCriteria];
      const valueB = nodeB[sortCriteria];
      
      return valueA > valueB ? 1 : -1;
    });
  }
}
```

### 3.2 Semantic Search with Embeddings

```javascript
class SemanticSearchEngine {
  constructor() {
    this.embeddingCache = new Map();
    this.model = null;
  }
  
  async initializeModel() {
    // Initialize embedding model (e.g., using transformers)
    const tf = require('@tensorflow/tfjs');
    const use = require('@tensorflow-hub/universal-sentence-encoder');
    
    this.model = await use.load();
  }
  
  async getEmbedding(text) {
    if (this.embeddingCache.has(text)) {
      return this.embeddingCache.get(text);
    }
    
    const embedding = await this.model.embed(text);
    const array = await embedding.data();
    
    this.embeddingCache.set(text, array);
    return array;
  }
  
  cosineSimilarity(vecA, vecB) {
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;
    
    for (let i = 0; i < vecA.length; i++) {
      dotProduct += vecA[i] * vecB[i];
      normA += vecA[i] * vecA[i];
      normB += vecB[i] * vecB[i];
    }
    
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
  }
  
  async findSimilarKnowledge(query, topK = 5) {
    const queryEmbedding = await this.getEmbedding(query);
    const similarities = [];
    
    for (const [text, embedding] of this.embeddingCache) {
      const similarity = this.cosineSimilarity(queryEmbedding, embedding);
      similarities.push({ text, similarity });
    }
    
    return similarities
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, topK);
  }
}
```

---

## 4. Knowledge Contributions and Updates

### 4.1 Knowledge Contribution Workflow

```javascript
class KnowledgeContributionManager {
  constructor() {
    this.pendingContributions = [];
    this.approvedKnowledge = new Map();
    this.rejectedKnowledge = [];
    this.validators = [];
  }
  
  async submitContribution(agent, knowledge) {
    const contribution = {
      id: this.generateId(),
      agentId: agent.id,
      knowledge,
      timestamp: Date.now(),
      status: 'PENDING',
      validations: [],
      approvals: [],
      rejections: []
    };
    
    this.pendingContributions.push(contribution);
    
    // Run validators
    await this.validateContribution(contribution);
    
    return contribution;
  }
  
  async validateContribution(contribution) {
    for (const validator of this.validators) {
      try {
        const result = await validator(contribution.knowledge);
        
        contribution.validations.push({
          validator: validator.name,
          passed: result.passed,
          message: result.message
        });
        
        if (!result.passed && result.severity === 'error') {
          contribution.status = 'INVALID';
          return;
        }
      } catch (error) {
        contribution.validations.push({
          validator: validator.name,
          passed: false,
          error: error.message
        });
      }
    }
    
    contribution.status = 'VALIDATED';
  }
  
  registerValidator(name, validator) {
    validator.name = name;
    this.validators.push(validator);
  }
  
  async approveContribution(contributionId, approver) {
    const contribution = this.pendingContributions.find(c => c.id === contributionId);
    
    if (!contribution) {
      throw new Error(`Contribution not found: ${contributionId}`);
    }
    
    contribution.approvals.push({
      approver,
      timestamp: Date.now()
    });
    
    if (contribution.approvals.length >= 2) {
      contribution.status = 'APPROVED';
      await this.storeApprovedKnowledge(contribution);
    }
  }
  
  async rejectContribution(contributionId, rejector, reason) {
    const contribution = this.pendingContributions.find(c => c.id === contributionId);
    
    if (!contribution) {
      throw new Error(`Contribution not found: ${contributionId}`);
    }
    
    contribution.rejections.push({
      rejector,
      reason,
      timestamp: Date.now()
    });
    
    contribution.status = 'REJECTED';
    this.rejectedKnowledge.push(contribution);
  }
  
  async storeApprovedKnowledge(contribution) {
    this.approvedKnowledge.set(
      contribution.knowledge.id,
      contribution.knowledge
    );
    
    // Remove from pending
    const index = this.pendingContributions.indexOf(contribution);
    if (index > -1) {
      this.pendingContributions.splice(index, 1);
    }
  }
  
  generateId() {
    const crypto = require('crypto');
    return `contrib_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
  }
}
```

### 4.2 Knowledge Versioning and Evolution

```javascript
class KnowledgeVersioning {
  constructor() {
    this.versions = new Map();
    this.history = [];
  }
  
  createVersion(knowledge) {
    const version = {
      id: knowledge.id,
      versionNumber: this.getNextVersion(knowledge.id),
      content: knowledge,
      createdAt: Date.now(),
      createdBy: knowledge.sourceAgent,
      changes: []
    };
    
    if (!this.versions.has(knowledge.id)) {
      this.versions.set(knowledge.id, []);
    }
    
    this.versions.get(knowledge.id).push(version);
    this.history.push(version);
    
    return version;
  }
  
  updateKnowledge(knowledge, changes) {
    const currentVersions = this.versions.get(knowledge.id) || [];
    const latestVersion = currentVersions[currentVersions.length - 1];
    
    const newVersion = {
      id: knowledge.id,
      versionNumber: latestVersion ? latestVersion.versionNumber + 1 : 1,
      content: { ...knowledge },
      createdAt: Date.now(),
      createdBy: knowledge.sourceAgent,
      changes: this.calculateChanges(latestVersion?.content, knowledge)
    };
    
    this.versions.get(knowledge.id).push(newVersion);
    this.history.push(newVersion);
    
    return newVersion;
  }
  
  calculateChanges(oldContent, newContent) {
    const changes = [];
    
    for (const [key, newValue] of Object.entries(newContent)) {
      const oldValue = oldContent[key];
      
      if (JSON.stringify(oldValue) !== JSON.stringify(newValue)) {
        changes.push({
          field: key,
          oldValue,
          newValue,
          timestamp: Date.now()
        });
      }
    }
    
    return changes;
  }
  
  getVersion(id, versionNumber) {
    const versions = this.versions.get(id);
    if (!versions) return null;
    
    return versions.find(v => v.versionNumber === versionNumber);
  }
  
  getVersionHistory(id) {
    return this.versions.get(id) || [];
  }
  
  getNextVersion(id) {
    const versions = this.versions.get(id);
    if (!versions || versions.length === 0) return 1;
    
    return Math.max(...versions.map(v => v.versionNumber)) + 1;
  }
  
  rollbackToVersion(id, versionNumber) {
    const version = this.getVersion(id, versionNumber);
    if (!version) throw new Error(`Version not found: ${versionNumber}`);
    
    return version.content;
  }
}
```

---

## 5. Knowledge Consistency and Integrity

### 5.1 Conflict Resolution

```javascript
class ConflictResolver {
  constructor() {
    this.conflicts = [];
    this.resolutionStrategies = new Map();
  }
  
  detectConflict(knowledge1, knowledge2) {
    if (knowledge1.id !== knowledge2.id) return null;
    
    const conflict = {
      id: knowledge1.id,
      source1: { knowledge: knowledge1, agent: knowledge1.sourceAgent },
      source2: { knowledge: knowledge2, agent: knowledge2.sourceAgent },
      timestamp: Date.now(),
      status: 'UNRESOLVED'
    };
    
    this.conflicts.push(conflict);
    return conflict;
  }
  
  registerResolutionStrategy(name, strategy) {
    this.resolutionStrategies.set(name, strategy);
  }
  
  async resolveConflict(conflict, strategy = 'latest') {
    const resolver = this.resolutionStrategies.get(strategy);
    
    if (!resolver) {
      throw new Error(`Unknown resolution strategy: ${strategy}`);
    }
    
    const resolved = await resolver(conflict);
    
    conflict.status = 'RESOLVED';
    conflict.resolution = resolved;
    conflict.resolvedAt = Date.now();
    conflict.resolvedUsing = strategy;
    
    return resolved;
  }
}

// Built-in resolution strategies
const resolutionStrategies = {
  latest: (conflict) => {
    return conflict.source1.knowledge.timestamp > conflict.source2.knowledge.timestamp ?
      conflict.source1.knowledge :
      conflict.source2.knowledge;
  },
  
  merge: (conflict) => {
    return {
      ...conflict.source1.knowledge,
      ...conflict.source2.knowledge,
      merged: true,
      sources: [conflict.source1.agent, conflict.source2.agent]
    };
  },
  
  confidence: (conflict) => {
    const conf1 = conflict.source1.knowledge.confidence || 0.5;
    const conf2 = conflict.source2.knowledge.confidence || 0.5;
    
    return conf1 > conf2 ?
      conflict.source1.knowledge :
      conflict.source2.knowledge;
  },
  
  weighted: (conflict, weights = {}) => {
    const score1 = (weights[conflict.source1.agent] || 1) *
      (conflict.source1.knowledge.confidence || 0.5);
    const score2 = (weights[conflict.source2.agent] || 1) *
      (conflict.source2.knowledge.confidence || 0.5);
    
    return score1 > score2 ?
      conflict.source1.knowledge :
      conflict.source2.knowledge;
  }
};
```

### 5.2 Data Validation and Sanitization

```javascript
class KnowledgeValidator {
  constructor() {
    this.schemas = new Map();
    this.sanitizers = [];
  }
  
  registerSchema(domain, schema) {
    this.schemas.set(domain, schema);
  }
  
  async validateKnowledge(knowledge) {
    const schema = this.schemas.get(knowledge.domain);
    
    if (!schema) {
      throw new Error(`No schema defined for domain: ${knowledge.domain}`);
    }
    
    const errors = [];
    
    // Validate content against schema
    for (const [field, requirement] of Object.entries(schema)) {
      const value = knowledge.content[field];
      
      if (requirement.required && !value) {
        errors.push(`Missing required field: ${field}`);
      }
      
      if (value && requirement.type && typeof value !== requirement.type) {
        errors.push(`Field ${field} has wrong type`);
      }
      
      if (requirement.validator) {
        const validationResult = requirement.validator(value);
        if (!validationResult.valid) {
          errors.push(validationResult.error);
        }
      }
    }
    
    if (errors.length > 0) {
      throw new Error(`Validation failed: ${errors.join(', ')}`);
    }
    
    return true;
  }
  
  async sanitizeKnowledge(knowledge) {
    let sanitized = { ...knowledge };
    
    for (const sanitizer of this.sanitizers) {
      sanitized = await sanitizer(sanitized);
    }
    
    return sanitized;
  }
  
  registerSanitizer(sanitizer) {
    this.sanitizers.push(sanitizer);
  }
}

// Example sanitizers
const dataSanitizers = {
  removeNull: (knowledge) => {
    const clean = { ...knowledge };
    
    for (const [key, value] of Object.entries(clean.content)) {
      if (value === null) {
        delete clean.content[key];
      }
    }
    
    return clean;
  },
  
  trimStrings: (knowledge) => {
    const clean = { ...knowledge };
    
    for (const [key, value] of Object.entries(clean.content)) {
      if (typeof value === 'string') {
        clean.content[key] = value.trim();
      }
    }
    
    return clean;
  },
  
  normalizeData: (knowledge) => {
    const clean = { ...knowledge };
    
    // Normalize dates to ISO format
    for (const [key, value] of Object.entries(clean.content)) {
      if (value instanceof Date) {
        clean.content[key] = value.toISOString();
      }
    }
    
    return clean;
  }
};
```

---

## 6. Knowledge Analytics

### 6.1 Knowledge Metrics

```javascript
class KnowledgeAnalytics {
  constructor() {
    this.accessLogs = [];
    this.contributors = new Map();
    this.domains = new Map();
  }
  
  logAccess(knowledgeId, agent, action) {
    this.accessLogs.push({
      knowledgeId,
      agent,
      action,
      timestamp: Date.now()
    });
  }
  
  getMostAccessedKnowledge(limit = 10) {
    const accessCounts = new Map();
    
    for (const log of this.accessLogs) {
      const count = accessCounts.get(log.knowledgeId) || 0;
      accessCounts.set(log.knowledgeId, count + 1);
    }
    
    return [...accessCounts.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, limit)
      .map(([id, count]) => ({ id, accessCount: count }));
  }
  
  getTopContributors(limit = 10) {
    const contributions = new Map();
    
    for (const [agent, count] of this.contributors) {
      contributions.set(agent, count);
    }
    
    return [...contributions.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, limit)
      .map(([agent, count]) => ({ agent, contributions: count }));
  }
  
  getKnowledgeByDomain(domain) {
    return this.domains.get(domain) || [];
  }
  
  recordContribution(agent) {
    const count = this.contributors.get(agent) || 0;
    this.contributors.set(agent, count + 1);
  }
}
```

---

## 7. Best Practices

### Knowledge Management Best Practices
- Maintain consistent schema definitions per domain
- Use versioning for all critical knowledge updates
- Implement multi-tier caching for performance
- Regular validation and sanitization of knowledge
- Track knowledge lineage and provenance
- Implement access controls based on sensitivity
- Use semantic search for discovery
- Maintain knowledge expiration policies

### Knowledge Sharing Best Practices
- Document knowledge context clearly
- Use consistent terminology
- Tag knowledge with relevant domains
- Implement knowledge review workflows
- Monitor knowledge usage patterns
- Maintain knowledge quality metrics

---

## Conclusion

The shared knowledge base enables effective knowledge sharing between agents while maintaining data integrity, consistency, and performance. This document provides comprehensive patterns and implementations for production-grade knowledge management systems.
