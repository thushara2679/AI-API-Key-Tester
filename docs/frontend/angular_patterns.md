# Angular Patterns Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Angular Patterns & Techniques Guide
**Angular Version:** 17+
**Focus:** Enterprise-grade Angular with RxJS

---

## 🎯 Angular Service Patterns

### Service Architecture

```typescript
// features.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { tap, catchError, shareReplay, finalize } from 'rxjs/operators';

interface Feature {
  id: string;
  name: string;
  priority: number;
}

@Injectable({
  providedIn: 'root'
})
export class FeaturesService {
  private readonly API_URL = '/api/features';
  
  private featuresSubject = new BehaviorSubject<Feature[]>([]);
  public features$ = this.featuresSubject.asObservable();
  
  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$ = this.loadingSubject.asObservable();
  
  private errorSubject = new Subject<Error>();
  public error$ = this.errorSubject.asObservable();

  constructor(private http: HttpClient) {}

  loadFeatures(): Observable<Feature[]> {
    this.loadingSubject.next(true);
    
    return this.http.get<Feature[]>(this.API_URL).pipe(
      tap(features => {
        this.featuresSubject.next(features);
        this.loadingSubject.next(false);
      }),
      catchError(error => {
        this.errorSubject.next(error);
        this.loadingSubject.next(false);
        throw error;
      }),
      shareReplay(1)
    );
  }

  createFeature(feature: Omit<Feature, 'id'>): Observable<Feature> {
    return this.http.post<Feature>(this.API_URL, feature).pipe(
      tap(newFeature => {
        const current = this.featuresSubject.value;
        this.featuresSubject.next([...current, newFeature]);
      })
    );
  }

  deleteFeature(id: string): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/${id}`).pipe(
      tap(() => {
        const features = this.featuresSubject.value.filter(f => f.id !== id);
        this.featuresSubject.next(features);
      })
    );
  }
}
```

### Smart vs Presentational Components

```typescript
// Smart component
@Component({
  selector: 'app-features-container',
  template: `
    <div *ngIf="loading$ | async; else loaded">
      <app-loading></app-loading>
    </div>
    <ng-template #loaded>
      <app-features-list
        [features]="features$ | async"
        (featureSelected)="onFeatureSelected($event)"
        (featureDeleted)="onFeatureDeleted($event)"
      ></app-features-list>
    </ng-template>
  `
})
export class FeaturesContainerComponent {
  features$: Observable<Feature[]>;
  loading$: Observable<boolean>;

  constructor(private featuresService: FeaturesService) {
    this.features$ = this.featuresService.features$;
    this.loading$ = this.featuresService.loading$;
  }

  ngOnInit() {
    this.featuresService.loadFeatures().subscribe();
  }

  onFeatureSelected(feature: Feature) {
    // Handle selection
  }

  onFeatureDeleted(id: string) {
    this.featuresService.deleteFeature(id).subscribe();
  }
}

// Presentational component
@Component({
  selector: 'app-features-list',
  template: `
    <ul>
      <li *ngFor="let feature of features; trackBy: trackByFn">
        {{ feature.name }}
        <button (click)="delete.emit(feature.id)">Delete</button>
      </li>
    </ul>
  `
})
export class FeaturesListComponent {
  @Input() features: Feature[] | null = null;
  @Output() featureSelected = new EventEmitter<Feature>();
  @Output() featureDeleted = new EventEmitter<string>();

  trackByFn(index: number, item: Feature) {
    return item.id;
  }
}
```

---

## 🎯 RxJS Patterns

### Operators and Composition

```typescript
// Feature facade service combining multiple observables
@Injectable({
  providedIn: 'root'
})
export class FeatureFacade {
  features$: Observable<Feature[]>;
  selectedFeature$: Observable<Feature | null>;
  filteredFeatures$: Observable<Feature[]>;

  private filterSubject = new Subject<string>();
  private selectedSubject = new BehaviorSubject<string | null>(null);

