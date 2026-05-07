# Frontend Architecture

## Service Layer Pattern

This frontend uses a **centralized API service layer** to handle all HTTP requests. This pattern provides:

### Benefits
- **Single Source of Truth**: All API endpoints defined in one place
- **Easy Maintenance**: Change API URLs or add interceptors without touching components
- **Consistency**: Uniform error handling and request/response formatting
- **Testability**: Mock API service for unit tests

### Architecture

```
Components (UI Layer)
    ↓ imports services
API Service (api.js)
    ↓ uses axios
Backend API
    ↓
Database
```

## Services

### `api.js` - Centralized API Module

**Purpose**: Handles all HTTP communication with the backend

**Exports**:
- `applicationService` - Job application CRUD operations
- `statsService` - Dashboard statistics endpoint
- `aiService` - AI resume tip generation
- `api` - Raw Axios instance (for advanced usage)

### Usage Example

**Bad** (direct HTTP calls scattered in components):
```jsx
// ❌ Anti-pattern - don't do this
const [apps, setApps] = useState([]);

useEffect(() => {
  axios.get('http://localhost:8000/applications')
    .then(res => setApps(res.data));
}, []);
```

**Good** (using service layer):
```jsx
// ✅ Pattern - use the service layer
import { applicationService } from '../services/api';

const [apps, setApps] = useState([]);

useEffect(() => {
  applicationService.getAll()
    .then(setApps);
}, []);
```

## Component Structure

### Dashboard.jsx
- **Imports**: `statsService`, `applicationService`
- **Calls**: `getStats()`, `getAll()`, `updateStatus()`, `delete()`
- **Responsibility**: Display stats, charts, and application list

### ApplicationForm.jsx
- **Imports**: `applicationService`
- **Calls**: `create()`
- **Responsibility**: Form UI and submission

### AITip.jsx
- **Imports**: `aiService`
- **Calls**: `generateTip()`
- **Responsibility**: AI integration UI

## Future Improvements

1. **Request Interceptors**: Add auth headers, request logging
2. **Response Interceptors**: Global error handling, token refresh
3. **Caching**: Cache frequently requested data
4. **Request Deduplication**: Cancel duplicate in-flight requests
5. **Mock Service**: For unit testing without backend
6. **Error Boundary**: Global error handling component

## Adding New Endpoints

When the backend adds a new endpoint:

1. **Add service method in `api.js`**:
```jsx
export const newService = {
  getNewData: async () => {
    const response = await api.get('/new-endpoint');
    return response.data;
  },
};
```

2. **Import and use in component**:
```jsx
import { newService } from '../services/api';

// In component
const data = await newService.getNewData();
```

This keeps API logic centralized and components focused on UI.
