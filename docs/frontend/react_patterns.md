# React Patterns Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Last Updated:** October 26, 2024
**Document Type:** React Patterns & Techniques Guide
**React Version:** 18+
**Focus:** Production-grade React patterns with 150+ techniques

---

## 📖 Introduction

Comprehensive guide covering React patterns, hooks, component design, optimization, and best practices for the AI Agent System frontend.

---

## 🎣 Hooks Patterns

### useState with Custom Hooks

```typescript
// Basic useState
const [features, setFeatures] = useState<Feature[]>([]);
const [loading, setLoading] = useState(false);
const [error, setError] = useState<Error | null>(null);

// ✅ GOOD: Combine related state
interface FeatureState {
  data: Feature[];
  loading: boolean;
  error: Error | null;
}

const [state, dispatch] = useReducer(
  (state: FeatureState, action) => {
    switch (action.type) {
      case 'FETCH_START':
        return { ...state, loading: true, error: null };
      case 'FETCH_SUCCESS':
        return { data: action.payload, loading: false, error: null };
      case 'FETCH_ERROR':
        return { ...state, loading: false, error: action.error };
      default:
        return state;
    }
  },
  { data: [], loading: false, error: null }
);

// Custom hook for API call
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url);
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
}

// Usage
const { data: features, loading } = useFetch<Feature[]>('/api/features');
```

### useEffect Patterns

```typescript
// ✅ GOOD: Proper dependency array
useEffect(() => {
  const controller = new AbortController();
  
  const loadFeatures = async () => {
    try {
      const response = await fetch('/api/features', {
        signal: controller.signal
      });
      setFeatures(await response.json());
    } catch (err) {
      if (err.name !== 'AbortError') {
        setError(err);
      }
    }
  };

  loadFeatures();

  return () => controller.abort(); // Cleanup
}, []);

// ❌ AVOID: Empty dependency array in mounted effect
useEffect(() => {
  // This runs on EVERY render!
  const loadData = async () => { /* ... */ };
  loadData();
}, []); // Missing dependencies

// ✅ GOOD: Run on specific dependency change
useEffect(() => {
  fetchFeatureDetails(featureId);
}, [featureId]); // Re-run when featureId changes
```

### useContext for State Management

```typescript
interface User {
  id: string;
  email: string;
  role: 'admin' | 'developer' | 'viewer';
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

// Provider
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = async (email: string, password: string) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const userData = await response.json();
    setUser(userData);
  };

  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook
function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}

// Usage
function Profile() {
  const { user, logout } = useAuth();
  return (
    <div>
      <p>Welcome, {user?.email}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

---

## 🧩 Component Patterns

### Higher-Order Components (HOC)

```typescript
// HOC for adding authentication
function withAuth<P extends object>(
  Component: React.ComponentType<P>
) {
  return function ProtectedComponent(props: P) {
    const { user } = useAuth();
    const [authorized, setAuthorized] = useState(false);

    useEffect(() => {
      const checkAccess = async () => {
        const hasAccess = await verifyAccess(user);
        setAuthorized(hasAccess);
      };

      if (user) {
        checkAccess();
      }
    }, [user]);

    if (!user || !authorized) {
      return <div>Access Denied</div>;
    }

    return <Component {...props} />;
  };
}

// Usage
const ProtectedDashboard = withAuth(Dashboard);
```

### Compound Components

```typescript
// Form with compound components
interface FormContextType {
  values: Record<string, any>;
  errors: Record<string, string>;
  touched: Record<string, boolean>;
  setFieldValue: (field: string, value: any) => void;
}

const FormContext = createContext<FormContextType | null>(null);

function Form({ children, onSubmit }: any) {
  const [values, setValues] = useState({});
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  const setFieldValue = (field: string, value: any) => {
    setValues(prev => ({ ...prev, [field]: value }));
  };

  return (
    <FormContext.Provider value={{ values, errors, touched, setFieldValue }}>
      <form onSubmit={(e) => {
        e.preventDefault();
        onSubmit(values);
      }}>
        {children}
      </form>
    </FormContext.Provider>
  );
}

function FormField({ name, label }: any) {
  const context = useContext(FormContext);
  if (!context) throw new Error('FormField must be in Form');

  return (
    <div>
      <label>{label}</label>
      <input
        value={context.values[name] || ''}
        onChange={(e) => context.setFieldValue(name, e.target.value)}
      />
      {context.errors[name] && <span>{context.errors[name]}</span>}
    </div>
  );
}

// Usage
<Form onSubmit={handleSubmit}>
  <FormField name="email" label="Email" />
  <FormField name="password" label="Password" />
  <button type="submit">Login</button>
</Form>
```

### Render Props Pattern

```typescript
// Mouse position tracker with render props
interface MouseTrackerProps {
  children: (position: { x: number; y: number }) => React.ReactNode;
}