  constructor(private featuresService: FeaturesService) {
    this.features$ = this.featuresService.features$;
    
    this.selectedFeature$ = this.selectedSubject.pipe(
      switchMap(id => 
        id ? this.featuresService.getFeature(id) : of(null)
      )
    );

    this.filteredFeatures$ = combineLatest([
      this.features$,
      this.filterSubject.pipe(startWith(''))
    ]).pipe(
      map(([features, filter]) =>
        features.filter(f =>
          f.name.toLowerCase().includes(filter.toLowerCase())
        )
      ),
      debounceTime(300),
      distinctUntilChanged()
    );
  }

  selectFeature(id: string) {
    this.selectedSubject.next(id);
  }

  filterFeatures(query: string) {
    this.filterSubject.next(query);
  }
}
```

---

## 🏠 Dependency Injection

```typescript
// Configuration provider
@Injectable()
export class AppConfig {
  config: IAppConfig;

  constructor(private http: HttpClient) {
    this.config = {
      apiUrl: 'https://api.example.com',
      timeout: 30000
    };
  }
}

// Provide configuration
const providers = [
  { provide: APP_INITIALIZER, useFactory: initializeApp, deps: [AppConfig], multi: true }
];

export function initializeApp(config: AppConfig) {
  return () => config.init();
}

// Usage in component
@Component({
  selector: 'app-root',
  template: `<app-features></app-features>`
})
export class AppComponent {
  constructor(private config: AppConfig) {}
}
```

---

## ✅ Form Validation

```typescript
@Component({
  selector: 'app-feature-form',
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <div class="form-group">
        <label>Name</label>
        <input formControlName="name" />
        <div *ngIf="name?.invalid && name?.touched">
          <span *ngIf="name?.errors?.['required']">Required</span>
          <span *ngIf="name?.errors?.['minlength']">Min 2 chars</span>
        </div>
      </div>

      <div class="form-group">
        <label>Priority</label>
        <input type="number" formControlName="priority" />
      </div>

      <button type="submit" [disabled]="!form.valid">
        Create
      </button>
    </form>
  `
})
export class FeatureFormComponent {
  form: FormGroup;

  get name() {
    return this.form.get('name');
  }

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      priority: [5, [Validators.required, Validators.min(1), Validators.max(13)]],
    });
  }

  onSubmit() {
    if (this.form.valid) {
      console.log(this.form.value);
    }
  }
}
```

---

## 🔄 State Management with NgRx

```typescript
// actions
export const loadFeatures = createAction('[Features Page] Load Features');
export const loadFeaturesSuccess = createAction(
  '[Features API] Load Features Success',
  props<{ features: Feature[] }>()
);
export const loadFeaturesFailure = createAction(
  '[Features API] Load Features Failure',
  props<{ error: Error }>()
);

// reducer
interface FeaturesState {
  features: Feature[];
  loading: boolean;
  error: Error | null;
}

export const initialState: FeaturesState = {
  features: [],
  loading: false,
  error: null,
};

export const featuresReducer = createReducer(
  initialState,
  on(loadFeatures, state => ({ ...state, loading: true })),
  on(loadFeaturesSuccess, (state, { features }) => ({
    ...state,
    features,
    loading: false,
  })),
  on(loadFeaturesFailure, (state, { error }) => ({
    ...state,
    error,
    loading: false,
  }))
);

// effects
@Injectable()
export class FeaturesEffects {
  loadFeatures$ = createEffect(() =>
    this.actions$.pipe(
      ofType(loadFeatures),
      switchMap(() =>
        this.featuresService.loadFeatures().pipe(
          map(features => loadFeaturesSuccess({ features })),
          catchError(error => of(loadFeaturesFailure({ error })))
        )
      )
    )
  );

  constructor(
    private actions$: Actions,
    private featuresService: FeaturesService
  ) {}
}

// selectors
export const selectFeaturesState = (state: any) => state.features;
export const selectFeatures = createSelector(
  selectFeaturesState,
  (state: FeaturesState) => state.features
);
export const selectLoading = createSelector(
  selectFeaturesState,
  (state: FeaturesState) => state.loading
);
```

---

## 📚 Related Documents

- React Patterns (react_patterns.md)
- State Management (state_management.md)

---

**END OF ANGULAR PATTERNS DOCUMENT**
