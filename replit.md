# Overview

This is a full-stack AI chatbot application built with React and Express that provides conversational AI capabilities using Google's Gemini 2.0 Flash model. The application features a modern chat interface with real-time messaging, session management, and a clean UI built with shadcn/ui components.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: React with TypeScript running on Vite for fast development and builds
- **UI Framework**: shadcn/ui components built on Radix UI primitives for accessible, customizable components
- **Styling**: Tailwind CSS with a comprehensive design system including custom color variables and component variants
- **State Management**: TanStack Query (React Query) for server state management and caching
- **Routing**: Wouter for lightweight client-side routing
- **Build Tool**: Vite with custom configuration for development and production builds

## Backend Architecture
- **Runtime**: Node.js with Express.js framework
- **Language**: TypeScript with ES modules
- **API Design**: RESTful endpoints for message handling and session management
- **Development Setup**: Custom Vite integration for seamless full-stack development experience
- **Session Management**: In-memory storage with unique session IDs for conversation context

## Data Storage Solutions
- **Primary Database**: PostgreSQL configured via Drizzle ORM
- **Development Storage**: In-memory storage implementation for local development
- **Schema Management**: Drizzle Kit for database migrations and schema management
- **Data Models**: Strongly typed schemas for users and messages with Zod validation

## Authentication and Authorization
- **Session Management**: Express sessions with configurable secret keys
- **User Model**: Basic username/password authentication schema (prepared but not fully implemented)
- **Security**: CORS enabled for cross-origin requests in development

## API Architecture
- **Chat Endpoints**: 
  - GET `/api/messages/:sessionId` - Retrieve conversation history
  - POST `/api/messages` - Send message and receive AI response
  - DELETE `/api/messages/:sessionId` - Clear conversation history
- **Session Management**: Automatic session creation and context preservation
- **Error Handling**: Comprehensive error handling with proper HTTP status codes
- **Request Logging**: Detailed API request logging for development and debugging

# External Dependencies

## AI Services
- **Google Generative AI**: Gemini 2.0 Flash model for conversational AI responses
- **API Integration**: Direct integration with Google's GenAI SDK for reliable AI responses

## Database Services
- **Neon Database**: Serverless PostgreSQL database for production data storage
- **Connection Management**: Environment-based database URL configuration

## UI Component Libraries
- **Radix UI**: Comprehensive set of unstyled, accessible UI primitives
- **Lucide React**: Icon library for consistent iconography throughout the application
- **React Hook Form**: Form management with validation resolvers

## Development Tools
- **TypeScript**: Full type safety across frontend and backend
- **ESLint/Prettier**: Code quality and formatting (configured via package.json)
- **PostCSS**: CSS processing with Tailwind CSS and autoprefixer plugins

## Build and Development
- **Vite**: Fast build tool with HMR for development
- **ESBuild**: Fast bundling for production builds
- **Replit Integration**: Custom plugins for Replit development environment