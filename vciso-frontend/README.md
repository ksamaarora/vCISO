# vCISO Frontend

A modern Next.js frontend for the Virtual CISO application that generates customized Incident Response Plans.

## Features

- ✨ **Beautiful UI**: Modern, responsive design with Tailwind CSS
- 📝 **6-Step Onboarding Flow**: Guided questionnaire with progress tracking
- ✅ **Form Validation**: Real-time validation using Zod and React Hook Form
- 📄 **Plan Preview**: View generated plans with Markdown rendering
- 📥 **Export Options**: Export plans as PDF or copy to clipboard
- 🎯 **Conversational UX**: User-friendly prompts and clear instructions

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running (see `vciso-backend` README)

### Installation

1. Install dependencies:
```bash
npm install
# or
yarn install
```

2. Create a `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Run the development server:
```bash
npm run dev
# or
yarn dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
vciso-frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx              # Home page
│   │   ├── create-plan/
│   │   │   └── page.tsx          # Onboarding flow
│   │   ├── layout.tsx            # Root layout
│   │   └── globals.css           # Global styles
│   ├── components/
│   │   └── plan/
│   │       └── PlanPreview.tsx   # Plan display component
│   └── lib/
│       ├── validation.ts         # Zod schemas
│       └── api-client.ts         # API client
├── public/                       # Static assets
└── package.json
```

## Onboarding Flow

The application guides users through 6 steps:

1. **Company Basics**: Name and employee count
2. **Industry**: Select from predefined industries
3. **Technology Tools**: Email, storage, communication, CRM tools
4. **Current Security**: Existing security measures
5. **Main Concerns**: Primary security concerns
6. **Security Lead**: Who handles IT/security

## Technologies

- **Next.js 16**: React framework with App Router
- **React Hook Form**: Form state management
- **Zod**: Schema validation
- **Tailwind CSS**: Styling
- **Axios**: HTTP client
- **React Markdown**: Markdown rendering
- **jsPDF & html2canvas**: PDF export

## Building for Production

```bash
npm run build
npm start
```

## Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL (default: `http://localhost:8000`)

## License

MIT