function MouseTracker({ children }: MouseTrackerProps) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (event: MouseEvent) => {
      setPosition({ x: event.clientX, y: event.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return <>{children(position)}</>;
}

// Usage
<MouseTracker>
  {(position) => (
    <div>
      Mouse position: {position.x}, {position.y}
    </div>
  )}
</MouseTracker>
```

---

## 🎨 Advanced Component Patterns

### Controlled vs Uncontrolled Components

```typescript
// ✅ GOOD: Controlled component
interface ControlledInputProps {
  value: string;
  onChange: (value: string) => void;
}

function ControlledInput({ value, onChange }: ControlledInputProps) {
  return (
    <input
      value={value}
      onChange={(e) => onChange(e.target.value)}
    />
  );
}

// Usage
function FeatureForm() {
  const [name, setName] = useState('');
  
  return (
    <ControlledInput
      value={name}
      onChange={setName}
    />
  );
}

// ❌ AVOID: Uncontrolled unless necessary
function UncontrolledInput() {
  const inputRef = useRef<HTMLInputElement>(null);
  
  const handleSubmit = () => {
    console.log(inputRef.current?.value);
  };
  
  return (
    <>
      <input ref={inputRef} defaultValue="default" />
      <button onClick={handleSubmit}>Submit</button>
    </>
  );
}
```

### Memoization for Performance

```typescript
// useMemo for expensive computations
function ExpensiveComponent({ items }: { items: Item[] }) {
  const sortedItems = useMemo(() => {
    return items.sort((a, b) => a.priority - b.priority);
  }, [items]);

  return <div>{sortedItems.map(item => <div key={item.id}>{item.name}</div>)}</div>;
}

// useCallback for stable function references
interface ListProps {
  items: Item[];
  onSelect: (item: Item) => void;
}

function List({ items, onSelect }: ListProps) {
  const memoizedOnSelect = useCallback((item: Item) => {
    onSelect(item);
  }, [onSelect]);

  return (
    <ul>
      {items.map(item => (
        <ListItem
          key={item.id}
          item={item}
          onSelect={memoizedOnSelect}
        />
      ))}
    </ul>
  );
}

// React.memo for component memoization
const ListItem = React.memo(({ item, onSelect }: any) => {
  return (
    <li onClick={() => onSelect(item)}>
      {item.name}
    </li>
  );
});
```

---

## 🎯 React Query / TanStack Query

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Query hook
function useFeatures() {
  return useQuery({
    queryKey: ['features'],
    queryFn: async () => {
      const response = await fetch('/api/features');
      return response.json();
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
    gcTime: 1000 * 60 * 10, // 10 minutes
  });
}

// Mutation hook
function useCreateFeature() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (feature: FeatureCreate) => {
      const response = await fetch('/api/features', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(feature),
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['features'] });
    },
  });
}

// Usage
function FeatureList() {
  const { data: features, isLoading, error } = useFeatures();
  const createMutation = useCreateFeature();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      {features?.map(feature => (
        <div key={feature.id}>{feature.name}</div>
      ))}
      <button onClick={() => createMutation.mutate({ name: 'New' })}>
        Create
      </button>
    </div>
  );
}
```

---

## ✅ Form Handling

```typescript
// React Hook Form integration
import { useForm } from 'react-hook-form';

interface LoginForm {
  email: string;
  password: string;
}

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginForm>({
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const onSubmit = async (data: LoginForm) => {
    await loginAPI(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register('email', {
          required: 'Email is required',
          pattern: {
            value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
            message: 'Invalid email',
          },
        })}
        placeholder="Email"
      />
      {errors.email && <span>{errors.email.message}</span>}

      <input
        {...register('password', {
          required: 'Password required',
          minLength: { value: 8, message: 'Min 8 chars' },
        })}
        type="password"
        placeholder="Password"
      />
      {errors.password && <span>{errors.password.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}
```

---

## 🎬 Animation Patterns

```typescript
// Framer Motion animations
import { motion } from 'framer-motion';

function AnimatedList({ items }: { items: any[] }) {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.2 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map((item) => (
        <motion.li key={item.id} variants={itemVariants}>
          {item.name}
        </motion.li>
      ))}
    </motion.ul>
  );
}

// Page transitions
function PageTransition({ children }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
}
```

---

## 🎓 Advanced Patterns

### Custom Hook for Form State

```typescript
function useFormState<T>(initialValues: T) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  const setFieldValue = (field: keyof T, value: any) => {
    setValues(prev => ({ ...prev, [field]: value }));
  };

  const setFieldError = (field: keyof T, error: string) => {
    setErrors(prev => ({ ...prev, [field]: error }));
  };

  const setFieldTouched = (field: keyof T) => {
    setTouched(prev => ({ ...prev, [field]: true }));
  };

  return {
    values,
    errors,
    touched,
    setFieldValue,
    setFieldError,
    setFieldTouched,
    reset: () => {
      setValues(initialValues);
      setErrors({});
      setTouched({});
    },
  };
}
```

### Error Boundary Pattern

```typescript
interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error) {
    logger.error('Error caught by boundary:', error);
  }

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div>
            <h1>Something went wrong</h1>
            <p>{this.state.error?.message}</p>
          </div>
        )
      );
    }

    return this.props.children;
  }
}
```

---

## 📚 Related Documents

- State Management (state_management.md)
- Performance (performance.md)
- UI/UX Patterns (ui_ux_patterns.md)

---

**END OF REACT PATTERNS DOCUMENT**
