# Frontend-Backend OAuth Integration

This document explains how the frontend is integrated with the backend OAuth authentication system.

## 🔑 Authentication Flow

### 1. Google OAuth Login Flow

```
User clicks "Sign in with Google" 
    ↓
Frontend redirects to: http://localhost:8000/auth/login/google
    ↓
Backend redirects to Google OAuth consent screen
    ↓
User grants permission
    ↓
Google redirects to: http://localhost:8000/auth/google/callback
    ↓
Backend exchanges code for user info and creates JWT token
    ↓
Backend redirects to: http://localhost:8080/auth/callback?token={jwt_token}
    ↓
Frontend extracts token and stores in localStorage
    ↓
Frontend fetches user data and redirects to dashboard
```

## 📁 Key Files Created/Modified

### New Files

1. **`src/lib/api.ts`** - API client for backend communication
   - `getCurrentUser()` - Fetches current user data
   - `logout()` - Logs out user
   - `getGoogleLoginUrl()` - Returns Google OAuth URL

2. **`src/contexts/AuthContext.tsx`** - Authentication context provider
   - Manages user state and authentication status
   - Provides `login()` and `logout()` functions
   - Persists token in localStorage

3. **`src/pages/AuthCallback.tsx`** - OAuth callback handler
   - Receives token from backend redirect
   - Stores token and fetches user data
   - Redirects to dashboard on success

4. **`src/components/ProtectedRoute.tsx`** - Route protection component
   - Redirects unauthenticated users to `/auth`
   - Shows loading spinner during auth check

### Modified Files

1. **`Frontend/.env`** - Added backend URL
   ```
   VITE_BACKEND_URL=http://localhost:8000
   ```

2. **`src/vite-env.d.ts`** - Added TypeScript definitions for env variables

3. **`src/App.tsx`** - Updated routing
   - Wrapped app with `AuthProvider`
   - Added `/auth/callback` route
   - Protected dashboard routes with `ProtectedRoute`

4. **`src/pages/Auth.tsx`** - Updated login page
   - Removed Supabase authentication
   - Now redirects to backend OAuth endpoint
   - Disabled email/password (marked as "Coming Soon")

5. **`src/pages/Dashboard.tsx`** - Added user profile
   - Display user avatar and name
   - Added logout dropdown menu
   - Personalized welcome message

## 🔧 Backend Configuration

The backend is already configured with your Google OAuth credentials:

**File:** `login/.env`
```env
GOOGLE_CLIENT_ID=1074145388426-hed0jeanieulhnglm8pggm0qmkp3biv8.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
FRONTEND_URL=http://localhost:8080
BACKEND_URL=http://localhost:8000
```

## 🚀 Running the Application

### 1. Start Backend (FastAPI)

```powershell
cd login
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.main
```

Backend will run on: **http://localhost:8000**

### 2. Start Frontend (React + Vite)

```powershell
cd Frontend
npm install   # or bun install
npm run dev   # or bun run dev
```

Frontend will run on: **http://localhost:8080**

### 3. Test the Authentication

1. Open http://localhost:8080
2. Click "Get Started" or navigate to `/auth`
3. Click "Sign in with Google"
4. Complete Google OAuth flow
5. You'll be redirected to dashboard with your profile

## 🔒 Protected Routes

The following routes now require authentication:
- `/dashboard`
- `/learning-path`
- `/interview-prep`
- `/skill-analysis`
- `/industry-connect`

Unauthenticated users will be redirected to `/auth`.

## 📊 User Data Structure

```typescript
interface User {
  id: number;
  email: string;
  name: string;
  picture?: string;
  provider: string;
  is_active: boolean;
  created_at: string;
  last_login: string;
}
```

## 🎯 API Endpoints

### Backend Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/login/google` | GET | Initiate Google OAuth |
| `/auth/google/callback` | GET | OAuth callback (handled by backend) |
| `/auth/me` | GET | Get current user (requires token) |
| `/auth/logout` | POST | Logout endpoint |
| `/auth/health` | GET | Health check |

### Frontend API Usage

```typescript
import { getCurrentUser, logout, getGoogleLoginUrl } from '@/lib/api';

// Get current user
const user = await getCurrentUser(token);

// Logout
await logout(token);

// Get Google login URL
const loginUrl = getGoogleLoginUrl();
window.location.href = loginUrl;
```

## 🔐 Token Management

- Tokens are stored in `localStorage` under key `auth_token`
- Tokens are included in API requests via `Authorization: Bearer <token>` header
- Tokens expire after 60 minutes (configurable in backend)

## 🎨 UI Components Used

- **Avatar** - Display user profile picture
- **DropdownMenu** - User profile menu
- **Button** - Google sign-in button
- **Card** - Auth page container
- **Separator** - Visual separator
- **Toast** - Success/error notifications

## 📝 Notes

1. **Email/Password Login**: Currently disabled. To enable:
   - Implement backend endpoint for email/password registration
   - Update `handleEmailAuth()` in `Auth.tsx`
   - Update database to support password hashing

2. **Token Refresh**: Not implemented. For production:
   - Add refresh token mechanism
   - Implement token renewal before expiration

3. **Error Handling**: Basic error handling is in place. For production:
   - Add more detailed error messages
   - Implement retry logic
   - Add error logging

4. **Security Considerations**:
   - Tokens are stored in localStorage (consider httpOnly cookies for production)
   - CORS is configured to allow frontend requests
   - Change `SECRET_KEY` in backend for production

## 🐛 Troubleshooting

### Issue: "Cannot connect to backend"
- Ensure backend is running on port 8000
- Check CORS configuration in `login/app/main.py`
- Verify `VITE_BACKEND_URL` in `.env`

### Issue: "OAuth redirect fails"
- Verify Google OAuth credentials in backend `.env`
- Check authorized redirect URIs in Google Console:
  - Add: `http://localhost:8000/auth/google/callback`
- Ensure `FRONTEND_URL` matches frontend port (8080)

### Issue: "Token expired"
- Re-login via `/auth`
- Increase `ACCESS_TOKEN_EXPIRE_MINUTES` in backend config

## 🎉 Success!

Your frontend is now fully integrated with the backend OAuth system!

Users can:
- ✅ Sign in with Google
- ✅ Access protected routes
- ✅ View their profile
- ✅ Logout securely
