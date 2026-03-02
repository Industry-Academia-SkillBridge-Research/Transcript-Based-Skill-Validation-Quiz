# SkillBridge Frontend

A React + Vite frontend application for the Transcript-Based Skill Validation Quiz system.

## ✨ Features

- **Upload Transcript**: Upload academic transcripts (PDF or images)
- **View Transcript**: See extracted courses and details
- **Claim Skills**: View parent skills derived from courses
- **Take Quiz**: Answer validation questions for selected skills
- **View Results**: See verified skill scores and performance

## 🛠 Tech Stack

- **React 19.2** - UI library
- **Vite 7.2** - Build tool
- **React Router 6.30** - Routing
- **Tailwind CSS 3.4** - Styling
- **Axios** - API calls
- **Lucide React** - Icons

## 🎨 Design System

The frontend follows the shadcn/ui design system with:
- Custom color palette using CSS variables
- Consistent component styling
- Responsive layout
- Clean and modern UI

## 🚀 Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm

### Installation

```bash
# Install dependencies
npm install
```

### Configuration

The `.env` file is already configured:

```env
VITE_API_BASE=http://localhost:8000
```

### Development

```bash
# Start development server
npm run dev
```

The app will be available at `http://localhost:8080`

### Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## 📱 Application Flow

1. **Upload Page** (`/students/:id/upload`)
   - Upload transcript file (PDF/Image)
   - File is sent to backend for processing

2. **Transcript Page** (`/students/:id/transcript`)
   - View extracted student information
   - View list of courses from transcript
   - Navigate to skills page

3. **Skills Page** (`/students/:id/skills`)
   - View claimed parent skills with scores
   - Select up to 5 skills for validation
   - Plan quiz for selected skills

4. **Quiz Page** (`/students/:id/quiz`)
   - Answer multiple-choice questions
   - Track progress through quiz
   - Submit answers for validation

5. **Results Page** (`/students/:id/results`)
   - View verified skill scores
   - See performance breakdown
   - Option to take another quiz

## 🔌 API Integration

All API calls are handled through `src/api/api.js`:

- `uploadTranscript(studentId, file)` - Upload transcript
- `getTranscript(studentId)` - Get transcript details
- `getClaimedSkills(studentId)` - Get parent skills
- `planQuiz(studentId, selectedSkills)` - Plan quiz
- `generateQuizFromBank(studentId)` - Generate quiz questions
- `submitQuiz(studentId, attemptId, answers)` - Submit quiz answers

## 📁 Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── api.js              # API client and endpoints
│   ├── components/
│   │   └── ui/                 # Reusable UI components
│   │       ├── Button.jsx
│   │       ├── Card.jsx
│   │       ├── Input.jsx
│   │       ├── Table.jsx
│   │       ├── Spinner.jsx
│   │       └── ErrorAlert.jsx
│   ├── lib/
│   │   └── utils.js            # Utility functions
│   ├── pages/
│   │   ├── UploadPage.jsx
│   │   ├── TranscriptPage.jsx
│   │   ├── SkillsPage.jsx
│   │   ├── QuizPage.jsx
│   │   └── ResultsPage.jsx
│   ├── App.jsx                 # Main app with routing
│   ├── main.jsx                # Entry point
│   └── index.css               # Global styles
├── .env                        # Environment variables
├── tailwind.config.js          # Tailwind configuration
├── vite.config.js              # Vite configuration
└── package.json                # Dependencies
```

## 🎨 Styling

The app uses Tailwind CSS with a custom theme based on shadcn/ui:

- **Colors**: Primary, secondary, muted, accent, destructive
- **Components**: Pre-styled Card, Button, Table, Input components
- **Responsive**: Mobile-first design
- **Dark Mode Ready**: CSS variables for easy theming

## 🔐 Default Student ID

For development purposes, the app uses a default student ID: `IT21013928`

You can access the app at `/` which redirects to `/students/IT21013928/upload`

## ⚠️ Error Handling

- All API calls include error handling
- User-friendly error messages displayed
- Loading states for async operations
- Form validation on user inputs

## 🚧 Future Enhancements

- Role recommendation based on validated skills
- User authentication
- Multiple student profiles
- Quiz history and analytics
- Export results as PDF
- Dark mode toggle

## 📝 License

Part of the SkillBridge Research Project - SLIIT
